class EmAySee_GreaterThanNode:
    """
    A custom ComfyUI node that checks if float input A is greater than float input B.
    Returns 1 if A > B (True), and 0 otherwise (False).
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        'A' and 'B' are float inputs with default values of 0.0.
        """
        return {
            "required": {
                "A": ("FLOAT", {"default": 0.0, "min": -10000.0, "max": 10000.0, "step": 0.01}),
                "B": ("FLOAT", {"default": 0.0, "min": -10000.0, "max": 10000.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("INT",)  # The node will return an integer (0 or 1)
    RETURN_NAMES = ("RESULT",) # The output port will be named 'RESULT'
    FUNCTION = "compare_floats"  # The name of the function that executes the node's logic
    CATEGORY = "Logic"  # The category where the node will appear in ComfyUI

    def compare_floats(self, A, B):
        """
        Compares float A and float B.
        Returns 1 if A is greater than B, otherwise returns 0.
        """
        if A > B:
            return (1,)  # Return as a tuple, as ComfyUI expects
        else:
            return (0,)  # Return as a tuple

# A dictionary of all custom nodes available in this file.
# The key is the node class name, and the value is the class itself.
NODE_CLASS_MAPPINGS = {
    "EmAySee_GreaterThanNode": EmAySee_GreaterThanNode
}

# A dictionary that provides more user-friendly names for the nodes in the UI.
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_GreaterThanNode": "EmAySee Greater Than (Float)"
}

