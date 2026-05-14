import node_helpers
import math
from typing_extensions import override
from comfy_api.latest import ComfyExtension, io
import comfy.model_management
import torch
import nodes

class EmAySee_TextEncodeQwenImageEdit_noRS(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="EmAySee_TextEncodeQwenImageEdit_noRS",
            category="advanced/conditioning",
            inputs=[
                io.Clip.Input("clip"),
                io.String.Input("prompt", multiline=True, dynamic_prompts=True),
                io.Vae.Input("vae", optional=True),
                io.Image.Input("image", optional=True),
            ],
            outputs=[
                io.Conditioning.Output(),
            ],
        )

    @classmethod
    def execute(cls, clip, prompt, vae=None, image=None) -> io.NodeOutput:
        ref_latent = None
        if image is None:
            images = []
        else:
            image_rgb = image[:, :, :, :3]
            images = [image_rgb]
            if vae is not None:
                ref_latent = vae.encode(image_rgb)

        tokens = clip.tokenize(prompt, images=images)
        conditioning = clip.encode_from_tokens_scheduled(tokens)
        if ref_latent is not None:
            conditioning = node_helpers.conditioning_set_values(conditioning, {"reference_latents": [ref_latent]}, append=True)
        return io.NodeOutput(conditioning)

class EmAySee_TextEncodeQwenImageEditPlus_noRS(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="EmAySee_TextEncodeQwenImageEditPlus_noRS",
            category="advanced/conditioning",
            inputs=[
                io.Clip.Input("clip"),
                io.String.Input("prompt", multiline=True, dynamic_prompts=True),
                io.Vae.Input("vae", optional=True),
                io.Image.Input("image1", optional=True),
                io.Image.Input("image2", optional=True),
                io.Image.Input("image3", optional=True),
                io.Image.Input("image4", optional=True),
                io.Image.Input("image5", optional=True),
                io.Image.Input("image6", optional=True),
                io.Image.Input("image7", optional=True),
            ],
            outputs=[
                io.Conditioning.Output(),
            ],
        )

    @classmethod
    def execute(cls, clip, prompt, vae=None, image1=None, image2=None, image3=None, image4=None, image5=None, image6=None, image7=None) -> io.NodeOutput:
        ref_latents = []
        images_input = [image1, image2, image3, image4, image5, image6, image7]
        images_vl = []
        llama_template = "<|im_start|>system\nDescribe the key features of the input image (color, shape, size, texture, objects, background), then explain how the user's text instruction should alter or modify the image. Generate a new image that meets the user's requirements while maintaining consistency with the original input where appropriate.<|im_end|>\n<|im_start|>user\n{}<|im_end|>\n<|im_start|>assistant\n"
        image_prompt = ""

        for i, image in enumerate(images_input):
            if image is not None:
                image_rgb = image[:, :, :, :3]
                images_vl.append(image_rgb)
                if vae is not None:
                    ref_latents.append(vae.encode(image_rgb))

                image_prompt += "Picture {}: <|vision_start|><|image_pad|><|vision_end|>".format(i + 1)

        tokens = clip.tokenize(image_prompt + prompt, images=images_vl, llama_template=llama_template)
        conditioning = clip.encode_from_tokens_scheduled(tokens)
        if len(ref_latents) > 0:
            conditioning = node_helpers.conditioning_set_values(conditioning, {"reference_latents": ref_latents}, append=True)
        return io.NodeOutput(conditioning)

class EmAySee_EmptyQwenImageLayeredLatentImage_noRS(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="EmAySee_EmptyQwenImageLayeredLatentImage_noRS",
            display_name="EmAySee Empty Qwen Image Layered Latent noRS",
            category="latent/qwen",
            inputs=[
                io.Int.Input("width", default=640, min=16, max=nodes.MAX_RESOLUTION, step=16),
                io.Int.Input("height", default=640, min=16, max=nodes.MAX_RESOLUTION, step=16),
                io.Int.Input("layers", default=3, min=0, max=nodes.MAX_RESOLUTION, step=1, advanced=True),
                io.Int.Input("batch_size", default=1, min=1, max=4096),
            ],
            outputs=[
                io.Latent.Output(),
            ],
        )

    @classmethod
    def execute(cls, width, height, layers, batch_size=1) -> io.NodeOutput:
        latent = torch.zeros([batch_size, 16, layers + 1, height // 8, width // 8], device=comfy.model_management.intermediate_device())
        return io.NodeOutput({"samples": latent})

class EmAySee_QwenExtension_noRS(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            EmAySee_TextEncodeQwenImageEdit_noRS,
            EmAySee_TextEncodeQwenImageEditPlus_noRS,
            EmAySee_EmptyQwenImageLayeredLatentImage_noRS,
        ]

async def comfy_entrypoint() -> EmAySee_QwenExtension_noRS:
    return EmAySee_QwenExtension_noRS()

NODE_CLASS_MAPPINGS = {
    "EmAySee_TextEncodeQwenImageEdit_noRS": EmAySee_TextEncodeQwenImageEdit_noRS,
    "EmAySee_TextEncodeQwenImageEditPlus_noRS": EmAySee_TextEncodeQwenImageEditPlus_noRS,
    "EmAySee_EmptyQwenImageLayeredLatentImage_noRS": EmAySee_EmptyQwenImageLayeredLatentImage_noRS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_TextEncodeQwenImageEdit_noRS": "EmAySee Text Encode Qwen Image Edit noRS",
    "EmAySee_TextEncodeQwenImageEditPlus_noRS": "EmAySee Text Encode Qwen Image Edit Plus noRS",
    "EmAySee_EmptyQwenImageLayeredLatentImage_noRS": "EmAySee Empty Qwen Image Layered Latent noRS",
}