"""Command-line entry point for the OAL-001 harmless local dry-run."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .governor import load_policy
from .runtime import execute_cycle, write_cycle_artifacts


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXED_GIT_READ_COMMANDS = {
    ("git", "branch", "--show-current"),
    ("git", "rev-parse", "HEAD"),
}


def _run_fixed_git_read(command: list[str]) -> str:
    if tuple(command) not in FIXED_GIT_READ_COMMANDS:
        raise ValueError("Git command is outside the fixed read-only allowlist")
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(command)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def git_branch() -> str:
    return _run_fixed_git_read(["git", "branch", "--show-current"])


def git_head() -> str:
    return _run_fixed_git_read(["git", "rev-parse", "HEAD"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the OAL-001 controlled self-modification dry-run."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the deterministic result summary as JSON.",
    )
    args = parser.parse_args(argv)

    try:
        policy = load_policy(REPO_ROOT)
        branch = git_branch()
        base_sha = git_head()
        result = execute_cycle(REPO_ROOT, policy, branch, base_sha)
        output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
    except (OSError, ValueError, PermissionError, RuntimeError) as exc:
        print(f"[oal-001] ERROR: {exc}", file=sys.stderr)
        return 1

    summary = {
        "run_id": result.run_id,
        "decision": result.trace["evaluation"]["decision"],
        "rollback_status": result.rollback_proof["status"],
        "external_mutation_count": result.trace["external_mutation_count"],
        "output_dir": output_dir.relative_to(REPO_ROOT).as_posix(),
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"[oal-001] run_id={summary['run_id']}")
        print(f"[oal-001] decision={summary['decision']}")
        print(f"[oal-001] rollback_status={summary['rollback_status']}")
        print("[oal-001] external_mutation_count=0")
        print(f"[oal-001] output_dir={summary['output_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
