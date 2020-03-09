from gpiozero import Button
import config as cfg

class ProgressRequestSystem:
    def __init__(self, state_machine):
        self._button = Button(cfg.buttonGpioPort)        
        self._button_was_pressed = False
        self._state_machine = state_machine
        
    def update(self, dt):
        if self._button.is_pressed:
            self._button_was_pressed = True
        
        if self._button.is_pressed == False and self._button_was_pressed:
            self._on_button_up()
            self._button_was_pressed = False

    def _on_button_up(self):        
        print("Requested Progress")        
        # set state
        if self._state_machine.is_in_state("request-progress"):
            return
        
        self._state_machine.change_to("request-progress")