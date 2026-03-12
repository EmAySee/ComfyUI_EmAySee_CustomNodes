import torch
import gc
import comfy.model_management

class EmAySee_CacheCleaner:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": ("*", {}),
            },
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("output",)
    FUNCTION = "clean_cache"
    CATEGORY = "EmAySee/Utils"

    def clean_cache(self, anything):
        comfy.model_management.unload_all_models()
        comfy.model_management.soft_empty_cache()
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        
        return (anything,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_CacheCleaner": EmAySee_CacheCleaner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_CacheCleaner": "EmAySee Cache Cleaner"
}