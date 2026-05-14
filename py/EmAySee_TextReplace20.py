class EmAySee_TextReplace20:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }
        for i in range(1, 21):
            inputs["required"][f"find_{i}"] = ("STRING", {"default": ""})
            inputs["required"][f"replace_{i}"] = ("STRING", {"default": ""})
        return inputs

    RETURN_TYPES = ("STRING",)
    FUNCTION = "replace"
    CATEGORY = "EmAySee/Text"

    def replace(self, text, **kwargs):
        for i in range(1, 21):
            find_text = kwargs.get(f"find_{i}", "")
            replace_with = kwargs.get(f"replace_{i}", "")
            if find_text:
                text = text.replace(find_text, replace_with)
        return (text,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_TextReplace20": EmAySee_TextReplace20
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TextReplace20": "EmAySee Text Replace 20"
}