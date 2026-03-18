class EmAySee_AnyPassthrough:
    """
    A simple passthrough node for any data type.
    Takes any input and outputs the same data.
    Useful for renaming input connections in the workflow.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Input connection that accepts any data type (*).
                # You can rename this input visually in the UI.
                "input_any": ("*",),
            }
        }

    # The node outputs the same type as the input (any type)
    RETURN_TYPES = ("*",)
    # You can rename the output connection visually in the UI as well.
    RETURN_NAMES = ("output_any",)

    # Category for the ComfyUI menu
    CATEGORY = "EmAySee_Utils"
    # Title displayed on the node
    TITLE = "EmAySee Any Passthrough"

    # The method that will be executed when the node runs
    FUNCTION = "pass_through_any"

    def pass_through_any(self, input_any):
        """
        Simply returns the input data of any type.
        """
        # The node's logic is just to return the input data.
        return (input_any,)

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_AnyPassthrough": EmAySee_AnyPassthrough
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_AnyPassthrough": "EmAySee Any Passthrough"
}
