import re

class Emaysee_TagParser:
    """
    Parses a combined text string to extract the Natural Description 
    and Image Tags based on custom bracket definitions.
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Natural Description", "Image Tags")
    FUNCTION = "parse_tags"
    CATEGORY = "Emaysee/Text"

    def parse_tags(self, text):
        # Extract the natural language description
        # re.DOTALL ensures that the regex matches across multiple lines
        nat_match = re.search(r'\[NatDes\](.*?)\[/NatDes\]', text, re.DOTALL | re.IGNORECASE)
        nat_des = nat_match.group(1).strip() if nat_match else ""

        # Extract the tag list
        tag_match = re.search(r'\[TagDes\](.*?)\[/TagDes\]', text, re.DOTALL | re.IGNORECASE)
        tag_des = tag_match.group(1).strip() if tag_match else ""

        return (nat_des, tag_des)


# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "Emaysee_TagParser": Emaysee_TagParser
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Emaysee_TagParser": "Emaysee Tag Parser"
}