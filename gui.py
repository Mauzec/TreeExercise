import tkinter as tk
from tkinter import ttk
import json
from tkinter.messagebox import showinfo
import os;

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
VERTEX_RADIUS = 10
LINE_WIDTH = 2

class UI:
    def __init__(self, master: tk.Tk, title: str):
        self.edges = dict()
        self.vertices = list()
        self.vertices_xy = set()


        self.master = master
        self.master.title(title)
        
        self.master['background'] = "#D6EAF8"
        self.create_widgets()
        self.current_vertex = None
        self.canvas.bind('<Button-1>', self.handle_canvas_click)
        self.master.mainloop()

    def add_vertex(self, event):
        x, y = event.x, event.y
        self.draw_vertex((x, y))

    def handle_canvas_click(self, event):
        x, y = event.x, event.y
        yes = False
        for vertex in self.vertices:
            vx, vy, w = vertex
            if self.current_vertex == vertex: 
                yes = True
                continue
            if (x - vx) ** 2 + (y - vy) ** 2 <= VERTEX_RADIUS ** 2:
                if self.current_vertex is None:
                    self.current_vertex = vertex
                else:
                    print((self.current_vertex[0], self.current_vertex[1], vx, vy))
                    print((vx, vy, self.current_vertex[0], self.current_vertex[1]))
                    if (((vx, vy) not in self.edges) or ((self.current_vertex[0], self.current_vertex[1]) not in self.edges[vx, vy])) and\
                        (((self.current_vertex[0], self.current_vertex[1]) not in self.edges) or ((vx, vy) not in self.edges[self.current_vertex[0], self.current_vertex[1]])):
                        print(self.edges)
                        self.draw_edge(self.current_vertex, vertex)
                    self.current_vertex = None
                return
        if not yes:
            idx = self.draw_vertex((x,y))
        else:
            self.current_vertex = None

    def set_vertex_number(self, x, y, number, dialog, idx):
        self.canvas.create_text(x, y, text=number, fill='white') 
        print(idx)
        self.vertices[idx][2] = number
        print(self.vertices)
        dialog.destroy()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#EBF5FB')
        self.canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.master, columns=('From', 'To'), show='headings', style='Custom.Treeview')
        self.tree.heading('From', text='From')
        self.tree.heading('To', text='To')
        self.tree.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        ttk.Button(self.master, text="Clear", command=self.clear_all, style='Custom.TButton', cursor='hand2', takefocus=False).grid(row=3, column=2, columnspan=2, pady=10, sticky="nsew")
        ttk.Button(self.master, text="Read JSON", command=self.read_json, style='Custom.TButton', cursor='hand2', takefocus=False).grid(row=4, column=2, columnspan=2, pady=10, sticky="nsew")
        ttk.Button(self.master, text="Solve", command=self.solve, style='Custom.TButton', cursor='hand2', takefocus=False).grid(row=5, column=2, columnspan=2, pady=10, sticky="nsew")
    
    def solve(self):
        with open('temp.log', mode='w') as file:
            file.write(f'{len(self.vertices)}\n')
            for vx, vy, w in self.vertices:
                file.write(f'{vx} {vy} {w}\n')
            file.write(f'{len(self.edges.keys())}\n')
            for key, values in self.edges.items():
                file.write(f'{len(values)} {key[0]} {key[1]}\n')
                for x, y in values:
                    file.write(f'{x} {y}\n')
        os.system('./algo')
        lines = []
        with open("out.log", mode="r") as out:
            lines = out.readlines()
        showinfo("Results", str.join('\n', lines))


    def clear_all(self):
        self.vertices.clear()
        self.edges.clear()
        self.canvas.delete('all')
        self.tree.delete(*self.tree.get_children())


    def draw_vertex(self, coordinates: tuple, append=True, fromjs=False):
        x,y = -1, -1
        w = -1
        if fromjs:
            x,y, w = coordinates
        else:
            x,y = coordinates
        idx = len(self.vertices)
        self.vertices.append([x, y, -1])
        self.canvas.create_oval(x-VERTEX_RADIUS, y-VERTEX_RADIUS, x+VERTEX_RADIUS, y+VERTEX_RADIUS, fill='#58D68D')
        
        if fromjs:
            self.canvas.create_text(x, y, text=w, fill='white') 
            self.vertices[idx][2] = coordinates[2]
            return

        number_dialog = tk.Toplevel(self.master)
        number_dialog.title("Choose Number")
        
        number_label = ttk.Label(number_dialog, text="Choose number for the vertex:")
        number_label.pack()

        number_var = tk.StringVar()
        number_entry = ttk.Entry(number_dialog, textvariable=number_var)
        number_entry.pack()

        confirm_button = ttk.Button(number_dialog, text="Confirm", command=lambda: self.set_vertex_number(x, y, number_var.get(), number_dialog, idx))
        confirm_button.pack()
        return idx


    def draw_edge(self, from_vertex: list, to_vertex: list):
        if (to_vertex[0] == -1 or from_vertex[0] == -1): return
        self.tree.insert('', 'end', values=(f"{from_vertex[0]}, {from_vertex[1]}, {from_vertex[2]}", 
                                            f"{to_vertex[0]}, {to_vertex[1]}, {to_vertex[2]}"))
        if (from_vertex[0], from_vertex[1]) in self.edges:
            if (self.edges[from_vertex[0], from_vertex[1]][0] == (-1, -1)):
                self.edges[from_vertex[0], from_vertex[1]][0] = (to_vertex[0], to_vertex[1])
            else:
                self.edges[from_vertex[0], from_vertex[1]][1] = (to_vertex[0], to_vertex[1])
        else:
            self.edges[from_vertex[0], from_vertex[1]] = list()
            if (to_vertex[0] > from_vertex[0]):
                self.edges[from_vertex[0], from_vertex[1]].append((-1, -1))
                self.edges[from_vertex[0], from_vertex[1]].append((to_vertex[0], to_vertex[1]))
            elif (to_vertex[0] < from_vertex[0]):
                self.edges[from_vertex[0], from_vertex[1]].append((to_vertex[0], to_vertex[1]))
                self.edges[from_vertex[0], from_vertex[1]].append((-1, -1))
        from_x, from_y = from_vertex[0], from_vertex[1]
        to_x, to_y = to_vertex[0], to_vertex[1]
        
        to_x, to_y = self.get_coordinate_edge(from_x, from_y, to_x, to_y)

        line = self.canvas.create_line(from_x, from_y, to_x, to_y, width=LINE_WIDTH, fill='#E74C3C', tag='line')
        self.canvas.tag_lower(line)

    def get_coordinate_edge(self, x1, y1, x2, y2, r=VERTEX_RADIUS):
        k = (y2-y1) / (x2 - x1)
        d = (x2 + k**2 * x1 + k * (y2 - y1))**2 - (k**2 + 1) * (x2**2 + (k*x1)**2 + 2*k*x1*(y2-y1) + (y2-y1)**2 - r**2)
        
        x = (x2 + k**2 * x1 + k * (y2 - y1) - d**0.5) / (k**2 + 1)
        y = (x - x1) * k + y1
        o_1 = (x, y)
        
        x = (x2 + k**2 * x1 + k * (y2 - y1) + d**0.5) / (k**2 + 1)
        y = (x - x1) * k + y1
        o_2 = (x, y)
        
        return o_1 if (x1 - o_1[0])**2 + (y1 - o_1[1]) ** 2 < (x1 - o_2[0])**2 + (y1 - o_2[1]) ** 2 else o_2

    def read_json(self, name="graph.json"):
        self.vertices.clear()
        self.edges.clear()
        self.canvas.delete('all')
        self.tree.delete(*self.tree.get_children())
        with open(f"{name}", 'r') as file:
            data = json.load(file)
            for i in range(len(data["vertexes"])):
                vertex = (data["vertexes"][i]["x"], data["vertexes"][i]["y"], str(data["vertexes"][i]["w"]))
                self.draw_vertex(vertex, fromjs=True)
            for i in range(len(data["edges"])):
                edge = data["edges"][i]
                for too in edge["to"]:
                    self.draw_edge(edge["from"], too)

if __name__ == "__main__":
    root = tk.Tk()
    gui = UI(root, "TSBST")
