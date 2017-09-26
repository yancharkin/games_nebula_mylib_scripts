#!/usr/bin/python
# -*- Mode: Python; coding: utf-8 -*-

# HiRes/Language fix from here: http://forum.daedalic.de/viewtopic.php?f=273&t=5949

import sys, os
from struct import pack, unpack
import PIL
from PIL import Image

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

dict_lang = {
    'English':'forcelang_en',
    'Deutsch':'forcelang_de',
    'Français':'forcelang_fr',
    'Русский':'forcelang_ru',
    }

def patch_exe(exe_path, RES_X, RES_Y):

    if not os.path.exists(exe_path + '.original'):
        os.system('mv ' + exe_path + ' ' + exe_path + '.original')

    resX = pack('<L', RES_X).encode('hex')
    resY = pack('<L', RES_Y).encode('hex')

    ratios,offsets = [
        round(1280/1024.0, 2),
        round(640/480.0, 2),
        round(720/480.0, 2),
        round(1920/1200.0, 2),
        round(1280/768.0, 2),
        round(1024/600.0, 2),
        round(1920/1080.0, 2),
        round(4096/2160.0, 2)
        ], \
        [
        -0.1,   # 1280/1024 = 1.25 (5:4)
        0,      # 640/480 = 1.333333333 (4:3)
        0.11,   # 720/480 = 1.5 (3:2)
        0.17,   # 1920/1200 = 1.6 (16:10)
        0.21,   # 1280/768 = 1.666666667 (5:3)
        0.23,   # 1024/600 = 1.706666667 (17:10)
        0.25,   # 1920/1080 = 1.77777777 (16:9)
        0.32    # 4096/2160 = 1.896296296 (256:135)
        ]

    r = offsets[ratios.index(round(RES_X/float(RES_Y), 2))]

    p1 = [0x001078, '9090']
    p2 = [0x01128c, 'e90e2c1900']
    p3 = [0x0f5c43, '59595968'+resY+'68'+resX+'5233c9894c2414894c2410b820000000']
    p4 = [0x1a3e9f, '8d732c8bcec7442408'+resX+'c744240c'+resY+'e9d8d3e6ff']
    p5 = [0x1a5fcc, pack('<f', RES_Y/float(RES_X)).encode('hex')]
    p6 = [0x1a6508, pack('<f', RES_Y/float(RES_X)).encode('hex')]
    p7 = [0x019430, 'e987aa1800' + '90'*26]
    p8 = [0x1a3ebc, 'c74108'+resX+'c7410c'+resY+'c7411020000000c74114000000005ec20400']
    skills,icon,gauge,bars = [0x1a60ac],[0x1a7278, 0x1a727c],[0x1a7290, 0x1a7294],[0x1a6e6c, 0x1a72ac]

    with open(exe_path + '.original', 'rb') as f: blob = f.read()
    for p in [p1, p2, p3, p4, p5, p6, p7, p8]: blob = blob[:p[0]] + p[1].decode('hex') + blob[p[0]+len(p[1].decode('hex')):]
    for i in (skills+icon+gauge+bars):
        t = unpack('<f', blob[i:i+4])[0]
        blob = blob[:i] + pack('<f', t-t*r) + blob[i+4:]
    with open(exe_path, 'wb') as f: f.write(blob)

    tmp_list = exe_path.split('/')
    del tmp_list[-1]
    del tmp_list[-1]
    images_dir = '/'.join(tmp_list) + '/Resources/Bitmaps/'
    scale_images(images_dir, RES_X, RES_Y)

def scale_images(images_dir, RES_X, RES_Y):

    images_list = ['FRM000.BMP', 'PRELUDE0.BMP', 'PRELUDE1.BMP', 'PRELUDE2.BMP']

    for image_name in images_list:

        image = Image.open(images_dir + image_name)

        image_width = image.size[0]
        image_height = image.size[1]
        image_scale = RES_X / float(image_width)
        new_image_width = RES_X
        new_image_height = int(image_height * image_scale)

        image = image.resize((new_image_width, new_image_height), PIL.Image.ANTIALIAS)
        new_image = Image.new('RGB', (RES_X, RES_Y), 0)
        offset = ((RES_X - new_image_width)/2, (RES_Y - new_image_height)/2)
        new_image.paste(image, offset)

        new_image.save(images_dir + image_name)

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            self.language = 'English'
            self.custom_width = 800
            self.custom_height = 600

            config_parser.add_section('Settings')
            config_parser.set('Settings', 'language', self.language)
            config_parser.set('Settings', 'custom_width', self.custom_width)
            config_parser.set('Settings', 'custom_height', self.custom_height)

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()

        else:
            self.language = config_parser.get('Settings', 'language')
            self.custom_width = config_parser.get('Settings', 'custom_width')
            self.custom_height = config_parser.get('Settings', 'custom_height')

    def config_save(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'language', self.language)
        config_parser.set('Settings', 'custom_width', self.custom_width)
        config_parser.set('Settings', 'custom_height', self.custom_height)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Zanzarah: The Hidden Portal"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            margin_left = 5,
            margin_right = 5,
            margin_top = 5,
            margin_bottom = 5,
            row_spacing = 5,
            column_spacing = 5,
            column_homogeneous = True,
            )

        label_language = Gtk.Label(
            label = _("Language")
            )

        combobox_language = Gtk.ComboBoxText()
        active_lang = 0
        i = 0
        for lang in sorted(dict_lang):
            combobox_language.append_text(lang)
            if lang == self.language:
                active_lang = i
            i += 1

        combobox_language.set_active(active_lang)
        combobox_language.connect('changed', self.cb_combobox_language)

        label_resolution = Gtk.Label(
            label = _("Resolution")
            )

        entry_custom_width = Gtk.Entry(
            placeholder_text = _("Width"),
            max_length = 4,
            xalign = 0.5,
            text = self.custom_width
            )
        entry_custom_width.connect('changed', self.cb_entry_custom_width)

        entry_custom_height = Gtk.Entry(
            placeholder_text = _("Height"),
            max_length = 4,
            xalign = 0.5,
            text = self.custom_height
            )
        entry_custom_height.connect('changed', self.cb_entry_custom_height)

        button_save = Gtk.Button(
            label = _("Save and quit")
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_language, 0, 0, 1, 1)
        grid.attach(combobox_language, 1, 0, 2, 1)
        grid.attach(label_resolution, 0, 1, 1, 1)
        grid.attach(entry_custom_width, 1, 1, 1, 1)
        grid.attach(entry_custom_height, 2, 1, 1, 1)
        grid.attach(button_save, 0, 2, 3, 1)

        self.main_window.add(grid)

        self.main_window.show_all()

    def cb_combobox_language(self, combobox):
        self.language = combobox.get_active_text()

    def cb_entry_custom_width(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.custom_width = new_text

    def cb_entry_custom_height(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.custom_height = new_text

    def cb_button_save(self, button):

        self.config_save()

        lang_to_set = current_dir + '/game/Data/Languages/' + self.language  + '/*'
        os.system('cp -r ' + lang_to_set + ' ' + current_dir + '/game/')

        exe_path = current_dir + '/game/System/zanthp.exe'
        patch_exe(exe_path, int(self.custom_width), int(self.custom_height))

        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        patch_exe(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        sys.exit(main())
