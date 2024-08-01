print("Kandinsky not implemented please use the Numworks simulator")

def get_pixel(x: int, y: int, /) -> tuple[int, int, int]:
    """Returne the color of the pixel at the given coordinates. 
    Return (R, G, B) from 0 to 255."""

def set_pixel(x: int, y: int, color: tuple[int, int, int], /):
    """Set the color of the pixel at the given coordinates."""

def color(r: int, g: int, b: int, /) -> tuple[int, int, int]:
    """Convert the given color to the nearest compatible color.
    Return (R, G, B) from 0 to 255."""

def draw_string(text: str, x: int, y: int, text_color: tuple[int, int, int] = (0, 0, 0), background_color: tuple[int, int, int] = (255, 255, 255), /):
    """Draw the text at the given coordinates with the given colors."""

def fill_rect(x: int, y: int, w: int, h: int, color: tuple[int, int, int], /):
    """Fill the rect with the given color."""