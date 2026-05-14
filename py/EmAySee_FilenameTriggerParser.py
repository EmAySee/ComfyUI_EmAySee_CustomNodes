import os

class EmAySee_FilenameTriggerParser:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "filename": ("STRING", {"forceInput": True}),
                "separator": ("STRING", {"default": "_"}),
                "target_index": ("INT", {"default": 1, "min": 0, "max": 10}),
                "map_1_code": ("STRING", {"default": "01"}),
                "map_1_value": ("STRING", {"default": "teen"}),
                "map_2_code": ("STRING", {"default": "02"}),
                "map_2_value": ("STRING", {"default": "young adult"}),
                "map_3_code": ("STRING", {"default": "03"}),
                "map_3_value": ("STRING", {"default": "woman"}),
                "map_4_code": ("STRING", {"default": ""}),
                "map_4_value": ("STRING", {"default": ""}),
                "map_5_code": ("STRING", {"default": ""}),
                "map_5_value": ("STRING", {"default": ""}),
                "fallback_value": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("trigger",)
    FUNCTION = "parse"
    CATEGORY = "EmAySee/Text"

    def parse(self, filename, separator, target_index, map_1_code, map_1_value, map_2_code, map_2_value, map_3_code, map_3_value, map_4_code, map_4_value, map_5_code, map_5_value, fallback_value):
        base_name = os.path.splitext(os.path.basename(filename))[0]
        parts = base_name.split(separator)
        
        target_code = ""
        if len(parts) > target_index:
            target_code = parts[target_index]
            
        mappings = {
            map_1_code: map_1_value,
            map_2_code: map_2_value,
            map_3_code: map_3_value,
            map_4_code: map_4_value,
            map_5_code: map_5_value,
        }
        
        if target_code in mappings and mappings[target_code] != "":
            return (mappings[target_code],)
            
        return (fallback_value,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_FilenameTriggerParser": EmAySee_FilenameTriggerParser
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_FilenameTriggerParser": "EmAySee Filename Trigger Parser"
}