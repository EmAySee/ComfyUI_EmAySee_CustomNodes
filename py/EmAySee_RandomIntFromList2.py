import random
import time  # Import the time module

class EmAySee_RandomIntFromList:
    """
    ComfyUI custom node to select a random integer from a user-defined list or range,
    with an optional seed for reproducibility.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "integer_list": ("STRING", {
                    "default": "1, 2, 4-6, 9, 11, 13-18",
                    "multiline": False,
                    "placeholder": "Enter integers or ranges (e.g., 1, 2, 4-6, 9)"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,  # Minimum seed value
                    "step": 1,  # Increment/decrement step
                    "display": "number" # Optional, for better UI
                    # Can add "forceInput": True to *require* a connection.
                }),
            },
            "optional": {
               "use_system_time": ("BOOLEAN", {
                   "default": True,  #Default to a new seed on each run
                   "label_on": "Enabled", #Optional better UI
                   "label_off": "Disabled"
               })
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("random_integer",)
    FUNCTION = "get_random_integer"
    CATEGORY = "EmAySee/Utilities/List"

    def get_random_integer(self, integer_list, seed, use_system_time=True):
        """
        Parses the input, sets the seed, and returns a random integer.
        """
        try:
            numbers = self.parse_integer_list(integer_list)
            if not numbers:
                return (0,)
            
            # Seed handling:
            if use_system_time:
                # Use system time * number of milliseconds for a more unique seed each run
                seed = int(time.time() * 1000)  # Use milliseconds for more variation
                
            random.seed(seed)  # Set the seed *before* calling random.choice
            random_int = random.choice(numbers)
            return (random_int,)

        except ValueError:
            print("Error: Invalid integer list format. Please use comma-separated integers and ranges (e.g., 1, 2-5, 10).")
            return (0,)

    def parse_integer_list(self, integer_list_string):
        """
        Parses the comma-separated string of integers and ranges.
        """
        numbers = []
        parts = integer_list_string.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    numbers.extend(range(start, end + 1))
                except ValueError:
                    raise ValueError("Invalid range format.")
            else:
                try:
                    numbers.append(int(part))
                except ValueError:
                    raise ValueError("Invalid integer format.")
        return numbers

NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomIntFromList": EmAySee_RandomIntFromList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomIntFromList": "EmAySee Vroom Random Integer from List 2"
}