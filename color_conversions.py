#? maybe combine the two functions since I use them only together 
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

# what a complicated function rofl
def rgb_to_bgr(rgb):
    return tuple(reversed(rgb))