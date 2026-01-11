DEVICE_DATA = {
  "manufacturer": "Panasonic",
  "supportedModels": [
    "CS-221DFL",
  ],
  "commandsEncoding": "Generic",
  "minTemperature": {
    "cool": 16,
    "heat": 16,
    "dry":  16,
  },
  "maxTemperature": {
    "cool": 30,
    "heat": 30,
    "dry":  30,
  },
  "precision": 0.5,
  "operationModes": [
    "cool",
    "heat",
    "dry",
  ],
  "fanModes": [
    "auto",
    "auto_quiet",
    "auto_powerful",
    "low",
    "low_medium",
    "medium",
    "high",
  ],
  "swingModes": [
    "auto",
    "top",
    "upper",
    "middle",
    "lower",
    "bottom",
  ],
  "toggles": [
    "self_cleaning",
  ],
  #"actions": [
  #  "start_self_cleaning",
  #]
}

def command(hvac_mode, swing_mode, fan_mode, temp, self_cleaning=True):# action=None):
    c_mode = {
        "off":  0x40, # the top nibble can be heat/cool/dry but should be ignored
        "heat": 0x41,
        "cool": 0x31,
        "dry":  0x21,
    }[hvac_mode]

    c_fan_direction = {
        "auto":          0xf,
        "top":           0x1,
        "upper":         0x2,
        "middle":        0x3,
        "lower":         0x4,
        "bottom":        0x5,
    }[swing_mode]

    c_fan_mode = {
        "auto":          0xa0,
        "auto_quiet":    0xa0,
        "auto_powerful": 0xa0,
        "low":           0x30,
        "low_medium":    0x40,
        "medium":        0x50,
        "high":          0x70,
    }[fan_mode]

    c_temp = int(temp) * 2
    c_temp_half = (int(temp*2) & 0x1) << 7

    c_flags = 0
    if self_cleaning and hvac_mode != "heat":
        c_flags |= 0x40
    if fan_mode == "auto_quiet" and hvac_mode != "heat":
        c_flags |= 0x20
    if fan_mode == "auto_powerful":
        c_flags |= 0x01

    d0 = [
        0x02, 0x20, 0xe0, 0x04, 0x00, 0x00, 0x00
    ]
    d1 = [
        0x02, 0x20, 0xe0, 0x04, 0x00,
        c_mode,
        c_temp,
        0x80,
        c_fan_mode | c_fan_direction,
        0x00, 0x00, 0x06, 0x60,
        c_flags,
        c_temp_half,
        0x80, 0x00, 0x06
    ]

    return ("nec", "tp=400,t0=451,ph=3357,pg=9858,ck=1", [d0, d1])
