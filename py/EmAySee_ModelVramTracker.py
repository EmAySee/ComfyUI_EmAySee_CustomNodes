import comfy.model_management
import json

class EmAySee_ModelVramTracker:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": ("*", {}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("model_list", "debug_dump", "count")
    FUNCTION = "get_models"
    CATEGORY = "EmAySee/Utils"

    def get_models(self, anything):
        loaded_models_info = []
        detailed_dump = []
        loaded_models = comfy.model_management.current_loaded_models[:]

        for idx, m in enumerate(loaded_models):
            m_info = {
                "index": idx,
                "patcher_class": m.__class__.__name__,
                "attributes": {},
                "model_wrapper": "None",
                "inner_model": "None",
                "config": "None",
            }

            for attr in dir(m):
                if not attr.startswith("__"):
                    try:
                        val = getattr(m, attr)
                        if isinstance(val, (str, int, float, bool)):
                            m_info["attributes"][attr] = val
                    except:
                        pass

            model_obj = getattr(m, "model", None)
            if model_obj:
                m_info["model_wrapper"] = model_obj.__class__.__name__
                inner_model = getattr(model_obj, "model", None)
                if inner_model:
                    m_info["inner_model"] = inner_model.__class__.__name__

                if hasattr(model_obj, "model_config"):
                    m_info["config"] = model_obj.model_config.__class__.__name__
                    try:
                        conf_vars = vars(model_obj.model_config)
                        m_info["config_details"] = {str(k): str(v) for k, v in conf_vars.items() if not k.startswith("_")}
                    except:
                        m_info["config_details"] = "Error dumping vars"

                for attr in ["model_name", "name", "architecture", "type", "model_id", "sam_model", "predictor", "ckpt_name"]:
                    if hasattr(model_obj, attr):
                        val = getattr(model_obj, attr)
                        m_info[f"found_{attr}"] = str(val.__class__.__name__ if hasattr(val, "__class__") and not isinstance(val, str) else val)

            current_name = "Unknown"
            if m_info.get("found_model_name"): current_name = m_info["found_model_name"]
            elif m_info.get("found_sam_model"): current_name = f"SAM:{m_info['found_sam_model']}"
            elif m_info["config"] != "None": current_name = m_info["config"]
            elif m_info["inner_model"] != "None": current_name = m_info["inner_model"]
            else: current_name = m_info["model_wrapper"]

            loaded_models_info.append(current_name)
            detailed_dump.append(json.dumps(m_info, indent=2))

        if not loaded_models_info:
            return ("No models in VRAM", "VRAM Empty", 0)

        final_list = "\n".join(loaded_models_info)
        final_dump = "\n\n========================================\n\n".join(detailed_dump)
            
        return (final_list, final_dump, len(loaded_models_info))

NODE_CLASS_MAPPINGS = {
    "EmAySee_ModelVramTracker": EmAySee_ModelVramTracker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_ModelVramTracker": "EmAySee Model VRAM Tracker"
}