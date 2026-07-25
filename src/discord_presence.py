import time
from pypresence import Presence
from pypresence.exceptions import PyPresenceException
import config


class DiscordPresence:
    def __init__(self):
        self.client_id = config.DISCORD_CLIENT_ID
        self.rpc = None
        self.is_connected = False
        self.start_time = None
        self.current_status = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    def connect(self):
        """Connect to Discord's RPC"""
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.is_connected = True
            self.reconnect_attempts = 0
            print("Connected to Discord RPC")
            return True
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            self.is_connected = False
            self.rpc = None
            return False

    def disconnect(self):
        """Disconnect from Discord RPC"""
        if self.rpc and self.is_connected:
            try:
                self.rpc.close()
                print("Disconnected from Discord RPC")
            except:
                pass
        self.is_connected = False
        self.rpc = None

    def reconnect(self):
        """Attempt to reconnect to Discord"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            print(
                f"Max reconnection attempts ({self.max_reconnect_attempts}) reached. Giving up for now."
            )
            return False

        self.reconnect_attempts += 1
        print(
            f"Attempting to reconnect to Discord (attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})..."
        )

        # Clean up old connection
        if self.rpc:
            try:
                self.rpc.close()
            except:
                pass
            self.rpc = None

        self.is_connected = False
        time.sleep(2)  # Wait before reconnecting

        return self.connect()

    def update_status(self, project, timeline, page):
        """Update Discord presence with current Resolve status"""
        # Try to connect if not connected
        if not self.is_connected:
            if not self.connect():
                return False

        # Don't spam Discord if nothing changed
        current_status_key = f"{project}|{timeline}|{page}"
        if self.current_status == current_status_key:
            return True

        # Format the presence based on what's happening
        presence_data = self._format_presence(project, timeline, page)

        try:
            # Filter out None values
            presence_data = {k: v for k, v in presence_data.items() if v is not None}
            self.rpc.update(**presence_data)
            self.current_status = current_status_key
            self.reconnect_attempts = 0  # Reset reconnect attempts on successful update
            print(f"Updated Discord status: {presence_data}")
            return True
        except PyPresenceException as e:
            error_str = str(e).lower()
            if (
                "pipe" in error_str
                or "closed" in error_str
                or "connection" in error_str
            ):
                print("Discord connection lost. Attempting to reconnect...")
                self.is_connected = False
                if self.reconnect():
                    return self.update_status(project, timeline, page)
            else:
                print(f"Failed to update Discord status: {e}")
            return False
        except (BrokenPipeError, ConnectionError, OSError) as e:
            print(f"Discord connection error: {e}. Attempting to reconnect...")
            self.is_connected = False
            if self.reconnect():
                return self.update_status(project, timeline, page)
            return False
        except Exception as e:
            print(f"Failed to update Discord status: {e}")
            return False

    def _format_presence(self, project, timeline, page):
        """Format the presence data for Discord based on current state"""

        # Handle Resolve starting up
        if (
            page == "starting"
            or project == "Starting..."
            or timeline == "Loading..."
            or project == "Unknown"
        ):
            return {
                "state": "Starting DaVinci Resolve",
                "details": "Please wait...",
                "large_image": "resolve_logo",
                "large_text": "DaVinci Resolve",
                "small_image": "loading",
                "small_text": "Starting up",
            }

        # Handle being in menus
        if page == "menu":
            return {
                "state": "In Menus",
                "details": "Project Settings or Manager",
                "large_image": "resolve_logo",
                "large_text": "DaVinci Resolve",
                "small_image": "settings",
                "small_text": "In Settings/Menus",
            }

        # Check if Project Manager is open
        if page == "none":
            return {
                "state": config.PROJECT_MANAGER_STATE,
                "details": config.PROJECT_MANAGER_DETAILS,
                "large_image": "resolve_logo",
                "large_text": "DaVinci Resolve",
                "small_image": "project_manager",
                "small_text": config.PROJECT_MANAGER_SMALL_TEXT,
            }

        # Check if no project is open
        if page is None:
            return {
                "state": config.NO_PROJECT_STATE,
                "details": config.NO_PROJECT_DETAILS,
                "large_image": "resolve_logo",
                "large_text": "DaVinci Resolve",
                "small_image": "idle",
                "small_text": "Idle",
            }

        # Handle timeline display
        if (
            not timeline
            or timeline == "None"
            or timeline == "No Timeline Open"
            or timeline == "Loading..."
        ):
            timeline_display = config.NO_TIMELINE_TEXT
        else:
            timeline_display = config.TIMELINE_FORMAT.format(timeline=timeline)

        # Get the action message from config.PAGE_MESSAGES (not self.page_messages)
        if page in config.PAGE_MESSAGES:
            action = config.PAGE_MESSAGES[page]
        else:
            # Use default message template from config
            action = config.DEFAULT_PAGE_MESSAGE.format(page=page)

        # Create the status message
        status_text = f"{action} {timeline_display}"

        # Format the small text
        if page and isinstance(page, str) and page not in ["None", "none"]:
            small_text = config.PAGE_SMALL_TEXT.format(page=page.title())
        else:
            small_text = "DaVinci Resolve"

        # Set details line
        if project == "Untitled Project":
            details_text = config.UNSAVED_PROJECT_DETAILS
        elif project == "Starting..." or project == "Loading...":
            details_text = "Starting up..."
        else:
            details_text = f"Project: {project}"

        # Safe small_image
        if page and isinstance(page, str) and page not in ["None", "none", None]:
            small_image = page
        else:
            small_image = "resolve_logo"

        # Don't show timer in menus or during startup
        show_timer = project not in [
            "Untitled Project",
            "Starting...",
            "Loading...",
            "Unknown",
            "In Menus",
        ]

        # Base presence
        presence = {
            "state": status_text,
            "details": details_text,
            "large_image": "resolve_logo",
            "large_text": "DaVinci Resolve",
            "small_image": small_image,
            "small_text": small_text,
            "start": self._get_start_time() if show_timer else None,
        }

        # Remove None values
        presence = {k: v for k, v in presence.items() if v is not None}

        return presence

    def _get_start_time(self):
        """Get or create start timestamp for elapsed time display"""
        if self.start_time is None:
            self.start_time = int(time.time())
        return self.start_time

    def reset_start_time(self):
        """Reset the elapsed time counter (call when project changes)"""
        self.start_time = int(time.time())

    def clear_status(self):
        """Clear the Discord presence (show nothing)"""
        if self.is_connected and self.rpc:
            try:
                self.rpc.clear()
                self.current_status = None
                print("Cleared Discord status")
            except PyPresenceException as e:
                error_str = str(e).lower()
                if "pipe" in error_str or "closed" in error_str:
                    print("Discord not available to clear status")
                else:
                    print(f"Failed to clear status: {e}")
                self.is_connected = False
            except Exception as e:
                print(f"Failed to clear status: {e}")
