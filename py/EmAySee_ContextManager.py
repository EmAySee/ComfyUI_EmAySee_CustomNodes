import os
import re

class EmAySee_ContextManager:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "prompt.txt"}),
                "history_count": ("INT", {"default": 2, "min": 1, "max": 10, "step": 1}),
                "mode": (["Read_Context", "Append_and_Prune"],),
                "force_reset": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "new_generation": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "manage_context"
    CATEGORY = "EmAySee/Automation"

    def manage_context(self, file_path, history_count, mode, force_reset, new_generation=""):
        #  Force absolute path to avoid "Ghost" file issues in ComfyUI temp folders
        abs_path = os.path.abspath(file_path)
        
        if force_reset and os.path.exists(abs_path):
            os.remove(abs_path)

        #  Helper to read blocks
        def get_blocks(path):
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                return []
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
            found = re.findall(r"(PROMPT:.*?STATE:.*?)(?=PROMPT:|\Z)", data, re.DOTALL)
            return [b.strip() for b in found if b.strip()]

        blocks = get_blocks(abs_path)

        if mode == "Read_Context":
            #  SEEDING: If file is empty, use the input wire as the current state
            if not blocks:
                if new_generation and new_generation.strip():
                    seed = new_generation.strip()
                    #  Write immediately so the Append node sees it later in the same cycle
                    with open(abs_path, 'w', encoding='utf-8') as f:
                        f.write(seed + "\n\n")
                        f.flush()
                        os.fsync(f.fileno())
                    return (seed,)
                return ("",)
            
            recent_blocks = blocks[-history_count:]
            return ("\n\n".join(recent_blocks),)

        if mode == "Append_and_Prune":
            if new_generation and new_generation.strip():
                #  Avoid doubling up if Read_Context already seeded it
                if not blocks or blocks[-1] != new_generation.strip():
                    blocks.append(new_generation.strip())
            
            pruned = blocks[-history_count:]
            
            #  ATOMIC WRITE
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write("\n\n".join(pruned))
                f.flush()
                os.fsync(f.fileno()) #  Forces Windows/Linux to write to disk NOW
                
            return (new_generation if new_generation else "",)

NODE_CLASS_MAPPINGS = {"EmAySee_ContextManager": EmAySee_ContextManager}
NODE_DISPLAY_NAME_MAPPINGS = {"EmAySee_ContextManager": "EmAySee Context Manager"}