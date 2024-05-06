import cairo

# 1 = HIGH E
# 2 = B
# 3 = G
# 4 = D
# 5 = A
# 6 = LOW E

# --- notes ---
NOTES_1 = ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]
NOTES_2 = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTES_3 = ["G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"]
NOTES_4 = ["D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"]
NOTES_5 = ["A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"]
NOTES_6 = ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]

ALL_NOTES = [NOTES_6, NOTES_5, NOTES_4, NOTES_3, NOTES_2, NOTES_1]

# Scale intervals in semitones for the minor pentatonic scale
MINOR_PENTATONIC_INTERVALS = [0, 3, 5, 7, 10]

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
WHITE_COLOR = (1, 1, 1)     # white Green

# --- Custom Drawing Settings ---
C_RADIUS = 30                 # Radius for the custom circles
C_STROKE_WIDTH = 12           # Stroke width for the custom circles

# --- Settings ---
NUM_FRETS = 24
NUM_STRINGS = 6
FRET_WIDTH = 96
NECK_WIDTH = 450
FONT_SIZE = 18
NUT_WIDTH = 28
PADDING = 125
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

# --- Draw Strings and Open String Notes ---
string_spacing = FRETBOARD_HEIGHT / (NUM_STRINGS - 1)
open_string_notes = ["E", "B", "G", "D", "A", "E"]

# --- Draw Fretboard ---
ctx.set_source_rgb(*FRETBOARD_COLOR)
ctx.rectangle(half_padding, half_padding, FRETBOARD_WIDTH, FRETBOARD_HEIGHT)
ctx.fill()

# Draw open string notes
ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(FONT_SIZE)
ctx.set_source_rgb(*FRETS_COLOR)
for i, note in enumerate(open_string_notes):
    y = half_padding + string_spacing * i
    ctx.move_to(half_padding - 30, y + FONT_SIZE / 2)
    ctx.show_text(note)

# Draw strings
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
    ctx.set_font_size(radius-7)  
    ctx.set_source_rgb(*label_color) 

    text_extents = ctx.text_extents(label_text)
    ctx.move_to(fret_x - text_extents.width / 2, string_y + text_extents.height / 2)
    ctx.show_text(label_text)

def draw_circles_from_data(ctx, data):
    for string, fret, label_text, main_color, stroked, stroke_color in data:
        stroke_width = 0
        if stroked:
            stroke_width = C_STROKE_WIDTH
        draw_fret_circle2(ctx, main_color, C_RADIUS, fret, string, label_text, C_TEXT_COLOR, stroke_color, stroke_width)


# Find the fret positions of all occurrences of a particular note on a given string
def find_note_positions(string_notes, note, min_fret, max_fret):
    return [i + 1 for i, n in enumerate(string_notes) if n == note and min_fret <= i + 1 <= max_fret]

# Generate fret ranges based on the root position on the low E string
def calculate_fret_ranges(root_fret):
    def wrap_fret_range(range_start, range_end):
        """Adjusts fret range to fall between 2 and 22."""
        while range_start < 2:
            range_start += 12
            range_end += 12
        while range_end > 22:
            range_start -= 12
            range_end -= 12
        return range_start, range_end

    # Original ranges before wrapping
    raw_ranges = {
        1: (root_fret - 3, root_fret),
        2: (root_fret - 1, root_fret + 2),
        3: (root_fret + 1, root_fret + 5),
        4: (root_fret + 4, root_fret + 7),
        5: (root_fret - 6, root_fret - 3)
    }

    # Wrap each range to ensure it stays within 2-22
    wrapped_ranges = {pos: wrap_fret_range(*rng) for pos, rng in raw_ranges.items()}
    return wrapped_ranges

def calculate_fret_ranges_minor(root_fret):
    def wrap_fret_range(range_start, range_end):
        """Adjusts fret range to fall between 2 and 22."""
        while range_start < 2:
            range_start += 12
            range_end += 12
        while range_end > 22:
            range_start -= 12
            range_end -= 12
        return range_start, range_end

    # Original ranges before wrapping
    raw_ranges = {
        1: (root_fret, root_fret + 3),
        2: (root_fret + 2, root_fret + 5),
        3: (root_fret + 4, root_fret + 8),
        4: (root_fret + 7, root_fret + 10),
        5: (root_fret - 3, root_fret)
    }

    # Wrap each range to ensure it stays within 2-22
    wrapped_ranges = {pos: wrap_fret_range(*rng) for pos, rng in raw_ranges.items()}
    return wrapped_ranges

# Generate the pentatonic scale data for a given root note and position
def generate_pentatonic_c_data(root, position, color_map):
    # Get the index of the root note on the low E string
    root_index = NOTES_6.index(root) + 1  # Fret positions are 1-based

    # Calculate the fret ranges dynamically based on the root index
    fret_ranges = calculate_fret_ranges(root_index)
    min_fret, max_fret = fret_ranges[position]

    # Retrieve the degree patterns and corresponding notes
    scale_intervals = [0, 2, 4, 7, 9]
    scale = [NOTES_6[(root_index - 1 + interval) % 12] for interval in scale_intervals]
    degree_note_pairs = dict(zip(["R", "2", "3", "5", "6"], scale))

    data = []

    for string_index, string_notes in enumerate(ALL_NOTES):
        for degree, note_name in degree_note_pairs.items():
            frets = find_note_positions(string_notes, note_name, min_fret, max_fret)
            for fret in frets:
                data.append((6 - string_index, fret, f"{degree}/{note_name}", color_map[degree], 0, WHITE_COLOR))

    return sorted(data, key=lambda x: (x[0], x[1]))


# Generate the pentatonic scale data for a given root note and position (minor version)
def generate_minor_pentatonic_c_data(root, position, color_map):

    # Get the index of the root note on the low E string
    root_index = NOTES_6.index(root) + 1  # Fret positions are 1-based

    # Calculate the fret ranges dynamically based on the root index
    fret_ranges = calculate_fret_ranges_minor(root_index)
    min_fret, max_fret = fret_ranges[position]

    # Retrieve the degree patterns and corresponding notes for the minor pentatonic
    scale_intervals = [0, 3, 5, 7, 10]
    scale = [NOTES_6[(root_index - 1 + interval) % 12] for interval in scale_intervals]
    degree_note_pairs = dict(zip(["R", "b3", "4", "5", "b7"], scale))

    data = []

    for string_index, string_notes in enumerate(ALL_NOTES):
        for degree, note_name in degree_note_pairs.items():
            frets = find_note_positions(string_notes, note_name, min_fret, max_fret)
            for fret in frets:
                data.append((6 - string_index, fret, f"{degree}/{note_name}", color_map[degree], 0, WHITE_COLOR))

    return sorted(data, key=lambda x: (x[0], x[1]))


COLOR_MAP = {"R": BLUE_COLOR, "2": ORANGE_COLOR, "3": ORANGE_COLOR, "5": ORANGE_COLOR, "6": ORANGE_COLOR}
COLOR_MAP_MINOR = {"R": BLUE_COLOR, "b3": ORANGE_COLOR, "4": ORANGE_COLOR, "5": ORANGE_COLOR, "b7": ORANGE_COLOR}

#c_data = generate_pentatonic_c_data("F", 1)
c_data = generate_minor_pentatonic_c_data("A", 1, COLOR_MAP_MINOR)

draw_circles_from_data(ctx, c_data)
# --- Save Image ---
surface.write_to_png("fret.png")
