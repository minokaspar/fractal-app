from turtle import *
import math
ht()
bgcolor("lightblue")
tracer(0)
colormode(255)
FRACTAL_BUTTON_CENTERS = [[-140, 75], [140, 75], [-140, -10], [140, -10], [-140, -95], [140, -95], [-140, -180], [140, -180]] # [[x1, y1], [x2, y2], ... ]
FRACTAL_BUTTON_SIZE = [130, 30] # [width/2, height/2]
EXIT_BUTTON_SIZE = [90, 30] # [width/2, height/2]
COLORS = ["black", "purple", "green", "pink", "blue", "red", "brown"]
execution_mode = "home"
writing_color_index = 0

class Fractal:
    def __init__(self, index, frac_names = ["fractal", "good fractal"], max_depth = 5, start_pos_h = ((0, 0), 0), par_usage = False, parameter = 0, par_range = [], par_interval = 0, par_modulo = None, par_name = "unclassed parameter"):
        self.index = index
        "Int: Key to press to choose, and at which place the button is displayed"
        self.frac_short_name, self.frac_full_name = frac_names
        "Str: short name is displayed on button, full name on fractal screen when fractal selected"
        self.max_depth = max_depth
        "Int: max_depth"
        self.start_pos_h = start_pos_h
        "Iterable: [[x, y], heading]: t.goto/t.seth before drawing the fractal"
        self.par_usage = par_usage
        "Bool: wether the optional parameter is used or not"
        self.depth = 0
        "Int: current recursion depth"
        if par_usage:
            self.parameter = parameter
            "Int: optional parameter for fractals, this can represent aything, for example an angle. THis is steered with K_Left/K_Right"
            self.par_default = parameter
            "Int: default parameter value parameter is set to in self.get_chosen()"
            self.par_range = par_range
            "Iterable: [min, max]: maximal and minimal parameter values | bool(self.par_range) == False if unlimited (self.par_range == [])"
            self.par_interval = par_interval
            "Int: how much the parameter changes per keypress"
            self.par_modulo = par_modulo
            "Int: if self.par_modulo: self.parameter=self.parameter%self.par_modulo"
            self.par_name = par_name
            "Str: how the parameter is displayed"
    
    def keypress(self, key):
        "reaction on keypress"
        global writing_color_index, current_obj
        if execution_mode == "fractal":   # if not drawing atm
            old_state = (self.depth, self.parameter if self.par_usage else None, writing_color_index, current_obj) # jetztigen status speichern
            up_down = (key == "Up") - (key == "Down")
            left_right = (key == "Left") - (key == "Right")
            if up_down:
                self.depth = max(0, min(self.depth+up_down, self.max_depth))
            elif self.depth > 0 and left_right and self.par_usage:
                if self.par_range:
                    self.parameter = max(self.par_range[0], min(self.parameter-left_right*self.par_interval, self.par_range[1]))
                else:
                    self.parameter += left_right*self.par_interval
                if self.par_modulo: self.parameter = self.parameter%self.par_modulo
            
            elif key == "Escape":
                current_obj = home_obj
            
            elif key == "c":
                writing_color_index = (writing_color_index+1)%len(COLORS)
            
            if old_state != (self.depth, self.parameter if self.par_usage else None, writing_color_index, current_obj): # nur bei änderung zeichnen
                current_obj.draw()
    
    def draw(self):
        global execution_mode
        width=window_width()//2
        height=window_height()//2
        pensize(1)
        pu()
        pencolor(COLORS[writing_color_index])
        execution_mode="drawing"
        goto(-width+22, -height+22)
        write("drawing...", align = "left", font = ("Consolas", 20, "italic"))
        update()
        clear()
        goto(self.start_pos_h[0])
        seth(self.start_pos_h[1])
        pd()
        self._draw()
        pensize(1)
        pu()
        pencolor(COLORS[writing_color_index])
        goto(width-22, height-55)
        write(f"{self.frac_full_name}", align = "right", font = ("Consolas", 30, "bold"))
        goto(width-22, height-88)
        write(f'{"↑" if self.depth<self.max_depth else ""}/{"↓" if self.depth else " "}: recursion depth: {self.depth}', align = "right", font = ("Consolas", 20, "normal"))
        w, h=EXIT_BUTTON_SIZE
        draw_rectangle(-width+22+w, height-h-22, w, h, "Esc: HOME")
        if self.par_usage:
            goto(width-22, -height+22)
            pfeil_links_str = "←" if not self.par_range or self.parameter > self.par_range[0]  else ""
            pfeil_rechts_str = "→" if not self.par_range or self.parameter < self.par_range[1] else " "
            par_str_length = int(len(str(self.par_range[1] if self.par_range else self.par_modulo)) + len(str(self.par_interval))) # diese Formel macht dass self.parameter immer gleich viel platz braucht
            write(((pfeil_links_str + "/" + pfeil_rechts_str + ": ") if self.depth else " ") + # pfeile nur wenn möglich
                f"{self.par_name}: {self.parameter:{par_str_length}}", 
                  align = "right", font = ("Consolas", 20, "normal"))            
        
        update()
        execution_mode="fractal"
    
    def get_chosen(self):
        global current_obj
        self.depth = 0
        if self.par_usage: self.parameter = self.par_default
        current_obj = self
        self.draw()
    
    def get_clicked_try(self, mx, my):
        w, h = FRACTAL_BUTTON_SIZE
        bx, by = FRACTAL_BUTTON_CENTERS[self.index-1]
        if bx-w < mx < bx+w and by-h < my < by+h: self.get_chosen()
    
    def mouseclick(self, mx, my):
        w, h = EXIT_BUTTON_SIZE
        bx, by = -window_width()//2+22+w, window_height()//2-h-22
        if bx-w < mx < bx+w and by-h < my < by+h: home_obj.get_chosen()
    
    def draw_button(self):
        "draw its button on the home screen"
        w, h = FRACTAL_BUTTON_SIZE
        x, y = FRACTAL_BUTTON_CENTERS[self.index-1]
        draw_rectangle(x, y, w, h, label = f"{self.index}: {self.frac_short_name}")

