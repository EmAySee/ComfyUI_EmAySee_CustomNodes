import comfy.sd
import torch
import numpy as np
import datetime

class EmAySee_DateTimeStringNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("DATE_TIME_STRING",)
    CATEGORY = "EmAySee_Utils"

    FUNCTION = "generate_datetime_string"

    def generate_datetime_string(self, seed):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S") + str(int(now.microsecond / 100000)) #tenths of second
        return (formatted_datetime,)

NODE_CLASS_MAPPINGS = {
    "EmAySee_DateTimeStringNode": EmAySee_DateTimeStringNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_DateTimeStringNode": "EmAySee Date Time Filename String - Seeded"
}