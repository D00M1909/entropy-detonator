import time
from watchdog.observers import Observer
from monitor import RansomwareEventHandler

if __name__ == "__main__":
    path = "target_directory"

    event_handler = RansomwareEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print(f"Started monitoring '{path}'. Press Ctrl+C to stop.")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
