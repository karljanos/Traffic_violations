from kivy.app import App
#from kivy.uix.widget import Widget
from kivy.uix.label import Label
#from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import pyautogui
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty#, ObjectProperty
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
#import time
from kivy.clock import Clock
#import pyautogui
from kivy.graphics.vertex_instructions import Line
import matplotlib
#import matplotlib.pyplot as plt
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Ellipse

let_bun_array = np.load("./let_bun.npy")
kor_ora_array = np.load("./kor_ora.npy")
# Specify window size and place
Window.size = (1400,800)
Window.top = int( (pyautogui.size().height - Window.height) ) / 2
Window.left = int( (pyautogui.size().width  - Window.width) ) / 2


class KorOraWindow(Screen):        
    def reset_but(self):
        for i in self.children:
            for j in i.ids:
                if j == 'toggle_ko':
                    i.ids.toggle_ko.state = 'normal'
    info_layout = None

class LetBunWindow(Screen):
    def reset_but(self):
        for i in self.children:
            i.init_axes()
    info_layout = None
    
class CanvasFolytWindow(Screen):
    def reset_but(self):
        for i in self.children:
            for j in i.ids:
                if j == 'butt_f':
                    i.ids.butt_f.state = 'normal'
    info_layout = None        
            
class LetBun(GridLayout):
    def __init__(self, **kwargs):
        super(LetBun, self).__init__(**kwargs)
        self.cols = 1
        
        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(.95, .71, .54, 1)
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )
    
    let_bun_text = StringProperty()
    let_bun_text = ""
    
    
    arr_down = False
    is_arrested = 0    
    def valasztas_arr(self, button):
        if button == self.ids.arr:
            if button.state == "down":
                self.ids.narr.disabled = True
                self.is_arrested = 0
                self.arr_down = True
            else:
                self.ids.narr.disabled = False
                self.arr_down = False
        elif button == self.ids.narr:
            if button.state == "down":
                self.ids.arr.disabled = True
                self.is_arrested = 1
                self.arr_down = True
            else:
                self.ids.arr.disabled = False
                self.arr_down = False
        self.update_num_label()
                
    viol_down = False
    violation_type = 0
    def valasztas_viol(self, button):
        buttons = [self.ids.sp, self.ids.eq, self.ids.mo, self.ids.pl, self.ids.ot]
        if button == self.ids.sp:
            if button.state == "down":
                for i in buttons:
                    if i != button:
                        i.disabled = True
                self.violation_type = 0
                self.viol_down = True
            else:
                for  i in buttons:
                    if i != button:
                        i.disabled = False
                self.viol_down = False
        elif button == self.ids.eq:
            if button.state == "down":
                for i in buttons:
                    if i != button:
                        i.disabled = True
                self.violation_type = 1
                self.viol_down = True
            else:
                for  i in buttons:
                    if i != button:
                        i.disabled = False
                self.viol_down = False
        elif button == self.ids.mo:
            if button.state == "down":
                for i in buttons:
                    if i != button:
                        i.disabled = True
                self.violation_type = 2
                self.viol_down = True
            else:
                for  i in buttons:
                    if i != button:
                        i.disabled = False
                self.viol_down = False
        elif button == self.ids.pl:
            if button.state == "down":
                for i in buttons:
                    if i != button:
                        i.disabled = True
                self.violation_type = 3
                self.viol_down = True
            else:
                for  i in buttons:
                    if i != button:
                        i.disabled = False
                self.viol_down = False
        elif button == self.ids.ot:
            if button.state == "down":
                for i in buttons:
                    if i != button:
                        i.disabled = True
                self.violation_type = 4
                self.viol_down = True
            else:
                for  i in buttons:
                    if i != button:
                        i.disabled = False
                self.viol_down = False
        self.update_num_label()
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
       
    def month_calculator(self, szam):
        outp = ""
        yrr = 2005
        mnn = 10
        sy = 0
        sm = 0
        for i in range(szam):
            if mnn < 12:
                mnn += 1
            else:
                yrr += 1
                mnn = 1
        sy = yrr
        sm = mnn
        vissz = min(szam, 9)
        for i in range(vissz):
            if sm > 1:
                sm -= 1
            else:
                sy -= 1
                sm = 12
        outp = "%i/%i - %i/%i" %(sy,sm,yrr,mnn)
        return outp
      
    def on_slider_value(self, widget):
        self.ids.img_lb.source = "./let_bun/let_bun%s.png" % str(int(widget.value))
        self.update_num_label()
        x_lab = self.month_calculator(int(widget.value))   
        self.ids.mon.text = x_lab
    
    def windowchangecancel(self):
        if len(Clock.get_events()) == 4:
            self.mozi_interval.cancel()
            self.ids.butt_lb.state = "normal"
            self.speed = 1
        else:
            pass
    
    
    circles = InstructionGroup()
    lines = InstructionGroup()
    circles.add(Color(.75, .24, .09, 1))
    lines.add(Color(.75, .24, .09, 1))
    def update_num_label(self):
        self.points = []
        if self.viol_down and self.arr_down:
            canv = self.ids.graf
            self.circles.clear()
            self.lines.clear()
            honapp = int(self.ids.slid_lb.value)
            max_val = 0
            for i in range(72):
                if max_val < let_bun_array[i][self.is_arrested][self.violation_type]:
                    max_val = let_bun_array[i][self.is_arrested][self.violation_type]
            self.y_max = str(int(max_val))
            self.ids.max.text = str(int(max_val))
            self.ids.cas.text = "cases"
            for i in range(10):
                if honapp - i >= 0:
                    self.points.append(let_bun_array[honapp-i][self.is_arrested][self.violation_type])
                else:
                    break
            # 0.02 == 0 ; 0.9 == y_max
            # 0.98/ymax * current + 0.02
            j = 0.9
            currents = []
            js = [0.9]
            for i in self.points:
                current = 0.88/max_val * i + 0.02
                currents.append(current)
                self.circles.add(Ellipse(pos=(canv.width*j, canv.height*current), size=(10, 10)))
                if j <0.2:
                    j = 0.01
                else:
                    j -= 0.1
                js.append(j)
            for i in range(len(currents)-1,0,-1):
                self.lines.add(Line(points = [canv.width*js[i]+5, canv.height*currents[i]+5, canv.width*js[i-1]+5, canv.height*currents[i-1]+5], width = 1))
            canv.canvas.add(self.circles)
            canv.canvas.add(self.lines)
        else:
            pass
    
    disabled_buttons = []
    def infopanel(self, togbutt):
        scr = self.parent
        valasztos_butts = [self.ids.arr, self.ids.narr, self.ids.sp, self.ids.eq, self.ids.mo, self.ids.pl,self.ids.ot]
        if togbutt.state == "down":
            self.ids.butt_lb.state = "normal"
            self.ids.a_t_l.disabled = True
            self.ids.l_b_l.disabled = True
            self.ids.a_t_p_l.disabled = True
            self.ids.b_l.disabled = True
            self.ids.f_l.disabled = True
            self.ids.butt_lb.disabled = True
            self.ids.slid_lb.disabled = True
            scr.info_layout = FloatLayout(size_hint = (None,None), size = (self.width, self.height))
            with scr.info_layout.canvas.before:
                Color(0, 0, .0, 0.5)
                scr.info_layout.rect = Rectangle(
                    size=scr.info_layout.size,
                    pos=scr.info_layout.pos
                )
            for buton in valasztos_butts:
                if buton.disabled == True:
                    self.disabled_buttons.append(buton)
                else:
                    buton.background_disabled_normal = "toggle_button_enabled.png"
                    buton.background_disabled_down = "toggle_button_down.png"
                    buton.disabled = True
                buton.color = [.75, .24, .09, 1]
            self.ids.a_t_l.color = [.75, .24, .09, 1]
            self.ids.l_b_l.color = [1,1,1,1]
            self.ids.a_t_p_l.color = [.75, .24, .09, 1]
            age_time = Label(text = "A simple heatmap showing the number\nof cases of a given age at a given\ntime.\n ", font_size = 20, pos_hint={'x':-0.35, 'y':0.32}, font_name = "./trebuc.ttf")
            arr_viol = Label(text = "A heatmap showing the number\nof cases of arrested and not arrested\nsuspects for a given violation type,\nwith some additional features. ", font_size = 20, pos_hint = {'x':-0.05, 'y':0.32}, font_name = "./trebuc.ttf")
            age_time_pro = Label(text = "A heatmap showing the number\nof cases of a given age at a given\ntime, with additional features and\n\"on the fly\" computations.", font_size = 20, pos_hint = {'x':0.25, 'y':0.32}, font_name = "./trebuc.ttf")
            slider_inf = Label(text = "By moving the slider, the image switches to another month, starting with october of 2005, and ending with september of 2011.\nOne can enter in a slideshow mode, with adjustable speed.", font_size = "20", pos_hint = {'x':-0.085, 'y':-0.34}, font_name = "./trebuc.ttf")
            graf_inf = Label(text = "One can pick\na variable along\nboth axes, and\nthe corresponding\nvalues are displayed\non the graph retroactively\nfor nine months.", font_size = 20, pos_hint={'x':-0.12, 'y':0.02}, font_name = "./trebuc.ttf")
            scr.info_layout.add_widget(graf_inf)
            scr.info_layout.add_widget(age_time)
            scr.info_layout.add_widget(arr_viol)
            scr.info_layout.add_widget(age_time_pro)
            scr.info_layout.add_widget(slider_inf)
            scr.add_widget(scr.info_layout)
        else:
            scr.remove_widget(scr.info_layout)
            for buton in valasztos_butts:
                if buton not in self.disabled_buttons:
                    buton.disabled = False
                    buton.background_disabled_normal = "toggle_button_disabled.png"
                    buton.background_disabled_down = "toggle_button_disabled.png"
                buton.color = [.75, .24, .09, 1]
            self.ids.a_t_l.color = [.75, .24, .09, 1]
            self.ids.l_b_l.color = [.75, .24, .09, 1]
            self.ids.a_t_p_l.color = [.75, .24, .09, 1]
            self.ids.a_t_l.disabled = False
            self.ids.l_b_l.disabled = False
            self.ids.a_t_p_l.disabled = False
            self.ids.b_l.disabled = False
            self.ids.f_l.disabled = False
            self.ids.butt_lb.disabled = False
            self.ids.slid_lb.disabled = False    
    
    month = StringProperty()
    month = "2005/10 - 2005/10"
    drawn_points = []
    axes = [] 
    points = []
    def init_axes(self):
        with self.ids.graf.canvas.before:
            Color(.75, .24, .09, 1)
            #Color(147,56,4,1) #Not Working
            holder = self.ids.graf
            self.axes.append(Line(points = [holder.width*0.02, holder.height*0.01, holder.width*0.02, holder.height*0.99], width = 2)) #∟y
            self.axes.append(Line(points = [holder.width*0.01, holder.height*0.02, holder.width*0.99, holder.height*0.02], width = 2)) #○x TODO
            self.axes.append(Line(points = [holder.width*0.02, holder.height*0.99, holder.width*0.015, holder.height*0.98], width = 2)) #♥y balra nyil
            self.axes.append(Line(points = [holder.width*0.02, holder.height*0.99, holder.width*0.025, holder.height*0.98], width = 2)) # y jobbra nyil
            self.axes.append(Line(points = [holder.width*0.99, holder.height*0.02, holder.width*0.98, holder.height*0.01], width = 2)) # x le nyil
            self.axes.append(Line(points = [holder.width*0.99, holder.height*0.02, holder.width*0.98, holder.height*0.03], width = 2)) # x fel nyil
            self.axes.append(Line(points = [holder.width*0.01, holder.height*0.9+5, holder.width*0.03, holder.height*0.9+5], width = 2)) #↨ y max
            #self.axes.append(Line(points = [holder.width*0.9, holder.height*0.01, holder.width*0.9, holder.height*0.03])) # x max
    
    y_max = StringProperty()
    y_max = ""
    speed = 1
    def meret(self):
        #print(widget.size)
        print("ez a fgv")
        
    def forw_speed(self):
        if len(Clock.get_events()) == 4:
            if (self.speed + 1) == 5:
                pass
            else:
                self.speed = (self.speed + 1)
            self.mozi_interval.cancel()
            current = 1/self.speed
            self.mozi_interval = Clock.schedule_interval(self.mozi, current)
        else:
            pass 
    
    def back_speed(self):
        if len(Clock.get_events()) == 4:
            if (self.speed - 1)  == 0:
                pass
            else:
                self.speed = (self.speed - 1)
            self.mozi_interval.cancel()
            current = 1/self.speed
            self.mozi_interval = Clock.schedule_interval(self.mozi, current)
        else:
            pass
    
    def mozi(self, *args):
        self.ids.slid_lb.value = (self.ids.slid_lb.value + 1) % 72  
            
    def start_stop(self, buton):
        if buton.state == "down":
            self.mozi_interval = Clock.schedule_interval(self.mozi, (1/self.speed))
        else:
            self.mozi_interval.cancel()
            self.speed = 1
    
    def on_size(self, *args):
        pass             
            
