import tkinter as tk, json

# TODO:
# Add the ability to place forcefields, weapon spawns, and payloads 

with open('output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

map = data.get('eventBuffer', [])[0]['data']['map']

# Configuration
CELL_SIZE = 20
ROWS = len(map["map"])
COLS = len(map["map"][0])
CALC_ROWS = int(ROWS * CELL_SIZE)
CALC_COLS = int(COLS * CELL_SIZE)

MAP_DEF = {
    0: "Empty",
    1: "Wall",
    2: "Fence",
    3: "Ice",
    # Roofs are defined in roof_spawns ¯\_(ツ)_/¯
    4: "Roof",
    5: "Blue Wall",
    6: "Red Wall",
    7: "Pale Blue Wall",
    8: "Pale Red Wall"
}

# Tkinter Setup
root = tk.Tk()
root.title("BlockTanks Map Editor")
root.attributes("-topmost", True)
canvas = tk.Canvas(root, width=CALC_COLS, height=CALC_ROWS)
canvas.pack()

# 0 = Eraser, 1 = Wall, 2 = Fence, 3 = Ice, 4 = Roof, 5 = Blue wall, 6 = Red Wall, 7 = Pale Blue Wall, 8 = Pale Red Wall
colors = {0: "white", 1: "gray65", 2: "slate gray", 3: "turquoise2", 4: "black", 5: "DodgerBlue3", 6: "firebrick3", 7: "dodger blue", 8: "firebrick1"}
selected_color = 0

def draw_map():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = colors.get(map["map"][r][c], "white")
            for roof in map["roof_spawns"]:
                if c == roof[0] // 100 and r == roof[1] // 100:
                    color = colors[4]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")

def add_block(event):
    c, r = event.x // CELL_SIZE, event.y // CELL_SIZE
    safe = False

    if 0 <= r < ROWS and 0 <= c < COLS:
        if selected_color == 4:
            for roof in map["roof_spawns"]:
                if c == roof[0] // 100 and r == roof[1] // 100:
                    return # dont do anything when we have a roof there
                safe = True
            if safe:
                map["roof_spawns"] += [[(c * 100) + 50, (r * 100) + 50]]
        else:
            map["map"][r][c] = selected_color
            for roof in map["roof_spawns"]:
                if c == roof[0] // 100 and r == roof[1] // 100:
                    edited_roofs = [i for i in map["roof_spawns"] if i != roof]
                    map["roof_spawns"] = edited_roofs
                    break

        # Copy map data from first to a duplicate welcome event if there is one to ensure accuracy
        if data.get('eventBuffer', [])[1]['data']['map'] != None:
            data.get('eventBuffer', [])[1]['data']['map'] = data.get('eventBuffer', [])[0]['data']['map']
        
        # Save changes
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))

        draw_map()

def change_map_block(event):
    global selected_color
    match event.char:
        case '0':
            selected_color = 0
        case '1':
            selected_color = 1
        case '2':
            selected_color = 2
        case '3':
            selected_color = 3
        case '4':
            selected_color = 4
        case '5':
            selected_color = 5
        case '6':
            selected_color = 6
        case '7':
            selected_color = 7
        case '8':
            selected_color = 8
        case _:
            return

    print(f"Selected {MAP_DEF[selected_color]}")
    
def center_window(window, rel):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (rel[0] // 2)
    y = (screen_height // 2) - (rel[1] // 2)

    window.geometry(f'+{x}+{y}')
    
canvas.bind("<Button-1>", add_block)
canvas.bind("<Key>", change_map_block)
canvas.focus_set()

draw_map()
center_window(root, [CALC_COLS, CALC_ROWS])
root.mainloop()