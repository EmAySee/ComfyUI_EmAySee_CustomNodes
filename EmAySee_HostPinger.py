import subprocess
import platform
import os

class EmAySee_HostPinger:
    """
    Pings a specified host and outputs 1 if the host is reachable (up)
    and 0 if the host is unreachable (down).
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "host": ("STRING", {"default": "google.com"}), # Hostname or IP address to ping
            }
        }

    RETURN_TYPES = ("INT",) # Output is a single integer (1 or 0)
    RETURN_NAMES = ("is_up",) # Name for the output
    CATEGORY = "EmAySee_Network" # Category in the ComfyUI menu
    TITLE = "EmAySee Host Pinger" # Title displayed on the node

    FUNCTION = "EmAySee_check_host" # The method that will be executed

    def EmAySee_check_host(self, host):
        """
        Executes a system ping command to check if the host is reachable.
        Returns 1 if successful, 0 otherwise.
        """
        # Determine the correct ping command based on the operating system
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        count = '1' # Number of ping requests
        timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
        timeout_value = '1000' if platform.system().lower() == 'windows' else '1' # Timeout in ms (Windows) or seconds (Linux/macOS)

        command = [
            'ping',
            param, count,
            timeout_param, timeout_value,
            host
        ]

        is_up = 0 # Default to 0 (down)

        try:
            # Execute the ping command
            # capture_output=True captures stdout and stderr
            # text=True decodes stdout/stderr as text
            # timeout sets a maximum time to wait for the command to complete
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=2, # Set a reasonable timeout for the subprocess itself
                check=False # Do not raise an exception for non-zero exit codes (like host unreachable)
            )

            # Check the return code
            # A return code of 0 usually indicates success (host is reachable)
            if result.returncode == 0:
                is_up = 1
            else:
                # You can optionally print stderr for debugging if the ping fails
                # print(f"Ping command failed for {host}: {result.stderr}")
                is_up = 0

        except FileNotFoundError:
            print(f"Error: 'ping' command not found. Make sure ping is installed and in your system's PATH.")
            is_up = 0
        except subprocess.TimeoutExpired:
            print(f"Error: Ping command timed out for {host}.")
            is_up = 0
        except Exception as e:
            print(f"An unexpected error occurred while pinging {host}: {e}")
            is_up = 0

        return (is_up,) # Return the result as a tuple

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_HostPinger": EmAySee_HostPinger
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_HostPinger": "EmAySee Host Pinger"
}
