import sys
import datetime
import re

# Platform-specific imports with error handling
try:
    from AppKit import NSWorkspace
except ImportError:
    NSWorkspace = None

try:
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGNullWindowID,
        kCGWindowListOptionOnScreenOnly,
    )
except ImportError:
    CGWindowListCopyWindowInfo = None
    kCGNullWindowID = None
    kCGWindowListOptionOnScreenOnly = None

try:
    import subprocess
except ImportError:
    subprocess = None  # Should always be available in standard lib


def human_readable_time(timestamp: int) -> str:
    """Converts a Unix timestamp into a human-readable relative time string.

    Args:
        timestamp: The Unix timestamp (seconds since epoch).

    Returns:
        A string representing the relative time (e.g., "5 minutes ago").
    """
    now = datetime.datetime.now()
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    diff = now - dt_object
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds < 60:
        return f"{diff.seconds} seconds ago"
    elif diff.seconds < 3600:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return f"{diff.seconds // 3600} hours ago"


def timestamp_to_human_readable(timestamp: int) -> str:
    """Converts a Unix timestamp into a human-readable absolute date/time string.

    Args:
        timestamp: The Unix timestamp (seconds since epoch).

    Returns:
        A string representing the absolute date and time (YYYY-MM-DD HH:MM:SS),
        or an empty string if conversion fails.
    """
    try:
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        return dt_object.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""


def get_active_app_name_osx() -> str:
    """Gets the name of the active application on macOS.

    Requires the pyobjc package.

    Returns:
        The name of the active application, or an empty string if unavailable.
    """
    if NSWorkspace is None:
        return ""  # Indicate unavailability if import failed
    try:
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        return active_app.get("NSApplicationName", "")
    except:
        return ""


def get_active_window_title_osx() -> str:
    """Gets the title of the active window on macOS.

    Requires the pyobjc package. Finds the frontmost window associated with the
    currently active application.

    Returns:
        The title of the active window, or an empty string if unavailable.
    """
    if CGWindowListCopyWindowInfo is None or kCGNullWindowID is None or kCGWindowListOptionOnScreenOnly is None:
        return ""  # Indicate unavailability if import failed
    try:
        app_name = get_active_app_name_osx()
        if not app_name:
            return ""

        # Get window list ordered front-to-back
        options = kCGWindowListOptionOnScreenOnly
        window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

        for window in window_list:
            # Check if the window belongs to the active application
            if window.get("kCGWindowOwnerName") == app_name:
                # Check if it's a normal window (layer 0) and has a title
                if window.get("kCGWindowLayer") == 0 and "kCGWindowName" in window:
                    title = window.get("kCGWindowName", "")
                    if title:  # Return the first non-empty title found
                        return title
        # Fallback if no suitable window title found for the active app
        return ""
    except Exception as e:
        print(f"Error getting macOS window title: {e}")
        return ""
    return ""  # Default if no specific window is found
    
def get_active_app_name() -> str:
    """Gets the active application name for the current platform.

    Returns:
        The name of the active application, or an empty string if unavailable
        or the platform is unsupported (or not implemented).
    """
    if sys.platform == "darwin":
        return get_active_app_name_osx()
    else:
        raise NotImplementedError(f"Platform '{sys.platform}' not supported yet for get_active_app_name")


def get_active_window_title() -> str:
    """Gets the active window title for the current platform.

    Returns:
        The title of the active window, or an empty string if unavailable
        or the platform is unsupported (or not implemented).
    """
    if sys.platform == "darwin":
        return get_active_window_title_osx()
    else:
        print("Warning: Active window title retrieval not implemented for this platform.")
        raise NotImplementedError(f"Platform '{sys.platform}' not supported yet for get_active_window_title")


def is_user_active_osx() -> bool:
    """Checks if the user is active on macOS based on HID idle time.

    Requires the pyobjc package and uses the 'ioreg' command. Considers the user
    active if the idle time is less than 5 seconds.

    Returns:
        True if the user is considered active, False otherwise. Returns True
        if the check fails for any reason.
    """
    if subprocess is None:
        print("Warning: 'subprocess' module not available, assuming user is active.")
        return True
    try:
        # Run the 'ioreg' command to get idle time information
        # Filtering directly with -k is more efficient
        output = subprocess.check_output(
            ["ioreg", "-c", "IOHIDSystem", "-r", "-k", "HIDIdleTime"], timeout=1
        ).decode()

        # Find the line containing "HIDIdleTime"
        for line in output.splitlines():
            if "HIDIdleTime" in line:
                # Extract the idle time value
                idle_time = int(line.split("=")[-1].strip())

                # Convert idle time from nanoseconds to seconds
                idle_seconds = idle_time / 1_000_000_000  # Use underscore for clarity

                # If idle time is less than 5 seconds, consider the user active
                return idle_seconds < 5.0

        # If "HIDIdleTime" is not found (e.g., screen locked), assume inactive?
        # Or assume active as a fallback? Let's assume active for now.
        print("Warning: Could not find HIDIdleTime in ioreg output.")
        return True

    except subprocess.TimeoutExpired:
        print("Warning: 'ioreg' command timed out, assuming user is active.")
        return True
    except subprocess.CalledProcessError as e:
        # This might happen if the class IOHIDSystem is not found, etc.
        print(f"Warning: 'ioreg' command failed ({e}), assuming user is active.")
        return True
    except Exception as e:
        print(f"An error occurred during macOS idle check: {e}")
        # Fallback: assume the user is active
        return True

def is_user_active() -> bool:
    """Checks if the user is active on the current platform.

    Considers the user active if their last input was recent (e.g., < 5 seconds ago).
    Implementation varies by platform.

    Returns:
        True if the user is considered active, False otherwise. Returns True
        if the check is not implemented or fails.
    """
    if sys.platform == "darwin":
        return is_user_active_osx()
    else:
        print(f"Warning: User active check not supported for platform '{sys.platform}', assuming active.")
        raise NotImplementedError(f"Platform '{sys.platform}' not supported yet for is_user_active")
