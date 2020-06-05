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
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

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
    '''Root Class'''
    # property of traffic light counter
    connect = BooleanProperty(False)
    state = StringProperty('')
    timeleft = NumericProperty(0)

    def nav(self):
        # self.root.ids.navbox.pos_hint = {'right':1}
        # print(self.root.children[0].ids)
        self.root.children[0].ids.nav.toggle_state()

    def add_counter(self,dt):
        self.root.children[0].ids.mainpanel.add_widget(self.wid,index=1)
    
    def remove_counter(self, dt):
        self.root.children[0].ids.mainpanel.remove_widget(self.wid)

    def on_state(self, state):
        # not yet complete
        if self.connect == True:
            if state == 'red':
                self.wid.color = (1,0,0,1)
            else:
                self.wid.color = (0,1,0,1)

    def on_timeleft(self, event):
        '''handle the time left of the traffic light'''
        if self.connect = True:
            self.wid.text = timeleft

    def on_connect(self, obj, value):
        '''check if nodemcu is connected, and toggle Counter widget'''
        if self.connect is True:
            animation = Animation(font_size =40, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.add_counter,.5)
        else:
            animation = Animation(font_size =90, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.remove_counter,.5)
        animation.start(self.root.children[0].ids.time)

    def decrement_counter(self,dt):
        if self.connect == True:
            if self.timeleft > 0:
                self.timeleft -= 1
            else:
                try:
                    Clock.unschedule(self.timer)
                except:
                    print('the timer event does not exist!')
        
    def update_time(self, nap):
        '''update clock current time'''
        now = datetime.now() # get current time as datetime object
        self.root.children[0].ids.time.text = now.strftime('%H:%M:%S')

    def serial_read(self,dt):
        '''connection, state and time change is handled here'''
        res = self.ser.read().decode()

        # TL not connected & counter is rendered
        if res == 'n' and self.connect == True:
            self.connect = not self.connect # True
        else: # connected
            if self.connect == False: # not showing
                self.connect = not self.connect # add widget
            # handle state and trigger on_state
            if res == 'r':
                self.state = 'red'
            elif res == 'g':
                self.state = 'green'
            elif res == 'y':
                self.state = 'yellow'
            elif res == 's':
                self.state = 'standby'
            else:
                pass

        # check time left
        if self.timeleft == 0:
            if res == 'r':
                self.timeleft = 10
            elif res == 'g':
                self.timeleft = 10
            elif res == 'y':
                self.timeleft = 3
            self.timer = Clock.schedule_interval(self.decrement_counter, 1)

    def on_start(self):
        # init Counter object
        self.wid = Counter()
        try:    
            self.ser = serial.Serial(baudrate=115200,port='/dev/ttyUSB0')
        except SerialException:
            print('the port is not exist. exiting...')
            exit(-1)
        if self.ser.is_open == False:
            self.ser.open()
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.serial_read, 1)
    

if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular = 'font/Roboto-Thin.ttf',
        fn_bold = 'font/Roboto-Medium.ttf')
    # Window.clearcolor = get_color_from_hex('#808080')
    DashApp().run()