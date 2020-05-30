from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.animation import Animation

import serial
from datetime import datetime


class Navigator(NavigationDrawer):
    pass

class Counter(Label):
    id = 'count'
    text = 'Counter'
    font_size = 90

class MainScreen(Screen):
    pass

class NavScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class DashApp(App):
    # navdrawer = NavigationDrawer()
    # navdrawer.anim_type = 'slide_above_anim'
    # navdrawer.add_widget(BoxLayout())

    def nav(self):
        # self.root.ids.navbox.pos_hint = {'right':1}
        # print(self.root.children[0].ids)
        self.root.children[0].ids.nav.toggle_state()

    def add_counter(self,dt):
        self.root.children[0].ids.mainpanel.add_widget(self.wid,index=1)
    
    def remove_counter(self, dt):
        self.root.children[0].ids.mainpanel.remove_widget(self.wid)

    def counter(self):
        if self.state is True:
            animation = Animation(font_size =40, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.add_counter,.5)
        else:
            animation = Animation(font_size =90, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.remove_counter,.5)
        animation.start(self.root.children[0].ids.time)
        self.state = not self.state
    
    def update_time(self, nap):
        now = datetime.now() # get current time as datetime object
        self.root.children[0].ids.time.text = now.strftime('%H:%M:%S')

    def serial_read(self): # not yet complete
        res = self.ser.read().decode()
        # check res format
        if res == 'r':
            state = 'red'
        elif res == 'g':
            state = 'green'
        return state

    def on_start(self):
        #init
        self.state = True
        self.wid = Counter()
        try:    
            self.ser = serial.Serial(baudrate=115200,port='eth0')
        except SerialException:
            print('the port is not exist. exiting...')
            exit(-1)
        if self.ser.is_open() == False:
            self.ser.open()
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.serial_read, 1)
    

if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular = 'font/Roboto-Thin.ttf',
        fn_bold = 'font/Roboto-Medium.ttf')
    # Window.clearcolor = get_color_from_hex('#808080')
    DashApp().run()