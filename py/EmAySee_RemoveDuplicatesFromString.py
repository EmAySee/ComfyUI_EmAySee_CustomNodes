class EmAySee_RemoveDuplicatesFromString:
    """
    Takes a comma-separated string of words, removes duplicate words,
    and returns a new comma-separated string with only unique words.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"multiline": True, "default": "apple, banana, apple, orange, banana, grape"}), # Comma-separated list of words
            }
        }

    RETURN_TYPES = ("STRING",) # Output is a single string
    RETURN_NAMES = ("unique_list_string",) # Name for the output
    CATEGORY = "EmAySee_Text" # Category in the ComfyUI menu
    TITLE = "EmAySee Remove Duplicates From String" # Title displayed on the node

    FUNCTION = "EmAySee_process_string" # The method that will be executed

    def EmAySee_process_string(self, input_string):
        """
        Splits the input string, removes duplicates, and rejoins.
        """
        if not input_string:
            return ("",) # Return an empty string if input is empty

        # 1. Split the string by comma
        #    strip() removes leading/trailing whitespace from each word
        words = [word.strip() for word in input_string.split(',')]

        # 2. Use a set to automatically handle uniqueness
        #    Sets do not preserve order, but for a simple list of words,
        #    this is often acceptable. If order is crucial, more complex
        #    logic would be needed (e.g., iterating and adding to a new list
        #    only if not already present).
        unique_words_set = set(words)

        # 3. Convert the set back to a list (optional, but useful for joining)
        #    Sorting here makes the output consistent, otherwise order is arbitrary.
        unique_words_list = sorted(list(unique_words_set))

        # 4. Join the unique words back into a comma-separated string
        output_string = ", ".join(unique_words_list)

        return (output_string,) # Return the result as a tuple

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_RemoveDuplicatesFromString": EmAySee_RemoveDuplicatesFromString
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RemoveDuplicatesFromString": "EmAySee Remove Duplicates From String"
}