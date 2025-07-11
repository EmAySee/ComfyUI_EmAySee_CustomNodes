class EmAySee_ImagePassthrough:
    """
    A simple passthrough node for images.
    Takes an image input and outputs the same image.
    Useful for renaming input connections in the workflow.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Input image connection. You can rename this input visually in the UI.
                "input_image": ("IMAGE",),
            }
        }

    # The node outputs an image
    RETURN_TYPES = ("IMAGE",)
    # You can rename the output connection visually in the UI as well.
    RETURN_NAMES = ("output_image",)

    # Category for the ComfyUI menu
    CATEGORY = "EmAySee_Utils"
    # Title displayed on the node
    TITLE = "EmAySee Image Passthrough"

    # The method that will be executed when the node runs
    FUNCTION = "pass_through"

    def pass_through(self, input_image):
        """
        Simply returns the input image.
        """
        # The node's logic is just to return the input image.
        return (input_image,)

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_ImagePassthrough": EmAySee_ImagePassthrough
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ImagePassthrough": "EmAySee Image Passthrough"
}
