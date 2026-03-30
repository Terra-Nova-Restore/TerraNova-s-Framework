"""
Preflight validation module for Notion-GitHub sync.

Validates all prerequisites before sync execution:
- Secrets exist and are non-empty (NOTION_API_KEY, GH_PAT/GITHUB_TOKEN)
- Notion database is accessible
- GitHub repository is accessible
- Configuration file is valid
- No other sync process is running (concurrency check)
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from functools import wraps
import requests


class PreflightError(Exception):
    """Raised when preflight validation fails."""
    pass


class SecretValidator:
    """Validates API credentials."""
    
    @staticmethod
    def get_notion_key():
        """Get Notion API key from env. Current workflow uses NOTION_TOKEN."""
        key = os.environ.get('NOTION_TOKEN')
        if key:
            return key
        # Also accept NOTION_API_KEY for flexibility/future migration
        alternative_key = os.environ.get('NOTION_API_KEY')
        if alternative_key:
            logging.warning("NOTION_API_KEY detected; workflow currently expects NOTION_TOKEN")
            return alternative_key
        return None
    
    @staticmethod
    def get_github_token():
        """Get GitHub token from env. Prefers GH_PAT, falls back to GITHUB_TOKEN."""
        token = os.environ.get('GH_PAT')
        if token:
            return token
        token = os.environ.get('GITHUB_TOKEN')
        if token:
            return token
        return None


class NotionValidator:
    """Validates Notion API access."""
    
    BASE_URL = 'https://api.notion.com/v1'
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        })
    
    def test_database_access(self, database_id):
        """
        Test read access to Notion database.
        
        Returns:
            dict: Database info if successful
            
        Raises:
            PreflightError: If database is not accessible
        """
        try:
            resp = self.session.post(
                f'{self.BASE_URL}/databases/{database_id}/query',
                json={'page_size': 1}
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                'object': data.get('object'),
                'database_id': database_id,
                'record_count': data.get('results', []),
                'accessible': True
            }
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            error_msg = e.response.text
            
            if status == 401:
                raise PreflightError(f"Notion auth failed: API key invalid or expired\n  Database: {database_id}\n  Error: {error_msg}")
            elif status == 403:
                raise PreflightError(f"Notion permission denied: integration lacks database access\n  Database: {database_id}\n  Error: {error_msg}")
            elif status == 404:
                raise PreflightError(f"Notion database not found\n  Database ID: {database_id}\n  Error: {error_msg}")
            else:
                raise PreflightError(f"Notion API error (HTTP {status}):\n  Database: {database_id}\n  Error: {error_msg}")
        except requests.exceptions.RequestException as e:
            raise PreflightError(f"Notion connection failed: {str(e)}\n  Database: {database_id}")


class GitHubValidator:
    """Validates GitHub API access."""
    
    BASE_URL = 'https://api.github.com'
    
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json'
        })
    
    def test_repo_access(self, repo):
        """
        Test read/write access to GitHub repository.
        
        Args:
            repo: Repository in format 'owner/repo'
            
        Returns:
            dict: Repository info if successful
            
        Raises:
            PreflightError: If repository is not accessible
        """
        try:
            resp = self.session.get(f'{self.BASE_URL}/repos/{repo}')
            resp.raise_for_status()
            data = resp.json()
            
            # Check if token has write permission (pusher permission)
            if not data.get('permissions', {}).get('push'):
                raise PreflightError(
                    f"GitHub token lacks write permission to repository\n"
                    f"  Repository: {repo}\n"
                    f"  Required: repo write access\n"
                    f"  Permissions: {data.get('permissions', {})}"
                )
            
            return {
                'repository': repo,
                'full_name': data.get('full_name'),
                'private': data.get('private'),
                'push_permission': True
            }
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            error_msg = e.response.text
            
            if status == 401:
                raise PreflightError(f"GitHub auth failed: token invalid or expired\n  Repository: {repo}\n  Error: {error_msg}")
            elif status == 403:
                raise PreflightError(f"GitHub permission denied: token lacks repo access\n  Repository: {repo}\n  Error: {error_msg}")
            elif status == 404:
                raise PreflightError(f"GitHub repository not found\n  Repository: {repo}\n  Error: {error_msg}")
            else:
                raise PreflightError(f"GitHub API error (HTTP {status}):\n  Repository: {repo}\n  Error: {error_msg}")
        except requests.exceptions.RequestException as e:
            raise PreflightError(f"GitHub connection failed: {str(e)}\n  Repository: {repo}")


class ConfigValidator:
    """Validates configuration file."""
    
    @staticmethod
    def validate(config_path):
        """
        Validate configuration JSON file.
        
        Returns:
            dict: Configuration if valid
            
        Raises:
            PreflightError: If configuration is invalid
        """
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                raise PreflightError(f"Config file not found: {config_path}")
            
            config = json.loads(config_file.read_text())
            
            # Check required keys
            required = ['github_repo']
            for key in required:
                if key not in config:
                    raise PreflightError(f"Missing required config key: {key}")
            
            return config
        except json.JSONDecodeError as e:
            raise PreflightError(f"Config file invalid JSON: {config_path}\n  Error: {str(e)}")
        except Exception as e:
            raise PreflightError(f"Config validation failed: {str(e)}")


class ConcurrencyChecker:
    """Prevents concurrent sync executions."""
    
    def __init__(self, lock_file='.tnv_sync.lock'):
        self.lock_file = Path(lock_file)
    
    def acquire(self, timeout=30):
        """
        Acquire process lock.
        
        Args:
            timeout: Max seconds to wait for lock
            
        Returns:
            bool: True if lock acquired
            
        Raises:
            PreflightError: If lock cannot be acquired
        """
        start = time.time()
        while time.time() - start < timeout:
            try:
                # Try to create lock file exclusively (fails if exists)
                with self.lock_file.open('x') as f:
                    f.write(f'{os.getpid()}\n{time.time()}')
                return True
            except FileExistsError:
                # Lock exists, check if process is still alive
                try:
                    pid, ts = self._read_lock()
                    if not self._process_alive(pid):
                        # Stale lock, remove and retry
                        self.lock_file.unlink(missing_ok=True)
                        time.sleep(0.1)
                        continue
                except Exception:
                    pass
                
                time.sleep(0.5)
        
        raise PreflightError(
            f"Another sync process is running.\n"
            f"  Lock file: {self.lock_file}\n"
            f"  Wait for completion or remove lock file manually if process has crashed."
        )
    
    def release(self):
        """Release process lock."""
        self.lock_file.unlink(missing_ok=True)
    
    def _read_lock(self):
        """Read PID and timestamp from lock file."""
        content = self.lock_file.read_text().strip().split('\n')
        return int(content[0]), float(content[1])
    
    @staticmethod
    def _process_alive(pid):
        """Check if process with given PID is still running."""
        try:
            os.kill(pid, 0)  # Signal 0 = check if process exists
            return True
        except (ProcessLookupError, OSError):
            return False


class PreflightChecker:
    """Orchestrates all preflight validations."""
    
    def __init__(self, log=None):
        self.log = log or logging.getLogger('preflight')
    
    def run(self, database_id, config_path, lock_file='.tnv_sync.lock'):
        """
        Run complete preflight check.
        
        Args:
            database_id: Notion database ID to sync from
            config_path: Path to configuration file
            lock_file: Path to concurrency lock file
            
        Returns:
            dict: Validation results
            
        Raises:
            PreflightError: If any check fails
        """
        results = {
            'passed': 0,
            'failed': 0,
            'checks': {}
        }
        
        # Check 1: Secrets
        self.log.info("Preflight: Checking secrets...")
        try:
            notion_key = SecretValidator.get_notion_key()
            if not notion_key:
                raise PreflightError("Missing NOTION_TOKEN (workflow env var)")
            
            github_token = SecretValidator.get_github_token()
            if not github_token:
                raise PreflightError("Missing GH_PAT (workflow env var)")
            
            results['checks']['secrets'] = {'status': 'pass', 'notion_key': bool(notion_key), 'github_token': bool(github_token)}
            results['passed'] += 1
            self.log.info("  ✓ Secrets configured")
        except PreflightError as e:
            results['checks']['secrets'] = {'status': 'fail', 'error': str(e)}
            results['failed'] += 1
            raise
        
        # Check 2: Config file
        self.log.info("Preflight: Validating configuration...")
        try:
            config = ConfigValidator.validate(config_path)
            results['checks']['config'] = {'status': 'pass', 'github_repo': config.get('github_repo')}
            results['passed'] += 1
            self.log.info(f"  ✓ Config valid: repo={config.get('github_repo')}")
        except PreflightError as e:
            results['checks']['config'] = {'status': 'fail', 'error': str(e)}
            results['failed'] += 1
            raise
        
        # Check 3: Notion database access
        self.log.info("Preflight: Testing Notion database access...")
        try:
            notion = NotionValidator(notion_key)
            db_info = notion.test_database_access(database_id)
            results['checks']['notion_access'] = {'status': 'pass', 'database_id': database_id}
            results['passed'] += 1
            self.log.info(f"  ✓ Notion DB accessible: {database_id}")
        except PreflightError as e:
            results['checks']['notion_access'] = {'status': 'fail', 'error': str(e)}
            results['failed'] += 1
            raise
        
        # Check 4: GitHub repository access
        self.log.info("Preflight: Testing GitHub repository access...")
        try:
            repo = (
                os.environ.get('TARGET_GITHUB_REPO')
                or os.environ.get('GITHUB_REPO')
                or config.get('github_repo', '')
            )
            if not repo:
                raise PreflightError(
                    "Missing GitHub repository: set TARGET_GITHUB_REPO, GITHUB_REPO, or github_repo in config"
                )
            github = GitHubValidator(github_token)
            repo_info = github.test_repo_access(repo)
            results['checks']['github_access'] = {'status': 'pass', 'repository': repo_info.get('repository')}
            results['passed'] += 1
            self.log.info(f"  ✓ GitHub repo accessible: {repo}")
        except PreflightError as e:
            results['checks']['github_access'] = {'status': 'fail', 'error': str(e)}
            results['failed'] += 1
            raise
        
        # Check 5: Concurrency
        self.log.info("Preflight: Checking for concurrent syncs...")
        try:
            concurrency = ConcurrencyChecker(lock_file)
            concurrency.acquire()
            results['checks']['concurrency'] = {'status': 'pass'}
            results['passed'] += 1
            self.log.info("  ✓ No concurrent sync in progress")
            return results, concurrency  # Return concurrency checker for cleanup
        except PreflightError as e:
            results['checks']['concurrency'] = {'status': 'fail', 'error': str(e)}
            results['failed'] += 1
            raise


def preflight_check(database_id, config_path, lock_file='.tnv_sync.lock'):
    """
    Convenience function for preflight validation.
    
    Usage:
        try:
            results, concurrency = preflight_check(db_id, config_path)
            # ... run sync ...
        finally:
            concurrency.release()
    
    Returns:
        (results, concurrency_checker): Tuple of validation results and concurrency checker
    """
    log = logging.getLogger('preflight')
    checker = PreflightChecker(log)
    return checker.run(database_id, config_path, lock_file)
