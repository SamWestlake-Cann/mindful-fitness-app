from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import FadeTransition
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage

import os

# Constants
FADE_DURATION = 3


class AnimatedTextField(MDTextField):
    def on_focus(self, instance, value):
        if value:  # When focused
            anim = Animation(height=dp(60), duration=0.2)
        else:  #  When unfocussed
            anim = (Animation(height=dp(50), duration=0.1) +
                    Animation(height=dp(56), duration=0.1))
        anim.start(self)


class OpeningScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            # Set up a reference to the logo color (for transparency)
            self.fade_color = Color(1, 1, 1, 0)  # Transparent color initially
            self.logo_texture = Image(source="../assets/logo.png").texture

            # To ensure no duplicate logos are drawn:
            self.logo_rect = None

        # Bind the screen size so the logo resizes with the screen
        self.bind(size=self.update_logo_position,
                  pos=self.update_logo_position)

        # Start fade-in animation for the screen's opacity
        self.fade_in_animation = Animation(opacity=1, duration=FADE_DURATION)
        self.fade_in_animation.start(self)

    def update_logo_position(self, *args):
        # Check if there's an existing logo, then remove it
        if self.logo_rect:
            self.canvas.before.remove(self.logo_rect)

        # Calculate the logo size based on screen width
        screen_width = self.width
        target_width = screen_width * 0.8  # Adjust this for size preference
        aspect_ratio = self.logo_texture.height / self.logo_texture.width
        target_height = target_width * aspect_ratio

        # Create the new logo and center it
        self.logo_rect = Rectangle(
            texture=self.logo_texture,
            size=(target_width, target_height),
            pos=((self.width - target_width) / 2,
                 (self.height - target_height) / 2)
        )
        self.canvas.before.add(self.logo_rect)


class MindfulSportsCoachApp(MDApp):
    def build(self):
        # Setting the colors for the app
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.primary_hue = "500"  # Default shade of Amber
        self.theme_cls.theme_style = "Dark"  # Backgrounds

        # load the kv layout file for the opening screen
        kv_path = os.path.join(os.path.dirname(
            __file__), "screens", "opening.kv")
        Builder.load_file(kv_path)

        sm = MDScreenManager(transition=FadeTransition())
        opening_screen = OpeningScreen(name="opening")
        sm.add_widget(opening_screen)

        # Set initial opacity to 0 for fade-in effect
        opening_screen.opacity = 0

        #  Fade-in effect to the screen then the app starts
        Animation(opacity=1, duration=FADE_DURATION).start(opening_screen)

        return sm

    def change_screen(self, screen_name):
        # Switch screen based on the screen name
        self.root.current = screen_name


if __name__ == "__main__":
    MindfulSportsCoachApp().run()
