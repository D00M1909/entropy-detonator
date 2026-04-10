import time
import psutil
from watchdog.events import FileSystemEventHandler
from entropy import calculate_entropy
from executioner import kill_process_tree


class RansomwareEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.high_entropy_events = []
        self.threshold = 7.5
        self.time_window = 2.0
        self.trigger_count = 3

    def check_and_kill(self):
        current_time = time.time()
        self.high_entropy_events = [
            t for t in self.high_entropy_events if current_time - t < self.time_window
        ]

        if len(self.high_entropy_events) >= self.trigger_count:
            print("\nTHRESHOLD MET! RANSOMWARE BEHAVIOR DETECTED!")
            self.high_entropy_events = []

            killed = False
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = proc.info["cmdline"]
                    if cmdline and "test_attack.py" in " ".join(cmdline):
                        print(
                            f"Target Acquired: test_attack.py (PID {proc.info['pid']})"
                        )
                        print("Executing process tree...")
                        kill_process_tree(proc.info["pid"])
                        killed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            if not killed:
                print("Could not locate the attacker process!")

    def process_event(self, event):
        if event.is_directory:
            return

        score = calculate_entropy(event.src_path)

        if score > self.threshold:
            print(f"HIGH ENTROPY ({score:.2f}): {event.src_path}")
            self.high_entropy_events.append(time.time())
            self.check_and_kill()
        else:
            print(f"Normal File ({score:.2f}): {event.src_path}")

    def on_created(self, event):
        self.process_event(event)

    def on_modified(self, event):
        self.process_event(event)
