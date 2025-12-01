import os
from datetime import datetime

class ShipLogger:
    def __init__(self):
        self.log_entries = []
        self.start_time = datetime.now()
        self.log_filename = None

    def get_timestamp(self):
        """Return formatted timestamp MM DD YYYY: HH:MM"""
        now = datetime.now()
        return now.strftime("%m %d %Y: %H:%M")

    def log(self, message):
        """Add a log entry with timestamp"""
        timestamp = self.get_timestamp()
        entry = f"{timestamp} {message}"
        self.log_entries.append(entry)

    def log_user_comment(self):
        """Allow operator to add a custom comment to the log"""
        print("\n--- Add a comment to the log ---")
        comment = input("Enter your comment (or press ENTER to skip): ").strip()
        if comment:
            self.log(comment)
            print("Comment added to log.\n")

    def write_log_to_desktop(self):
        """Write the log file to Log folder in the repository"""
        # Get path to the repo root (assumes main.py is inside src/)
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        log_folder = os.path.join(repo_root, "Log")
        os.makedirs(log_folder, exist_ok=True)
        
        # Create filename: KeoghsPort<MM_DD_YYYY_HHMM>.txt
        start = self.start_time
        filename = f"KeoghsPortLog_{start.strftime('%m_%d_%Y_%H%M')}.txt"
        filepath = os.path.join(log_folder, filename)
        
        # Write all log entries
        with open(filepath, 'w') as f:
            for entry in self.log_entries:
                f.write(entry + '\n')
        
        self.log_filename = filepath
        print(f"\nLog file written to: {filepath}")
        return filepath


# Global singleton logger instance
_logger = None


def get_logger():
    global _logger
    if _logger is None:
        _logger = ShipLogger()
    return _logger


def log_event(message):
    get_logger().log(message)


def log_user_comment():
    get_logger().log_user_comment()


def save_log():
    return get_logger().write_log_to_desktop()
