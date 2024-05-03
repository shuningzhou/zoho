import cairo
import webcolors

# --- Settings ---
NUM_FRETS = 24
NUM_STRINGS = 6
FRET_WIDTH = 96
NECK_WIDTH = 360
BACKGROUND_COLOR = 'white'
FRETS_COLOR = 'black'
STRINGS_COLOR = 'black'
NUT_COLOR = 'black'
INLAY_COLOR = 'red'
FONT_SIZE = 14
NUT_WIDTH = 10
PADDING = 100
FRET = 3
INLAY_RADIUS = 10

half_padding = PADDING / 2

# 1 = HIGH E

# --- Calculations ---
FRETBOARD_WIDTH = (FRET_WIDTH * NUM_FRETS) + NUT_WIDTH + (FRET * (NUM_FRETS - 1))  # Corrected calculation
FRETBOARD_HEIGHT = NECK_WIDTH
TOTAL_WIDTH = FRETBOARD_WIDTH + PADDING
TOTAL_HEIGHT = FRETBOARD_HEIGHT + PADDING + FONT_SIZE

# --- Cairo Setup ---
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, TOTAL_WIDTH, TOTAL_HEIGHT)
ctx = cairo.Context(surface)

# --- Draw Background ---
ctx.set_source_rgb(*webcolors.name_to_rgb(BACKGROUND_COLOR))
ctx.rectangle(0, 0, TOTAL_WIDTH, TOTAL_HEIGHT)
ctx.fill()

# --- Draw Fretboard ---
ctx.set_source_rgb(*webcolors.name_to_rgb('white'))
ctx.rectangle(half_padding, half_padding, FRETBOARD_WIDTH, FRETBOARD_HEIGHT)
ctx.fill()

# --- Draw Strings ---
string_spacing = FRETBOARD_HEIGHT / (NUM_STRINGS - 1)
for i in range(NUM_STRINGS):
    y = half_padding + string_spacing * i
    ctx.set_source_rgb(*webcolors.name_to_rgb(STRINGS_COLOR))
    ctx.move_to(half_padding, y)
    ctx.line_to(half_padding + FRETBOARD_WIDTH, y)
    ctx.set_line_width(1.5)  
    ctx.stroke()

# --- Draw Nut and Frets ---
ctx.set_source_rgb(*webcolors.name_to_rgb(NUT_COLOR))
ctx.rectangle(half_padding, half_padding, NUT_WIDTH, FRETBOARD_HEIGHT)  # Nut
ctx.fill()

ctx.set_source_rgb(*webcolors.name_to_rgb(FRETS_COLOR))
ctx.set_line_width(FRET)
for i in range(1, NUM_FRETS + 1):
    x = half_padding + NUT_WIDTH + (FRET_WIDTH * i) + FRET * (i - 1)
    ctx.move_to(x, half_padding)
    ctx.line_to(x, half_padding + FRETBOARD_HEIGHT)
    ctx.stroke()

# --- Draw Inlays ---

# Adjust positions as needed
inlay_positions = [(3, 3), (5, 3), (7, 3), (9, 3), (12, 2), (12, 4), (15, 3), (17, 3), (19, 3), (21, 3), (24, 2), (24, 4)]

for fret, string in inlay_positions:
    fret = fret - 1
    x = half_padding + NUT_WIDTH + (FRET_WIDTH * fret) + FRET * (fret - 1) + FRET_WIDTH // 2
    y = half_padding + string_spacing * (string - 1) + string_spacing // 2
    ctx.set_source_rgb(*webcolors.name_to_rgb(INLAY_COLOR))
    ctx.arc(x, y, INLAY_RADIUS, 0, 2 * 3.14159)
    ctx.fill()

# --- Draw Fret Labels ---
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(FONT_SIZE)
ctx.set_source_rgb(*webcolors.name_to_rgb(FRETS_COLOR))
for i in range(0, NUM_FRETS):
    x = half_padding + NUT_WIDTH + (FRET_WIDTH * i) + FRET * (i - 1) + FRET_WIDTH // 2
    y = half_padding + FRETBOARD_HEIGHT + FONT_SIZE + 30
    ctx.move_to(x, y)
    ctx.show_text(str(i+1))

def draw_fret_circle2(ctx, color, radius, fret, string, label_text, label_color, stroke_color, stroke_width):
    fret = fret - 1
    fret_x = half_padding + NUT_WIDTH + (FRET_WIDTH * fret) + FRET * (fret - 1) + FRET_WIDTH // 2
    string_spacing = NECK_WIDTH / (NUM_STRINGS - 1)
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
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD) 
    ctx.set_font_size(radius)  
    ctx.set_source_rgb(*label_color) 

    text_extents = ctx.text_extents(label_text)
    ctx.move_to(fret_x - text_extents.width / 2, string_y + text_extents.height / 2)
    ctx.show_text(label_text)

# draw_fret_circle(ctx, webcolors.name_to_rgb('blue'), 20, 1, 1)
# draw_fret_circle1(ctx, webcolors.name_to_rgb('blue'), 20, 2, 1, "C#", webcolors.name_to_rgb('white'), webcolors.name_to_rgb('red'), 2)

#-----------------------custom code

C_TEXT_COLOR = webcolors.name_to_rgb('white')
C_COLOR = webcolors.name_to_rgb('blue')
C_STROKE_COLOR = webcolors.name_to_rgb('red')
C_STROKE_WIDTH = 8
C_RADIUS = 21

c_data = [(5, 6, "6"),
          (8, 6, "R"),
          (5, 5, "2"),
          (7, 5, "3"),
          (5, 4, "5"),
          (7, 4, "6"),
          (5, 3, "R"),
          (7, 3, "2"),
          (5, 2, "3"),
          (8, 2, "5"),
          (5, 1, "6"),
          (8, 1, "R")]

def draw_circles_from_data(ctx, data):
    for fret, string, label_text in data:
        draw_fret_circle2(ctx, C_COLOR, C_RADIUS, fret, string, label_text, C_TEXT_COLOR, C_STROKE_COLOR, C_STROKE_WIDTH)

draw_circles_from_data(ctx, c_data)

# --- Save Image ---
surface.write_to_png("guitar_fretboard.png")
