class EmAySee_SegsUnion:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {},
            "optional": {
                "fallback_segs": ("SEGS",),
            }
        }
        for i in range(1, 11):
            inputs["optional"][f"segs_{i}"] = ("SEGS",)
        return inputs

    RETURN_TYPES = ("SEGS",)
    RETURN_NAMES = ("segs",)
    FUNCTION = "combine"
    CATEGORY = "EmAySee/Segs"

    def combine(self, fallback_segs=None, **kwargs):
        combined_items = []
        base_shape = None

        for i in range(1, 11):
            seg_input = kwargs.get(f"segs_{i}")
            if seg_input is not None:
                if base_shape is None:
                    base_shape = seg_input[0]
                combined_items.extend(seg_input[1])

        if not combined_items:
            if fallback_segs is not None:
                return (fallback_segs,)
            return ((base_shape if base_shape else (64, 64), []),)

        return ((base_shape, combined_items),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_SegsUnion": EmAySee_SegsUnion
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SegsUnion": "EmAySee Segs Union"
}