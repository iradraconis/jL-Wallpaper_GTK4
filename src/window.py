# window.py
#
# Copyright 2023 Maximilian Steinert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio, GLib

from zipfile import ZipFile
import shutil
import os
import json
import subprocess

from .pics_darker import pics_darker


@Gtk.Template(resource_path='/com/github/iradraconis/jLWallpaper/window.ui')
class JlWallpaperWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'JlWallpaperWindow'

    label = Gtk.Template.Child()
    button_pics_folder = Gtk.Template.Child()
    button_jl_folder = Gtk.Template.Child()
    button_run = Gtk.Template.Child()
    label_pics_folder = Gtk.Template.Child()
    label_jl_folder = Gtk.Template.Child()

    pics_folder = None
    jl_folder = None

    SETTINGS_FILE = 'settings.json'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_pics_action = Gio.SimpleAction(name="open_pics")
        open_pics_action.connect("activate", lambda a, p: self.open_file_dialog(self.on_pics_selected))
        self.add_action(open_pics_action)

        open_jl_action = Gio.SimpleAction(name="open_jl")
        open_jl_action.connect("activate", lambda a, p: self.open_file_dialog(self.on_jl_selected))
        self.add_action(open_jl_action)

        run_action = Gio.SimpleAction(name="run")
        run_action.connect("activate", self.run)
        self.add_action(run_action)

        self.load_saved_settings()

        # Update the labels with the loaded settings
        self.update_labels()

        # Ausgabe der ggs. gespeicherten Pfade
        print(self.pics_folder)
        print(self.jl_folder)


    def open_file_dialog(self, callback):
        # Create a new file selection dialog, using the "open" mode
        # and keep a reference to it
        self._native = Gtk.FileChooserNative(
            title="Select Folder",
            transient_for=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            accept_label="_Open",
            cancel_label="_Cancel",
        )
        # Connect the "response" signal of the folder selection dialog;
        # this signal is emitted when the user selects a file, or when
        # they cancel the operation
        self._native.connect("response", self.on_open_response, callback)
        # Present the dialog to the user
        self._native.show()

    def on_open_response(self, dialog, response, callback):
        # If the user selected a file...
        if response == Gtk.ResponseType.ACCEPT:
            # ... retrieve the location from the dialog
            gfile = dialog.get_file()
            folder_path = gfile.get_path()
            callback(folder_path)
        # Release the reference on the file selection dialog now that we
        # do not need it any more
        self._native = None

    def on_pics_selected(self, folder_path):
        self.pics_folder = folder_path
        print("Pics folder selected:", folder_path)
        self.save_current_settings()
        self.update_labels()

    def on_jl_selected(self, folder_path):
        self.jl_folder = folder_path
        print("jL folder selected:", folder_path)
        self.save_current_settings()
        self.update_labels()

    def load_saved_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
                self.pics_folder = settings.get('pics_folder')
                self.jl_folder = settings.get('jl_folder')

    def save_current_settings(self):
        settings = {
            'pics_folder': self.pics_folder,
            'jl_folder': self.jl_folder
        }
        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)

    def update_labels(self):
        self.label_pics_folder.set_visible(bool(self.pics_folder))
        self.label_jl_folder.set_visible(bool(self.jl_folder))

        self.label_pics_folder.set_label(f"Bilder-Ordner: {self.pics_folder}")
        self.label_jl_folder.set_label(f"j-Lawyer-Ordner: {self.jl_folder}")


    def run(self, action, parameter):
        print("Selected Pics Folder: ", self.pics_folder)
        print("Selected jL-Folder: ", self.jl_folder)
        self.button_run.set_label("arbeitet...")
        self.button_run.set_sensitive(False)
        self.do_your_work()
        self.button_run.set_label("Erfolg!")
        #self.button_run.set_sensitive(True)


    def do_your_work(self):

        try:
            file_path_wallpaper = self.pics_folder
            file_path_installation = self.jl_folder

            # Funktion setzt Helligkeit und Schärfe der Bilder herab
            pics_darker(self.pics_folder)

            file_path_wallpaper = f'{self.pics_folder}/darker_pictures'

            source_zip = str(file_path_installation + '/j-lawyer-client.jar')
            pict_folder = 'temp/themes/default/backgroundsrandom'
            target_zip_folder = 'temp'
            zip_file = 'j-lawyer-client'

            print(f'Entpacke die Daten zum {target_zip_folder} Ordner')

            # Create a ZipFile Object
            with ZipFile(source_zip, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                zipObj.extractall('temp')

            shutil.rmtree(pict_folder)
            print("Lösche alte Wallpaper...")

            shutil.copytree(file_path_wallpaper, pict_folder, symlinks=False, ignore=None, ignore_dangling_symlinks=False,
                            dirs_exist_ok=False)

            print("Kopiere neue Wallpaper...")

            shutil.make_archive(zip_file, 'zip', target_zip_folder)
            print('Komprimiere Dateien...')

            # Renaming the file
            os.rename('j-lawyer-client.zip', 'j-lawyer-client.jar')

            # move .jar File to target folder
            shutil.move(r'j-lawyer-client.jar',
                        f'{file_path_installation}/j-lawyer-client.jar')

            print("Räume auf")

            # remove temp folder
            shutil.rmtree(target_zip_folder)
            shutil.rmtree(file_path_wallpaper)

            print('Beseitige Spuren')
            print("Fertig!")

        except Exception as e:
            print(str(e))



