from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from encryptscreen.encryptscreen import SearchPopupMenu,SearchPopupMenuDecrypt

if platform == 'macosx':

    Window.size = (450, 750)
    #if you use macosx you will be resized like this
else:
    pass
class EncryptApp(MDApp):
    def __init__(self):
        super().__init__()
        self.screen = Builder.load_file('main.kv')
        self.search_menu =SearchPopupMenu()
        self.search_menu_decrypt = SearchPopupMenuDecrypt()
    def show_toast(self):
        from kivymd.toast import toast

        toast(f'Encryption Finished saved as {self.dir_image}/{self.image_name}.enc')

    def show_decrypt_toast(self):
        from kivymd.toast import toast

        toast(f'Decryption Finished saved as {self.dir_image_decrypt}/{self.name_decrypt_file}')
    def build(self):


        return self.screen


EncryptApp().run()