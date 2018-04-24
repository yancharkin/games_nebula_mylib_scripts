# -*- Mode: Python; coding: utf-8; -*-

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

dict_lang = {
    'English':'ENG',
    'Cesky':'CZE',
    'German':'GER',
    'Français':'FRA',
    'Español':'SPA',
    'Italian':'ITA',
    'Polski':'POL',
    'Русский':'RUS',
    'Japanease':'JAP'
}

class GUI:

    def __init__(self):

        self.config_load()
        self.create_main_window()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            self.language = 'English'
            self.same_res = False
            self.custom_res = False
            self.custom_width = 800
            self.custom_height = 600

            config_parser.add_section('Settings')
            config_parser.set('Settings', 'language', str(self.language))
            config_parser.set('Settings', 'same_res', str(self.same_res))
            config_parser.set('Settings', 'custom_res', str(self.custom_res))
            config_parser.set('Settings', 'custom_width', str(self.custom_width))
            config_parser.set('Settings', 'custom_height', str(self.custom_height))

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()

        else:
            self.language = config_parser.get('Settings', 'language')
            self.same_res = config_parser.getboolean('Settings', 'same_res')
            self.custom_res = config_parser.getboolean('Settings', 'custom_res')
            self.custom_width = config_parser.get('Settings', 'custom_width')
            self.custom_height = config_parser.get('Settings', 'custom_height')

    def config_save(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'language', str(self.language))
        config_parser.set('Settings', 'same_res', str(self.same_res))
        config_parser.set('Settings', 'custom_res', str(self.custom_res))
        config_parser.set('Settings', 'custom_width', str(self.custom_width))
        config_parser.set('Settings', 'custom_height', str(self.custom_height))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        config_file = current_dir + '/game/owar.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)
        config_parser.set('Main', 'Language', str(dict_lang[self.language]))
        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.modify_start_file()

    def quit_app(self, window, event):
        self.config_save()
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Original War"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        self.grid = Gtk.Grid(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            row_spacing = 10,
            column_spacing = 10,
            column_homogeneous = True,
            )

        self.label_language = Gtk.Label(
            label = _("Language")
            )

        self.combobox_language = Gtk.ComboBoxText()
        i = 0
        for lang in dict_lang:
            self.combobox_language.append_text(lang)
            if lang == self.language:
                active_lang = i
            i += 1

        self.combobox_language.set_active(active_lang)
        self.combobox_language.connect('changed', self.cb_combobox_language)

        self.checkbutton_custom_res = Gtk.CheckButton(
            label = _("Custom resolution"),
            active = self.custom_res,
            tooltip_text = _("Makes the ingame resolution set to a custom resolution.")
            )
        self.checkbutton_custom_res.connect('toggled', self.cb_checkbutton_custom_res)

        self.entry_width = Gtk.Entry(
            placeholder_text = _("Width"),
            no_show_all = True,
            max_length = 4,
            max_width_chars = 4,
            xalign = 0.5,
            text = self.custom_width
            )
        self.entry_width.set_visible(self.custom_res)
        self.entry_width.connect('changed', self.cb_entry_width)

        self.entry_height = Gtk.Entry(
            placeholder_text = _("Height"),
            no_show_all = True,
            max_length = 4,
            max_width_chars = 4,
            xalign = 0.5,
            text = self.custom_height
            )
        self.entry_height.set_visible(self.custom_res)
        self.entry_height.connect('changed', self.cb_entry_height)

        self.checkbutton_same_res = Gtk.CheckButton(
            label = _("Same resolution"),
            active = self.same_res,
            tooltip_text = _("Makes the menus and videos use the same resolution\n" + \
            "as the game instead of 800x600 and 640x480")
            )

        self.checkbutton_same_res.connect('toggled', self.cb_checkbutton_same_res)

        self.button_save = Gtk.Button(
            label = _("Save and quit")
            )
        self.button_save.connect('clicked', self.cb_button_save)

        self.grid.attach(self.label_language, 0, 0, 1, 1)
        self.grid.attach(self.combobox_language, 1, 0, 1, 1)
        self.grid.attach(self.checkbutton_same_res, 0, 1, 2, 1)
        self.grid.attach(self.checkbutton_custom_res, 0, 2, 2, 1)
        self.grid.attach(self.entry_width, 0, 3, 1, 1)
        self.grid.attach(self.entry_height, 1, 3, 1, 1)
        self.grid.attach(self.button_save, 0, 4, 2, 1)

        self.main_window.add(self.grid)

        self.main_window.show_all()

    def cb_combobox_language(self, combobox):
        self.language = combobox.get_active_text()

    def cb_checkbutton_custom_res(self, button):
        self.custom_res = button.get_active()
        self.entry_width.set_visible(self.custom_res)
        self.entry_height.set_visible(self.custom_res)

    def cb_checkbutton_same_res(self, button):
        self.same_res = button.get_active()

    def cb_entry_width(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.custom_width = new_text

    def cb_entry_height(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.custom_height = new_text

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def modify_start_file(self):

        parameters_list = []

        if self.same_res == True:
            parameters_list.append('SameRes')
        if self.custom_res == True:
            parameters_list.append('CustomRes')
            parameters_list.append(str(self.custom_width))
            parameters_list.append(str(self.custom_height))

        parameters_str = ' '.join(parameters_list)

        new_launch_command = 'python "$NEBULA_DIR/launcher_wine.py" ' + \
        'original_war "OwarOGL.exe' + ' ' + parameters_str + '"'

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if 'Owar' in start_file_content[i]:
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
