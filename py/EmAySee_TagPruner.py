import re

class EmAySee_TagPruner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_tags": ("STRING", {"multiline": True, "default": "tag1, tag2, bad_tag, tag3, 1girl"}),
                "tags_to_remove": ("STRING", {"multiline": True, "default": "bad_tag, 1girl, solo"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("cleaned_tags",)
    FUNCTION = "prune"
    CATEGORY = "EmAySee"

    def prune(self, input_tags, tags_to_remove):
        remove_tags_list = re.split(r'[,\n]+', tags_to_remove)
        remove_set = set(tag.strip().lower() for tag in remove_tags_list if tag.strip())

        input_tags_list = re.split(r'[,\n]+', input_tags)
        
        cleaned_list = []
        for tag in input_tags_list:
            stripped_tag = tag.strip()
            if stripped_tag and stripped_tag.lower() not in remove_set:
                cleaned_list.append(stripped_tag)

        final_string = ", ".join(cleaned_list)
        
        return (final_string,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_TagPruner": EmAySee_TagPruner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TagPruner": "EmAySee Tag Pruner"
}