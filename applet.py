import gi
import os # For simple commands
import subprocess # For more complex ones

gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3, Gdk, GObject		
import signal
	

def run_command(widget, command):
    # This runs the command in the background
    subprocess.Popen(command, shell=True)


def main():
    # 1. Create the Indicator
    app = 'SimpleApplet'
    icon = 'system-run-symbolic' # Icon name from theme
    
    # Creates an applet in the system tray
    indicator = AyatanaAppIndicator3.Indicator.new(
        app, icon, AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)

    # 2. Create the Menu
    menu = Gtk.Menu()
    
    # Add a menu item
    item = Gtk.MenuItem(label='Hello Taskbar')
    item.connect('activate', lambda x: print("Button clicked!"))
    menu.append(item)
    # I'm add a screen object
    screen_item = Gtk.MenuItem(label="Screen brightness")
    screen_item.connect('activate',lambda x: print('Screen outlet'))
    menu.append(screen_item)
    
    # I'm add a screen increase object
    screen_in_item = Gtk.MenuItem(label="increase brightness")
    screen_in_item.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

    screen_in_item.connect("activate", run_command,  'ddcutil setvcp 10 + 10 ; echo "/n Increase +5"')

    menu.append(screen_in_item)
    # I'm add a screen decrease object
    screen_de_item = Gtk.MenuItem(label="decrease brightness")
    screen_de_item.connect('activate', run_command, 'ddcutil setvcp 10 - 10 ; echo "/n Decrease -5"')
    menu.append(screen_de_item)

    # Add a quit item
    quit_item = Gtk.MenuItem(label='Quit')
    quit_item.connect('activate', Gtk.main_quit)
    menu.append(quit_item)
    
    # Show menu items
    menu.show_all()
    indicator.set_menu(menu)


    # 3. Start GTK Loop
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()




if __name__ == "__main__":
    main()
