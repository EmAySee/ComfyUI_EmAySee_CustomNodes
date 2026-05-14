import torch
import numpy as np

class EmAySee_SegsUnion:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {},
            "optional": {
                "fallback_segs": ("SEGS",),
            }
        }
        for i in range(1, 11):
            inputs["optional"][f"segs_{i}"] = ("SEGS",)
        return inputs

    RETURN_TYPES = ("SEGS",)
    RETURN_NAMES = ("segs",)
    FUNCTION = "combine"
    CATEGORY = "EmAySee/Segs"

    def combine(self, fallback_segs=None, **kwargs):
        combined_items = []
        base_shape = None

        for i in range(1, 11):
            seg_input = kwargs.get(f"segs_{i}")
            if seg_input is not None and isinstance(seg_input, tuple) and len(seg_input) >= 2:
                if base_shape is None:
                    base_shape = seg_input[0]
                
                items = seg_input[1]
                if isinstance(items, list):
                    # Filter out any accidental strings that might have leaked in from other nodes
                    valid_items = [item for item in items if not isinstance(item, str)]
                    combined_items.extend(valid_items)

        if not combined_items:
            if fallback_segs is not None:
                return (fallback_segs,)
            return ((base_shape if base_shape else (64, 64), []),)

        return ((base_shape, combined_items),)

class EmAySee_MultiBBoxDetector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "image": ("IMAGE",),
                "threshold": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01}),
                "dilation": ("INT", {"default": 10, "min": -512, "max": 512, "step": 1}),
                "crop_factor": ("FLOAT", {"default": 3.0, "min": 1.0, "max": 10.0, "step": 0.1}),
                "drop_size": ("INT", {"default": 10, "min": 1, "max": 1024, "step": 1}),
                "labels": ("STRING", {"multiline": True, "default": "all"}),
            },
            "optional": {}
        }
        for i in range(1, 11):
            inputs["optional"][f"bbox_detector_{i}"] = ("BBOX_DETECTOR",)
        return inputs

    RETURN_TYPES = ("SEGS",)
    RETURN_NAMES = ("segs",)
    FUNCTION = "detect"
    CATEGORY = "EmAySee/Segs"

    def detect(self, image, threshold, dilation, crop_factor, drop_size, labels, **kwargs):
        combined_items = []
        _, h, w, _ = image.shape
        base_shape = (h, w)
        
        for i in range(1, 11):
            detector = kwargs.get(f"bbox_detector_{i}")
            if detector is not None:
                try:
                    # Impact Pack detectors expect a detect method
                    if hasattr(detector, "detect"):
                        res = detector.detect(image, threshold, dilation, crop_factor, drop_size, labels)
                        if res is not None and isinstance(res, tuple) and len(res) >= 2:
                            items = res[1]
                            if isinstance(items, list):
                                # Ensure we only grab valid objects, not strings/labels
                                valid_items = [item for item in items if not isinstance(item, str)]
                                combined_items.extend(valid_items)
                except Exception as e:
                    print(f"[EmAySee] Detector {i} failed: {e}")
                    continue
            
        return ((base_shape, combined_items),)

class EmAySee_BBoxToSegs:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {}
        }
        for i in range(1, 11):
            inputs["optional"][f"bbox_{i}"] = ("BBOX",)
        return inputs

    RETURN_TYPES = ("SEGS",)
    RETURN_NAMES = ("segs",)
    FUNCTION = "create"
    CATEGORY = "EmAySee/Segs"

    def create(self, image, **kwargs):
        _, h, w, _ = image.shape
        items = []
        
        # We define a minimal class that mimics an Impact Pack SEGEL/SEG object
        # to avoid the 'str' object has no attribute 'post_crop_region' error.
        class SimpleSegItem:
            def __init__(self, cropped_image, cropped_mask, bbox, shape, label, confidence):
                self.cropped_image = cropped_image
                self.cropped_mask = cropped_mask
                self.bbox = bbox
                self.shape = shape
                self.label = label
                self.confidence = confidence
                self.crop_region = bbox
                # These are required by newer Detailers
                self.post_crop_region = None
                self.post_crop_mask = None

            def __getitem__(self, item):
                # Backwards compatibility for nodes that treat this as a tuple
                mapping = [self.cropped_image, self.cropped_mask, self.bbox, self.shape, self.label, self.confidence]
                return mapping[item]

        for i in range(1, 11):
            bbox = kwargs.get(f"bbox_{i}")
            if bbox is not None:
                try:
                    # BBOX is usually [x1, y1, x2, y2]
                    x1, y1, x2, y2 = map(int, bbox)
                    
                    x1 = max(0, min(x1, w))
                    y1 = max(0, min(y1, h))
                    x2 = max(0, min(x2, w))
                    y2 = max(0, min(y2, h))
                    
                    bw, bh = x2 - x1, y2 - y1
                    
                    if bw > 0 and bh > 0:
                        crop_img = image[:, y1:y2, x1:x2, :]
                        crop_mask = torch.ones((1, bh, bw), dtype=torch.float32, device="cpu")
                        
                        # Create the object instead of a raw tuple
                        item = SimpleSegItem(crop_img, crop_mask, [x1, y1, x2, y2], (h, w), f"box_{i}", 1.0)
                        items.append(item)
                except Exception as e:
                    print(f"[EmAySee] BBox conversion failed: {e}")
                    continue
        
        return (((h, w), items),)

NODE_CLASS_MAPPINGS = {
    "EmAySee_SegsUnion": EmAySee_SegsUnion,
    "EmAySee_MultiBBoxDetector": EmAySee_MultiBBoxDetector,
    "EmAySee_BBoxToSegs": EmAySee_BBoxToSegs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmAySee_SegsUnion": "EmAySee Segs Union",
    "EmAySee_MultiBBoxDetector": "EmAySee Multi BBox Detector",
    "EmAySee_BBoxToSegs": "EmAySee BBox to Segs"
}