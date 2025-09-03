import os
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def start_process(self):
        print("Starting GUI process...")
        self.process = subprocess.Popen(self.command)

    def stop_process(self):
        if self.process and self.process.poll() is None:
            print("Stopping GUI process...")
            self.process.terminate()
            self.process.wait()
            self.process = None

    def on_any_event(self, event):
        # We only care about changes to Python files
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        print(f"File changed: {event.src_path}. Restarting...")
        self.stop_process()
        # Give the old process a moment to close
        time.sleep(1)
        self.start_process()

if __name__ == "__main__":
    # Command to run your GUI app using Poetry
    command = [
        "poetry",
        "run",
        "peac",
        "gui.py"  # Replace with the path to your GUI script
    ]
    
    # Path to monitor for changes
    path_to_watch = "."  # Current directory

    event_handler = RestartHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)

    # Start the GUI process initially
    event_handler.start_process()
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler.stop_process()
        observer.stop()
    finally:
        observer.join()