import time
import signal
import sys
from ResolveMonitor import ResolveMonitor
from discord_presence import DiscordPresence
import config as config


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
