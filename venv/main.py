from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
class Mainwindow(BoxLayout):
    pass
class uiApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.mainscreen = Mainwindow()
        screen = Screen(name='mainscreen')
        screen.add_widget(self.mainscreen)
        self.screen_manager.add_widget(screen)
        return self.screen_manager
if __name__ == '__main__':




    LabelBase.register(name='Modern Pictograms',
                       fn_regular='modernpics.ttf')

    uiApp().run()
