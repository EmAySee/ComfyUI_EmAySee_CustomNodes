class EmAySee_BodyAttributes_TextOut:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        labels = [
            "01 Breast Size", "02 Breast Sag", "03 Areola Size", "04 Puffies",
            "05 Belly Fat", "06 Waist Size", "07 Butt Size", "08 Thigh Size",
            "09 Thigh Gap", "10 Body Type", "11 Pregnant", "12 Pubic Hair Peek",
            "Option 01", "Option 02", "Option 03", "Option 04", "Option 05"
        ]
        inputs = {"required": {}}
        for label in labels:
            inputs["required"][label] = ("STRING", {"default": "", "multiline": True})
        return inputs

    RETURN_TYPES = ("STRING",) * 17
    RETURN_NAMES = (
        "01 Breast Size", "02 Breast Sag", "03 Areola Size", "04 Puffies",
        "05 Belly Fat", "06 Waist Size", "07 Butt Size", "08 Thigh Size",
        "09 Thigh Gap", "10 Body Type", "11 Pregnant", "12 Pubic Hair Peek",
        "Option 01", "Option 02", "Option 03", "Option 04", "Option 05"
    )
    FUNCTION = "get_text"
    CATEGORY = "EmAySee/Text"

    def get_text(self, **kwargs):
        labels = [
            "01 Breast Size", "02 Breast Sag", "03 Areola Size", "04 Puffies",
            "05 Belly Fat", "06 Waist Size", "07 Butt Size", "08 Thigh Size",
            "09 Thigh Gap", "10 Body Type", "11 Pregnant", "12 Pubic Hair Peek",
            "Option 01", "Option 02", "Option 03", "Option 04", "Option 05"
        ]
        results = [kwargs.get(label, "") for label in labels]
        return tuple(results)

NODE_CLASS_MAPPINGS = {
    "EmAySee_BodyAttributes_TextOut": EmAySee_BodyAttributes_TextOut
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_BodyAttributes_TextOut": "EmAySee Body Attributes Text Out"
}