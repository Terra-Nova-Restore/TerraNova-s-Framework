#!/usr/bin/env python3
"""
Standalone validation script for Notion-GitHub sync environment.

Run this to validate your setup WITHOUT executing an actual sync.
Useful for diagnosing configuration issues before deployment.

Usage:
    python scripts/validate-sync-environment.py
    
    Or with custom config:
    python scripts/validate-sync-environment.py --config config/notion_map.json
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add scripts directory to path so we can import preflight
sys.path.insert(0, str(Path(__file__).parent))

from preflight import PreflightChecker, PreflightError

def setup_logging():
    """Set up console logging for validation output."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger('validate')

def main():
    parser = argparse.ArgumentParser(
        description='Validate Notion-GitHub sync environment',
        epilog='This script only validates; it does not run an actual sync.'
    )
    parser.add_argument(
        '--config',
        default='config/notion_map.json',
        help='Path to configuration file (default: config/notion_map.json)'
    )
    parser.add_argument(
        '--database-id',
        help='Notion database ID (overrides NOTION_DATABASE_ID_CHANGES env var)'
    )
    
    args = parser.parse_args()
    log = setup_logging()
    
    # Get database ID
    db_id = args.database_id or os.environ.get('NOTION_DATABASE_ID_CHANGES', '')
    if not db_id:
        log.error('ERROR: NOTION_DATABASE_ID_CHANGES not set and --database-id not provided')
        sys.exit(1)
    
    log.info('=' * 70)
    log.info('Notion-GitHub Sync Environment Validation')
    log.info('=' * 70)
    log.info('')
    
    # Run preflight checks
    checker = PreflightChecker(log)
    results = {'checks': {}}
    try:
        results, concurrency = checker.run(db_id, args.config)
        
        # Print summary
        log.info('')
        log.info('=' * 70)
        log.info('VALIDATION PASSED')
        log.info('=' * 70)
        log.info(f'✓ All {results["passed"]} checks passed')
        log.info('')
        log.info('Details:')
        for check_name, check_result in results['checks'].items():
            status = check_result.get('status', 'unknown')
            status_emoji = '✓' if status == 'pass' else '✗'
            log.info(f'  {status_emoji} {check_name}: {status}')
            if 'database_id' in check_result:
                log.info(f'      Database: {check_result["database_id"]}')
            if 'repository' in check_result:
                log.info(f'      Repository: {check_result["repository"]}')
        
        log.info('')
        log.info('You can now safely run the sync script:')
        log.info('  python scripts/notion_to_github.py')
        log.info('')
        
        # Release lock
        concurrency.release()
        return 0
        
    except PreflightError as e:
        log.error('')
        log.error('=' * 70)
        log.error('VALIDATION FAILED')
        log.error('=' * 70)
        log.error(f'✗ {str(e)}')
        log.error('')
        
        # Print what failed
        log.error('Failed checks:')
        for check_name, check_result in results.get('checks', {}).items():
            if check_result.get('status') == 'fail':
                log.error(f'  ✗ {check_name}')
                if 'error' in check_result:
                    error_msg = check_result['error']
                    for line in error_msg.split('\n'):
                        log.error(f'      {line}')
        
        log.error('')
        log.error('Troubleshooting:')
        log.error('  1. Review the error messages above')
        log.error('  2. Check your Notion integration sharing settings')
        log.error('  3. Verify API tokens are valid and not expired')
        log.error('  4. See scripts/PREFLIGHT_README.md for detailed diagnostics')
        log.error('')
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
