import psutil


def kill_process_tree(pid: int):
    try:
        parent = psutil.Process(pid)

        parent.suspend()

        children = parent.children(recursive=True)

        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                print(f"Warning: Access denied terminating child PID {child.pid}.")

        parent.terminate()

        gone, alive = psutil.wait_procs(children + [parent], timeout=3)

        for p in alive:
            try:
                p.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        print(f"Process tree for PID {pid} has been terminated.")

    except psutil.NoSuchProcess:
        print(f"Error: Process with PID {pid} was not found or has already exited.")
    except psutil.AccessDenied:
        print(
            f"Error: Access denied. You may need elevated (Administrator/Root) privileges to suspend or terminate PID {pid}."
        )
