"""Main module"""
from infi.systray import SysTrayIcon

from keyboard_listener import KeyboardListener
import threading

def start_keyboard_listener(systray):
    keyboard_thread = threading.Thread(target=KeyboardListener)
    keyboard_thread.start()

if __name__ == '__main__':
    KeyboardListener()
    # menu_options = (("Start Overlay", None, start_keyboard_listener),)
    # systray = SysTrayIcon('small.png',"Overlay Py", menu_options)
    # systray.start()