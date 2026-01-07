import tkinter as tk
import math
import random


BG_COLOR = "#050505"
TRUNK_COLOR = "#3E2723"
PETAL_COLORS = [
    "#FFCDD2", "#FFAB91", "#F48FB1", "#F06292", 
    "#FFFFFF", "#FF80AB", "#FF4081", "#FFEBEE"
]
SPARKLE_COLORS = ["#FFFFFF", "#FFF59D", "#FFE082", "#E1F5FE"]

class Plugin(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.running = True
        self.active_branches = []
        self.falling_particles = [] 
        self.wind_offset = 0.0
        self.tree_built = False   
        self.after(100, self.init_tree)
        self.bind("<Configure>", self.on_resize)

    def init_tree(self):
        self.reset_scene()
        self.animate()

    def on_resize(self, event):
        if hasattr(self, 'width'):
            if abs(self.width - event.width) > 100 or abs(self.height - event.height) > 100:
                self.reset_scene()

    def reset_scene(self):
        self.canvas.delete("all")
        self.active_branches = []
        self.falling_particles = []
        self.wind_offset = 0.0
        self.tree_built = False
        
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        if self.width <= 1: self.width = 1000
        if self.height <= 1: self.height = 800

        initial_depth = 9

        self.active_branches.append({
            "id": None,
            "x": self.width / 2, "y": self.height, 
            "angle": -90, "current_length": 0,
            "max_length": self.height * 0.25, 
            "width": 26, "depth": initial_depth,
            "color": TRUNK_COLOR
        })
        self.create_background_stars()

    def create_background_stars(self):
        
        for _ in range(70):
            x = random.randint(0, self.width)
            y = random.randint(0, int(self.height * 0.7))
            size = random.uniform(0.5, 2)
            alpha = random.choice(["#333", "#555", "#777", "#444"])
            self.canvas.create_oval(x, y, x+size, y+size, fill=alpha, outline="")

    def draw_growing_tree(self):
        if not self.active_branches:
            self.tree_built = True
            return

        new_branches = []
        for b in self.active_branches:
            growth = 12 if b["depth"] > 5 else 18
            b["current_length"] += growth
            
            rad = math.radians(b["angle"])
            cx = b["x"] + math.cos(rad) * b["current_length"]
            cy = b["y"] + math.sin(rad) * b["current_length"]

            if b["id"] is None:
                b["id"] = self.canvas.create_line(
                    b["x"], b["y"], cx, cy,
                    width=b["width"], fill=b["color"], capstyle=tk.ROUND, tag="tree"
                )
            else:
                self.canvas.coords(b["id"], b["x"], b["y"], cx, cy)            
            
            if b["depth"] <= 4 and random.random() < 0.15:
                self.bloom_visual_trick(cx, cy, scale=0.5)

            if b["current_length"] < b["max_length"]:
                new_branches.append(b)
            else:
                fx = b["x"] + math.cos(rad) * b["max_length"]
                fy = b["y"] + math.sin(rad) * b["max_length"]
                self.canvas.coords(b["id"], b["x"], b["y"], fx, fy)
                
                if b["depth"] > 0:
                    self.branch_out(fx, fy, b["angle"], b["depth"], b["width"], new_branches)
                else:
                    self.bloom_visual_trick(fx, fy, scale=1.2, dense=True)
                    if random.random() < 0.3:
                        self.spawn_particle(fx, fy, "sparkle")
        
        self.active_branches = new_branches

    def branch_out(self, x, y, angle, depth, width, branch_list):
        count = random.choice([2, 2, 3]) 
        for _ in range(count):
            divergence = random.uniform(20, 50)
            direction = random.choice([-1, 1])
            new_angle = angle + (direction * divergence) + random.uniform(-5, 5)
            
            scale = random.uniform(0.65, 0.8)
            new_len = 120 * (scale ** (10 - depth))
            new_width = width * 0.65
            
            color = TRUNK_COLOR
            if depth <= 4: color = "#5D4037"
            if depth <= 2: color = "#795548"

            branch_list.append({
                "id": None, "x": x, "y": y,
                "angle": new_angle, "current_length": 0,
                "max_length": max(15, new_len),
                "width": max(2, new_width),
                "depth": depth - 1, "color": color
            })

    def bloom_visual_trick(self, x, y, scale=1.0, dense=False):         
        
        base_size = random.randint(6, 10) * scale
        base_color = random.choice(PETAL_COLORS)
        self.canvas.create_oval(
            x - base_size, y - base_size, x + base_size, y + base_size,
            fill=base_color, outline=base_color, tag="blossom"
        )
            
        count = 2 if dense else 1
        for _ in range(count):
            off_x = random.uniform(-4, 4) * scale
            off_y = random.uniform(-4, 4) * scale
            s = random.randint(2, 5) * scale
            c = random.choice(SPARKLE_COLORS if random.random() < 0.2 else PETAL_COLORS)
            self.canvas.create_oval(
                x + off_x - s, y + off_y - s, x + off_x + s, y + off_y + s,
                fill=c, outline="", tag="blossom"
            )

        if dense and random.random() < 0.2:
            self.spawn_particle(x, y, "petal")

    def spawn_particle(self, x, y, p_type):
        
        if len(self.falling_particles) > 150: return

        if p_type == "petal":
            color = random.choice(PETAL_COLORS)
            size = random.randint(3, 5)
            
            pid = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="", tag="falling")
            vy = random.uniform(2, 4.5)
            vx = random.uniform(-1, 1)
        else: 
            color = random.choice(SPARKLE_COLORS)
            size = random.randint(1, 3)
            pid = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="", tag="falling")
            vy = random.uniform(-1, -3) 
            vx = random.uniform(-0.5, 0.5)

        self.falling_particles.append({
            "id": pid, "x": x, "y": y,
            "vx": vx, "vy": vy,
            "phase": random.uniform(0, 10),
            "type": p_type,
            "life": 100 if p_type == "sparkle" else 999
        })

    def update_physics(self):
        self.wind_offset += 0.08
        active_p = []
        width, height = self.width, self.height
        
        for p in self.falling_particles:
            sway = math.sin(self.wind_offset + p["phase"])
            if p["type"] == "petal":
                dx = p["vx"] + sway * 1.5
                dy = p["vy"]
            else: 
                dx = p["vx"] + sway * 0.5
                dy = p["vy"]
                p["life"] -= 1

            p["x"] += dx
            p["y"] += dy
            self.canvas.move(p["id"], dx, dy)
            
            
            keep = True
            if p["type"] == "petal" and p["y"] > height + 20: keep = False
            if p["type"] == "sparkle" and p["life"] <= 0: keep = False
            
            if keep:
                active_p.append(p)
            else:
                self.canvas.delete(p["id"])
           
        self.falling_particles = active_p
        
        if self.tree_built and len(self.falling_particles) < 120:
            if random.random() < 0.5:
                start_x = random.randint(0, int(width))
                self.spawn_particle(start_x, -10, "petal")

    def animate(self):
        if not self.running: return
        self.draw_growing_tree()
        self.update_physics()
        self.after(30, self.animate) 

    def teardown(self):
        self.running = False