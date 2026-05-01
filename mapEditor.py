import tkinter as tk, json, sys
from tkinter import messagebox

try:
    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError as err:
    sys.exit(f"Decode first before editing the map\n\n{err}")

map = data.get('eventBuffer', [])[0]['data']['map']

# VALUES

CELL_SIZE = 20
ROWS = len(map["map"])
COLS = len(map["map"][0])
CALC_ROWS = int(ROWS * CELL_SIZE)
CALC_COLS = int(COLS * CELL_SIZE)

MAP_DEF = {
    "0": "Eraser",
    "1": "Wall",
    "2": "Fence",
    "3": "Ice",
    "4": "Roof",
    "5": "Blue Wall",
    "6": "Red Wall",
    "7": "Pale Blue Wall",
    "8": "Pale Red Wall",
    "c": "Capture Point",
    "f": "ForceField" # Force Fields might not exist in older replays since they're new
}

colors = {
    "0": "white",

    # Blocks
    "1": "gray65", # Wall
    "2": "slate gray", # Fence
    "3": "turquoise2", # Ice
    "4": "black", # Roof

    # Team Blocks
    "5": "DodgerBlue3",
    "6": "firebrick3",
    "7": "dodger blue", # pale
    "8": "firebrick1", # pale

    # Interactable Blocks
    "c": "purple2", # Capture point/payload
    "f": "SteelBlue2", # forcefield
    
    # Combined Blocks (Non-selectable)
    "ir": "midnight blue", # Ice Roof
    "fr": "dim gray", # Fence Roof
    "cr": "purple4", # Capture point Roof
    "ffr": "steel blue", # Force field Roof
    "ffi": "CadetBlue3", # Force field Ice
    "ci": "maroon3" # Capture point Ice
}

selected_color = 0

# Tkinter Setup
root = tk.Tk()
root.title("BlockTanks Map Editor")
root.attributes("-topmost", True)
root.resizable(False, False)
canvas = tk.Canvas(root, width=CALC_COLS, height=CALC_ROWS)
canvas.pack()

# FUNCTIONS

def draw_map():
    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            block_type = str(map["map"][r][c])
            color = colors.get(block_type, "white")

            for roof in map["roof_spawns"]:
                roof_pos_calc = c == roof[0] // 100 and r == roof[1] // 100

                if roof_pos_calc and block_type != "0":
                    if block_type == "3":
                        color = colors["ir"]
                    elif block_type == "2":
                        color = colors["fr"]
                    else:
                        color = colors["4"]
                elif roof_pos_calc:
                    color = colors["4"]

            for p in map["control_points"]:
                payload_pos_calc = c == p[0] // 100 and r == p[1] // 100

                if payload_pos_calc and block_type == "3":
                    color = colors["ci"]
                elif payload_pos_calc and p in map["roof_spawns"]:
                    color = colors["cr"]
                elif payload_pos_calc:
                    color = colors["c"]

            try:
                for ff in map["force_field_spawns"]:
                    force_field_pos_calc = c == ff[0] // 100 and r == ff[1] // 100

                    if force_field_pos_calc and block_type == "3":
                        color = colors["ffi"]
                    elif force_field_pos_calc and ff in map["roof_spawns"]:
                        color = colors["ffr"]
                    elif force_field_pos_calc:
                        color = colors["f"]
            except Exception:
                pass

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")

def add_block(event):
    c, r = event.x // CELL_SIZE, event.y // CELL_SIZE

    if 0 < r < ROWS and 0 < c < COLS:
        if selected_color == "4":
            for roof in map["roof_spawns"]:
                if c == roof[0] // 100 and r == roof[1] // 100:
                    return # dont do anything when we have a roof there

            map["roof_spawns"] += [[(c * 100) + 50, (r * 100) + 50]]
        elif selected_color == "c":
            for p in map["control_points"]:
                if c == p[0] // 100 and r == p[1] // 100:
                    return # dont do anything when we have a control point there

            map["control_points"] += [[(c * 100) + 50, (r * 100) + 50]]
        elif selected_color == "f":
            for ff in map["force_field_spawns"]:
                if c == ff[0] // 100 and r == ff[1] // 100:
                    return # dont do anything when we have a force field there

            map["force_field_spawns"] += [[(c * 100) + 50, (r * 100) + 50]]
        else:
            if map["map"][r][c] == int(selected_color) and selected_color != "0": return

            map["map"][r][c] = int(selected_color)

            if selected_color == "0":
                for roof in map["roof_spawns"]:
                    if c == roof[0] // 100 and r == roof[1] // 100:
                        edited_roofs = [i for i in map["roof_spawns"] if i != roof]
                        map["roof_spawns"] = edited_roofs
                        break

                for p in map["control_points"]:
                    if c == p[0] // 100 and r == p[1] // 100:
                        edited_payloads = [i for i in map["control_points"] if i != p]
                        map["control_points"] = edited_payloads
                        break

                for ff in map["force_field_spawns"]:
                    if c == ff[0] // 100 and r == ff[1] // 100:
                        edited_ff = [i for i in map["force_field_spawns"] if i != ff]
                        map["force_field_spawns"] = edited_ff
                        break

        # Copy map data from first to a duplicate welcome event if there is one to ensure accuracy
        second_welcome_event = data.get('eventBuffer', [])[1]['data']['map']

        if second_welcome_event != None and len(second_welcome_event) != 0:
            data.get('eventBuffer', [])[1]['data']['map'] = data.get('eventBuffer', [])[0]['data']['map']

        draw_map()

def change_map_block(event):
    global selected_color

    if event.char in colors:
        selected_color = event.char
        print(f"Selected {MAP_DEF[selected_color]}")

# HELPER FUNCTIONS

def center_window(window, rel):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (rel[0] // 2)
    y = (screen_height // 2) - (rel[1] // 2)

    window.geometry(f'+{x}+{y}')

def on_closing():
    x = messagebox.askyesnocancel("Save Changes?", "Do you want to save changes before quitting?", parent=root)

    if x:
        # Save changes
        try:
            with open('output.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, separators=(',', ':'))
        except FileNotFoundError as err:
            # root.destroy()
            sys.exit(f"output.json might've been deleted or moved, map did not save.\n\n{err}")

        # Quit
        root.destroy()
    elif x == None:
        print("\n\nUser has cancled, not quitting.\n\n")
    else:
        print("Map not saved")
        root.destroy()

# Bind left click and all keys, then make canvas input focus
canvas.bind("<Button-1>", add_block)
canvas.bind("<Key>", change_map_block)
canvas.focus_set()

# Draw the map, canter the window, and set-up window closing function (Does not work when terminal closes).
draw_map()
center_window(root, [CALC_COLS, CALC_ROWS])
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()