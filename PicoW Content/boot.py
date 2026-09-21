# Au lancement cache le dossier du PicoW si le pin GND et GP7 ne sont pas reliés


import usb_hid
import storage
import digitalio
import board

# Bouton de secours sur GP7
btn = digitalio.DigitalInOut(board.GP7)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

if btn.value:
    # GP7 non connecté = mode furtif
    storage.disable_usb_drive()
else:
    # GP7 relié à GND = mode normal, lecteur visible
    pass

usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE, usb_hid.Device.CONSUMER_CONTROL))
