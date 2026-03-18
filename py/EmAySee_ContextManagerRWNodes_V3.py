import os
import re

def get_comfy_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def atomic_write(path, blocks):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, mode=0o777, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(blocks))

def get_blocks(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    # V5 RE-DESIGNED REGEX: Looks for PROMPT and the LAST occurrence of STATE in a chunk
    found = re.findall(r"(PROMPT:.*?STATE:.*?)(?=PROMPT:|\Z)", data, re.IGNORECASE | re.DOTALL)
    return [b.strip() for b in found if b.strip()]

class EmAySee_ContextReader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_name": ("STRING", {"default": "user/default/emaysee_prompts/prompt_v2.txt"}),
                "history_count": ("INT", {"default": 2, "min": 1, "max": 10}),
                "force_reset_file": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {"seed_text": ("STRING", {"forceInput": True})}
        }
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("history_text", "status")
    FUNCTION = "read_context"
    CATEGORY = "EmAySee_Automation/V5"

    def read_context(self, file_name, history_count, force_reset_file, seed, seed_text=""):
        abs_path = os.path.join(get_comfy_root(), file_name)
        if force_reset_file and os.path.exists(abs_path):
            os.remove(abs_path)
        blocks = get_blocks(abs_path)
        if not blocks:
            if seed_text:
                atomic_write(abs_path, [seed_text.strip()])
                return (seed_text.strip(), "SEEDED")
            return ("", "EMPTY")
        return ("\n\n".join(blocks[-history_count:]), f"READ {len(blocks[-history_count:])}")

class EmAySee_ContextWriter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_name": ("STRING", {"default": "user/default/emaysee_prompts/prompt_v2.txt"}),
                "history_count": ("INT", {"default": 2, "min": 1, "max": 10}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {"new_generation": ("STRING", {"forceInput": True})}
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "write_context"
    CATEGORY = "EmAySee_Automation/V5"
    OUTPUT_NODE = True 

    def write_context(self, file_name, history_count, seed, new_generation=""):
        if not new_generation or not new_generation.strip(): return ("",)
        
        text = new_generation.strip()
        
        # --- V5 REPAIR LOGIC ---
        # 1. Ensure PROMPT header
        if not re.search(r"^PROMPT:", text, re.IGNORECASE):
            text = "PROMPT: " + text
        
        # 2. Check for STATE header (case insensitive)
        if not re.search(r"STATE:", text, re.IGNORECASE):
            print("--- [V5 WRITER] Repairing Missing STATE ---")
            text = text + "\n\nSTATE: [Repaired Placeholder]"

        abs_path = os.path.join(get_comfy_root(), file_name)
        blocks = get_blocks(abs_path)
        
        # Deduplication check
        if not (blocks and blocks[-1][:100] == text[:100]):
            blocks.append(text)
            # Keep only the requested history depth
            atomic_write(abs_path, blocks[-history_count:])
        
        return (text,)

NODE_CLASS_MAPPINGS = {"EmAySee_ContextReader": EmAySee_ContextReader, "EmAySee_ContextWriter": EmAySee_ContextWriter}
NODE_DISPLAY_NAME_MAPPINGS = {"EmAySee_ContextReader": "EmAySee Context Reader V5", "EmAySee_ContextWriter": "EmAySee Context Writer V5"}