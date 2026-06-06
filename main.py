import time
import sys
import signal
from ResolveMonitor import ResolveMonitor
from discord_presence import DiscordPresence
import config

class DaVinciResolveRPC:
    def __init__(self):
        self.monitor = ResolveMonitor()
        self.discord = DiscordPresence()
        self.running = True
        self.last_project = None
        self.last_timeline = None
        self.last_page = None
        
    def setup_signal_handlers(self):
        """Handle Ctrl+C gracefully"""
        def signal_handler(sig, frame):
            print("\n\nShutting down...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self):
        """Main loop"""
        print("=" * 50)
        print("DaVinci Resolve Discord Rich Presence")
        print("=" * 50)
        print(f"Discord Client ID: {config.DISCORD_CLIENT_ID}")
        print(f"Polling Interval: {config.POLL_INTERVAL} seconds")
        print("\nMonitoring for DaVinci Resolve...")
        print("Press Ctrl+C to stop\n")
        
        # Setup signal handlers for clean shutdown
        self.setup_signal_handlers()
        
        # Connect to Discord
        if not self.discord.connect():
            print("Failed to connect to Discord. Please check your Client ID.")
            return
        
        # Track Resolve state to avoid spamming
        resolve_was_running = False
        
        try:
            while self.running:
                # Check if DaVinci Resolve is running
                if self.monitor.check_if_running():
                    if not resolve_was_running:
                        print("DaVinci Resolve detected! Connecting...")
                        self.monitor.connect_to_resolve()
                        # Reset start time for new session
                        self.discord.reset_start_time()
                    
                    # Update project information
                    if self.monitor.update_project_info():
                        project = self.monitor.get_current_project()
                        timeline = self.monitor.get_current_timeline()
                        page = self.monitor.get_current_page()
                        
                        # Check if project changed (reset timer)
                        if project != self.last_project:
                            print(f"Project changed: {self.last_project} -> {project}")
                            self.discord.reset_start_time()
                        
                        # Update Discord status
                        self.discord.update_status(project, timeline, page)
                        
                        # Store for next comparison
                        self.last_project = project
                        self.last_timeline = timeline
                        self.last_page = page
                    else:
                        # Failed to update, show offline status
                        self.discord.update_status("Unknown", "Unknown", "None")
                    
                    resolve_was_running = True
                    
                else:
                    # Resolve is not running
                    if resolve_was_running:
                        print("DaVinci Resolve closed. Clearing Discord status...")
                        self.discord.clear_status()
                        resolve_was_running = False
                        self.last_project = None
                        self.last_timeline = None
                        self.last_page = None
                    elif self.running:
                        # Only print this occasionally to avoid spam
                        if int(time.time()) % 30 == 0:  # Print every 30 seconds
                            print("Waiting for DaVinci Resolve to start...")
                
                # Wait before next check
                time.sleep(config.POLL_INTERVAL)
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown"""
        print("Cleaning up...")
        if self.discord:
            self.discord.clear_status()
            self.discord.disconnect()
        print("Shutdown complete. Goodbye!")

def main():
    """Entry point"""
    app = DaVinciResolveRPC()
    app.run()

if __name__ == "__main__":
    main()