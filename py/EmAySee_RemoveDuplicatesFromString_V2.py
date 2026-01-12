class EmAySee_RemoveDuplicatesFromStringV2:
    """
    Takes a comma-separated string of words, removes duplicate words,
    and returns a new comma-separated string with only unique words.
    Includes an option to sort the output alphabetically or maintain original order.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"multiline": True, "default": "apple, banana, apple, orange, banana, grape"}), # Comma-separated list of words
                "sort_output": ("BOOLEAN", {"default": True}), # New: Toggle to sort the unique words alphabetically
            }
        }

    RETURN_TYPES = ("STRING",) # Output is a single string
    RETURN_NAMES = ("unique_list_string",) # Name for the output
    CATEGORY = "EmAySee_Text" # Category in the ComfyUI menu
    TITLE = "EmAySee Remove Duplicates From String" # Title displayed on the node

    FUNCTION = "EmAySee_process_string" # The method that will be executed

    def EmAySee_process_string(self, input_string, sort_output):
        """
        Splits the input string, removes duplicates, and rejoins.
        Can optionally sort the unique words.
        """
        if not input_string:
            return ("",) # Return an empty string if input is empty

        # 1. Split the string by comma and strip whitespace from each word
        words = [word.strip() for word in input_string.split(',')]

        # 2. Remove duplicates while preserving original order (for Python 3.7+ dicts are insertion-ordered)
        #    This method uses dict.fromkeys() to create a dict where keys are unique words
        #    and then converts the keys back to a list, preserving their first-seen order.
        unique_words_list = list(dict.fromkeys(words))

        # 3. If sorting is requested, sort the list alphabetically
        if sort_output:
            unique_words_list.sort() # Sorts in-place alphabetically

        # 4. Join the unique words back into a comma-separated string
        output_string = ", ".join(unique_words_list)

        return (output_string,) # Return the result as a tuple

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_RemoveDuplicatesFromStringV2": EmAySee_RemoveDuplicatesFromStringV2
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RemoveDuplicatesFromStringV2": "EmAySee Remove Duplicates From StringV2"
}
