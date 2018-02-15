import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import gettext
import imp

try:
    from ConfigParser import ConfigParser as ConfigParser
except:
    from configparser import ConfigParser as ConfigParser

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

current_dir = sys.path[0]

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):

        config_file = current_dir + '/game/acsetup.cfg'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('graphics'):
            self.screen_width = 800
            self.screen_height = 600

            config_parser.add_section('graphics')
            config_parser.set('graphics', 'screen_width', str(self.screen_width))
            config_parser.set('graphics', 'screen_height', str(self.screen_height))

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()

        else:
            self.screen_width = config_parser.get('graphics', 'screen_width')
            self.screen_height = config_parser.get('graphics', 'screen_height')

    def config_save(self):

        config_file = current_dir + '/game/acsetup.cfg'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('graphics', 'screen_width', str(self.screen_width))
        config_parser.set('graphics', 'screen_height', str(self.screen_height))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("King's Quest I Remake"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            row_spacing = 10,
            column_spacing = 10,
            column_homogeneous = True,
            )

        label_custom_res = Gtk.Label(
            label = _("Set custom resolution:")
            )

        entry_screen_width = Gtk.Entry(
            placeholder_text = _("Width"),
            max_length = 4,
            xalign = 0.5,
            text = self.screen_width
            )
        entry_screen_width.connect('changed', self.cb_entry_screen_width)

        entry_screen_height = Gtk.Entry(
            placeholder_text = _("Height"),
            max_length = 4,
            xalign = 0.5,
            text = self.screen_height
            )
        entry_screen_height.connect('changed', self.cb_entry_screen_height)

        button_save = Gtk.Button(
            label = _("Save and quit")
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_custom_res, 0, 0, 2, 1)
        grid.attach(entry_screen_width, 0, 1, 1, 1)
        grid.attach(entry_screen_height, 1, 1, 1, 1)
        grid.attach(button_save, 0, 2, 2, 1)

        self.main_window.add(grid)

        self.main_window.show_all()

    def cb_entry_screen_width(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.screen_width = new_text

    def cb_entry_screen_height(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.screen_height = new_text

    def cb_button_save(self, button):

        if (self.screen_width == '') or (self.screen_height == ''):
            message_dialog = Gtk.MessageDialog(
                self.main_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Error")
                )
            message_dialog.format_secondary_text(_("You have to set width and height."))
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)
            message_dialog.run()
            message_dialog.destroy()

            return

        self.config_save()
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
