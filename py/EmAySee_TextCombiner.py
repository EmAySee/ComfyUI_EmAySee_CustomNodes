class EmAySee_TextCombiner:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {},
            "optional": {}
        }
        for i in range(1, 51):
            inputs["optional"][f"text_{i}"] = ("STRING", {"forceInput": True})
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "combine"
    CATEGORY = "EmAySee/Text"

    def combine(self, **kwargs):
        text_list = []
        for i in range(1, 51):
            key = f"text_{i}"
            if key in kwargs and kwargs[key] is not None and kwargs[key] != "":
                text_list.append(str(kwargs[key]))
        
        return ("\n".join(text_list),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_TextCombiner": EmAySee_TextCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TextCombiner": "EmAySee Text Combiner"
}