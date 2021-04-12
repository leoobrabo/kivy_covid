from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen

from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.behaviors import FocusBehavior
import certifi

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

os.environ['SSL_CERT_FILE'] = certifi.where()

#Window.size = (300, 500)
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
        pos_hint: {'center_y':0.75}
        text: "Numero de Casos"  
        font_style: 'H4'
        text_color: {1, 0.2, 0.3, 1}
        theme_text_color: 'Custom'
    MDRectangleFlatIconButton:
        pos_hint: {"x": .1, "center_y": .6} 
        icon: "heart-off-outline"
        text: "Mortes"       
        size_hint_x: .43
        size_hint_y: .09 
    MDLabel:
        id: mortes
        size_hint_x: .43
        size_hint_y: .09
        text: "0"  
        pos_hint: {"x": .65, "center_y": .6}      
        font_style:'Subtitle1'         
    MDRectangleFlatIconButton:
        size_hint_x: .43
        size_hint_y: .09
        pos_hint: {"x": .1, "center_y": .5} 
        icon: "heart-pulse"
        text: "Ativos"      
    MDLabel:
        id: ativos
        text: "0"   
        pos_hint: {"x": .65, "center_y": .5}  
        size_hint_x: .43
        size_hint_y: .09                  
    MDRectangleFlatIconButton:
        pos_hint: {"x": .1, "center_y": .4} 
        icon: "heart-broken-outline"
        text: "Confirmados"  
        size_hint_x: .43
        size_hint_y: .09
    MDLabel:
        id: confirmados
        text: "0"  
        pos_hint: {"x": .65, "center_y": .4}  
        size_hint_x: .43
        size_hint_y: .09       
    MDRectangleFlatIconButton:
        pos_hint: {"x": .1, "center_y": .3} 
        icon: "heart-plus-outline"
        text: "Recuperados" 
        size_hint_x: .43
        size_hint_y: .09
    MDLabel:
        id: recuperados    
        text: "0"
        pos_hint: {"x": .65, "center_y": .3}  
        size_hint_x: .43
        size_hint_y: .09                 
    ButtonFocus:
        icon: "arrow-left"
        text: 'Voltar'
        pos_hint: {'center_x': 0.3, 'center_y': 0.2}
        on_press:  root.manager.current = 'menu'       
    ButtonFocus:
        icon: "sync-circle"
        text: 'Atualizar'
        pos_hint: {'center_x': 0.7, 'center_y': 0.2}
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
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:

            covid = Covid()
            covid_brasil = covid.get_status_by_country_id(24)
            ativos = covid_brasil['active']
            confirmados = covid_brasil['confirmed']
            mortes = covid_brasil['deaths']
            recuperados = covid_brasil['recovered']
            self.ids.ativos.text = str(ativos)
            self.ids.confirmados.text = str(confirmados)
            self.ids.mortes.text = str(mortes)
            self.ids.recuperados.text = str(recuperados)

        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            # renewIPadress()

        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            # renewIPadress()

        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            # renewIPadress()

        except KeyboardInterrupt:
            print("Someone closed the program")


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
