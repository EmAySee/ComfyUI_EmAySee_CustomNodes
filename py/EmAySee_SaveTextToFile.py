import os
import folder_paths # ComfyUI utility to get paths

class EmAySee_SaveTextToFile:
    """
    Saves a string input to a text file with a specified filename and subfolder.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_to_save": ("STRING", {"multiline": True}), # The text content to save
                "filename": ("STRING", {"default": "output_text"}), # The desired filename (without extension)
                "subfolder": ("STRING", {"default": ""}), # Optional subfolder within the output directory
            }
        }

    # Define RETURN_TYPES as an empty tuple since this node has no direct outputs
    # This is required by ComfyUI even for nodes without outputs.
    RETURN_TYPES = ()
    # RETURN_NAMES = () # RETURN_NAMES is not strictly necessary if RETURN_TYPES is empty

    CATEGORY = "EmAySee_Utils" # Category in the ComfyUI menu
    TITLE = "EmAySee Save Text to File" # Title displayed on the node

    FUNCTION = "EmAySee_save_text" # The method that will be executed

    def EmAySee_save_text(self, text_to_save, filename, subfolder):
        """
        Saves the text content to a file in the specified subfolder.
        """
        # Get the base output directory for ComfyUI
        output_dir = folder_paths.get_output_paths(None)[0] # Get the first output path

        # Construct the full directory path
        if subfolder:
            save_dir = os.path.join(output_dir, subfolder)
        else:
            save_dir = output_dir

        # Ensure the directory exists, create if necessary
        os.makedirs(save_dir, exist_ok=True)

        # Construct the full file path with .txt extension
        # Sanitize filename to remove potentially problematic characters
        safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
        if not safe_filename:
             safe_filename = "output_text" # Fallback if filename becomes empty after sanitization

        file_path = os.path.join(save_dir, f"{safe_filename}.txt")

        try:
            # Save the text content to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_to_save)

            print(f"Successfully saved text to: {file_path}")

        except IOError as e:
            print(f"Error saving text to file {file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving text: {e}")

        # This node doesn't return any specific output values, so return an empty tuple.
        return ()

# Mapping of node class name to the class
NODE_CLASS_MAPPINGS = {
    "EmAySee_SaveTextToFile": EmAySee_SaveTextToFile
}

# Mapping of node class name to the display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SaveTextToFile": "EmAySee Save Text to File"
}
