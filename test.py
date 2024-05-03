import cairo

# --- Color Definitions ---
BACKGROUND_COLOR = (1, 1, 1)  # White
FRETS_COLOR = (0, 0, 0)       # Black
STRINGS_COLOR = (0, 0, 0)     # Black
NUT_COLOR = (0, 0, 0)         # Black
INLAY_COLOR = (0.7, 0.7, 0.7)       # Red
FRETBOARD_COLOR = (1, 1, 1)   # White

C_TEXT_COLOR = (1, 1, 1)      # White
ORANGE_COLOR = (1, 0.5, 0.2)    # Vibrant Orange
BLUE_COLOR = (0, 0, 1)          # Vivid Blue
GREEN_COLOR = (0, 0.502, 0)     # Rich Green

# --- Custom Drawing Settings ---
C_RADIUS = 21                 # Radius for the custom circles
C_STROKE_WIDTH = 16           # Stroke width for the custom circles

# --- Settings ---
NUM_FRETS = 24
NUM_STRINGS = 6
FRET_WIDTH = 96
NECK_WIDTH = 425
FONT_SIZE = 18
NUT_WIDTH = 28
PADDING = 100
FRET = 3
INLAY_RADIUS = 10
FONT = "Arial Rounded MT Bold"
half_padding = PADDING / 2

# --- Calculations ---
FRETBOARD_WIDTH = (FRET_WIDTH * NUM_FRETS) + NUT_WIDTH + (FRET * (NUM_FRETS - 1))  
FRETBOARD_HEIGHT = NECK_WIDTH
TOTAL_WIDTH = FRETBOARD_WIDTH + PADDING
TOTAL_HEIGHT = FRETBOARD_HEIGHT + PADDING + FONT_SIZE

# --- Cairo Setup ---
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, TOTAL_WIDTH, TOTAL_HEIGHT)
ctx = cairo.Context(surface)

# --- Draw Background ---
ctx.set_source_rgb(*BACKGROUND_COLOR)
ctx.rectangle(0, 0, TOTAL_WIDTH, TOTAL_HEIGHT)
ctx.fill()

# --- Draw Fretboard ---
ctx.set_source_rgb(*FRETBOARD_COLOR)
ctx.rectangle(half_padding, half_padding, FRETBOARD_WIDTH, FRETBOARD_HEIGHT)
ctx.fill()

# --- Draw Strings ---
string_spacing = FRETBOARD_HEIGHT / (NUM_STRINGS - 1)
for i in range(NUM_STRINGS):
    y = half_padding + string_spacing * i
    ctx.set_source_rgb(*STRINGS_COLOR)
    ctx.move_to(half_padding, y)
    ctx.line_to(half_padding + FRETBOARD_WIDTH, y)
    ctx.set_line_width(1.5)  
    ctx.stroke()

# --- Draw Nut and Frets ---
ctx.set_source_rgb(*NUT_COLOR)
ctx.rectangle(half_padding, half_padding, NUT_WIDTH, FRETBOARD_HEIGHT)  # Nut
ctx.fill()

ctx.set_source_rgb(*FRETS_COLOR)
ctx.set_line_width(FRET)
for i in range(1, NUM_FRETS + 1):
    x = half_padding + NUT_WIDTH + (FRET_WIDTH * i) + FRET * (i - 1)
    ctx.move_to(x, half_padding)
    ctx.line_to(x, half_padding + FRETBOARD_HEIGHT)
    ctx.stroke()

inlay_positions = [(3, 3), (5, 3), (7, 3), (9, 3), (12, 2), (12, 4), (15, 3), (17, 3), (19, 3), (21, 3), (24, 2), (24, 4)]

for fret, string in inlay_positions:
    fret = fret - 1
    x = half_padding + NUT_WIDTH + (FRET_WIDTH * fret) + FRET * (fret - 1) + FRET_WIDTH // 2
    y = half_padding + string_spacing * (string - 1) + string_spacing // 2
    ctx.set_source_rgb(*INLAY_COLOR)
    ctx.arc(x, y, INLAY_RADIUS, 0, 2 * 3.14159)
    ctx.fill()

# --- Draw Fret Labels ---
ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(FONT_SIZE)
ctx.set_source_rgb(*FRETS_COLOR)
for i in range(0, NUM_FRETS):
    x = half_padding + NUT_WIDTH + (FRET_WIDTH * i) + FRET * (i - 1) + FRET_WIDTH // 2 - FRET
    y = half_padding + FRETBOARD_HEIGHT + FONT_SIZE + 30
    ctx.move_to(x, y)
    ctx.show_text(str(i+1))

# Function to draw circles with labels for notes
def draw_fret_circle2(ctx, color, radius, fret, string, label_text, label_color, stroke_color, stroke_width):
    fret = fret - 1
    fret_x = half_padding + NUT_WIDTH + (FRET_WIDTH * fret) + FRET * (fret - 1) + FRET_WIDTH // 2
    string_y = half_padding + string_spacing * (string - 1)

    # Draw "stroke" circle (larger and with stroke_color)
    ctx.arc(fret_x, string_y, radius + stroke_width / 2, 0, 2 * 3.14159) 
    ctx.set_source_rgb(*stroke_color)
    ctx.fill()

    # Draw main circle
    ctx.arc(fret_x, string_y, radius, 0, 2 * 3.14159) 
    ctx.set_source_rgb(*color)
    ctx.fill()

    # Draw label
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD) 
    ctx.set_font_size(radius)  
    ctx.set_source_rgb(*label_color) 

    text_extents = ctx.text_extents(label_text)
    ctx.move_to(fret_x - text_extents.width / 2, string_y + text_extents.height / 2)
    ctx.show_text(label_text)

# Data and function call to draw circles based on predefined data
c_data = [(5, 6, "6"), (8, 6, "R"), (5, 5, "2"), (7, 5, "3"), (5, 4, "5"), (7, 4, "6"), (5, 3, "R"), (7, 3, "2"), (5, 2, "3"), (8, 2, "5"), (5, 1, "6"), (8, 1, "R")]

def draw_circles_from_data(ctx, data):
    for fret, string, label_text in data:
        draw_fret_circle2(ctx, ORANGE_COLOR, C_RADIUS, fret, string, label_text, C_TEXT_COLOR, BLUE_COLOR, C_STROKE_WIDTH)

draw_circles_from_data(ctx, c_data)

# --- Save Image ---
surface.write_to_png("fret.png")