class KorOra(GridLayout):
    def __init__(self, **kwargs):
        super(KorOra, self).__init__(**kwargs)
        self.cols = 1

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        with self.canvas.before:
            Color(.95, .71, .54, 1)
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    speed = 1
    def on_slider_value(self, widget):
        self.ids.img.source = "./kor_ora/kor_ora%s.png" % str(int(widget.value))
     
        
    def infopanel(self, togbutt):
        scr = self.parent
        if togbutt.state == "down":
            self.ids.toggle_ko.state = "normal"
            self.ids.a_t_k.disabled = True
            self.ids.l_b_k.disabled = True
            self.ids.a_t_p_k.disabled = True
            self.ids.b_k.disabled = True
            self.ids.f_k.disabled = True
            self.ids.toggle_ko.disabled = True
            self.ids.slid.disabled = True
            scr.info_layout = FloatLayout(size_hint = (None,None), size = (self.width, self.height))
            with scr.info_layout.canvas.before:
                Color(0, 0, .0, 0.5)
                scr.info_layout.rect = Rectangle(
                    size=scr.info_layout.size,
                    pos=scr.info_layout.pos
                )
            self.ids.a_t_k.color = [1,1,1,1]
            self.ids.l_b_k.color = [.75, .24, .09, 1]
            self.ids.a_t_p_k.color = [.75, .24, .09, 1]
            age_time = Label(text = "A simple heatmap showing the number\nof cases of a given age at a given\ntime.\n ", font_size = 20, pos_hint={'x':-0.35, 'y':0.32}, font_name = "./trebuc.ttf")
            arr_viol = Label(text = "A heatmap showing the number\nof cases of arrested and not arrested\nsuspects for a given violation type,\nwith some additional features. ", font_size = 20, pos_hint = {'x':-0.05, 'y':0.32}, font_name = "./trebuc.ttf")
            age_time_pro = Label(text = "A heatmap showing the number\nof cases of a given age at a given\ntime, with additional features and\n\"on the fly\" computations.", font_size = 20, pos_hint = {'x':0.25, 'y':0.32}, font_name = "./trebuc.ttf")
            slider_inf = Label(text = "By moving the slider, the image switches to another month, starting with october of 2005, and ending with september of 2011.\nOne can enter in a slideshow mode, with adjustable speed.", font_size = "20", pos_hint = {'x':-0.085, 'y':-0.34}, font_name = "./trebuc.ttf")
            scr.info_layout.add_widget(age_time)
            scr.info_layout.add_widget(arr_viol)
            scr.info_layout.add_widget(age_time_pro)
            scr.info_layout.add_widget(slider_inf)
            scr.add_widget(scr.info_layout)
        else:
            scr.remove_widget(scr.info_layout)
            self.ids.a_t_k.color = [.75, .24, .09, 1]
            self.ids.l_b_k.color = [.75, .24, .09, 1]
            self.ids.a_t_p_k.color = [.75, .24, .09, 1]
            self.ids.a_t_k.disabled = False
            self.ids.l_b_k.disabled = False
            self.ids.a_t_p_k.disabled = False
            self.ids.b_k.disabled = False
            self.ids.f_k.disabled = False
            self.ids.toggle_ko.disabled = False
            self.ids.slid.disabled = False
            
    def meret(self, widget):
        print(widget.size)
    
    def mozi(self, *args):
        self.ids.slid.value = (self.ids.slid.value + 1) % 72  
    
    def forw_speed(self):
        if len(Clock.get_events()) == 4:
            if (self.speed + 1) == 5:
                pass
            else:
                self.speed = (self.speed + 1)
            self.mozi_interval.cancel()
            current = 1/self.speed
            self.mozi_interval = Clock.schedule_interval(self.mozi, current)
        else:
            pass 
    
    def back_speed(self):
        if len(Clock.get_events()) == 4:
            if (self.speed - 1)  == 0:
                pass
            else:
                self.speed = (self.speed - 1)
            self.mozi_interval.cancel()
            current = 1/self.speed
            self.mozi_interval = Clock.schedule_interval(self.mozi, current)
        else:
            pass
    
    def windowchangecancel(self):
        if len(Clock.get_events()) == 4:
            self.mozi_interval.cancel()
            self.ids.toggle_ko.state = "normal"
            self.speed = 1
        else:
            pass
        
    def start_stop(self, buton):
        if buton.state == "down":    
            self.mozi_interval = Clock.schedule_interval(self.mozi, (1/self.speed))
            print(len(Clock.get_events()))
        else:
            self.mozi_interval.cancel()
            self.speed = 1
            print(Clock.get_events())
  
