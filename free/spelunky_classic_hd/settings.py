#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext
import imp

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

        config_file = open(current_dir + '/game/assets/settings.cfg', 'r')
        data = config_file.readlines()
        config_file.close()

        self.language = data[-1]

    def config_save(self):

        config_file = open(current_dir + '/game/assets/settings.cfg', 'r')
        data = config_file.readlines()
        config_file.close()

        config_file = open(current_dir + '/game/assets/settings.cfg', 'w')
        for i in range(len(data) - 1):
            config_file.write(data[i])
        config_file.write(self.language)
        config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Spelunky Classic HD"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360,
            )
        self.main_window.connect('delete-event', self.quit_app)

        label = Gtk.Label(
            halign = Gtk.Align.FILL,
            label = _("Language:"),
            )

        combobox = Gtk.ComboBoxText()
        combobox.append_text('En')

        trans_dir_content = os.listdir(current_dir + '/game/assets/translations')

        for name in ['_source', 'README.md', 'LICENSE']:
            trans_dir_content.remove(name)

        index = 0
        for i in range(len(trans_dir_content)):
            combobox.append_text(trans_dir_content[i].title())
            if trans_dir_content[i].title() == self.language:
                index = i + 1

        combobox.set_active(index)
        combobox.connect('changed', self.cb_combobox)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            hexpand = True
            )
        button_save.connect('clicked', self.cb_button_save)

        grid = Gtk.Grid(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            row_spacing = 10,
            column_spacing = 10,
            )

        grid.attach(label, 0, 0, 1, 1)
        grid.attach(combobox, 1, 0, 1, 1)
        grid.attach(button_save, 0, 1, 2, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

    def cb_combobox(self, combobox):
        self.language = combobox.get_active_text()

    def cb_button_save(self, button):
        self.config_save()
        print self.language
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
