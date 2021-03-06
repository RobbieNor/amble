# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
import simplejson as json
logger = logging.getLogger('lecture_note_creator')
import datetime
import os
import imp
import subprocess
import shutil

from amble_lib import Window
from amble.AboutAmbleDialog import AboutAmbleDialog
from amble.PreferencesAmbleDialog import PreferencesAmbleDialog

# See amble_lib.Window.py for more details about how this class works
class AmbleWindow(Window):
    __gtype_name__ = "AmbleWindow"

    __programname__ = "Amble"
    __startdatetime__ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    __programdir__ = os.path.expanduser("~") + "/Projects/amble"
    __preferencesdir__ = __programdir__ + "/preferences"
    __programsdir__ = __programdir__ + "/programs"
    __templatesdir__ = __programdir__ + "/templates"
    __workspacedir__ = __programdir__ + "/workspace"
    __otherdir__ = __programdir__ + "/other"
    __compressiondir__ = __programdir__ + "/compression"
    __config__ = __preferencesdir__ + "/config.json"
    __nullcombo_string__ = 'Custom...'

    # Dialog Actions
    def changeRoutine(self, widget):
        routine = widget.get_label()
        with open(self.__config__, 'r') as json_data:
            data = json.loads(json_data.read())
        data['Defaults']['Backup Routine'] = routine
        with open(self.__config__,'w') as json_data:
            json_data.write(json.dumps(data, sort_keys=True, indent=4))
        self.mnu_bkp_routine.set_label("   Routine: " + routine)

    def switchModes(self,arg1, arg2, arg3):
        current_mode = self.mode_notebook.get_current_page()
        if current_mode == 0:
            index = len(self.type_list)
            self.typebox.set_active(index)
            self.prefixbox.hide()
            self.typebox.hide()
            self.titlebox.set_placeholder_text("Filename")
        elif current_mode == 1:
            self.prefixbox.show()
            index = len(self.type_list) - 1
            self.typebox.show()
            self.typebox.set_active(index)
            self.titlebox.set_placeholder_text("Title")

    def updateMenuItem(self, widget):
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            self.mnu_nbk_path.set_label("   Path: " + data['Defaults']['Notebook Location'])
            self.mnu_bkp_path.set_label("   Path: " + data['Defaults']['Backup Location'])
            self.mnu_bkp_routine.set_label("   Routine: " + data['Defaults']['Backup Routine'])
            set_program = data['Other']['Programs'][choices['Program']]
            self.mnu_save_raw.set_active(data['Settings'][set_program]['Save']['Raw'])
            self.mnu_save_pdf.set_active(data['Settings'][set_program]['Save']['PDF'])
            self.mnu_bkp_raw.set_active(data['Settings'][set_program]['Backup']['Raw'])
            self.mnu_bkp_pdf.set_active(data['Settings'][set_program]['Backup']['PDF'])
            self.mnu_gen_html.set_active(data['Settings']['Other']['Generate HTML'])
            self.mnu_comp_bkp.set_active(data['Settings']['Other']['Compress Backups'])
            self.mnu_sep_type.set_active(data['Settings']['Other']['Seperate by Type'])
            self.mnu_bkp_nbk.set_active(data['Settings']['Other']['Backup to Notebook'])

    def updateSaveBkp(self, widget):
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            set_program = self.getComboActive(self.programbox)
            self.mnu_save_raw.set_active(data['Settings'][set_program]['Save']['Raw'])
            self.mnu_save_pdf.set_active(data['Settings'][set_program]['Save']['PDF'])
            self.mnu_bkp_raw.set_active(data['Settings'][set_program]['Backup']['Raw'])
            self.mnu_bkp_pdf.set_active(data['Settings'][set_program]['Backup']['PDF'])


    def runFolderChooser(self, title):
        chooser = Gtk.FileChooserDialog(
            title="Select Notebook Directory.",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK)
        )
        ok = chooser.run()
        folder = None
        if ok:
            folder = chooser.get_current_folder()
        chooser.destroy()
        return ok, folder

    def editConfig(self, value, position_list):
        with open(self.__config__,'r') as json_data:
            data = json.loads(json_data.read())
        assignment_code = "data"
        for position in position_list:
            assignment_code = assignment_code + "['" + position + "']"
        assignment_code = assignment_code + " = value"
        exec(assignment_code)
        with open(self.__config__, 'w') as json_data:
            json_data.write(json.dumps(data, sort_keys=True, indent=4))

    def on_mnu_edit_config_activate(self, widget):
        subprocess.call('xdg-open "' + self.__config__ + '"' , shell=True)

    def on_mnu_change_nbk_activate(self, widget):
        response = self.runFolderChooser("Select Notebook Location.")
        if response[0] == -5:
            with open(self.__config__, 'r') as json_data:
                data = json.loads(json_data.read())
            data['Defaults']['Notebook Location'] = response[1]
            with open(self.__config__, 'w') as json_data:
                json_data.write(json.dumps(data, sort_keys=True, indent=4))
            self.updateMenuItem(widget)

    def on_mnu_change_bkp_path_activate(self, widget):
        response = self.runFolderChooser("Select Backup Location.")
        if response[0] == -5:
            with open(self.__config__, 'r') as json_data:
                data = json.loads(json_data.read())
            data['Defaults']['Backup Location'] = response[1]
            with open(self.__config__, 'w') as json_data:
                json_data.write(json.dumps(data, sort_keys=True, indent=4))
            self.updateMenuItem(widget)

    def on_mnu_save_raw_toggled(self, widget):
        value = self.mnu_save_raw.get_active()
        set_program = self.getComboActive(self.programbox)
        position_list = ['Settings',set_program, 'Save', 'Raw']
        self.editConfig(value, position_list)

    def on_mnu_save_pdf_toggled(self, widget):
        value = self.mnu_save_pdf.get_active()
        set_program = self.getComboActive(self.programbox)
        position_list = ['Settings',set_program, 'Save', 'PDF']
        self.editConfig(value, position_list)

    def on_mnu_bkp_raw_toggled(self, widget):
        value = self.mnu_bkp_raw.get_active()
        set_program = self.getComboActive(self.programbox)
        position_list = ['Settings',set_program, 'Backup', 'Raw']
        self.editConfig(value, position_list)

    def on_mnu_bkp_pdf_toggled(self, widget):
        value = self.mnu_bkp_pdf.get_active()
        set_program = self.getComboActive(self.programbox)
        position_list = ['Settings',set_program, 'Backup', 'PDF']
        self.editConfig(value, position_list)

    def on_mnu_gen_html_toggled(self, widget):
        value = self.mnu_gen_html.get_active()
        position_list = ['Settings', 'Other', 'Generate HTML']
        self.editConfig(value, position_list)

    def on_mnu_comp_bkp_toggled(self, widget):
        value = self.mnu_comp_bkp.get_active()
        position_list = ['Settings', 'Other', 'Compress Backups']
        self.editConfig(value, position_list)

    def on_mnu_bkp_nbk_toggled(self, widget):
        value = self.mnu_bkp_nbk.get_active()
        position_list = ['Settings', 'Other', 'Backup to Notebook']
        self.editConfig(value, position_list)

    def on_mnu_sep_type_toggled(self, widget):
        value = self.mnu_sep_type.get_active()
        position_list = ['Settings', 'Other', 'Seperate by Type']
        self.editConfig(value, position_list)

    def on_mnu_clear_default_activate(self, widget):
        with open(self.__config__, 'r') as json_data:
            data = json.loads(json_data.read())
            data['Defaults']['Choices Saved'] = False
            with open(self.__config__, 'w') as json_data:
                json_data.write(json.dumps(data, sort_keys=True, indent=4))
        self.main_statusbar.push(self.status_id, "Defaults Cleared.")

    def on_mnu_set_default_activate(self, widget):
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            data['Defaults']['Choices']['Top'] = self.topbox.get_active()
            data['Defaults']['Choices']['Mid'] = self.midbox.get_active()
            data['Defaults']['Choices']['Bottom'] = self.bottombox.get_active()
            data['Defaults']['Choices']['Type'] = self.typebox.get_active()
            data['Defaults']['Choices']['Program'] = self.programbox.get_active()
            data['Defaults']['Choices']['Folder'] = self.folderbox.get_text()
            data['Defaults']['Choices']['Prefix'] = self.prefixbox.get_text()
            data['Defaults']['Choices']['Title'] = self.titlebox.get_text()
            desig_index = None
            for i in range(len(self.designations)):
                if self.designations[i].get_active() is True:
                    desig_index = i
            data['Defaults']['Choices']['Designation'] = desig_index
            data['Defaults']['Choices Saved'] = True
            with open(self.__config__, 'w') as json_data:
                json_data.write(json.dumps(data, sort_keys=True, indent=4))
        self.main_statusbar.push(self.status_id, "Defaults Saved.")


    def on_mnu_regen_html_activate(self, widget):
        self.generateHTML()
        self.main_statusbar.push(self.status_id, "HTML File Regenerated.")

    # Combobox Update Logic
    def update_bottombox(self, top_item, mid_item):
        if mid_item == "":
            self.bottom_list.clear()
            self.bottom_list.append("")
            self.bottombox.set_active(0)
        else:
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                self.bottom_list.clear()
                bottom_entries = sorted(data['Directory']['Tree'][top_item]['Children'][mid_item]['Children'].keys(), key=lambda x: data['Directory']['Tree'][top_item]['Children'][mid_item]['Children'][x]['Position'])
                for i in range(len(bottom_entries)):
                    self.bottom_list.append()
                    self.bottom_list[i][0] = bottom_entries[i]
                self.bottom_list.prepend()
                self.bottom_list[0][0] = ""
                self.bottombox.set_active(0)

    def update_midbox(self, top_item):
        if top_item == "":
            self.mid_list.clear()
            self.mid_list.append("")
            self.midbox.set_active(0)
            self.bottom_list.clear()
            self.bottom_list.append("")
            self.bottombox.set_active(0)
        else:
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                self.bottom_list.clear()
                self.mid_list.clear()
                mid_entries = sorted(
                    data['Directory']['Tree'][top_item]['Children'].keys(),
                    key=lambda x: data['Directory']['Tree'][top_item]['Children'][x]['Position']
                )
                for i in range(len(mid_entries)):
                    self.mid_list.append()
                    self.mid_list[i][0] = mid_entries[i]
                self.mid_list.prepend()
                self.mid_list[0][0] = ""
                self.midbox.set_active(0)

    def loadSavedChoices(self):
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            if data['Defaults']['Choices Saved'] is True:
                choices = data['Defaults']['Choices']
                self.topbox.set_active(choices['Top'])
                self.midbox.set_active(choices['Mid'])
                self.bottombox.set_active(choices['Bottom'])
                self.typebox.set_active(choices['Type'])
                self.folderbox.set_text(choices['Folder'])
                self.prefixbox.set_text(choices['Prefix'])
                self.titlebox.set_text(choices['Title'])
                self.programbox.set_active(choices['Program'])
                self.designations[choices['Designation']].set_active(True)
                set_program = data['Other']['Programs'][choices['Program']]
                self.mnu_save_raw.set_active(data['Settings'][set_program]['Save']['Raw'])
                self.mnu_save_pdf.set_active(data['Settings'][set_program]['Save']['PDF'])
                self.mnu_bkp_raw.set_active(data['Settings'][set_program]['Backup']['Raw'])
                self.mnu_bkp_pdf.set_active(data['Settings'][set_program]['Backup']['PDF'])
                self.mnu_gen_html.set_active(data['Settings']['Other']['Generate HTML'])
                self.mnu_comp_bkp.set_active(data['Settings']['Other']['Compress Backups'])
                self.mnu_sep_type.set_active(data['Settings']['Other']['Seperate by Type'])
                self.mnu_bkp_nbk.set_active(data['Settings']['Other']['Backup to Notebook'])

    # Button Responses
    def on_midbox_changed(self, widget):
        try:
            # Get Current mid_item
            index = widget.get_active()
            model = widget.get_model()
            mid_item = model[index][0]
            # Get Current top_item
            index = self.topbox.get_active()
            model = self.topbox.get_model()
            top_item = model[index][0]
            self.update_bottombox(top_item, mid_item)
        except:
            pass

    def on_topbox_changed(self, widget):
        index = widget.get_active()
        model = widget.get_model()
        top_item = model[index][0]
        self.update_midbox(top_item)

    def getComboActive(self, combobox):
        index = combobox.get_active()
        model = combobox.get_model()
        active = model[index][0]
        return active

    def on_typebox_changed(self, widget):
        # Show manual controls if type set to null_string
        visibility = self.getComboActive(self.typebox) == self.__nullcombo_string__
        self.folderbox.set_visible(visibility)
        self.prefixbox.set_visible(visibility)

    def on_programbox_changed(self, widget):
        self.updateSaveBkp(widget)

    def generateHTML(self):
        genHTML = imp.load_source('other', self.__otherdir__ + "/gen_html.py")
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            defaults = data['Defaults']
            nbk_path = defaults['Notebook Location']
            html_title = os.path.basename(os.path.normpath(nbk_path))
        genHTML.run(html_title, nbk_path, nbk_path)

    def constructFileLocation_Create(self):
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            defaults = data['Defaults']
            directory = data['Directory']
            settings = data['Settings']
            base_dir = defaults["Notebook Location"]
            top = self.getComboActive(self.topbox)
            mid = self.getComboActive(self.midbox)
            bottom = self.getComboActive(self.bottombox)
            dirs = [top, mid, bottom]
            location = base_dir
            for item in dirs:
                if item is not None:
                    print "item: " + str(item)
                    location = location + '/' + item
            manual = self.getComboActive(self.typebox) == self.__nullcombo_string__
            if manual:
                location = location + '/' + self.folderbox.get_text()
            elif settings['Other']['Seperate by Type'] is True:
                location = location + '/' + directory['Types'][self.getComboActive(self.typebox)]
            else:
                pass
            if os.path.exists(location) is False:
                os.makedirs(location)
            return location

    def constructFilename_Create(self):
        manual = self.getComboActive(self.typebox) == self.__nullcombo_string__
        seperator = "-"
        prefix = ""
        if manual and self.prefixbox.get_text() == "":
            pass
        elif manual:
            prefix = self.prefixbox.get_text() + " "
        else:
            prefix = self.getComboActive(self.typebox) + " "
        designation = ""
        desig_active = [r for r in self.datetime_button.get_group() if r.get_active()][0]
        if self.builder.get_name(desig_active) == "datetime_button":
            designation = self.__startdatetime__ + " " + seperator + " "
        elif self.builder.get_name(desig_active) == "number_button":
            designation = str(int(self.number_dial.get_value())).zfill(2) + " " + seperator + " "
        elif self.builder.get_name(desig_active) == "none_button":
            if manual and self.prefixbox.get_text() == "":
                designation = ""
            else:
                designation = "- "
        title = self.titlebox.get_text()
        filename = prefix + designation + title
        return filename

    def constructFileLocation_Sort(self):
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            defaults = data['Defaults']
            base_dir = defaults["Notebook Location"]
            top = self.getComboActive(self.topbox)
            mid = self.getComboActive(self.midbox)
            bottom = self.getComboActive(self.bottombox)
            dirs = [top, mid, bottom]
            location = base_dir
            for item in dirs:
                if item != None:
                    location = location + '/' + item
            location = location + '/' + self.folderbox.get_text()
            if os.path.exists(location) is False:
                os.makedirs(location)
            return location

    def constructFilename_Sort(self):
        return self.titlebox.get_text()

    def on_sort_file_clicked(self, widget):
        file_path = self.sort_file_chooser.get_filename()
        if file_path is None:
            self.main_statusbar.push(self.status_id, "No File Selected.")
        else:
            file_extension = os.path.splitext(file_path)[1]
            filename = self.constructFilename_Sort()
            location = self.constructFileLocation_Sort()
            new_file_path = location + '/' + filename + file_extension
            shutil.copy(file_path, new_file_path)
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                if data['Settings']['Other']['Generate HTML'] is True:
                        self.generateHTML()
                self.main_statusbar.push(self.status_id, "File Sorted.")

    def on_createfile_clicked(self,widget):
        # Load Config File
        with open(self.__config__) as json_data:
            data = json.loads(json_data.read())
            defaults = data['Defaults']
            settings = data['Settings']
            set_program = self.getComboActive(self.programbox)
            # Construct Note Location and Create Path
            location = self.constructFileLocation_Create()
            # Construct Filename
            filename = self.constructFilename_Create()
            # Create Program Command
            prog_path = self.__programsdir__ + "/" + self.getComboActive(self.programbox) + ".py"
            program = imp.load_source('programs', prog_path)
            file_path = location + '/' + filename + program.getExtension()
            prog_line = program.createProgramLine(file_path)
            shutil.copy(self.__templatesdir__ + "/template" + program.getExtension(), file_path)
            self.main_statusbar.push(self.status_id, "File Created and open. Awaiting close...")
            subprocess.call(prog_line, shell=True)
            # Save and Backup File according to preferences
            if settings[set_program]['Save']['PDF'] is True or settings[set_program]['Backup']['PDF'] is True:
                genpdf_line = program.createPDFLine(file_path)
                subprocess.call(genpdf_line, shell=True)
            backup_list = []
            if settings[set_program]['Backup']['Raw'] is True:
                backup_list.append(program.getExtension())
            if settings[set_program]['Backup']['PDF'] is True:
                backup_list.append('.pdf')
            backup_file = None
            if settings['Other']['Compress Backups'] is True:
                bkp_com = self.__compressiondir__ +"/" + defaults['Backup Routine'] + ".py"
                compressor = imp.load_source('compressions', bkp_com)
                backup_file = compressor.compress(backup_list, location, filename)
            else:
                os.makedirs(location + "/" + filename)
                for extension in backup_list:
                    shutil.copy(location + "/" + filename + extension, location + "/"+ filename + "/" + filename + extension)
                backup_file = location + "/" + filename
            if settings['Other']['Backup to Notebook'] is True:
                try:
                    os.makedirs(location + "/.backup")
                except:
                    pass
                shutil.move(backup_file, location + "/.backup/")
            else:
                bkploc = defaults['Backup Location']
                day = datetime.datetime.now().strftime("%Y-%m-%d")
                try:
                    os.mkdir(bkploc + "/" + day)
                except:
                    pass
                shutil.move(backup_file, bkploc + "/" + day + "/")
            if settings[set_program]['Save']['Raw'] is False:
                os.remove(file_path)
            if settings[set_program]['Save']['PDF'] is False:
                filename, file_extension = os.path.splitext(file_path)
                os.remove(filename + ".pdf")
            if settings['Other']['Generate HTML'] is True:
                self.generateHTML()
            self.main_statusbar.push(self.status_id, "Note Created.")

    def finish_initializing(self, builder): #  pylint: disable=E1002
        """Set up the main window"""
        super(AmbleWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutAmbleDialog

        # Initiaise Boxes
        self.titlebox = self.builder.get_object("titlebox")
        self.folderbox = self.builder.get_object("folderbox")
        self.prefixbox = self.builder.get_object("prefixbox")

        # Initialise Designations
        self.datetime_button = self.builder.get_object("datetime_button")
        self.number_button = self.builder.get_object("number_button")
        self.datetimebox = self.builder.get_object("datetimebox")
        self.datetimebox.set_text(self.__startdatetime__)
        self.number_dial = self.builder.get_object("number_dial")
        self.none_button = self.builder.get_object("none_button")
        self.designations = [self.none_button, self.datetime_button, self.number_button]

        #  Initialise StatusBar
        self.main_statusbar = self.builder.get_object("main_statusbar")
        self.status_id = self.main_statusbar.get_context_id('startup')

        # Initialise ComboBoxes
        self.topbox = self.builder.get_object("topbox")
        self.midbox = self.builder.get_object("midbox")
        self.bottombox = self.builder.get_object("bottombox")
        self.typebox = self.builder.get_object("typebox")
        self.programbox = self.builder.get_object("programbox")

        # Initialise Mode Notebook
        self.mode_notebook = self.builder.get_object("mode_notebook")
        self.mode_notebook.connect("switch-page", self.switchModes)
        self.sort_file_chooser = self.builder.get_object("sort_file_chooser")

        # Intialise ListStores
        self.blank_list = self.builder.get_object("blank_list")
        self.top_list = self.builder.get_object("top_list")
        self.mid_list = self.builder.get_object("mid_list")
        self.bottom_list = self.builder.get_object("bottom_list")
        self.type_list = self.builder.get_object("type_list")
        self.program_list = self.builder.get_object("program_list")
        self.mnu_routine_list = self.builder.get_object("mnu_routine_list")

        # Initialise Labels
        self.top_label = self.builder.get_object("top_label")
        self.mid_label = self.builder.get_object("mid_label")
        self.bottom_label = self.builder.get_object("bottom_label")
        self.heading_labels = [self.top_label, self.mid_label, self.bottom_label]

        #  Initialise File MenuItems
        self.mnu_regen_html = self.builder.get_object("mnu_regen_html")

        # Initialise Edit MenuItems
        self.mnu_edit_format = self.builder.get_object("mnu_edit_format")
        self.mnu_edit_directory = self.builder.get_object("mnu_edit_directory")
        self.mnu_edit_programs = self.builder.get_object("mnu_edit_routines")
        self.mnu_edit_routines = self.builder.get_object("mnu_edit_routines")
        self.mnu_edit_config = self.builder.get_object("mnu_edit_config")

        # Initialise Default MenuItems
        self.mnu_nbk_path = self.builder.get_object("mnu_nbk_path")
        self.mnu_change_nbk = self.builder.get_object("mnu_change_nbk")
        self.mnu_bkp_routine = self.builder.get_object("mnu_bkp_routine")
        self.mnu_bkp_path = self.builder.get_object("mnu_bkp_path")
        self.mnu_change_routine = self.builder.get_object("mnu_change_routine")
        self.mnu_change_bkp_path = self.builder.get_object("mnu_change_bkp_path")
        self.mnu_set_default = self.builder.get_object("mnu_set_default")
        self.mnu_clear_default = self.builder.get_object("mnu_clear_defaults")

        # Initialise Settings MenuItems
        self.mnu_save_raw = self.builder.get_object("mnu_save_raw")
        self.mnu_save_pdf = self.builder.get_object("mnu_save_pdf")
        self.mnu_bkp_raw = self.builder.get_object("mnu_bkp_raw")
        self.mnu_bkp_pdf = self.builder.get_object("mnu_bkp_pdf")
        self.mnu_gen_html = self.builder.get_object("mnu_gen_html")
        self.mnu_comp_bkp = self.builder.get_object("mnu_comp_bkp")
        self.mnu_bkp_nbk = self.builder.get_object("mnu_bkp_nbk")
        self.mnu_sep_type = self.builder.get_object("mnu_sep_type")


        # Initialisation Functions
        def initialiseListStores(self):
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                # Initialise Headings
                headings = data['Directory']['Headings']
                for i in range(len(headings)):
                    self.heading_labels[i].set_label(headings[i])
                # Initialise Types
                types = sorted(data['Directory']['Types'].keys())
                for i in range(len(types)):
                    self.type_list.append()
                    self.type_list[i][0] = types[i]
                self.type_list.append()
                self.type_list[-1][0] = self.__nullcombo_string__
                null_index = len(types)
                self.typebox.set_active(null_index)
                # Initialise Top Box
                top_entries = sorted(data['Directory']['Tree'].keys(), key=lambda x: data['Directory']['Tree'][x]['Position'])
                for i in range(len(top_entries)):
                    self.top_list.append()
                    self.top_list[i][0] = top_entries[i]
                self.top_list.prepend()
                self.top_list[0][0] = ""
                self.topbox.set_active(0)

        def initialiseProgramList(self):
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                # Initialise Program List
                programs = sorted(data['Other']['Programs'])
                for i in range(len(programs)):
                    self.program_list.append()
                    self.program_list[i][0] = programs[i]
                self.programbox.set_active(0)

        def initialiseMenuItems(self):
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                self.mnu_nbk_path.set_label("   Path: " + data['Defaults']['Notebook Location'])
                self.mnu_bkp_path.set_label("   Path: " + data['Defaults']['Backup Location'])
                self.mnu_bkp_routine.set_label("   Routine: " + data['Defaults']['Backup Routine'])

        def initialiseRoutineList(self):
            with open(self.__config__) as json_data:
                data = json.loads(json_data.read())
                routines = sorted(data['Other']['Backup Routines'])
                for i in range(len(routines)):
                    menu_item = Gtk.MenuItem(routines[i])
                    menu_item.connect("activate", self.changeRoutine)
                    menu_item.show()
                    self.mnu_routine_list.append(menu_item)

        # Run Initialisation Functions
        initialiseListStores(self)
        initialiseProgramList(self)
        initialiseMenuItems(self)
        initialiseRoutineList(self)
        self.loadSavedChoices()
