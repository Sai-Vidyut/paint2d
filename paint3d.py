# Paint 3D style drawing app (Tkinter)
# Unit 5 - event driven programming
# Run: python3 paint3d.py   (on Mac try: /opt/homebrew/bin/python3.11 paint3d.py)

import tkinter as tk
from tkinter import colorchooser, messagebox

# -------- the main window --------
window = tk.Tk()
window.title("Paint 3D")
window.geometry("1000x700")
window.config(bg="#dddddd")

# -------- things we need to remember while drawing --------
# these are used by the mouse functions below
tool_name = tk.StringVar(value="pencil")
draw_color = tk.StringVar(value="#111111")
brush_size = tk.IntVar(value=4)
fill_shapes = tk.IntVar(value=0)

old_x = 0
old_y = 0
start_click_x = 0
start_click_y = 0

# list of shapes drawn in one drag (for undo)
things_to_undo = []
all_undos = []

# -------- functions that run when you click buttons (event handlers) --------

def update_bottom_text():
    if fill_shapes.get() == 1:
        fill_text = "on"
    else:
        fill_text = "off"
    bottom_label.config(
        text="Tool: " + tool_name.get()
        + "   Colour: " + draw_color.get()
        + "   Size: " + str(brush_size.get())
        + "   Fill: " + fill_text
    )


def set_color(new_color):
    draw_color.set(new_color)
    update_bottom_text()


def pick_more_colors():
    # opens a colour picker window
    picked = colorchooser.askcolor(title="Pick a colour")
    if picked[1]:
        set_color(picked[1])


def clear_everything():
    answer = messagebox.askyesno("New", "Clear the whole drawing?")
    if answer:
        paper.delete("all")
        all_undos.clear()
        update_bottom_text()


def undo_one_thing():
    if len(all_undos) == 0:
        messagebox.showinfo("Undo", "Nothing to undo")
        return
    last_group = all_undos.pop()
    for shape_id in last_group:
        paper.delete(shape_id)
    update_bottom_text()


# -------- mouse events on the canvas (bind) --------

def mouse_clicked(event):
    global old_x, old_y, start_click_x, start_click_y

    old_x = event.x
    old_y = event.y
    start_click_x = event.x
    start_click_y = event.y
    things_to_undo.clear()

    # text tool: put words on the canvas
    if tool_name.get() == "text":
        words = type_here.get()
        if words == "":
            return
        new_id = paper.create_text(
            event.x, event.y, text=words, fill=draw_color.get(),
            font=("Arial", 16), anchor="nw",
        )
        things_to_undo.append(new_id)
        all_undos.append(list(things_to_undo))


def mouse_dragged(event):
    global old_x, old_y

    if tool_name.get() == "text":
        return

    # eraser just draws white
    if tool_name.get() == "eraser":
        line_color = "#ffffff"
        line_width = brush_size.get() * 2
    else:
        line_color = draw_color.get()
        line_width = brush_size.get()

    # pencil and eraser = lots of small lines
    if tool_name.get() == "pencil" or tool_name.get() == "eraser":
        new_id = paper.create_line(
            old_x, old_y, event.x, event.y,
            fill=line_color, width=line_width,
        )
        things_to_undo.append(new_id)
        old_x = event.x
        old_y = event.y
        return

    # for line, rectangle, oval we draw one shape and update it while dragging
    if len(things_to_undo) > 0:
        paper.delete(things_to_undo[0])
        things_to_undo.clear()

    x1 = start_click_x
    y1 = start_click_y
    x2 = event.x
    y2 = event.y

    if fill_shapes.get() == 1:
        inside_color = line_color
    else:
        inside_color = ""

    if tool_name.get() == "line":
        new_id = paper.create_line(x1, y1, x2, y2, fill=line_color, width=line_width)
    elif tool_name.get() == "rectangle":
        new_id = paper.create_rectangle(
            x1, y1, x2, y2, outline=line_color, fill=inside_color, width=line_width,
        )
    elif tool_name.get() == "oval":
        new_id = paper.create_oval(
            x1, y1, x2, y2, outline=line_color, fill=inside_color, width=line_width,
        )
    else:
        return

    things_to_undo.append(new_id)


def mouse_released(event):
    if tool_name.get() == "text":
        return
    if len(things_to_undo) > 0:
        all_undos.append(list(things_to_undo))
    things_to_undo.clear()


def mouse_moved(event):
    xy_label.config(text="x=" + str(event.x) + "  y=" + str(event.y))


# -------- purple top bar like Paint 3D --------
top = tk.Frame(window, bg="#6a5acd", height=50)
top.pack(side="top", fill="x")

tk.Label(top, text="Paint 3D", bg="#6a5acd", fg="white", font=("Arial", 20, "bold")).pack(
    side="left", padx=10, pady=8,
)

