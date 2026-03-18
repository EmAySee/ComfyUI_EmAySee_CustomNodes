import json
import os
from safetensors import safe_open

# Node class mapping and display name (how it appears in ComfyUI)
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class EmAySee_LoRAMetadataExtractor: # Prepend EmAySee_ to the class name
    """
    A ComfyUI custom node to extract and display training metadata
    from a .safetensors LoRA file.

    It attempts to find the full Kohya_ss configuration under '__metadata__',
    or extracts individual 'ss_' prefixed keys if '__metadata__' is not present.
    """
    def __init__(self):
        pass

    # Define the return types of the node's outputs
    # This node will output a single STRING
    RETURN_TYPES = ("STRING",)

    # Define the names of the node's outputs
    RETURN_NAMES = ("metadata_json_string",)

    # Define the category where the node will appear in ComfyUI
    FUNCTION = "extract_metadata"
    CATEGORY = "Mac Custom Nodes/LoRA Tools" # You can change this category if you prefer

    # Define the input types of the node
    # This node requires a file path to a .safetensors file
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_filepath": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {
                # Optional input for a file upload, if you prefer to drag-and-drop
                # Note: ComfyUI's file input might not directly give a full path easily
                # Manual string path is often more reliable for existing files.
                "lora_upload": ("LORA", {"forceInput": True}), # This allows drag-and-drop, but you'd still need to get the path
            }
        }

    def extract_metadata(self, lora_filepath, lora_upload=None):
        """
        Extracts metadata from the specified .safetensors file.

        Args:
            lora_filepath (str): The full path to the .safetensors LoRA file.
            lora_upload (str, optional): ComfyUI's internal representation of an uploaded LORA.
                                         Not directly used for path here, but included for compatibility.

        Returns:
            tuple: A tuple containing the metadata as a formatted JSON string.
        """
        if not lora_filepath:
            return ("Error: LoRA filepath cannot be empty.",)

        # Ensure the file exists
        if not os.path.exists(lora_filepath):
            return (f"Error: File not found at '{lora_filepath}'. Please check the path.",)
        if not os.path.isfile(lora_filepath):
            return (f"Error: Path '{lora_filepath}' is not a valid file.",)

        try:
            with safe_open(lora_filepath, framework="pt", device="cpu") as f:
                metadata = f.metadata()
                output_data = {}

                # Attempt to get the full Kohya_ss config if nested under __metadata__ (newer Kohya)
                if "__metadata__" in metadata:
                    try:
                        output_data = json.loads(metadata["__metadata__"])
                        # Add a flag to indicate it's the full config
                        output_data["_metadata_source"] = "Full Kohya_ss Config (__metadata__)"
                    except json.JSONDecodeError:
                        output_data["_error"] = "Failed to parse __metadata__ as JSON."
                        output_data["_raw_metadata"] = metadata["__metadata__"]
                        output_data["_metadata_source"] = "Raw __metadata__ (Parse Error)"
                else:
                    # If not, extract individual ss_ prefixed keys and their values
                    extracted_params = {}
                    for key, value in metadata.items():
                        # First, attempt general type conversion (int, float, bool, None)
                        if isinstance(value, str):
                            if value.lower() == "true":
                                value = True
                            elif value.lower() == "false":
                                value = False
                            elif value.lower() == "none": # Handle "None" as Python None
                                value = None
                            else:
                                try:
                                    if "." in value: # Likely a float
                                        value = float(value)
                                    else: # Try integer
                                        value = int(value)
                                except ValueError:
                                    pass # Keep as string if not a simple number/boolean

                        # Then, specifically parse known nested JSON strings
                        if key in ["ss_tag_frequency", "ss_bucket_info", "ss_datasets"]:
                            if isinstance(value, str): # Only try to parse if it's still a string
                                try:
                                    value = json.loads(value)
                                except json.JSONDecodeError:
                                    # If parsing fails, keep it as a string but note the error
                                    value = f"ERROR_PARSING_JSON: {value}"
                        
                        # Store the processed value
                        extracted_params[key] = value

                    output_data = extracted_params
                    output_data["_metadata_source"] = "Extracted ss_ Prefixed Keys"

                # Return the data as a pretty-printed JSON string
                return (json.dumps(output_data, indent=2),)

        except Exception as e:
            return (f"An unexpected error occurred during metadata extraction: {e}",)

# Register the node
NODE_CLASS_MAPPINGS["EmAySee_LoRAMetadataExtractor"] = EmAySee_LoRAMetadataExtractor # Prepend EmAySee_
NODE_DISPLAY_NAME_MAPPINGS["EmAySee_LoRA Metadata Extractor"] = "EmAySee_LoRA Metadata Extractor" # Prepend EmAySee_
