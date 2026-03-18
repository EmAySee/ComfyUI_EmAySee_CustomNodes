import torch
import gc
import comfy.model_management
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="torch.distributed")
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.modules.module")

class EmAySee_SelectiveModelUnloader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_name_filter": ("STRING", {"default": "ModelConfig"}),
                "deep_gc_scan": ("BOOLEAN", {"default": False}),
                "exclude_checkpoints": ("BOOLEAN", {"default": True}),
                "unload_mode": (["move_to_cpu", "delete_references"], {"default": "move_to_cpu"}),
                "purge_cache": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "STRING")
    RETURN_NAMES = ("image", "unloaded_count", "debug_info")
    FUNCTION = "unload_specific"
    CATEGORY = "EmAySee/Utils"

    def unload_specific(self, image, model_name_filter, deep_gc_scan, exclude_checkpoints, unload_mode, purge_cache):
        unloaded_count = 0
        debug_logs = []
        
        filters = [f.strip().lower() for f in model_name_filter.split(",")]
        
        CHECKPOINT_TYPES = [
            "SD15", "SD21", "SDXL", "SDXLRefiner", "SVD_img2vid", 
            "Flux", "SD3", "Stable_Cascade", "SD_ASR", "PlaygroundV2", "Hyvid", "Wan", "HunyuanVideo"
        ]
        
        remaining_models = []
        loaded_models = comfy.model_management.current_loaded_models[:]
        
        for m in loaded_models:
            model_obj = m.model
            inner_model = getattr(model_obj, "model", None)
            
            meta_name = "Unknown"
            is_checkpoint = False
            
            if hasattr(model_obj, "model_config"):
                meta_name = model_obj.model_config.__class__.__name__
                if any(cp_type in meta_name for cp_type in CHECKPOINT_TYPES):
                    is_checkpoint = True
            elif inner_model:
                meta_name = inner_model.__class__.__name__
            else:
                meta_name = model_obj.__class__.__name__

            should_unload = (model_name_filter == "*" or 
                             any(f in meta_name.lower() for f in filters))
                
            if should_unload:
                if exclude_checkpoints and is_checkpoint:
                    debug_logs.append(f"Skipping Protected Checkpoint: {meta_name}")
                    remaining_models.append(m)
                else:
                    debug_logs.append(f"Standard Unload: {meta_name}")
                    m.model_unload()
                    unloaded_count += 1
            else:
                remaining_models.append(m)
        
        comfy.model_management.current_loaded_models = remaining_models

        if deep_gc_scan:
            for obj in list(gc.get_objects()):
                try:
                    if isinstance(obj, torch.nn.Module):
                        class_name = obj.__class__.__name__
                        is_gpu = False
                        try:
                            test_tensor = next(obj.parameters(), next(obj.buffers(), None))
                            if test_tensor is not None and "cuda" in str(test_tensor.device):
                                is_gpu = True
                        except (StopIteration, ReferenceError):
                            pass
                        
                        if is_gpu:
                            is_cp_hidden = any(cp_type in class_name for cp_type in CHECKPOINT_TYPES)
                            if model_name_filter == "*" or any(f in class_name.lower() for f in filters):
                                if exclude_checkpoints and is_cp_hidden:
                                    continue
                                obj.to("cpu")
                                unloaded_count += 1
                except:
                    continue

        if purge_cache:
            gc.collect()
            comfy.model_management.soft_empty_cache()
            
            # Replicating the "Free model and node cache" button backend logic:
            if not exclude_checkpoints:
                comfy.model_management.unload_all_models()
                if hasattr(comfy.model_management, "loaded_models"):
                    comfy.model_management.loaded_models.clear()
            
            # Clear the execution cache (Node Cache)
            if hasattr(comfy.model_management, "node_cache"):
                comfy.model_management.node_cache.clear()
            
            # Brute force memory cleanup
            try:
                comfy.model_management.cleanup_models(keep_free_mem=0)
            except:
                pass

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
        elif unloaded_count > 0:
            gc.collect()
            comfy.model_management.soft_empty_cache()
        
        final_debug = "\n".join(debug_logs) if debug_logs else "No matches found."
        return (image, unloaded_count, final_debug)

class EmAySee_SelectiveModelReloader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_name_filter": ("STRING", {"default": "SamImage"}),
                "force_bfloat16": ("BOOLEAN", {"default": False}),
                "purge_cache": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "STRING")
    RETURN_NAMES = ("image", "reloaded_count", "debug_info")
    FUNCTION = "reload_specific"
    CATEGORY = "EmAySee/Utils"

    def reload_specific(self, image, model_name_filter, force_bfloat16, purge_cache):
        reloaded_count = 0
        debug_logs = []
        device = comfy.model_management.get_torch_device()
        filters = [f.strip().lower() for f in model_name_filter.split(",")]
        
        for obj in list(gc.get_objects()):
            try:
                if isinstance(obj, torch.nn.Module):
                    class_name = obj.__class__.__name__
                    if any(f in class_name.lower() for f in filters):
                        is_cpu = False
                        try:
                            test_tensor = next(obj.parameters(), next(obj.buffers(), None))
                            if test_tensor is not None and "cpu" in str(test_tensor.device):
                                is_cpu = True
                        except (StopIteration, ReferenceError):
                            pass
                        
                        if is_cpu:
                            debug_logs.append(f"Moving back to GPU: {class_name}")
                            if force_bfloat16:
                                obj.to(device=device, dtype=torch.bfloat16)
                            else:
                                obj.to(device)
                            reloaded_count += 1
            except:
                continue
                
        if purge_cache:
            gc.collect()
            comfy.model_management.soft_empty_cache()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
        elif reloaded_count > 0:
            comfy.model_management.soft_empty_cache()
                
        final_debug = "\n".join(debug_logs) if debug_logs else "No models needed reloading."
        return (image, reloaded_count, final_debug)

NODE_CLASS_MAPPINGS = {
    "EmAySee_SelectiveModelUnloader": EmAySee_SelectiveModelUnloader,
    "EmAySee_SelectiveModelReloader": EmAySee_SelectiveModelReloader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SelectiveModelUnloader": "EmAySee Selective Model Unloader",
    "EmAySee_SelectiveModelReloader": "EmAySee Selective Model Reloader"
}