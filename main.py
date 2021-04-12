from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
<<<<<<< HEAD
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.behaviors import FocusBehavior
=======

from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.behaviors import FocusBehavior
import certifi

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
>>>>>>> 34243d092468ec0a9eaa0396e20f8f7ef2351e18

from kivy.network.urlrequest import UrlRequest


Window.size = (300, 500)
screen_helper = '''

MDBoxLayout:
    orientation: "vertical"
    MDToolbar:
        title: "Casos de Covid-19"
        elevation: 8
    ScreenManager:
        MenuScreen:
        ProfileScreen:
        UploadScreen:
    
<MenuScreen>:
    name: 'menu'
    MDIconButton:
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        user_font_size: '80sp'
        icon: "bacteria-outline"
    MDRectangleFlatButton:
        text: 'Começar'
        pos_hint: {'center_x':0.5, 'center_y':0.3}
        on_press:  root.manager.current = 'profile'      

<ProfileScreen>:
    name: 'profile'         
    MDIconButton:
        pos_hint: {"center_x": .5, "center_y": .9}
        user_font_size: '50sp'
        icon: "radioactive"
    MDLabel:
        halign: 'center'
        pos_hint: {'center_y':0.8}
        text: "Numero de Casos Brasil"  
        font_style: 'Subtitle2'
        
    MDRectangleFlatIconButton:
        pos_hint: {"x": .1, "center_y": .7} 
        icon: "heart-off-outline"
        text: "Mortes"       
        size_hint_x: .37
        size_hint_y: .08 
    MDLabel:
        id: mortes
        size_hint_x: .43
        size_hint_y: .09
        text: "0"  
        pos_hint: {"x": .65, "center_y": .7}      
        font_style:'Subtitle1'         
    MDRectangleFlatIconButton:
        size_hint_x: .37
        size_hint_y: .08
        pos_hint: {"x": .1, "center_y": .6} 
        icon: "heart-pulse"
        text: "Ativos"      
    MDLabel:
        id: ativos
        text: "0"   
        pos_hint: {"x": .65, "center_y": .6}  
        size_hint_x: .43
        size_hint_y: .09                  
    MDRectangleFlatIconButton:
        pos_hint: {"x": .1, "center_y": .5} 
        icon: "heart-broken-outline"
        text: "Confirmados"  
        size_hint_x: .37
        size_hint_y: .08
    MDLabel:
        id: confirmados
        text: "0"  
        pos_hint: {"x": .65, "center_y": .5}  
        size_hint_x: .43
        size_hint_y: .09     
    MDRectangleFlatIconButton:
        pos_hint: {"x": .1, "center_y": .4} 
        icon: "heart-plus-outline"
        text: "Recuperados" 
        size_hint_x: .37
        size_hint_y: .08
    MDLabel:
        id: recuperados    
        text: "0"
        pos_hint: {"x": .65, "center_y": .4}  
        size_hint_x: .43
        size_hint_y: .09                 
    ButtonFocus:
        icon: "arrow-left"
        text: 'Voltar'
        pos_hint: {'center_x': 0.3, 'center_y': 0.2}
        size_hint_x: .35
        size_hint_y: .08 
        on_press:  root.manager.current = 'menu'       
    ButtonFocus:
        icon: "sync-circle"
        text: 'Atualizar'
        pos_hint: {'center_x': 0.7, 'center_y': 0.2}
        size_hint_x: .35
        size_hint_y: .08  
        on_release: root.Calculo()    
        
<UploadScreen>:
    name: 'upload'
    MDLabel:
        text: 'Leonardo'
        halign: 'center'      
    MDRectangleFlatButton:
        text: 'Voltar'
        pos_hint: {'center_x':0.5, 'center_y':0.2}
        on_press:  root.manager.current = 'menu'     
'''


class ButtonFocus(MDRoundFlatIconButton, FocusBehavior):
    ...


class MenuScreen(MDScreen):
    pass


class ProfileScreen(MDScreen):

    def Calculo(self):

        search_url = "https://covid19-brazil-api.vercel.app/api/report/v1/brazil"

        self.request = UrlRequest(search_url)
        self.request.wait()
        print(self.request)
        dados = self.request.result['data']
        ativos = dados['cases']
        confirmados = dados['confirmed']
        mortes = dados['deaths']
        recuperados = dados['recovered']

        self.ids.ativos.text = str(ativos)
        self.ids.confirmados.text = str(confirmados)
        self.ids.mortes.text = str(mortes)
        self.ids.recuperados.text = str(recuperados)


class UploadScreen(MDScreen):
    pass


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(UploadScreen(name='upload'))


class CovidApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.accent_palette = 'Blue'
       # self.theme_cls.theme_style = 'Dark'
        return Builder.load_string(screen_helper)


if __name__ == '__main__':
    CovidApp().run()