class Folyt(GridLayout):
    def __init__(self, **kwargs):
        super(Folyt, self).__init__(**kwargs)
        self.cols = 1

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )
        
        with self.canvas.before:
            Color(.95, .71, .54, 1)
            self.rect = Rectangle(
                size=self.size,
                pos=self.pos
            )           
       
    def on_start(self, *args):
        print(self.ids.vaszon.size)
        self.update_rectangles()
        self.update_lines()
       
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
  
    def infopanel(self, togbutt):
        scr = self.parent
        if togbutt.state == "down":
            self.ids.butt_f.state = "normal"
            self.ids.a_t_f.disabled = True
            self.ids.l_b_f.disabled = True
            self.ids.a_t_p_f.disabled = True
            self.ids.b_f.disabled = True
            self.ids.f_f.disabled = True
            self.ids.butt_f.disabled = True
            self.ids.slid_f.disabled = True
            self.ids.fel.disabled = True
            self.ids.le.disabled = True
            scr.info_layout = FloatLayout(size_hint = (None,None), size = (self.width, self.height))
            with scr.info_layout.canvas.before:
                Color(0, 0, .0, 0.5)
                scr.info_layout.rect = Rectangle(
                    size=scr.info_layout.size,
                    pos=scr.info_layout.pos
                )
            self.ids.a_t_f.color = [.75, .24, .09, 1]
            self.ids.l_b_f.color = [.75, .24, .09, 1]
            self.ids.a_t_p_f.color = [1,1,1,1]
            age_time = Label(text = "A simple heatmap showing the number\nof cases of a given age at a given\ntime.\n ", font_size = 20, pos_hint={'x':-0.35, 'y':0.32}, font_name = "./trebuc.ttf")
            arr_viol = Label(text = "A heatmap showing the number\nof cases of arrested and not arrested\nsuspects for a given violation type,\nwith some additional features. ", font_size = 20, pos_hint = {'x':-0.05, 'y':0.32}, font_name = "./trebuc.ttf")
            age_time_pro = Label(text = "A heatmap showing the number\nof cases of a given age at a given\ntime, with additional features and\n\"on the fly\" computations.", font_size = 20, pos_hint = {'x':0.25, 'y':0.32}, font_name = "./trebuc.ttf")
            slider_inf = Label(text = "By moving the slider, the image switches to another month, starting with october of 2005, and ending with september of 2011.\nOne can enter in a slideshow mode, with adjustable speed.", font_size = "20", pos_hint = {'x':-0.085, 'y':-0.34}, font_name = "./trebuc.ttf")
            inter_inf = Label(text = "One can set the\ndistance, to take\ninto account the\nvalues of adjecent\ncells, compute and\ndisplay the average\nof those.",font_size = "20", pos_hint = {'x':-0.28, 'y':0.03}, font_name = "./trebuc.ttf")
            scr.info_layout.add_widget(inter_inf)
            scr.info_layout.add_widget(age_time)
            scr.info_layout.add_widget(arr_viol)
            scr.info_layout.add_widget(age_time_pro)
            scr.info_layout.add_widget(slider_inf)
            scr.add_widget(scr.info_layout)
        else:
            scr.remove_widget(scr.info_layout)
            self.ids.a_t_f.color = [.75, .24, .09, 1]
            self.ids.l_b_f.color = [.75, .24, .09, 1]
            self.ids.a_t_p_f.color = [.75, .24, .09, 1]
            self.ids.a_t_f.disabled = False
            self.ids.l_b_f.disabled = False
            self.ids.a_t_p_f.disabled = False
            self.ids.b_f.disabled = False
            self.ids.f_f.disabled = False
            self.ids.butt_f.disabled = False
            self.ids.slid_f.disabled = False  
            self.ids.fel.disabled = False
            self.ids.le.disabled = False
  
    def windowchangecancel(self):
        if len(Clock.get_events()) == 4:
            self.mozi_interval.cancel()
            self.speed = 1
            self.ids.butt_f.state = "normal"
        else:
            pass    

    v_l = 23
    h_l = 3
    v_space = 0.0416666
    h_space = 0.25                
    lines = InstructionGroup()
    def update_lines(self):
        self.lines.clear()
        canv = self.ids.vaszon
        central_line_x = int(self.ids.vaszon.width/2)
        v_spacing = self.v_space * self.ids.vaszon.width
        v_offset = -int(self.v_l/2)
        for i in range(self.v_l):
            line_x = central_line_x + v_offset*v_spacing
            self.lines.add(Color(1,1,1,1))
            self.lines.add(Line(points = [line_x, 0, line_x, self.ids.vaszon.height]))
            v_offset += 1
        central_line_y = int(self.ids.vaszon.height/2)
        h_spacing = self.h_space*self.ids.vaszon.height
        h_offset = -int(self.h_l/2)
        for j in range(self.h_l):
            line_y = central_line_y + h_offset*h_spacing
            self.lines.add(Color(1,1,1,1))
            self.lines.add(Line(points = [0, line_y, self.ids.vaszon.width, line_y]))
            h_offset += 1            
        canv.canvas.add(self.lines)
    
    rectangles = InstructionGroup()                   
    my_map = matplotlib.cm.get_cmap("magma_r")
    norm = matplotlib.colors.Normalize(0, 40)
    def update_rectangles(self):
        self.rectangles.clear()
        tavolsag = self.inter_dist 
        canv = self.ids.vaszon
        honap =  int(self.ids.slid_f.value)
        for v in range(self.v_l + 1): # ora
            for h in range(self.h_l + 1): # kor
                indulo = self.avg_hours(tavolsag,v,h,honap)
                normed_szam = self.norm(indulo)
                szin = self.my_map(normed_szam)
                self.rectangles.add(Color(rgba = szin))
                self.rectangles.add(Rectangle(pos = (0+v*self.ids.vaszon.width*self.v_space, 0 + h*self.ids.vaszon.height*self.h_space), size = (self.ids.vaszon.width*self.v_space, self.ids.vaszon.height*self.h_space)))
        canv.canvas.add(self.rectangles)
        
    def inter_plus(self):
        if self.inter_dist < 24:
            self.inter_dist += 1
            self.ids.tav_d.text = str(self.inter_dist)
            self.update_rectangles()
            self.update_lines()
        else:
            pass
    def inter_minus(self):
        if self.inter_dist > 0:
            self.inter_dist -= 1
            self.ids.tav_d.text = str(self.inter_dist)
            self.update_rectangles()
            self.update_lines()
        else:
            pass
        
    inter_dist = 0
    def avg_hours(self, tavolsag, ora, kor, honap):
        if tavolsag != 0:
            oszto = 2*tavolsag + 1
            #for i in range(1,tavolsag+1):   
            #    oszto += 2*i
            output = kor_ora_array[honap][3-kor][ora]
            if honap not in [0, 71]:
                for i in range(1, tavolsag+1):
                    if ora - i < 0:
                        output += kor_ora_array[honap-1][3-kor][24 + ora - i] #*(tavolsag+1-i)
                    else:
                        output += kor_ora_array[honap][3-kor][ora - i]
                    if ora + i > 23:
                        output += kor_ora_array[honap+1][3-kor][ora + i - 24]
                    else:
                        output += kor_ora_array[honap][3-kor][ora + i]
            elif honap == 0:
                for i in range(1, tavolsag+1):
                    if ora - i < 0:
                        pass
                    else:
                        output += kor_ora_array[honap][3-kor][ora - i]
                    if ora + i > 23:
                        output += kor_ora_array[honap+1][3-kor][ora + i - 24]
                    else:
                        output += kor_ora_array[honap][3-kor][ora + i]    
            elif honap == 71:
                for i in range(1, tavolsag+1):
                    if ora - i < 0:
                        output += kor_ora_array[honap-1][3-kor][24 + ora - i]
                    else:
                        output += kor_ora_array[honap][3-kor][ora - i]
                    if ora + i > 23:
                        pass
                    else:
                        output += kor_ora_array[honap][3-kor][ora + i]
                
            output = output/oszto
            return output
        else:
            output = kor_ora_array[honap][3-kor][ora]
            return output
    speed = 1
    def mozi(self, *args):
        self.ids.slid_f.value = (self.ids.slid_f.value + 1) % 72
    
    def start_stop(self, buton):
        if buton.state == "down":           
            self.mozi_interval = Clock.schedule_interval(self.mozi, (1/self.speed))
            print(len(Clock.get_events()))
        else:
            self.mozi_interval.cancel()
            self.speed = 1
            print(Clock.get_events())
    
    def forw_speed(self):
        if len(Clock.get_events()) == 4:
            if (self.speed + 1) == 5:
                pass
            else:
                self.speed = (self.speed + 1)
            self.mozi_interval.cancel()
            current = 1/self.speed
            self.mozi_interval = Clock.schedule_interval(self.mozi, current)
        else:
            pass 
    
    def back_speed(self):
        if len(Clock.get_events()) == 4:
            if (self.speed - 1)  == 0:
                pass
            else:
                self.speed = (self.speed - 1)
            self.mozi_interval.cancel()
            current = 1/self.speed
            self.mozi_interval = Clock.schedule_interval(self.mozi, current)
        else:
            pass 
    
    def on_size(self, *args):
        self.update_rectangles()
        self.update_lines()
        
    def on_slider_value_f(self):
        self.update_rectangles()
        self.update_lines()        
        
    def check_size(self, widget):
        print(widget.size)

        
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("adatviz.kv")
class AdatvizApp(App):    
    def build(self):
        self.title = "Traffic violations"
        self.icon = "./kam.ico"
        return kv

if __name__ == "__main__":
    AdatvizApp().run()