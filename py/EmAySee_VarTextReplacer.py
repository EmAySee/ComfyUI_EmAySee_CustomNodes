class EmAySee_VarTextReplacer:
    """
    Replaces placeholders in a main text with values from input variables.
    Placeholders should be in the format %variable_name%.
    Now supports var1 through var10.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "main_text": ("STRING", {"default": "This is %var1%, that is %var2%, and here is %var3%. We also have %var4%, %var5%, %var6%, %var7%, %var8%, %var9%, and finally %var10%.", "multiline": True}), # Main text with placeholders
                "var1": ("STRING", {"default": "Variable 1"}), # Input variable for %var1%
                "var2": ("STRING", {"default": "Variable 2"}), # Input variable for %var2%
                "var3": ("STRING", {"default": "Variable 3"}), # Input variable for %var3%
                "var4": ("STRING", {"default": "Variable 4"}), # Input variable for %var4%
                "var5": ("STRING", {"default": "Variable 5"}), # Input variable for %var5%
                "var6": ("STRING", {"default": "Variable 6"}), # Input variable for %var6%
                "var7": ("STRING", {"default": "Variable 7"}), # Input variable for %var7%
                "var8": ("STRING", {"default": "Variable 8"}), # Input variable for %var8%
                "var9": ("STRING", {"default": "Variable 9"}), # Input variable for %var9%
                "var10": ("STRING", {"default": "Variable 10"}), # Input variable for %var10%
            }
        }

    RETURN_TYPES = ("STRING",) # Output is a single string
    RETURN_NAMES = ("replaced_text",) # Name for the output
    CATEGORY = "EmAySee_Text" # Category in the ComfyUI menu
    TITLE = "EmAySee Var Text Replacer" # Title displayed on the node

    FUNCTION = "EmAySee_replace_placeholders" # The method that will be executed

    def EmAySee_replace_placeholders(self, main_text, var1, var2, var3, var4, var5, var6, var7, var8, var9, var10):
        """
        Replaces %var1% through %var10% in the main_text with provided values.
        """
        output_text = main_text

        # Replace the specific variables we defined in INPUT_TYPES
        output_text = output_text.replace("%var1%", str(var1))
        output_text = output_text.replace("%var2%", str(var2))
        output_text = output_text.replace("%var3%", str(var3))
        output_text = output_text.replace("%var4%", str(var4))
        output_text = output_text.replace("%var5%", str(var5))
        output_text = output_text.replace("%var6%", str(var6))
        output_text = output_text.replace("%var7%", str(var7))
        output_text = output_text.replace("%var8%", str(var8))
        output_text = output_text.replace("%var9%", str(var9))
        output_text = output_text.replace("%var10%", str(var10))

        # Note: Using str() just in case a non-string input is ever connected,
        # though INPUT_TYPES specifies STRING.

        return (output_text,) # Return the result as a tuple

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_VarTextReplacer": EmAySee_VarTextReplacer
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_VarTextReplacer": "EmAySee Var Text Replacer"
}
