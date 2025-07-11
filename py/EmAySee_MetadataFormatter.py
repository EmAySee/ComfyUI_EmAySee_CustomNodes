import json

# Node class mapping and display name (how it appears in ComfyUI)
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class EmAySee_MetadataFormatter:
    """
    A ComfyUI custom node to format the extracted LoRA metadata
    into a more human-readable, line-by-line string.
    It removes 'ss_' prefixes and handles nested JSON fields.
    """
    def __init__(self):
        pass

    # Define the return types of the node's outputs
    RETURN_TYPES = ("STRING",)

    # Define the names of the node's outputs
    RETURN_NAMES = ("formatted_metadata_string",)

    # Define the category where the node will appear in ComfyUI
    FUNCTION = "format_metadata"
    CATEGORY = "Mac Custom Nodes/LoRA Tools" # Consistent with your other node

    # Define the input types of the node
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "metadata_json_string": ("STRING", {"multiline": True, "default": "{}"}),
            }
        }

    def format_metadata(self, metadata_json_string):
        """
        Parses a JSON string of LoRA metadata and formats it into
        a readable line-by-line string.
        """
        try:
            # Parse the input JSON string
            metadata = json.loads(metadata_json_string)
        except json.JSONDecodeError as e:
            return (f"Error: Invalid JSON input for metadata: {e}",)

        formatted_lines = []
        
        # Add a header for clarity
        formatted_lines.append("--- LoRA Training Parameters ---")

        # Sort keys for consistent output order
        sorted_keys = sorted(metadata.keys())

        for key in sorted_keys:
            value = metadata[key]
            display_key = key.replace("ss_", "") # Remove ss_ prefix for display

            # Skip internal metadata source flag
            if key == "_metadata_source":
                continue

            # Handle specific nested JSON fields for better readability
            if key == "ss_tag_frequency":
                formatted_lines.append(f"\n{display_key.replace('_', ' ').title()}:")
                # Parse the nested tag frequency JSON string
                if isinstance(value, dict): # Should already be parsed by Extractor node
                    for sub_key, sub_value in value.items():
                        formatted_lines.append(f"  - {sub_key}: {sub_value}")
                else:
                    formatted_lines.append(f"  (Raw data, could not parse: {value})")
            elif key == "ss_bucket_info":
                formatted_lines.append(f"\n{display_key.replace('_', ' ').title()}:")
                if isinstance(value, dict): # Should already be parsed by Extractor node
                    if "buckets" in value and isinstance(value["buckets"], dict):
                        formatted_lines.append("  Buckets:")
                        for bucket_id, bucket_data in value["buckets"].items():
                            res = bucket_data.get("resolution", "N/A")
                            count = bucket_data.get("count", "N/A")
                            formatted_lines.append(f"    - ID {bucket_id}: Resolution {res}, Count {count}")
                    if "mean_img_ar_error" in value:
                        formatted_lines.append(f"  Mean Image AR Error: {value['mean_img_ar_error']:.6f}")
                else:
                    formatted_lines.append(f"  (Raw data, could not parse: {value})")
            elif key == "ss_datasets":
                formatted_lines.append(f"\n{display_key.replace('_', ' ').title()}:")
                if isinstance(value, list): # Should already be parsed by Extractor node
                    for i, dataset_entry in enumerate(value):
                        formatted_lines.append(f"  Dataset Entry {i}:")
                        for ds_key, ds_val in dataset_entry.items():
                            if isinstance(ds_val, dict): # For nested dicts like tag_frequency within datasets
                                formatted_lines.append(f"    - {ds_key.replace('_', ' ').title()}:")
                                for sub_key, sub_val in ds_val.items():
                                    formatted_lines.append(f"      - {sub_key}: {sub_val}")
                            else:
                                formatted_lines.append(f"    - {ds_key.replace('_', ' ').title()}: {ds_val}")
                else:
                    formatted_lines.append(f"  (Raw data, could not parse: {value})")
            else:
                # Format other parameters
                # Attempt to make values more readable (e.g., float to scientific notation if very small)
                display_value = value
                if isinstance(value, float) and value < 0.001 and value != 0.0:
                    display_value = f"{value:.1e}" # Scientific notation for small floats
                
                formatted_lines.append(f"{display_key.replace('_', ' ').title()}: {display_value}")

        formatted_lines.append("\n--- End of Parameters ---")

        return ("\n".join(formatted_lines),)

# Register the node
NODE_CLASS_MAPPINGS["EmAySee_MetadataFormatter"] = EmAySee_MetadataFormatter
NODE_DISPLAY_NAME_MAPPINGS["EmAySee_LoRA Metadata Formatter"] = "EmAySee_LoRA Metadata Formatter"
