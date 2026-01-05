import tkinter as tk
import math
import random
import colorsys

BG_COLOR = "#050505"

def safe_fade_color(hex_color, brightness):
    try:
        if not hex_color.startswith('#'): return hex_color
        hex_color = hex_color.lstrip('#')
        if len(hex_color) > 6: hex_color = hex_color[:6]
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, min(255, int(r * brightness)))
        g = max(0, min(255, int(g * brightness)))
        b = max(0, min(255, int(b * brightness)))
        return f'#{r:02x}{g:02x}{b:02x}'
    except: return "#000000"

class Plugin(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)        
        self.width = 800
        self.height = 600
        self.bind("<Configure>", self.on_resize)        
        self.MAX_PARTICLES = 500  
        self.running = True
        self.hue = 0.0      
        self.particles = []
        self.sparkles = []
        self.rockets = []
        self.stars = []
        
        self.create_stars()
        self.animate()
    
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        if not self.stars: self.create_stars()

    def create_stars(self):
        self.stars = []
        for _ in range(50):
            self.stars.append({
                "x": random.randint(0, self.width),
                "y": random.randint(0, self.height // 2),
                "size": random.uniform(0.5, 2.0), 
                "alpha": random.random()
            })

    def create_explosion(self, x, y, color):
        
        count = random.randint(50, 80)
        style = random.choice(["classic", "burst"]) 
             
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)          
            
            if style == "burst":
                speed = random.uniform(6, 12) 
            else:
                speed = random.uniform(4, 9)

            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            self.particles.append({
                "x": x, "y": y,
                "prev_x": x, "prev_y": y,
                "vx": vx, "vy": vy,
                "life": random.randint(40, 60),
                "max_life": 60,
                "color": color,
                "drag": 0.96 
            })
            
        if len(self.particles) > self.MAX_PARTICLES:
            self.particles = self.particles[-self.MAX_PARTICLES:]

    def launch_rocket(self):
        if len(self.rockets) >= 4: return 

        x = random.randint(100, self.width - 100)
        vy = random.uniform(-15, -20) 
        color = random.choice(["#FF0044", "#00FF99", "#00CCFF", "#FFFF00", "#FF00FF", "#FFFFFF"])
        
        self.rockets.append({
            "x": x, "y": self.height,
            "prev_x": x, "prev_y": self.height,
            "vy": vy,
            "color": color,
            "explode_y": random.randint(100, self.height // 2)
        })

    def update_physics(self):
        
        active_rockets = []
        for r in self.rockets:
            r["prev_x"], r["prev_y"] = r["x"], r["y"]
            r["y"] += r["vy"]
            r["vy"] += 0.25 
            
            if r["y"] <= r["explode_y"] or r["vy"] >= 0:
                self.create_explosion(r["x"], r["y"], r["color"])
            else:
                active_rockets.append(r)
        self.rockets = active_rockets

        
        active_particles = []
        for p in self.particles:
            p["prev_x"], p["prev_y"] = p["x"], p["y"]
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] *= p["drag"]
            p["vy"] *= p["drag"]
            p["vy"] += 0.15
            p["life"] -= 1
            
            
            if random.random() < 0.2 and p["life"] > 10:
                self.sparkles.append({
                    "x": p["x"], "y": p["y"],
                    "life": random.randint(5, 12),
                    "color": p["color"],
                    "vx": 0, "vy": 0.1
                })

            if p["life"] > 0: active_particles.append(p)
        self.particles = active_particles
        
        active_sparkles = []
        for s in self.sparkles:
            s["x"] += s["vx"]
            s["y"] += s["vy"]
            s["life"] -= 1
            if s["life"] > 0: active_sparkles.append(s)
        self.sparkles = active_sparkles[-150:]

    def animate(self):
        if not self.running: return
        
        self.canvas.delete("all")         
        for s in self.stars:
            if random.random() < 0.05: s["alpha"] = random.random()
            fill = safe_fade_color("#FFFFFF", s["alpha"])
            self.canvas.create_oval(s["x"], s["y"], s["x"]+s["size"], s["y"]+s["size"], fill=fill, outline="")

        if random.random() < 0.04: self.launch_rocket()
        
        self.update_physics()
      
        for p in self.particles:
            brightness = p["life"] / p["max_life"]
            color = safe_fade_color(p["color"], brightness)
            
            self.canvas.create_line(p["prev_x"], p["prev_y"], p["x"], p["y"], fill=color, width=3)
        
        for s in self.sparkles:
            self.canvas.create_rectangle(s["x"], s["y"], s["x"]+1, s["y"]+1, fill=s["color"], outline="")

        for r in self.rockets:
             self.canvas.create_line(r["prev_x"], r["prev_y"], r["x"], r["y"], fill="#DDDDDD", width=2)
   
        self.hue = (self.hue + 0.005) % 1.0
        r, g, b = colorsys.hsv_to_rgb(self.hue, 0.6, 1.0)
        text_color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        
        self.canvas.create_text(
            self.width // 2, self.height - 80,
            text="HAPPY NEW YEAR 2026",
            fill=text_color,
            font=("Verdana", 40, "bold"), 
            justify="center"
        )
        self.after(25, self.animate)

    def teardown(self):
        self.running = False