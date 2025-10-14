import re
import torch

class EmAySee_WD14TagFilter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "wd14_tags_input": ("STRING", {"multiline": True, "default": ""}),
                "tags_to_remove": ("STRING", {"multiline": True, "default": "best quality, masterpiece, highres, absurdres"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filtered_tags_output",)
    CATEGORY = "EmAySee/Text"
    FUNCTION = "EmAySee_filter_tags"

    def EmAySee_filter_tags(self, wd14_tags_input, tags_to_remove):
        # 1. Normalize the input WD14 tags string (replace newlines with commas, split)
        # This assumes the WD14 output is a string of tags separated by commas, spaces, or newlines.
        input_tags = re.split(r'[,\s\n]+', wd14_tags_input.lower().strip())
        input_tags = [tag.strip() for tag in input_tags if tag.strip()]

        # 2. Normalize the tags to remove string
        # Split the string in the text box by commas or newlines
        remove_list_raw = re.split(r'[,\n]+', tags_to_remove.lower().strip())
        tags_to_remove_set = {tag.strip() for tag in remove_list_raw if tag.strip()}

        # 3. Perform the filtering
        filtered_tags = []
        for tag in input_tags:
            # Only keep the tag if it is NOT in the set of tags to remove
            if tag not in tags_to_remove_set:
                filtered_tags.append(tag)

        # 4. Join the remaining tags back into a single string
        filtered_tags_output = ", ".join(filtered_tags)

        return (filtered_tags_output,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_WD14TagFilter": EmAySee_WD14TagFilter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_WD14TagFilter": "EmAySee WD14 Tag Filter"
}
