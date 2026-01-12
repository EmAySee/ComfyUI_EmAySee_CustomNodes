import torch

class EmAySee_GetModelPath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_path",)
    CATEGORY = "EmAySee/Utils"
    FUNCTION = "EmAySee_get_path"

    def EmAySee_get_path(self, model):
        # A model object in ComfyUI typically has the file path in a specific attribute
        # We assume the first path is the one you need.
        model_path = model.model_filenames[0]
        
        return (model_path,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_GetModelPath": EmAySee_GetModelPath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_GetModelPath": "EmAySee Get Model Path"
}
