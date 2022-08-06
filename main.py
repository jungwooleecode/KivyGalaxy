from platform import platform
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.core.window import Window
from kivy import platform

class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective

    perspective_point_x= NumericProperty(0)
    perspective_point_y= NumericProperty(0)

    V_NB_LINES=10
    V_LINES_SPACING= 0.22 #percentage in screen length
    vertical_lines=[]

    H_NB_LINES=15
    H_LINES_SPACING= 0.1 #percentage in screen length
    horizontal_lines=[]

    SPEED=4
    SPEED_X=12

    current_speed_x=0

    current_offset_y=0
    current_offset_x=0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'windows', 'macosx'):
            return True

        return False

    def on_parent(self, widget, parent):
        pass
    
    def on_size(self, *args):
        pass

    def on_perspective_point_x(self, widget, value):
        pass

    def on_perspective_point_y(self, widget, value):
        pass

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            # self.line=Line(points=[100,0,100,100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x=int(self.width/2)
        offset= -int(self.V_NB_LINES/2)+0.5
        spacing= self.V_LINES_SPACING*self.width

        for i in range(0, self.V_NB_LINES):
            line_x= central_line_x + offset*spacing + self.current_offset_x

            x1, y1= self.transform(line_x, 0)
            x2, y2= self.transform(line_x, self.height)
            self.vertical_lines[i].points=[x1, y1, x2, y2]
            offset +=1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            # self.line=Line(points=[100,0,100,100])
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        central_line_x=int(self.width/2)
        offset= -int(self.V_NB_LINES/2)+0.5
        spacing= self.V_LINES_SPACING*self.width
        
        xmin= central_line_x + offset*spacing + self.current_offset_x
        xmax= central_line_x - offset*spacing + self.current_offset_x

        spacing_y=self.H_LINES_SPACING*self.height

        for i in range(0, self.H_NB_LINES):

            line_y= 0 +i*spacing_y- self.current_offset_y
            x1, y1= self.transform( xmin, line_y)
            x2, y2= self.transform( xmax, line_y)
            self.horizontal_lines[i].points=[x1, y1, x2, y2]

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x= self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x= -self.SPEED_X
        
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x=0
        return True
    
    def on_touch_down(self, touch):
        if touch.x <self.width/2:
           # print("<-")
            self.current_speed_x= self.SPEED_X
        else:
           # print("->")
            self.current_speed_x= -self.SPEED_X

    def on_touch_up(self, touch):
        print("UP")    
        self.current_speed_x=0
    
    def update(self, dt):

        time_factor = dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()

        self.current_offset_y += self.SPEED*time_factor

        spacing_y=self.H_LINES_SPACING*self.height

        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        self.current_offset_x += self.current_speed_x *time_factor

class GalaxyApp(App):
    pass

GalaxyApp().run()