import requests
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from PIL import Image
from android.os import Environment
from android.content import Intent
from android.net import Uri
from android.provider import Settings
from jnius import autoclass

# URL do obrazu na GitHubie
GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/adamos2804/adamos2804/main/szczur.png"
IMAGE_PATH = os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), "Download", "wallpaper.jpg")

class WallpaperApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.image = KivyImage(source=GITHUB_IMAGE_URL)
        btn_download = Button(text='Pobierz i ustaw tapetę', on_press=self.download_and_set_wallpaper)
        
        layout.add_widget(self.image)
        layout.add_widget(btn_download)
        
        return layout
    
    def download_and_set_wallpaper(self, instance):
        response = requests.get(GITHUB_IMAGE_URL, stream=True)
        if response.status_code == 200:
            with open(IMAGE_PATH, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            self.set_wallpaper()
    
    def set_wallpaper(self):
        WallpaperManager = autoclass('android.app.WallpaperManager')
        Context = autoclass('android.content.Context')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        
        wallpaper_manager = WallpaperManager.getInstance(activity)
        bitmap = Image.open(IMAGE_PATH)
        wallpaper_manager.setBitmap(bitmap)

if __name__ == '__main__':
    WallpaperApp().run()
