import config
import psutil
from python_get_resolve import GetResolve

class ResolveMonitor:
    def __init__(self):
        self.is_running = False
        self.current_project = "None"
        self.current_timeline = "None"
        self.current_page = "None"
        self.resolve = None
        self.project_manager = None
        self.project = None
        self.timeline = None
    
    def check_if_running(self):
        """Check if DaVinci Resolve process is running"""
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] == config.RESOLVE_PROCESS_NAME:
                    self.is_running = True
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.is_running = False
        return False
    
    def connect_to_resolve(self):
        """Establish connection to Resolve API - call this after confirming it's running"""
        try:
            self.resolve = GetResolve()
            if self.resolve:
                self.project_manager = self.resolve.GetProjectManager()
                return True
        except Exception as e:
            print(f"Failed to connect to Resolve: {e}")
        return False
    
    def update_project_info(self):
        """Refresh project and timeline info - call this regularly"""
        if not self.resolve or not self.project_manager:
            if not self.connect_to_resolve():
                return False
        
        try:
            current_page = self.resolve.GetCurrentPage()
            
            if current_page == "None":
                self.current_page = "starting"
                self.current_project = "Starting..."
                self.current_timeline = "Loading..."
                return True
            
            try:
                self.project = self.project_manager.GetCurrentProject()
                if self.project:
                    self.timeline = self.project.GetCurrentTimeline()
                else:
                    self.timeline = None
            except Exception as e:
                print(f"DEBUG: Error getting project: {e}")
                self.project = None
                self.timeline = None
            
            # Handle Python None - this could be Project Manager, Settings, Preferences, etc.
            if current_page is None:
                if self.project is not None:
                    # Check if we have a timeline (in Project Manager you usually don't)
                    if self.timeline is None:
                        # Could be Project Manager, Settings, Preferences, etc.
                        self.current_page = "menu"
                        self.current_project = "In Menus"
                        self.current_timeline = "Project Settings or Manager"
                    else:
                        self.current_page = "menu"
                        self.current_project = "In Menus"
                        self.current_timeline = self.timeline.GetName() if self.timeline else "Unknown"
                    return True
                # Otherwise, Resolve is starting up
                else:
                    self.current_page = "starting"
                    self.current_project = "Starting..."
                    self.current_timeline = "Loading..."
                    return True
            
            # Detect Project Manager by page name
            if current_page == "none":
                self.current_page = "none"
                self.current_project = "Project Manager"
                self.current_timeline = "None"
                return True
            
            # Normal case - project is open
            self.current_page = current_page
            
            # Safely get project name
            if self.project:
                try:
                    project_name = self.project.GetName()
                    if project_name and project_name not in ["None", "Unknown", None]:
                        self.current_project = project_name
                    else:
                        self.current_project = "Loading..."
                except:
                    self.current_project = "Loading..."
            else:
                self.current_project = "Loading..."
            
            # Safely get timeline name
            if self.timeline:
                try:
                    timeline_name = self.timeline.GetName()
                    if timeline_name and timeline_name not in ["None", "Unknown", None]:
                        self.current_timeline = timeline_name
                    else:
                        self.current_timeline = "No Timeline Open"
                except:
                    self.current_timeline = "No Timeline Open"
            else:
                self.current_timeline = "No Timeline Open"
            
            return True
            
        except Exception as e:
            print(f"Error updating project info: {e}")
            self.current_page = "error"
            self.current_project = "Error"
            self.current_timeline = "None"
            return False

    def get_current_project(self):
        return self.current_project

    def get_current_timeline(self):
        return self.current_timeline

    def get_current_page(self):
        return self.current_page
    
    def get_full_status(self):
        """Returns dictionary with all current status info"""
        return {
            "project": self.current_project,
            "timeline": self.current_timeline,
            "page": self.current_page,
            "is_running": self.is_running
        }