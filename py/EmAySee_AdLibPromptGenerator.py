import random

class EmAySee_AdLibPromptGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "subject": ("STRING", {"multiline": True, "default": "a young woman named emac_megan"}),
                "attire": ("STRING", {"multiline": True, "default": "a matte-white, heavy arctic parka over a reflective silver thermal under-layer"}),
                "action": ("STRING", {"multiline": True, "default": "leaning her entire body weight forward, pulling a thick climbing rope"}),
                "expression": ("STRING", {"multiline": True, "default": "strained, exhausted grimace with narrowed eyes"}),
                "environment": ("STRING", {"multiline": True, "default": "a barren, jagged ice field during a blizzard"}),
                "lighting": ("STRING", {"multiline": True, "default": "a single, intense blue-white flare burning on the ground"}),
                "camera_and_tags": ("STRING", {"multiline": True, "default": "professional quality, cinematic depth of field, sharp focus, 8k"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("prompt", "layout_used",)
    FUNCTION = "generate_prompt"
    CATEGORY = "EmAySee"

    def generate_prompt(self, seed, subject, attire, action, expression, environment, lighting, camera_and_tags):
        random.seed(seed)
        
        templates = {
            "STANDARD NARRATIVE": "A {camera_and_tags} photograph of {subject}. She is wearing {attire} and is {action}. Her face shows a {expression}. She is located in {environment}. The lighting is dominated by {lighting}.",
            "EXTREME CLOSE-UP": "An extreme close-up of {subject} showing a {expression}. She is dressed in {attire} and is currently {action}. The surrounding {environment} is illuminated by {lighting}. {camera_and_tags}.",
            "ENVIRONMENTAL ESTABLISHING": "{camera_and_tags} wide establishing shot of {environment}. In the frame, {subject} is {action}. She is wearing {attire}. {lighting} heavily shadows her {expression}.",
            "MOODY CONTRAST": "A moody, high-contrast scene featuring {subject} wearing {attire}. She is {action} deep within {environment}. {lighting} catches the edge of her {expression}. {camera_and_tags}.",
            "HIGH FASHION EDITORIAL": "High fashion editorial format. {subject} modeling {attire}. She is {action}, exhibiting a {expression}. Shot in {environment} utilizing {lighting}. {camera_and_tags}."
        }
        
        layout_name = random.choice(list(templates.keys()))
        chosen_layout = templates[layout_name]
        
        formatted_text = chosen_layout.format(
            subject=subject.strip(),
            attire=attire.strip(),
            action=action.strip(),
            expression=expression.strip(),
            environment=environment.strip(),
            lighting=lighting.strip(),
            camera_and_tags=camera_and_tags.strip()
        )
        
        final_prompt = f"--- {layout_name} ---\n{formatted_text}"
        
        return (final_prompt, layout_name)

NODE_CLASS_MAPPINGS = {
    "EmAySee_AdLibPromptGenerator": EmAySee_AdLibPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_AdLibPromptGenerator": "EmAySee AdLib Prompt Generator"
}