import random

class EmAySee_RandomStringSelector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {}
        }
        
        for i in range(1, 21):
            inputs["optional"][f"string_{i}"] = ("STRING",)
            
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_string",)
    FUNCTION = "select_random_string"
    CATEGORY = "EmAySee/Utils"

    def select_random_string(self, seed, **kwargs):
        valid_strings = []
        for i in range(1, 21):
            s = kwargs.get(f"string_{i}", None)
            if s is not None:
                valid_strings.append(s)
        
        selected_string = ""
        if valid_strings:
            random.seed(seed)
            selected_string = random.choice(valid_strings)
            
        return (selected_string,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_RandomStringSelector": EmAySee_RandomStringSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_RandomStringSelector": "EmAySee Random String Selector (20)"
}