from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import sys
import os.path
import hashlib

from encryptor import enc_image,dec_image

sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/encryptscreen.kv")
Builder.load_file(folder+'/screen1.kv')
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
import os.path
from kivymd.app import App
from screen1 import Screen1

from plyer import filechooser

class EncryptScreen(MDScreen):
    def choose_decrypt_file(self):
        filechooser.open_file(on_selection=self.handle_selection_decrypt_file)
    def handle_selection_decrypt_file(self,selection):
        self.path_decrypt = selection[0]
        self.dir_decrypt = (os.path.split(self.path_decrypt)[0])

        from kivy.app import App
        App.get_running_app().search_menu_decrypt.open()
        App.get_running_app().image_decrypt = self.path_decrypt
        App.get_running_app().dir_image_decrypt = self.dir_decrypt

        App.get_running_app().image_name_decrypt = (os.path.split(self.path_decrypt)[1])


    def choose_file(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''

        self.path = selection[0]
        self.dir = (os.path.split(self.path)[0])
        self.ids.screen1.ids.chosen_image.source = selection[0]
        from kivy.app import App
        App.get_running_app().search_menu.open()
        App.get_running_app().image = self.path
        App.get_running_app().dir_image = self.dir
        App.get_running_app().image_name = (os.path.split(self.path)[1])

        #GENERATE KEY & INITIALIZATION VECTOR




class Content(BoxLayout):
    pass
class Content1(BoxLayout):
    pass

from kivymd.uix.dialog import MDDialog
class MDInputDecryptDialog:


    def __init__(self):

        self.dialog = MDDialog(
            title="PASSWORD",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=App.get_running_app().theme_cls.primary_color, on_press=self.dismiss_menu
                ),
                MDRaisedButton(
                    text="ENTER", on_press=self.get_value
                ),
            ],
        )

    def open_menu(self):
        self.dialog.open()

    def dismiss_menu(self, *args):
        self.dialog.dismiss()

    def get_value(self, *args):
        self.dialog.dismiss()

        self.value = (self.dialog.content_cls.ids.address.text)

        hash = hashlib.sha256(self.value.encode())
        p = hash.digest()
        key = p
        iv = p.ljust(16)[:16]
        input_file = open(App.get_running_app().image_decrypt, 'rb')
        input_data = input_file.read()
        input_file.close()

        dec_image(input_data, key, iv,App.get_running_app().dir_image_decrypt )
        App.get_running_app().show_decrypt_toast()
        os.remove(App.get_running_app().image_decrypt)


class MDInputDialog:


    def __init__(self):
        self.todaynow = None
        self.dialog = MDDialog(
            title="PASSWORD",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=App.get_running_app().theme_cls.primary_color, on_press=self.dismiss_menu
                ),
                MDRaisedButton(
                    text="ENTER", on_press=self.get_value
                ),
            ],
        )

    def open_menu(self):
        self.dialog.open()

    def dismiss_menu(self, *args):
        self.dialog.dismiss()

    def get_value(self, *args):
        self.dialog.dismiss()

        self.value = (self.dialog.content_cls.ids.address.text)

        hash = hashlib.sha256(self.value.encode())
        p = hash.digest()
        key = p
        iv = p.ljust(16)[:16]
        print("Encoding key is: ", key)

        input_file = open(App.get_running_app().image, 'rb')
        input_data = input_file.read()
        input_file.close()
        enc_image(input_data, key, iv, App.get_running_app().dir_image,App.get_running_app().image_name)
        App.get_running_app().show_toast()
        os.remove(App.get_running_app().image)


    # def snack_show(self,*args):
    #     self.snackbar = Snackbar(text=f"{self.value} Timezone Now:{self.todaynow.strftime('%H:%M:%S')}", duration=3)
    #     self.snackbar.open()




class SearchPopupMenu(MDInputDialog):
    def __init__(self):
        super().__init__()
        self.size = [.9, .3]

    def open(self, *args):
        self.open_menu()
class SearchPopupMenuDecrypt(MDInputDecryptDialog):
    def __init__(self):
        super().__init__()
        self.size = [.9, .3]

    def open(self, *args):
        self.open_menu()

from kivy.uix.image import Image
from kivy.uix.stencilview import StencilView
from kivy.properties import AliasProperty

class FillImage(Image, StencilView):
    def get_filled_image_size(self):
        ratio = self.image_ratio
        w, h = self.size

        widget_ratio = w / h
        iw = (h * ratio) if ratio > widget_ratio else w
        ih = (w / ratio) if ratio <= widget_ratio else h
        return iw, ih

    norm_image_size = AliasProperty(get_filled_image_size, bind=('texture', 'size', 'allow_stretch', 'image_ratio', 'keep_ratio'), cache=True)
