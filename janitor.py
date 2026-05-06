"""
SOVEREIGN JANITOR v1.0
Automatic maintenance & cleanup agent for IRON COMMANDER ELITE
Runs daily to maintain project health and remove stale data
"""

import os
import shutil
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import time

# --- LOGGING SETUP ---
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "janitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JANITOR")

class SovereignJanitor:
    """Maintenance daemon for project health."""
    
    def __init__(self):
        self.root = Path.cwd()
        self.cleaned_items = 0
        self.freed_space = 0
        
    def cleanup_old_logs(self, days=7):
        """Remove log files older than N days."""
        logger.info(f"--- CLEANUP: Log Files (older than {days} days) ---")
        cutoff = datetime.now() - timedelta(days=days)
        
        log_dirs = [
            Path("logs"),
            Path("core_v3"),
            Path("core_real")
        ]
        
        for log_dir in log_dirs:
            if not log_dir.exists():
                continue
                
            for log_file in log_dir.glob("*.log"):
                try:
                    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if mtime < cutoff:
                        size = log_file.stat().st_size
                        log_file.unlink()
                        self.cleaned_items += 1
                        self.freed_space += size
                        logger.info(f"  Deleted: {log_file.name} ({size} bytes)")
                except Exception as e:
                    logger.warning(f"  Failed to delete {log_file}: {e}")
    
    def cleanup_temp_files(self):
        """Remove temporary/cache files."""
        logger.info("--- CLEANUP: Temporary Files ---")
        
        temp_patterns = [
            "*.tmp",
            "*_temp.py",
            "*.pyc",
            "__pycache__",
            ".cache",
            "*.bak"
        ]
        
        for pattern in temp_patterns:
            for file in self.root.glob(f"**/{pattern}"):
                try:
                    if file.is_dir():
                        shutil.rmtree(file)
                    else:
                        size = file.stat().st_size
                        file.unlink()
                        self.cleaned_items += 1
                        self.freed_space += size
                        logger.info(f"  Deleted: {file}")
                except Exception as e:
                    logger.warning(f"  Failed to delete {file}: {e}")
    
    def archive_old_databases(self, days=30):
        """Move old database files to archive."""
        logger.info(f"--- ARCHIVE: Old Databases (older than {days} days) ---")
        archive_dir = Path("03_DATA/archive")
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        cutoff = datetime.now() - timedelta(days=days)
        
        for db_file in self.root.glob("**/*.db"):
            try:
                mtime = datetime.fromtimestamp(db_file.stat().st_mtime)
                if mtime < cutoff and "core_v3/iron_core.db" not in str(db_file) and "core_real/iron_core.db" not in str(db_file):
                    # Keep active databases, archive old ones
                    dest = archive_dir / db_file.name
                    shutil.move(str(db_file), str(dest))
                    self.cleaned_items += 1
                    logger.info(f"  Archived: {db_file.name}")
            except Exception as e:
                logger.warning(f"  Failed to archive {db_file}: {e}")
    
    def validate_database_integrity(self):
        """Check core databases for corruption."""
        logger.info("--- VALIDATE: Database Integrity ---")
        
        db_files = [
            Path("core_v3/iron_core.db"),
            Path("core_real/iron_core.db")
        ]
        
        for db_path in db_files:
            if not db_path.exists():
                logger.warning(f"  Database not found: {db_path}")
                continue
                
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()[0]
                conn.close()
                
                if result == "ok":
                    logger.info(f"  PASS: {db_path.name}")
                else:
                    logger.error(f"  FAIL: {db_path.name} - {result}")
            except Exception as e:
                logger.error(f"  Error checking {db_path}: {e}")
    
    def cleanup_stale_json(self):
        """Clean and validate JSON config files."""
        logger.info("--- CLEANUP: JSON Config Files ---")
        
        for json_file in self.root.glob("**/*.json"):
            if "node_modules" in str(json_file):
                continue
                
            try:
                with open(json_file, 'r') as f:
                    json.load(f)  # Validate
                logger.info(f"  Valid: {json_file.name}")
            except json.JSONDecodeError as e:
                logger.warning(f"  Invalid JSON: {json_file} - {e}")
                # Attempt to fix if it's a config file
                if "config" in json_file.name or "dna" in json_file.name:
                    logger.warning(f"  Keeping invalid file for manual review: {json_file}")
    
    def generate_health_report(self):
        """Generate project health report."""
        logger.info("--- HEALTH REPORT ---")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "cleaned_items": self.cleaned_items,
            "freed_space_bytes": self.freed_space,
            "freed_space_mb": round(self.freed_space / (1024**2), 2)
        }
        
        report_file = LOG_DIR / "janitor_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Cleanup Summary:")
        logger.info(f"  Items removed: {report['cleaned_items']}")
        logger.info(f"  Space freed: {report['freed_space_mb']} MB")
        logger.info(f"  Report saved: {report_file}")
    
    def run(self):
        """Execute full maintenance cycle."""
        logger.info("="*50)
        logger.info("SOVEREIGN JANITOR - Daily Maintenance Cycle")
        logger.info("="*50)
        
        self.cleanup_old_logs(days=7)
        self.cleanup_temp_files()
        self.archive_old_databases(days=30)
        self.validate_database_integrity()
        self.cleanup_stale_json()
        self.generate_health_report()
        
        logger.info("="*50)
        logger.info("Maintenance cycle complete")
        logger.info("="*50)


def schedule_daily():
    """Placeholder for daily scheduling (use Windows Task Scheduler)."""
    logger.info("To schedule daily, create a Windows Task Scheduler task:")
    logger.info("  Trigger: Daily at 02:00 AM")
    logger.info("  Action: python janitor.py --run")


if __name__ == "__main__":
    import sys
    
    janitor = SovereignJanitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        janitor.run()
    else:
        print("Usage: python janitor.py --run")
        print("\nTo schedule daily maintenance:")
        print("  Windows Task Scheduler:")
        print("    Program: python")
        print("    Arguments: janitor.py --run")
        print("    Trigger: Daily at 02:00 AM")
        print("\nOr run immediately:")
        print("  python janitor.py --run")