class Pythagoras(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Pythagoras", "Pythagoras Baum"], 9, ((-50, -230), 0), True, 50, [], 2.5, 360, "Winkel αλφα")
    
    def _draw(self):
        self.angle = self.parameter
        self.colors = [(255, 0, 0)] if self.depth == 0 else [(x*255//self.depth, 0, 255 - x*255//self.depth) for x in range(self.depth+1)] # Gradient from red to blue
        self.coeffs = [round(math.sin(math.radians(self.angle)), 4), round(math.sin(math.radians(90 - self.angle)), 4)] # Quelle von sin und so: Internet
        pd()
        self.pythagobaum(self.depth, 90)
    
    def pythagobaum(self, depth, size):
        fillcolor(self.colors[depth])
        begin_fill()
        for _ in range(4):
            forward(size)
            left(90)
        end_fill()
        if depth > 0:
            left(90)
            forward(size)
            right(self.angle)
            self.pythagobaum(depth - 1, size * self.coeffs[0])
            forward(size * self.coeffs[0])
            right(90)
            self.pythagobaum(depth - 1, size * self.coeffs[1])
            # return to start:
            forward(size * self.coeffs[1])
            right(90 - self.angle)
            forward(size)
            left(90)
            back(size)

class Farn(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Farn", "Farn"], 4, ((0, -275), 90), True, 2, [-40, 40], 0.25, None, "Neigungswinkel")
    
    def _draw(self):
        self.tilt_angle = abs(self.parameter)
        self.twigs_no = 5
        self.size_reduction = 9/10
        self.farn(self.depth, 280, side = 1 if self.parameter > 0 else -1)
    
    def farn(self, depth, size, side = 1):
        color("green")
        if depth == 0:
            fd(size)
            back(size)
        else:
            for _ in range(self.twigs_no):
                forward(size/self.twigs_no)
                left(60)
                self.farn(depth - 1, size/3)
                right(60+side*self.tilt_angle)
                size *= self.size_reduction
                forward(size/self.twigs_no)
                right(60)
                self.farn(depth - 1, size/3, side = -1)
                left(60-side*self.tilt_angle)
                size *= self.size_reduction
            self.farn(depth - 1, size, side)
            if depth > self.depth - 2: # make the stems
                color("brown")         # brown
            for _ in range(2*self.twigs_no):
                left(side*self.tilt_angle)
                size *= 1/self.size_reduction
                back(size/self.twigs_no)

class Baum(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Baum", "Baum"], 12, ((0, -250), 90), True, 20, [], 2.5, 360, "Winkel")
    
    def _draw(self):
        self.angle = self.parameter
        self.baum(self.depth, 400)
    
    def baum(self, depth, size):
        pensize((depth+2)/2)
        if depth == 0:
            forward(size)
            back(size)
        else:
            forward(size/2)
            left(self.angle)
            self.baum(depth-1, size*0.6)
            right(2*self.angle)
            self.baum(depth-1, size*0.6)
            left(self.angle)
            back(size/2)

class Sierpinsky(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Sierpinsky", "Sierpinsky Polygon"], 5, ((0, 0), 0), True, 3, [3, 8], 1, None, "Anzahl Ecken")
    
    def _draw(self):
        self.nodes = self.parameter
        self.coeffs = {3:3-1, 4:4-1.75, 5:5-2.38, 6:6-3, 7:7-3.75, 8:8-4.59}
        pu()
        goto(-310+(40-self.coeffs[self.nodes]**1.8) * self.nodes, -200)
        pd()
        self.sierpinski(self.depth, 1200/self.nodes)
    
    def sierpinski(self, depth, size):
        if depth == 0:
            for _ in range(self.nodes):
                forward(size)
                left(360/self.nodes)
        else:
            for _ in range(self.nodes):
                self.sierpinski(depth - 1, size/self.coeffs[self.nodes])
                forward(size)
                left(360/self.nodes)

class Koch(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Koch", "Koch Stern"], 7, ((-250, 120), 0))
    
    def _draw(self):
        for _ in range(3):
            self.koch(self.depth, 500)
            right(120)
    
    def koch(self, depth, size):
        if depth == 0:
            forward(size)
        else:
            self.koch(depth-1, size/3)
            left(60)
            self.koch(depth-1, size/3)
            right(120)
            self.koch(depth-1, size/3)
            left(60)
            self.koch(depth-1, size/3)

class Levy(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Levy", "Lévy Kurve"], 15, ((-150, -130), 0))
    
    def _draw(self):
        self.levy(self.depth, 290)
    
    def levy(self, depth, length):
        if depth == 0:
            forward(length)
        else:
            left(45)
            self.levy(depth - 1, length/1.41)
            right(90)
            self.levy(depth - 1, length/1.41)
            left(45)

class Blitz(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Blitz", "Blitz Kurve"], 9, ((0, -270), 90), True, 70, [45, 135], 1, 360, "Winkel")
    
    def _draw(self):
        self.schenkel = 1/2/math.sin(math.radians(self.parameter)) # berechnet die Länge der beiden anderen Linien, Quelle: Internet
        self.basis = 1/math.tan(math.radians(self.parameter)) # berechnet die Länge der mittleren horizontalen Linie, Quelle: Internet
        self.blitz(self.depth, 500)
    
    def blitz(self, depth, size):
        if depth == 0:
            fd(size)
        else:
            rt(90-self.parameter)
            self.blitz(depth-1, size*self.schenkel)
            lt(180-self.parameter)
            self.blitz(depth-1, size*self.basis)
            rt(180-self.parameter)
            self.blitz(depth-1, size*self.schenkel)
            lt(90-self.parameter)

class Dragon(Fractal):
    def __init__(self, index):
        super().__init__(index, ["Drachenkurve", "Drachenkurve"], 15, ((0, -30), 0), True, 90, [], 2, 360, "Winkel")
    
    def _draw(self):
        self.dragoncurve(self.depth, 220, 1)
    
    def dragoncurve(self, depth, size, direction):
        if depth == 0:
            forward(size)
        else:
            self.dragoncurve(depth - 1, size/1.41, 1)
            right(self.parameter * direction)
            self.dragoncurve(depth - 1, size/1.41, -1)

def draw_rectangle(x, y, w, h, label = ""): # x: x center, y: y center, w: width/2, h: height/2, label: optional label
    """ draw_rectangle(x: x center, y: y center, w: width/2, h: height/2, label: optional label) """
    pensize(3)
    color(COLORS[writing_color_index], "gray85")
    pu()
    goto(x-w, y-h)
    pd()
    begin_fill()
    goto(x+w, y-h)
    goto(x+w, y+h)
    goto(x-w, y+h)
    goto(x-w, y-h)
    end_fill()
    pu()
    goto(x, y-15)
    write(label, align = "center", font = ("Consolas", 20, "bold"))

class Home:
    def draw(self):
        "draw homescreen"
        global execution_mode
        """ create menu with title and buttons """
        clear()
        penup()
        pencolor(COLORS[writing_color_index])
        goto(0, 150)
        write("Informatik Projekt Fraktale", align = "center", font = ("Consolas", 20, "bold"))
        pensize(3)
        w, h = EXIT_BUTTON_SIZE
        width = window_width()//2
        height = window_height()//2
        draw_rectangle(-width+22+w, height-h-22, w, h, "Esc: EXIT")
        for frac in frac_objs:
            frac.draw_button()
        update()
        execution_mode = "home"
    
    def keypress(self, key):
        if isinstance(key, int) and 0 <= int(key) <= len(frac_objs):
            frac_objs[int(key-1)].get_chosen()
        elif key == "Escape":
            exit("Schönen Tag noch!")
        elif key == "c":
            global writing_color_index
            writing_color_index = (writing_color_index+1)%len(COLORS)
            current_obj.draw()
    
    def mouseclick(self, mx, my):
        for frac in frac_objs:frac.get_clicked_try(mx, my)
        w, h = EXIT_BUTTON_SIZE
        bx, by = -window_width()//2+22+w, window_height()//2-h-22
        if bx-w < mx < bx+w and by-h < my < by+h:
            exit("Schönen Tag noch!")
    
    def get_chosen(self):
        global current_obj
        current_obj=self
        self.draw()

def click(x, y):
    current_obj.mouseclick(x, y)

home_obj = Home()
frac_objs = [Koch(1), Farn(2), Levy(3), Baum(4), Sierpinsky(5), Pythagoras(6), Dragon(7), Blitz(8)]
current_obj = home_obj
current_obj.draw()

onscreenclick(click, 1)
def key(k): return current_obj.keypress(k)
for k in list(range(1, len(frac_objs) + 1)) + ["Up", "Down", "Escape", "Left", "Right", "c"]:
    onkeypress(lambda x=k: key(x), k) # bind each key to the "key" function, with a different argument
    # lambda x=k: freezes the current value of k (so each key does a different thing)
listen()
done()
