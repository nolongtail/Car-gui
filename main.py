from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition
from kivy.garden.navigationdrawer import NavigationDrawer

from datetime import datetime


class Navigator(NavigationDrawer):
    pass



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

    def update_time(self, nap):
        now = datetime.now() # get current time as datetime object
        self.root.children[0].ids.time.text = now.strftime('%H:%M:%S')

    def on_start(self):
        Clock.schedule_interval(self.update_time, 1)
        pass
    

if __name__ == '__main__':
    LabelBase.register(name="Roboto",
        fn_regular = 'font/Roboto-Thin.ttf',
        fn_bold = 'font/Roboto-Medium.ttf')
    # Window.clearcolor = get_color_from_hex('#808080')
    DashApp().run()