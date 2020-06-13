from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty, StringProperty

import serial
from datetime import datetime


class Navigator(NavigationDrawer):
    pass

class Counter(Label):
    pass

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

    def sleep(self):
        self.nav()
        Clock.unschedule(self.curr_time)
        self.root.current = 'second'

    def wake(self):
        self.root.current = 'main'
        self.curr_time = Clock.schedule_interval(self.update_time, 1)
        

    def add_counter(self,dt):
        self.root.children[0].ids.mainpanel.add_widget(self.wid,index=1)
    
    def remove_counter(self, dt):
        self.root.children[0].ids.mainpanel.remove_widget(self.wid)

    def on_state(self, obj, state):
        if self.connect == True:
            if state == 'red':
                self.wid.color = (1,0,0,1)
            if state == 'yellow':
                self.wid.color = (1,1,0,1)
            if state == 'green':
                self.wid.color = (0,1,0,1)
            if state == 'standby':
                self.wid.color = (1,0,0,1)
            else:
                self.wid.color = (1,1,1,1)

    def on_timeleft(self, obj, value):
        '''handle the time left of the traffic light'''
        if self.connect == True:
            self.wid.text = str(value)

    def on_connect(self, obj, value):
        '''check if nodemcu is connected, and toggle Counter widget'''
        if self.connect is True:
            animation = Animation(font_size =40, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.add_counter,.5)
        else:
            animation = Animation(font_size =90, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.remove_counter,.5)
        animation.start(self.root.children[0].ids.time)

    def update_time(self, nap):
        '''update clock current time'''
        now = datetime.now() # get current time as datetime object
        self.root.children[0].ids.time.text = now.strftime('%H:%M:%S')

    def serial_read(self,dt):
        '''connection, state and time change is handled here'''
        res = self.ser.read()
        res, tl = list(res.hex())
        # TL not connected & counter is rendered
        if res == 'f' and self.connect == True:
            self.connect = not self.connect # True
        else: # connected
            if self.connect == False: # not showing
                self.connect = not self.connect # add widget
            # check time left
            self.timeleft = int(tl, base=16)
            # handle state and trigger on_state
            if res == '1':
                self.state = 'red'
            elif res == '2':
                self.state = 'green'
            elif res == '3':
                self.state = 'yellow'
            elif res == '4':
                self.state = 'standby'
                self.wid.text = 'Waiting..'
            else:
                pass

    def on_start(self):
        # init Counter object
        self.wid = Counter()
        try:    
            self.ser = serial.Serial(baudrate=115200,port='/dev/ttyUSB0')
        except serial.SerialException:
            print('the port is not exist. exiting...')
            exit(-1)
        if self.ser.is_open == False:
            self.ser.open()
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.serial_read, .25)
    
if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular = 'font/Roboto-Thin.ttf',
        fn_bold = 'font/Roboto-Medium.ttf')
    # Window.clearcolor = get_color_from_hex('#808080')
    DashApp().run()