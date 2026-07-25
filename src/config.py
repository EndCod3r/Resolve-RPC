DISCORD_CLIENT_ID = "1512377180213088388"  # Your Discord application's Client ID. This is required to connect to Discord's Rich Presence API. You can find this in the Discord Developer Portal under your application settings or use the provided default ID.
POLL_INTERVAL = 5  # The interval (in seconds) at which the script checks for updates in DaVinci Resolve. Adjust as needed to balance responsiveness and performance.
RESOLVE_PROCESS_NAME = "Resolve.exe"  # The name of the DaVinci Resolve process executable. Used to check if DaVinci Resolve is running.
EXIT_AFTER_CLOSED = 30  # The duration (in seconds) to wait after DaVinci Resolve has closed before the script exits. This allows for a grace period in case of accidental closure or temporary issues.

# Change these to whatever you want Discord to display before the timeline name.
PAGE_MESSAGES = {
    "media": "Managing media for:",
    "cut": "Cutting:",
    "edit": "Editing:",
    "fusion": "Making effects for:",
    "color": "Color grading:",
    "fairlight": "Mixing audio for:",
    "deliver": "Rendering:",
    "photo": "Editing photos for:",
}

# Use {page} as a placeholder for the page name
PAGE_SMALL_TEXT = "{page} Page"  # Will show as "Edit Page", "Color Page", etc.


# Customize status for unsaved projects
UNSAVED_PROJECT_DETAILS = "Unsaved Project"

# Customize default message for unknown pages. Use {page} as a placeholder for the page name if you want to include it.
DEFAULT_PAGE_MESSAGE = "Working on {page} page"

# Timeline display settings. Use {timeline} as a placeholder for the timeline name. If no timeline is open, it will show "(No timeline)" by default.
NO_TIMELINE_TEXT = "(No timeline)"
TIMELINE_FORMAT = "'{timeline}'"  # How timeline names are displayed

# Menu state (Project Settings/Manager, Preferences, etc.)
MENU_STATE = "In Menus"
MENU_DETAILS = "Project Settings or Manager"
MENU_SMALL_TEXT = "In Settings/Menus"

# Customize status for when no project is open. This almost never happens since Resolve always has a project or project manager open, but just in case.
NO_PROJECT_STATE = "Idle"
NO_PROJECT_DETAILS = "No Project Open"
