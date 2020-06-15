from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior

import serial
from datetime import datetime

# Constant
COLOR = {'red': (1,0,0,1), 
        'yellow': (1,1,0,1), 
        'green': (0,1,0,1), 
        'standby': (1,0,0,1) }

class Counter(Label):
    pass

class SelBox(ButtonBehavior, BoxLayout):
    '''Selection BoxLayout with Button Behavior '''
    pass

class DashApp(App):
    '''Root Class'''
    # property of traffic light counter
    connect = BooleanProperty(False)
    state = ListProperty((1,1,1,1))
    timeleft = StringProperty('Counter')
    timenow = StringProperty('04:58:00')

    def nav(self, obj, touch, nav):
        if obj.collide_point(*touch.pos):
            nav.toggle_state()
            return True # stop propagating event
        return False

    def sleep(self, obj, touch, nav):
        if obj.collide_point(*touch.pos):
            nav.toggle_state()
            Clock.unschedule(self.curr_time)
            self.root.current = 'second'
            return True # stop propagating event
        return False


    def wake(self, obj, touch):
        if obj.collide_point(*touch.pos):
            self.root.current = 'main'
            self.curr_time = Clock.schedule_interval(self.update_time, 1)
            return True # stop propagating event
        return False

    def add_counter(self,dt):
        self.root.ids['mainpanel'].add_widget(self.wid,index=1)
    
    def remove_counter(self, dt):
        self.root.ids['mainpanel'].remove_widget(self.wid)

    def on_connect(self, obj, value):
        '''check if nodemcu is connected, and toggle Counter widget'''
        if self.connect is True:
            animation = Animation(font_size =40, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.add_counter,.5)
        else:
            animation = Animation(font_size =90, t='in_out_sine', duration= .5)
            Clock.schedule_once(self.remove_counter,.5)
        animation.start(self.root.ids['time'])

    def update_time(self, nap):
        '''update clock current time'''
        now = datetime.now() # get current time as datetime object
        self.timenow = now.strftime('%H:%M:%S')

    def serial_read(self,dt):
        '''connection, state and time change is handled here'''
        res = self.ser.read()
        res, tl = list(res.hex())
        # TL not connected & counter is rendered
        if res == 'f':
            self.connect = False
        else: # connected
            self.connect = True # add widget if False
            # change time left
            self.timeleft = str(int(tl, base=16))
            # handle state and trigger on_state
            if res == '1':
                self.state = COLOR['red']
            elif res == '2':
                self.state = COLOR['green']
            elif res == '3':
                self.state = COLOR['yellow']
            elif res == '4':
                self.state = COLOR['standby']
                self.timeleft = 'Waiting..'
            else:
                print('NodeMCU is initializing, exiting...')
                exit(-2)
                pass

    def on_start(self):
        # init Counter object
        self.wid = Counter()
        try:    
            self.ser = serial.Serial(baudrate=115200,port='/dev/ttyUSB0')
        except serial.SerialException:
            print('the port does not exist. exiting...')
            exit(-1)
        if self.ser.is_open == False:
            self.ser.open()
        self.curr_time = Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.serial_read, .25)
    
if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular = 'font/Roboto-Thin.ttf',
        fn_bold = 'font/Roboto-Medium.ttf')
    DashApp().run()