import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart()

    def on_any_event(self, event):
        if "__pycache__" in event.src_path:
            return
        if event.event_type in ('modified', 'created', 'deleted'):
            self.restart()

    def restart(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        time.sleep(2)  # Small delay to prevent rapid restarts
        self.process = subprocess.Popen([sys.executable, self.script])

if __name__ == "__main__":
    script_to_run = "main.py"  # Change this to your Pygame script
    event_handler = ChangeHandler(script_to_run)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()