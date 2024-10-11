from enum import Enum


class TriggerType(str, Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    solo_variation = "solo_variation"
    solo_low_variation = "solo_low_variation"
    solo_high_variation = "solo_high_variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"
    expand = "expand"
    zoomout = "zoomout"
