def detectColor(color):
    if color is None: return None
    c = color[1:]
    rgb = int(c, 16)
    r = (rgb >> 16) & 0xff
    g = (rgb >> 8) & 0xff
    b = (rgb >> 0) & 0xff
    lum = 0.2126 * r + 0.7152 * g + 0.0722 *b
    if lum < 40:
        return 'white'
    else:
        return 'black'