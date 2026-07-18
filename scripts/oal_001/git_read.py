"""Hardened, typed and read-only Git observations for OAL-001."""

from __future__ import annotations

import os
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath


TRUSTED_GIT_CANDIDATES = (
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files\Git\bin\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
    "/usr/bin/git",
)
FIXED_GIT_READ_ARGUMENTS = {
    ("branch", "--show-current"),
    ("rev-parse", "HEAD"),
    ("status", "--short", "--branch"),
}
GIT_SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")
BRANCH_PATTERN = re.compile(r"^[A-Za-z0-9._/-]+$")
_PASSTHROUGH_ENVIRONMENT = (
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "TEMP",
    "TMP",
    "TMPDIR",
)


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _contains_link_component(path: Path) -> bool:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink() or _is_reparse_point(current):
            return True
    return False


def _resolve_git_executable(repo_root: Path) -> Path:
    resolved_repo = repo_root.resolve(strict=True)
    if not resolved_repo.is_dir():
        raise RuntimeError("repository root is not a directory")
    for raw_candidate in TRUSTED_GIT_CANDIDATES:
        candidate = Path(raw_candidate)
        if not candidate.is_absolute() or _contains_link_component(candidate):
            continue
        try:
            resolved = candidate.resolve(strict=True)
        except (FileNotFoundError, OSError):
            continue
        if not resolved.is_file():
            continue
        try:
            resolved.relative_to(resolved_repo)
        except ValueError:
            return resolved
    raise RuntimeError("no fixed trusted Git executable is available")


def _sanitized_environment(git_executable: Path) -> dict[str, str]:
    environment: dict[str, str] = {}
    for key in _PASSTHROUGH_ENVIRONMENT:
        value = os.getenv(key)
        if value:
            environment[key] = value
    environment.update(
        {
            "PATH": str(git_executable.parent),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_PAGER": "cat",
            "LC_ALL": "C",
        }
    )
    return environment


def _validate_relative_path(relative_path: str) -> str:
    if (
        not relative_path
        or "\\" in relative_path
        or "\x00" in relative_path
        or re.match(r"^[A-Za-z]:", relative_path)
        or relative_path.startswith(":")
        or any(character in relative_path for character in "*?[")
    ):
        raise ValueError("Git path must be a non-empty normalized repository path")
    parsed = PurePosixPath(relative_path)
    if (
        parsed.is_absolute()
        or any(part in {"", ".", ".."} for part in parsed.parts)
        or parsed.as_posix() != relative_path
    ):
        raise ValueError("Git path must stay within the repository")
    return relative_path


def _run_git(
    repo_root: Path,
    arguments: tuple[str, ...],
    allowed_return_codes: frozenset[int] = frozenset({0}),
) -> tuple[int, str, str]:
    is_fixed_read = arguments in FIXED_GIT_READ_ARGUMENTS
    is_check_ignore = (
        len(arguments) == 4
        and arguments[:3] == ("check-ignore", "-q", "--")
        and arguments[3] == _validate_relative_path(arguments[3])
    )
    if not is_fixed_read and not is_check_ignore:
        raise ValueError("Git operation is outside the typed read-only API")

    resolved_repo = repo_root.resolve(strict=True)
    git_executable = _resolve_git_executable(resolved_repo)
    command = [
        str(git_executable),
        "--no-pager",
        "--no-optional-locks",
        "-c",
        "core.fsmonitor=false",
        "-c",
        f"core.hooksPath={os.devnull}",
        *arguments,
    ]
    result = subprocess.run(
        command,
        cwd=resolved_repo,
        env=_sanitized_environment(git_executable),
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode not in allowed_return_codes:
        detail = result.stderr.strip() or "no diagnostic output"
        raise RuntimeError(f"read-only Git observation failed: {detail}")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def current_branch(repo_root: Path) -> str:
    """Return the current branch through the fixed read-only Git boundary."""

    _, output, _ = _run_git(repo_root, ("branch", "--show-current"))
    if not output or not BRANCH_PATTERN.fullmatch(output):
        raise RuntimeError("Git branch observation returned an invalid branch")
    return output


def head_sha(repo_root: Path) -> str:
    """Return the current commit SHA through the fixed read-only Git boundary."""

    _, output, _ = _run_git(repo_root, ("rev-parse", "HEAD"))
    if not GIT_SHA_PATTERN.fullmatch(output):
        raise RuntimeError("Git HEAD observation returned an invalid SHA")
    return output


def worktree_status(repo_root: Path) -> str:
    """Return porcelain status without optional index writes or fsmonitor hooks."""

    _, output, _ = _run_git(repo_root, ("status", "--short", "--branch"))
    if not output.startswith("## ") or "\x00" in output:
        raise RuntimeError("Git status observation returned an invalid payload")
    return output


def is_ignored(repo_root: Path, relative_path: str) -> bool:
    """Return whether one validated repository-relative path is ignored."""

    normalized = _validate_relative_path(relative_path)
    return_code, _, _ = _run_git(
        repo_root,
        ("check-ignore", "-q", "--", normalized),
        allowed_return_codes=frozenset({0, 1}),
    )
    return return_code == 0
