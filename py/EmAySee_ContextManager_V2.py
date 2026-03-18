import os
import re

class EmAySee_ContextManager_V2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "prompt_v2.txt"}),
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
    CATEGORY = "EmAySee_Automation"

    def manage_context(self, file_path, history_count, mode, force_reset, new_generation=""):
        #  ABSOLUTE PATH LOGGING
        abs_path = os.path.abspath(file_path)
        print(f"--- [EmAySee V2] DEBUG: Working Directory is {os.getcwd()} ---")
        print(f"--- [EmAySee V2] DEBUG: Looking for file at {abs_path} ---")
        
        if force_reset:
            if os.path.exists(abs_path):
                os.remove(abs_path)
                print(f"--- [EmAySee V2] RESET: DELETED {abs_path} ---")

        def get_blocks(path):
            if not os.path.exists(path):
                print(f"--- [EmAySee V2] DEBUG: File does NOT exist on disk. ---")
                return []
            if os.path.getsize(path) == 0:
                print(f"--- [EmAySee V2] DEBUG: File exists but is EMPTY (0 bytes). ---")
                return []
            
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
            
            #  This regex is strict. If your file doesn't have "PROMPT:" it will return nothing.
            found = re.findall(r"(PROMPT:.*?STATE:.*?)(?=PROMPT:|\Z)", data, re.DOTALL)
            print(f"--- [EmAySee V2] DEBUG: Found {len(found)} valid PROMPT/STATE blocks. ---")
            return [b.strip() for b in found if b.strip()]

        blocks = get_blocks(abs_path)

        if mode == "Read_Context":
            if not blocks:
                if new_generation and new_generation.strip():
                    seed = new_generation.strip()
                    print(f"--- [EmAySee V2] SEEDING: Writing input to {abs_path} ---")
                    with open(abs_path, 'w', encoding='utf-8') as f:
                        f.write(seed + "\n\n")
                        f.flush()
                        os.fsync(f.fileno())
                    return (seed,)
                else:
                    print(f"--- [EmAySee V2] CRITICAL: No file and no seed input! ---")
                    return ("",)
            
            recent = blocks[-history_count:]
            print(f"--- [EmAySee V2] SUCCESS: Passing {len(recent)} blocks to LLM. ---")
            return ("\n\n".join(recent),)

        if mode == "Append_and_Prune":
            if new_generation and new_generation.strip():
                if not blocks or blocks[-1] != new_generation.strip():
                    blocks.append(new_generation.strip())
            
            pruned = blocks[-history_count:]
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write("\n\n".join(pruned))
                f.flush()
                os.fsync(f.fileno())
                
            return (new_generation if new_generation else "",)

NODE_CLASS_MAPPINGS = {"EmAySee_ContextManager_V2": EmAySee_ContextManager_V2}
NODE_DISPLAY_NAME_MAPPINGS = {"EmAySee_ContextManager_V2": "EmAySee Context Manager V2"}