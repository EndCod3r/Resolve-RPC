import time
import signal
import sys
from ResolveMonitor import ResolveMonitor
from discord_presence import DiscordPresence
import config as config
import os
import time
import atexit


def acquire_single_instance_lock():
    """Ensure only one instance of the script is running.
    If another instance is running, this one will exit.
    Returns True if this instance should continue, False if it should exit.
    """

    # Use a lock file in the same directory as main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lock_file_path = os.path.join(script_dir, "resolve_rpc.lock")

    try:
        # Try to open/create the lock file
        lock_file = open(lock_file_path, "w")

        # Try to lock the file (Windows exclusive lock)
        import msvcrt

        try:
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
            # Successfully locked - this is the only instance

            # Write PID to lock file
            lock_file.write(str(os.getpid()))
            lock_file.flush()

            # Store lock file handle for cleanup
            global __lock_handle
            __lock_handle = lock_file

            # Clean up on exit
            def cleanup_lock():
                try:
                    if __lock_handle:
                        msvcrt.locking(__lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
                        __lock_handle.close()
                        if os.path.exists(lock_file_path):
                            os.remove(lock_file_path)
                except:
                    pass

            atexit.register(cleanup_lock)

            print(f"[Lock] Acquired lock (PID: {os.getpid()})")
            return True

        except (IOError, OSError):
            # Failed to lock - another instance is running
            lock_file.close()
            print(f"[Lock] Another instance is already running. Exiting...")
            return False

    except Exception as e:
        print(f"[Lock] Error acquiring lock: {e}")
        # If we can't get a lock, let the script run anyway (fallback)
        return True


if __name__ == "__main__":
    if not acquire_single_instance_lock():
        sys.exit(0)


def main():
    print("=" * 50)
    print("DaVinci Resolve Discord Rich Presence")
    print("=" * 50)
    print("Script will exit when DaVinci Resolve closes...")

    monitor = ResolveMonitor()
    discord = DiscordPresence()

    # Connect to Discord once
    if not discord.connect():
        print("Failed to connect to Discord. Please check your Client ID.")
        return

    running = True
    resolve_was_running = False
    resolve_closed_count = 0  # Track how long Resolve has been closed

    def signal_handler(sig, frame):
        nonlocal running
        print("\nShutting down...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while running:
            if monitor.check_if_running():
                # Resolve is running - reset the closed counter
                resolve_closed_count = 0

                if not resolve_was_running:
                    print("DaVinci Resolve detected! Starting RPC...")
                    monitor.connect_to_resolve()
                    discord.reset_start_time()

                if monitor.update_project_info():
                    project = monitor.get_current_project()
                    timeline = monitor.get_current_timeline()
                    page = monitor.get_current_page()
                    discord.update_status(project, timeline, page)
                    resolve_was_running = True
                else:
                    discord.update_status("Unknown", "Unknown", "None")
            else:
                # Resolve is not running
                if resolve_was_running:
                    print("DaVinci Resolve closed. Clearing status...")
                    discord.clear_status()
                    resolve_was_running = False

                # Increment counter for how long Resolve has been closed
                resolve_closed_count += 1

                # Exit after Resolve has been closed for the specified duration
                if (
                    resolve_closed_count
                    > config.EXIT_AFTER_CLOSED / config.POLL_INTERVAL
                ):
                    print(
                        f"Resolve has been closed for {resolve_closed_count * config.POLL_INTERVAL} seconds. Exiting..."
                    )
                    break

            time.sleep(config.POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        discord.clear_status()
        discord.disconnect()
        print("Shutdown complete!")


if __name__ == "__main__":
    main()
