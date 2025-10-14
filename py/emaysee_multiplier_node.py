import torch # Often needed for ComfyUI nodes

class EmAySee_MultiplierNode:
    """
    A node with a slider and two integer inputs.
    Outputs are the integer inputs multiplied by the slider value.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "multiplier_slider": ("FLOAT", {"default": 1.0, "min": 1.0, "max": 2.0, "step": 0.01}), # Slider input
                "integer_field_1": ("INT", {"default": 10, "min": -10000, "max": 10000}), # First integer input field
                "integer_field_2": ("INT", {"default": 20, "min": -10000, "max": 10000}), # Second integer input field
            }
        }

    RETURN_TYPES = ("INT", "INT",) # Two integer outputs
    RETURN_NAMES = ("multiplied_output_1", "multiplied_output_2",) # Names for the outputs
    CATEGORY = "EmAySee_Utils" # Category in the ComfyUI menu
    TITLE = "EmAySee Multiplier Node" # Title displayed on the node

    FUNCTION = "EmAySee_calculate_multiplication" # The method that will be executed

    def EmAySee_calculate_multiplication(self, multiplier_slider, integer_field_1, integer_field_2):
        """
        Calculates the multiplication of each integer field by the slider value.
        """
        # Perform the multiplication and cast to integer for the output
        output_1 = int(integer_field_1 * multiplier_slider)
        output_2 = int(integer_field_2 * multiplier_slider)

        # Return the results as a tuple
        return (output_1, output_2,)

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_MultiplierNode": EmAySee_MultiplierNode
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_MultiplierNode": "EmAySee Multiplier Node"
}
