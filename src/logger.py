import os
from datetime import datetime
from zoneinfo import ZoneInfo

class ShipLogger:
    def __init__(self):
        self.logEntries = []
        self.startTime = datetime.now(ZoneInfo("America/Los_Angeles"))
        self.logFilename = None

    def getTimestamp(self):
        now = datetime.now(ZoneInfo("America/Los_Angeles"))
        return now.strftime("%m %d %Y: %H:%M")

    def log(self, message):
        timestamp = self.getTimestamp()
        entry = f"{timestamp} {message}"
        self.logEntries.append(entry)

    def logUserComment(self):
        print("\n--- Add a comment to the log ---")
        comment = input("Enter your comment (or press ENTER to skip): ").strip()
        if comment:
            self.log(f'A comment was added to the log: "{comment}"')
            print("Comment added to log.\n")

    def writeLogToDesktop(self, filename):
        repoRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        logFolder = os.path.join(repoRoot, "Log")
        os.makedirs(logFolder, exist_ok=True)
        
        start = self.startTime
        name = f"{filename}{start.strftime('%m_%d_%Y_%H%M')}.txt"
        filepath = os.path.join(logFolder, name)
        
        with open(filepath, 'w') as f:
            for entry in self.logEntries:
                f.write(entry + '\n')
        
        self.logFilename = filepath
        print(f"\nLog file written to: {filepath}")
        return filepath

_logger = None

def getLogger():
    global _logger
    if _logger is None:
        _logger = ShipLogger()
    return _logger


def logEvent(message):
    getLogger().log(message)


def logUserComment():
    getLogger().logUserComment()


def saveLog(filename):
    return getLogger().writeLogToDesktop(filename)