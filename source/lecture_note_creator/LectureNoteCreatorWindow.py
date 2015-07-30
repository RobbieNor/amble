# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('lecture_note_creator')
import datetime, os, imp, subprocess, re, shutil

from lecture_note_creator_lib import Window
from lecture_note_creator.AboutLectureNoteCreatorDialog import AboutLectureNoteCreatorDialog
from lecture_note_creator.PreferencesLectureNoteCreatorDialog import PreferencesLectureNoteCreatorDialog

# See lecture_note_creator_lib.Window.py for more details about how this class works
class LectureNoteCreatorWindow(Window):
    __gtype_name__ = "LectureNoteCreatorWindow"
    __programname__ = "lecture_note_creator"
    __startdatetime__ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    __programdir__ = os.path.expanduser("~") + "/." + __programname__
    __preferencesdir__ = __programdir__ + "/preferences"
    __applicationsdir__ = __programdir__ + "/applications"
    __templatesdir__ = __programdir__ + "/templates"
    __workspacedir__ = __programdir__ + "/workspace"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(LectureNoteCreatorWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutLectureNoteCreatorDialog
        self.PreferencesDialog = PreferencesLectureNoteCreatorDialog
    
        # Code for other initialization actions should be added here.


        #Initiaise TitleBox
        self.titlebox = self.builder.get_object("titlebox")

        #Initialise Designations
        self.datetime_button = self.builder.get_object("datetime_button")
        self.number_button = self.builder.get_object("number_button")
        self.datetimebox = self.builder.get_object("datetimebox")
        self.datetimebox.set_text(self.__startdatetime__)
        self.number_dial = self.builder.get_object("number_dial")

        #Initialise StatusBar
        self.main_statusbar = self.builder.get_object("main_statusbar")
        status_id = self.main_statusbar.get_context_id('startup')
        self.main_statusbar.push(status_id, "Welcome")        

        #Initialise ComboBoxes
        self.levelbox = self.builder.get_object("levelbox")
        self.modulebox = self.builder.get_object("modulebox")
        self.topicbox = self.builder.get_object("topicbox")
        self.typebox = self.builder.get_object("typebox")

        #Intialise ListStores
        self.clearlist = self.builder.get_object("clearlist")
        self.levels = self.builder.get_object("levels")      
        self.level1modules = self.builder.get_object("level1modules")
        self.level2modules = self.builder.get_object("level2modules")
        self.level3modules = self.builder.get_object("level3modules")
        self.level4modules = self.builder.get_object("level4modules")

        self.fop1topics = self.builder.get_object("fop1topics")
        self.dsiptopics = self.builder.get_object("dsiptopics")
        self.smatopics = self.builder.get_object("smatopics")
        self.smbtopics = self.builder.get_object("smbtopics")
        self.itptopics = self.builder.get_object("itptopics")

        self.fop2atopics = self.builder.get_object("fop2atopics")
        self.fop2btopics = self.builder.get_object("fop2btopics")
        self.lsandetopics = self.builder.get_object("lsandetopics")
        self.mmiptopics = self.builder.get_object("mmiptopics")
        self.sandgtopics = self.builder.get_object("sandgtopics")
        self.tp2topics = self.builder.get_object("tp2topics")

        self.fop3atopics = self.builder.get_object("fop3atopics")
        self.fop3btopics = self.builder.get_object("fop3btopics")
        self.lapprojtopics = self.builder.get_object("labprojtopics")
        self.ppstopics = self.builder.get_object("ppstopics")
        self.tp3topics = self.builder.get_object("tp3topics")
        self.teamprojtopics = self.builder.get_object("teamprojtopics")
        
        self.projecttopics = self.builder.get_object("projecttopics")
        self.alqtopics = self.builder.get_object("alqtopics")
        self.adv4topics = self.builder.get_object("adv4topics")
        self.parttheotopics = self.builder.get_object("parttheotopics")

        #Initiaise ComboBox dictionaries
        self.levels_dict = {'Level 1':self.level1modules, 'Level 2' : self.level2modules, 'Level 3' : self.level3modules, 'Level 4' : self.level4modules}
        self.level1_dict = {'Foundations of Physics 1' : self.fop1topics, 'Discovery Skills in Physics' : self.dsiptopics, 'Single Mathematics A' :self.smatopics, 'Single Mathematics B' : self.smbtopics  , 'Introduction to Programming': self.itptopics}
        self.level2_dict = {'Foundations of Physics 2A' : self.fop2atopics, 'Foundations of Physics 2B': self.fop2btopics, 'Laboratory Skills and Electronics' : self.lsandetopics, 'Mathematical Methods in Physics' : self.mmiptopics, 'Stars and Galaxies': self.sandgtopics, 'Theoretical Physics 2' : self.tp2topics}
        self.level3_dict = {'Foundations of Physics 3A' : self.fop3atopics, 'Foundations of Physics 3B': self.fop3btopics, 'Laboratory Project' : self.lapprojtopics, 'Physics Problem Solving' : self.ppstopics, 'Theoretical Physics 3' : self.tp3topics, 'Team Project' : self.teamprojtopics}
        self.level4_dict = {'Project' : self.projecttopics, 'Atoms, Lasers and Qubits' : self.alqtopics, 'Advanced Physics 4' : self.adv4topics, 'Particle Theory' : self.parttheotopics}       
        self.modules_dict = {'Level 1':self.level1_dict, 'Level 2' : self.level2_dict, 'Level 3' : self.level3_dict, 'Level 4' : self.level4_dict}

    #ComboBox Sanitisers
    def update_topicbox(self, module, level):
        self.topicbox.set_model(self.clearlist)
        module_dict = self.modules_dict[level]
        topics = module_dict[module]
        self.topicbox.set_model(topics)

    def update_modulebox(self, level):
        self.modulebox.set_model(self.clearlist) 
        self.topicbox.set_model(self.clearlist)
        self.modulebox.set_model(self.levels_dict[level])
        

    def on_modulebox_changed(self, widget):
        #Find Module            
        index = widget.get_active()
        model = widget.get_model()   
        module = model[index][0]
        #Find Level
        index = self.levelbox.get_active()
        model = self.levelbox.get_model()   
        level = model[index][0]
        self.update_topicbox(module, level)

    def on_levelbox_changed(self, widget):    
        index = widget.get_active()
        model = widget.get_model()   
        level = model[index][0]
        self.update_modulebox(level)

    def getComboActive(self, combobox):
        index = combobox.get_active()
        model = combobox.get_model()
        active = model[index][0]
        return active
        

    def constructNoteLocation(self, base_dir):
        level = self.getComboActive(self.levelbox)
        module = self.getComboActive(self.modulebox)
	    topic = self.getComboActive(self.topicbox)
        location = base_dir + '/' + level + '/' + module + '/' + topic
        return location


    def on_createnote_clicked(self,widget):
        #Create Program Script
        script = file(self.__workspacedir__ + "/script.sh",'w')
        script.write("#!/bin/bash\n\n")
        #Load Settings
        defaults = eval(open(self.__preferencesdir__ + "/defaults.conf",'r').read())
        default_values = eval(open(self.__preferencesdir__ + "/default_values.conf",'r').read())
        options = eval(open(self.__preferencesdir__ + "/options.conf",'r').read())
        course = eval(open(self.__preferencesdir__ + "/course.conf",'r').read())
        #Construct Note location
        location = self.constructNoteLocation(defaults['nbkloc_chooser'])   
        #Constuct Title
        if options['seperate_types_button'] == True:
              location = location + "/" + self.getComboActive(self.typebox)
        if os.path.exists(location) == False:
            os.makedirs(location)
        title = self.getComboActive(self.typebox) + " "


        active = [r for r in self.datetime_button.get_group() if r.get_active()][0]
        if self.builder.get_name(active) == "datetime_button":
            title = title + "(" + self.__startdatetime__ + ") "
        elif self.builder.get_name(active):
            title = title + str(int(self.number_dial.get_value())).zfill(2) + ' '
        else:
            print "wtf?!"
        title = title + "- " +str(self.titlebox.get_text())
        print title
        #Create Program Line    
        app_loc = self.__applicationsdir__ +"/" + str(default_values['application_chooser']) + ".py"
        application = imp.load_source('module.name', app_loc )
        path = location + '/' + title + application.getExtension()
        prog_line = application.createProgramLine(path)
        shutil.copy(self.__templatesdir__ + "/note" + application.getExtension(), path)
        script.write(prog_line + "\n")
        #script.write('test')
        




        print title
        script.close()
        #run script
        subprocess.call("chmod +x " + self.__programdir__ + "/script.sh", shell=True)
        subprocess.call(self.__programdir__ + "/script.sh", shell = True)

        
        
        
        
        
        

    
