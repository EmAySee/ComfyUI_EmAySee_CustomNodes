import re

class EmAySee_RemoveWordsFromText:
    """
    Removes specific words from a main text string based on a comma-separated list.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "main_text": ("STRING", {"multiline": True, "default": "A dog, a cat, and a bird."}), # The main text to be parsed
                "words_to_remove": ("STRING", {"multiline": True, "default": "dog, cat, and"}), # Comma-separated list of words to remove
            }
        }

    RETURN_TYPES = ("STRING",) # Output is a single string
    RETURN_NAMES = ("cleaned_text",) # Name for the output
    CATEGORY = "EmAySee_Text" # Category in the ComfyUI menu
    TITLE = "EmAySee Remove Words From Text" # Title displayed on the node

    FUNCTION = "EmAySee_process_text" # The method that will be executed

    def EmAySee_process_text(self, main_text, words_to_remove):
        """
        Removes each word from the 'words_to_remove' list from the 'main_text' string.
        """
        if not main_text or not words_to_remove:
            return (main_text,) # Return the original text if either input is empty

        # 1. Split the string of words to remove by comma, and strip whitespace.
        #    We escape special characters for use in a regex pattern.
        words_list = [re.escape(word.strip()) for word in words_to_remove.split(',')]
        
        # 2. Join the words with a pipe '|' to create a regex OR pattern.
        #    \b ensures we match whole words only, avoiding partial matches.
        #    For example, we don't want to remove "cat" from "caterpillar".
        pattern = r"\b(" + "|".join(words_list) + r")\b"

        # 3. Use re.sub to find and replace all matching words with an empty string.
        #    We also replace multiple spaces that might be left behind.
        cleaned_text = re.sub(pattern, "", main_text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

        return (cleaned_text,) # Return the cleaned string as a tuple

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_RemoveWordsFromText": EmAySee_RemoveWordsFromText
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RemoveWordsFromText": "EmAySee Remove Words From Text"
}