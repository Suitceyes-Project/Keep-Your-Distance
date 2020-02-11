from gpiozero import Button
import config as cfg

class ProgressRequestSystem:
    def __init__(self):
        self._button = Button(cfg.buttonGpioPort)        
        self._button_was_pressed = False
        
    def update(self, dt):
        if self._button.is_pressed:
            self._button_was_pressed = True
        
        if self._button.is_pressed == False and self._button_was_pressed:
            self._on_button_up()
            self._button_was_pressed = False

    def _on_button_up(self):
        # make request to indicate progress
        print("button pressed")        
        # set state?