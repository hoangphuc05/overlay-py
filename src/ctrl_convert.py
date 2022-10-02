"""Convert Ctrl + Key to presentable string"""

import string

convert_dict = {
    "\x00": "Ctrl + @",
    "\x01": "Ctrl + A",
    "\x02": "Ctrl + B",
    "\x03": "Ctrl + C",
    "\x04": "Ctrl + D",
    "\x05": "Ctrl + E",
    "\x06": "Ctrl + F",
    "\x07": "Ctrl + G",
    "\x08": "Ctrl + H",
    "\x09": "Ctrl + I",
    "\x0a": "Ctrl + J",
    "\x0b": "Ctrl + K",
    "\x0c": "Ctrl + L",
    "\x0d": "Ctrl + M",
    "\x0e": "Ctrl + N",
    "\x0f": "Ctrl + O",
    "\x10": "Ctrl + P",
    "\x11": "Ctrl + Q",
    "\x12": "Ctrl + R",
    "\x13": "Ctrl + S",
    "\x14": "Ctrl + T",
    "\x15": "Ctrl + U",
    "\x16": "Ctrl + V",
    "\x17": "Ctrl + W",
    "\x18": "Ctrl + X",
    "\x19": "Ctrl + Y",
    "\x1a": "Ctrl + Z",
    "\x1b": "Ctrl + [",
    "\x1c": "Ctrl + \\",
    "\x1d": "Ctrl + ]",
    "\x1e": "Ctrl + ^",
    "\x1f": "Ctrl + _",
}

def convert_ctrl(raw_string: string):
    """
    Convert raw string to presentable string
    """
    if raw_string in convert_dict:
        return convert_dict[raw_string]
    return raw_string.capitalize()