tk.Button(top, text="New", command=clear_everything).pack(side="right", padx=5, pady=8)
tk.Button(top, text="Undo", command=undo_one_thing).pack(side="right", padx=5, pady=8)

# -------- bottom status bar --------
bottom_bar = tk.Frame(window, bg="#cccccc")
bottom_bar.pack(side="bottom", fill="x")
bottom_label = tk.Label(bottom_bar, text="", bg="#cccccc", anchor="w")
bottom_label.pack(side="left", padx=10, pady=5)
xy_label = tk.Label(bottom_bar, text="x=0  y=0", bg="#cccccc", anchor="e")
xy_label.pack(side="right", padx=10, pady=5)

# -------- middle part: tools on left, drawing on right --------
middle = tk.Frame(window, bg="#dddddd")
middle.pack(fill="both", expand=True)

# left side - tools
left = tk.Frame(middle, bg="#eeeeee", width=120)
left.pack(side="left", fill="y")

tk.Label(left, text="Tools", bg="#eeeeee", fg="black", font=("Arial", 12, "bold")).pack(
    anchor="w", padx=10, pady=10,
)

tk.Radiobutton(
    left, text="Pencil", variable=tool_name, value="pencil",
    command=update_bottom_text, bg="#eeeeee", fg="black",
).pack(anchor="w", padx=10)
tk.Radiobutton(
    left, text="Line", variable=tool_name, value="line",
    command=update_bottom_text, bg="#eeeeee", fg="black",
).pack(anchor="w", padx=10)
tk.Radiobutton(
    left, text="Rectangle", variable=tool_name, value="rectangle",
    command=update_bottom_text, bg="#eeeeee", fg="black",
).pack(anchor="w", padx=10)
tk.Radiobutton(
    left, text="Oval", variable=tool_name, value="oval",
    command=update_bottom_text, bg="#eeeeee", fg="black",
).pack(anchor="w", padx=10)
tk.Radiobutton(
    left, text="Text", variable=tool_name, value="text",
    command=update_bottom_text, bg="#eeeeee", fg="black",
).pack(anchor="w", padx=10)
tk.Radiobutton(
    left, text="Eraser", variable=tool_name, value="eraser",
    command=update_bottom_text, bg="#eeeeee", fg="black",
).pack(anchor="w", padx=10)

# right side - colours and canvas
right = tk.Frame(middle, bg="#dddddd")
right.pack(side="left", fill="both", expand=True)

colour_bar = tk.Frame(right, bg="#eeeeee")
colour_bar.pack(fill="x")

tk.Label(colour_bar, text="Colours:", bg="#eeeeee").pack(side="left", padx=5, pady=5)

# each colour is a small label you can click
color_list = [
    "#111111", "#ffffff", "#ff0000", "#ff8800", "#ffff00",
    "#00aa00", "#0000ff", "#8800ff", "#ff00aa", "#888888",
]

for c in color_list:
    box = tk.Label(colour_bar, bg=c, width=2, relief="solid", borderwidth=1)
    box.pack(side="left", padx=2, pady=5)
    box.bind("<Button-1>", lambda event, col=c: set_color(col))

tk.Button(colour_bar, text="More colours", command=pick_more_colors).pack(side="left", padx=8)

tk.Label(colour_bar, text="Size", bg="#eeeeee").pack(side="left", padx=5)
tk.Scale(
    colour_bar, variable=brush_size, from_=1, to=20,
    orient=tk.HORIZONTAL, length=120, command=lambda x: update_bottom_text(),
).pack(side="left")

tk.Checkbutton(
    colour_bar, text="Fill shape", variable=fill_shapes,
    command=update_bottom_text, bg="#eeeeee",
).pack(side="left", padx=8)

tk.Label(colour_bar, text="Type here:", bg="#eeeeee").pack(side="left", padx=5)
type_here = tk.Entry(colour_bar, width=12)
type_here.pack(side="left", padx=5, pady=5)
type_here.insert(0, "Hello")

# white paper to draw on
paper_frame = tk.Frame(right, bg="#bbbbbb")
paper_frame.pack(fill="both", expand=True, padx=15, pady=15)

paper = tk.Canvas(paper_frame, bg="white", cursor="crosshair")
paper.pack(fill="both", expand=True)

# hook up mouse events (this is event driven programming)
paper.bind("<Button-1>", mouse_clicked)
paper.bind("<B1-Motion>", mouse_dragged)
paper.bind("<ButtonRelease-1>", mouse_released)
paper.bind("<Motion>", mouse_moved)

update_bottom_text()

# start the event loop - program waits for clicks and drags
if __name__ == "__main__":
    window.mainloop()
