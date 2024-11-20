import tkinter as tk
import math
from datetime import datetime, timedelta
from tkinter import font, messagebox
from PIL import Image, ImageTk

threshold_distance = 100
colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#FFC733"]
button_border_color = "#2C3E50"

nodes = []
edges = []
next_id = 1
show_edges = True

color_to_number = {color: index + 1 for index, color in enumerate(colors)}

root = tk.Tk()
root.title("Runtime Assignment")

window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = 0

root.geometry(f"{window_width}x{window_height + window_height}+{x}+{y}")

canvas = tk.Canvas(root, width=window_width, height=window_height - 200, bg="black")
canvas.pack()

node_image_path = "transistor-removebg.png"
node_image = Image.open(node_image_path)
node_image = node_image.resize((50, 50), Image.LANCZOS)
node_image_tk = ImageTk.PhotoImage(node_image)

table_frame = tk.Frame(root, bg="#F2F2F2", bd=2, relief="solid")
table_frame.pack(pady=10)

header_font = font.Font(family="Verdana", size=12, weight="bold")
header_bg = "#2C3E50"
header_fg = "#FDFEFE"

headers = ["Transistor ID", "Color", "Color Number", "Runtime"]
for col, header in enumerate(headers):
    tk.Label(table_frame, text=header, font=header_font, bg=header_bg, fg=header_fg, padx=10, pady=5).grid(row=0, column=col, sticky="ew")

time_frame = tk.Frame(root)
time_frame.pack(pady=10)

tk.Label(time_frame, text="Start Time (HH:MM):").grid(row=0, column=0)
start_time_entry = tk.Entry(time_frame)
start_time_entry.grid(row=0, column=1)

tk.Label(time_frame, text="Duration (minutes):").grid(row=0, column=2)
duration_entry = tk.Entry(time_frame)
duration_entry.grid(row=0, column=3)

def show_problem_statement():
    problem_window = tk.Toplevel(root)
    problem_window.title("Problem Statement")
    problem_window.geometry("400x350")
    problem_window.resizable(False, False)
    
    problem_text = """The efficient design of VLSI (Very Large Scale Integration) circuits requires optimal time slot management for transistor operations. This application tackles the challenge of assigning different time slots to adjacent transistors to avoid interference.

It provides a graphical interface for users to place transistors as nodes on a canvas, connecting them with edges based on a specified threshold distance. A graph coloring algorithm is utilized to assign distinct colors (representing time slots) to these nodes, ensuring effective runtime scheduling.

Users can input a start time and duration for each slot, facilitating systematic management of transistor operations. This visual representation enhances understanding and optimization of VLSI circuit performance."""
    
    text_box = tk.Text(problem_window, wrap=tk.WORD, bg="#F2F2F2", font=("Verdana", 10), padx=10, pady=10)
    text_box.insert(tk.END, problem_text)
    text_box.config(state=tk.DISABLED) 
    text_box.pack(expand=True, fill=tk.BOTH)

def add_node(x, y, color):
    global next_id
    new_node = {"x": x, "y": y, "color": color, "number": color_to_number[color], "id": next_id, "runtime": None}
    nodes.append(new_node)

    for i, node in enumerate(nodes[:-1]):
        if calculate_distance(node, new_node) < threshold_distance:
            edges.append((i, len(nodes) - 1))

    next_id += 1
    draw_nodes_and_edges()

