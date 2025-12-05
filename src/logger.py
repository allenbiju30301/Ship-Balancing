import os
from datetime import datetime
from zoneinfo import ZoneInfo

class ShipLogger:
    def __init__(self):
        self.log_entries = []
        self.start_time = (datetime.now(ZoneInfo("America/Los_Angeles")))
        self.log_filename = None

    def get_timestamp(self):
        now = (datetime.now(ZoneInfo("America/Los_Angeles")))
        return now.strftime("%m %d %Y: %H:%M")

    def log(self, message):
        timestamp = self.get_timestamp()
        entry = f"{timestamp} {message}"
        self.log_entries.append(entry)

    def log_user_comment(self):
        print("\n--- Add a comment to the log ---")
        comment = input("Enter your comment (or press ENTER to skip): ").strip()
        if comment:
            self.log(f'A comment was added to the log: "{comment}"')
            print("Comment added to log.\n")

    def write_log_to_desktop(self, filename):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        log_folder = os.path.join(repo_root, "Log")
        os.makedirs(log_folder, exist_ok=True)
        
        start = self.start_time
        name = f"{filename}{start.strftime('%m_%d_%Y_%H%M')}.txt"
        filepath = os.path.join(log_folder, name)
        
        with open(filepath, 'w') as f:
            for entry in self.log_entries:
                f.write(entry + '\n')
        
        self.log_filename = filepath
        print(f"\nLog file written to: {filepath}")
        return filepath

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


def save_log(filename):
    return get_logger().write_log_to_desktop(filename)