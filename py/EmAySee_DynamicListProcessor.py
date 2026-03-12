import random
import re

class EmAySee_DynamicListProcessor:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "{a|b|c{s1|s2}|d}"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "process"
    CATEGORY = "EmAySee/Text"

    def process(self, text, seed):
        rng = random.Random(seed)
        
        def parse_text(input_str):
            result = []
            i = 0
            while i < len(input_str):
                if input_str[i] == '{':
                    start = i
                    depth = 1
                    i += 1
                    while i < len(input_str) and depth > 0:
                        if input_str[i] == '{':
                            depth += 1
                        elif input_str[i] == '}':
                            depth -= 1
                        i += 1
                    
                    if depth == 0:
                        group_content = input_str[start + 1:i - 1]
                        options = []
                        current_option = []
                        inner_depth = 0
                        
                        for char in group_content:
                            if char == '|' and inner_depth == 0:
                                options.append("".join(current_option))
                                current_option = []
                            else:
                                if char == '{':
                                    inner_depth += 1
                                elif char == '}':
                                    inner_depth -= 1
                                current_option.append(char)
                        options.append("".join(current_option))
                        
                        choice = rng.choice(options)
                        result.append(parse_text(choice))
                    else:
                        result.append(input_str[start])
                        i = start + 1
                else:
                    result.append(input_str[i])
                    i += 1
            return "".join(result)

        return (parse_text(text),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_DynamicListProcessor": EmAySee_DynamicListProcessor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_DynamicListProcessor": "EmAySee Dynamic List Processor"
}