def calculate_distance(node1, node2):
    return math.sqrt((node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2)

def draw_nodes_and_edges():
    canvas.delete("all")

    if show_edges:
        for i, j in edges:
            x1, y1 = nodes[i]["x"], nodes[i]["y"]
            x2, y2 = nodes[j]["x"], nodes[j]["y"]
            canvas.create_line(x1, y1, x2, y2, fill="white", width=1)

    for node in nodes:
        x = node["x"] - 25
        y = node["y"] - 25
        canvas.create_image(x, y, anchor=tk.NW, image=node_image_tk)
        canvas.create_text(node["x"], node["y"] - 30, text=str(node["id"]), fill="white", font=("Arial", 10, "bold"))

def apply_graph_coloring():
    for node in nodes:
        node["color"] = None
        node["number"] = None
        node["runtime"] = None

    start_time_str = start_time_entry.get()
    duration_str = duration_entry.get()
    
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M")
        duration_minutes = int(duration_str)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs for time and duration.")
        return

    for index, node in enumerate(nodes):
        neighbor_colors = set()
        
        for i, j in edges:
            if i == index and nodes[j]["color"] is not None:
                neighbor_colors.add(nodes[j]["color"])
            if j == index and nodes[i]["color"] is not None:
                neighbor_colors.add(nodes[i]["color"])
        
        for color in colors:
            if color not in neighbor_colors:
                node["color"] = color
                node["number"] = color_to_number[color]
                break

    color_runtime = {}
    for index, color in enumerate(colors):
        color_runtime[color] = start_time + timedelta(minutes=index * duration_minutes)
        
    for node in nodes:
        if node["color"] in color_runtime:
            node["runtime"] = color_runtime[node["color"]]

    draw_nodes_and_edges()
    update_table()
    messagebox.showinfo("Graph Coloring", "Graph coloring successfully applied!")

def update_table():
    for widget in table_frame.winfo_children()[4:]:
        widget.destroy()

    row_counter = 1
    for node in nodes:
        bg_color = "#E8F8F5" if row_counter % 2 == 0 else "#FEF9E7"
        
        if node["number"] is not None:
            tk.Label(table_frame, text=str(node["id"]), bg=bg_color, padx=10, pady=5).grid(row=row_counter, column=0, sticky="ew")
            tk.Label(table_frame, text=node["color"], bg=node["color"], padx=10, pady=5).grid(row=row_counter, column=1, sticky="ew")
            tk.Label(table_frame, text=str(node["number"]), bg=bg_color, padx=10, pady=5).grid(row=row_counter, column=2, sticky="ew")
            runtime_str = node["runtime"].strftime("%H:%M") if node["runtime"] else ""
            tk.Label(table_frame, text=runtime_str, bg=bg_color, padx=10, pady=5).grid(row=row_counter, column=3, sticky="ew")
        
        row_counter += 1

def clear_canvas():
    global next_id
    canvas.delete("all")
    nodes.clear()
    edges.clear()
    next_id = 1
    update_table()
    messagebox.showinfo("Canvas Cleared", "All nodes and edges have been cleared.")

def toggle_edges():
    global show_edges
    show_edges = not show_edges
    draw_nodes_and_edges()

def create_draggable_image():
    node_label = tk.Label(root, image=node_image_tk)
    node_label.place(x=375, y=0)

    def on_drag(event):
        node_label.place(x=event.x_root - 585, y=event.y_root - 80)

    def on_drop(event):
        x, y = event.x_root - 560, event.y_root - 60
        add_node(x, y, colors[0])
        node_label.place(x=375, y=0)

    node_label.bind("<Button-1>", lambda e: node_label.bind("<B1-Motion>", on_drag))
    node_label.bind("<ButtonRelease-1>", on_drop)

button_frame = tk.Frame(root)
button_frame.pack()

apply_button = tk.Button(button_frame, text="Apply", command=apply_graph_coloring,
                         bg="white", fg="#2C3E50", font=("Verdana", 10, "bold"),
                         highlightbackground=button_border_color, highlightthickness=2, bd=1)
apply_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear Canvas", command=clear_canvas,
                         bg="white", fg="#2C3E50", font=("Verdana", 10, "bold"),
                         highlightbackground=button_border_color, highlightthickness=2, bd=1)
clear_button.pack(side=tk.LEFT, padx=5)

toggle_edges_button = tk.Button(button_frame, text="Toggle Edges", command=toggle_edges,
                                 bg="white", fg="#2C3E50", font=("Verdana", 10, "bold"),
                                 highlightbackground=button_border_color, highlightthickness=2, bd=1)
toggle_edges_button.pack(side=tk.LEFT, padx=5)

problem_statement_button = tk.Button(button_frame, text="Problem Statement", command=show_problem_statement,
                                     bg="white", fg="#2C3E50", font=("Verdana", 10, "bold"),
                                     highlightbackground=button_border_color, highlightthickness=2, bd=1)
problem_statement_button.pack(side=tk.LEFT, padx=5)

create_draggable_image()

root.mainloop()
