import os
import folder_paths # ComfyUI utility to get model paths

# Define the main class for your custom node.
# The class name will be used in NODE_CLASS_MAPPINGS.
class EmAySee_LoraFilePicker:
    """
    A ComfyUI custom node to pick LORA files from configured paths.
    It provides a dropdown list of available LORA files and outputs
    the selected filename and its full file path.
    """
    def __init__(self):
        # Constructor for the node. No special initialization needed for this node.
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types (widgets and connections) for the node.
        This method is a class method and must return a dictionary.
        """
        # Get all LORA files from ComfyUI's configured LORA paths.
        # folder_paths.get_filename_list("loras") returns a list of relative filenames
        # (e.g., "my_lora.safetensors", "subdir/another_lora.pt").
        lora_files = folder_paths.get_filename_list("loras")
        
        # Add a "None" option at the beginning of the list.
        # This allows the user to explicitly select no LORA.
        lora_files.insert(0, "None")

        return {
            "required": {
                # "lora_name" is the name of the input port that will appear on the node.
                # (lora_files,) creates a dropdown widget in the ComfyUI interface,
                # populated with the list of LORA files.
                "lora_name": (lora_files,), 
            },
        }

    # Define the types of data that this node will output.
    # RETURN_TYPES must be a tuple of ComfyUI data types (e.g., "STRING", "IMAGE", "MODEL").
    RETURN_TYPES = ("STRING", "STRING",) # Outputs two strings.

    # Define the names for the output ports. These names will appear on the node.
    RETURN_NAMES = ("filename", "full_filepath",)

    # Specifies the Python function within this class that ComfyUI should call
    # when the node is executed in a workflow.
    FUNCTION = "pick_lora_file"

    # Defines the category under which this node will appear in the ComfyUI "Add Node" menu.
    # Using "EmAySee/" as a prefix helps organize your custom nodes.
    CATEGORY = "EmAySee/File Utilities" 

    def pick_lora_file(self, lora_name):
        """
        The core logic of the node. This function is executed when the node runs.
        It takes the selected LORA filename as input and returns the filename
        and its corresponding full file path.
        """
        # If the "None" option is selected in the dropdown, return empty strings.
        if lora_name == "None":
            return ("", "") 

        full_lora_path = None

        # Attempt to find the full path of the selected LORA file.
        # folder_paths.get_filename_list("loras", return_full_paths=True)
        # returns a list of absolute paths for all LORA files that ComfyUI has discovered.
        for lora_path in folder_paths.get_filename_list("loras", return_full_paths=True):
            # Check if the base name of the current lora_path matches the selected lora_name,
            # or if the full lora_path ends with the selected lora_name (this handles
            # cases where lora_name might include subdirectories, e.g., "my_folder/my_lora.safetensors").
            if os.path.basename(lora_path) == lora_name or lora_path.endswith(lora_name):
                full_lora_path = lora_path
                break
        
        # Fallback mechanism: If the LORA was not found by direct matching (e.g., due to
        # inconsistencies in how names are reported vs. stored, or new files not yet indexed).
        if full_lora_path is None:
            # Get all configured base directories for LORAs.
            lora_folders = folder_paths.get_folder_paths("loras")
            for folder in lora_folders:
                # Construct a potential full path by joining the base folder and the selected LORA name.
                potential_path = os.path.join(folder, lora_name)
                # Verify if this constructed path actually exists and points to a file.
                if os.path.exists(potential_path) and os.path.isfile(potential_path):
                    full_lora_path = potential_path
                    break
            
            # If after all attempts, the file still cannot be located, print a warning
            # and return empty strings to ensure the workflow doesn't crash.
            if full_lora_path is None:
                print(f"Warning: LORA file '{lora_name}' not found in known ComfyUI LORA paths.")
                return ("", "")

        # Return the selected filename and its successfully determined full path.
        return (lora_name, full_lora_path)

# NODE_CLASS_MAPPINGS is a mandatory dictionary that ComfyUI uses to discover
# and register your custom nodes. The keys are internal identifiers, and the
# values are the Python classes that define your nodes.
NODE_CLASS_MAPPINGS = {
    "EmAySee_LoraFilePicker": EmAySee_LoraFilePicker,
}

# NODE_DISPLAY_NAME_MAPPINGS is an optional dictionary that provides
# more user-friendly names for your nodes in the ComfyUI interface.
# This name will appear in the "Add Node" menu.
NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_LoraFilePicker": "EmAySee Lora File Picker",
}

# WEB_DIRECTORY can be defined if your node has custom web components (JavaScript/CSS).
# For this node, it's not strictly necessary, but it's a common practice to include it
# if you plan to extend the node with a custom UI later.
# WEB_DIRECTORY = "./web" # Uncomment and create a 'web' folder if needed for JS/CSS