# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.lecture-note-creator.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

from locale import gettext as _

import logging, os, shutil
logger = logging.getLogger('lecture_note_creator')

from lecture_note_creator_lib.PreferencesDialog import PreferencesDialog

class PreferencesLectureNoteCreatorDialog(PreferencesDialog):
    __programname__ = "note_organiser"
    __gtype_name__ = "PreferencesLectureNoteCreatorDialog"
    __programdir__ = os.path.expanduser("~") + "/." + __programname__
    __preferencesdir__ = __programdir__ + "/preferences"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesLectureNoteCreatorDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        #settings = Gio.Settings("net.launchpad.lecture-note-creator")
        #widget = self.builder.get_object('example_entry')
        #settings.bind("example", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        # Code for other initialization actions should be added here.

        self.pref_statusbar = self.builder.get_object("pref_statusbar")
        self.status_id = self.pref_statusbar.get_context_id('startup')
        self.pref_statusbar.push(self.status_id, "Welcome") 

        #Initialise Defaults
        self.application_chooser = self.builder.get_object("application_chooser")
        self.nbkloc_chooser = self.builder.get_object("nbkloc_chooser")
        self.bkploc_chooser = self.builder.get_object("bkploc_chooser")
        self.bkpcom_chooser = self.builder.get_object("bkpcom_chooser")


        #Initialise Options
        self.save_xoj_button = self.builder.get_object("save_xoj_button")
        self.save_pdf_button = self.builder.get_object("save_pdf_button")
        self.gen_html_button = self.builder.get_object("gen_html_button")
        self.bkp_xoj_button = self.builder.get_object("bkp_xoj_button")
        self.bkp_pdf_button = self.builder.get_object("bkp_pdf_button")
        self.bkp_html_button = self.builder.get_object("bkp_html_button")
        self.compress_button = self.builder.get_object("compress_button")
        self.html_index_button = self.builder.get_object("html_index_button")
        self.seperate_types_button = self.builder.get_object("seperate_types_button")

        self.options_list = [self.save_xoj_button, self.save_pdf_button, self.gen_html_button, self.bkp_xoj_button, self.bkp_pdf_button, self.bkp_html_button, self.compress_button, self.html_index_button, self.seperate_types_button]


        #PLACEHOLDER: Initialise Course


        def loadPreferences(self):
            self.pref_statusbar.push(self.status_id, "Loading preferences...") 
            try:
                print 0
                defaults = eval(open(self.__preferencesdir__ + "/defaults.conf",'r').read())
                print 0.2
                options = eval(open(self.__preferencesdir__ + "/options.conf",'r').read())
                print 0.3
                course = eval(open(self.__preferencesdir__ + "/course.conf",'r').read())             
                for default, value in defaults.iteritems():
                    print value
                    chooser = "self." + default          
                    if default in ['application_chooser','bkpcom_chooser']:
                        cmd = chooser + ".set_active(value)"
                        print cmd   
                        eval(chooser + ".set_active(value)")
                        print 2
                    else:
                        print 2.5
                        eval(chooser + ".set_current_folder(value)")
                for option, value in options.iteritems():
                    print 3
                    button = "self." + option
                    eval(button + ".set_active(value)")
                #Loop through course info here
                self.pref_statusbar.push(self.status_id, "Preferences Loaded") 
            except:
                print "oh?"


        loadPreferences(self)
            


    def getCourse(self):
        return {0:0}

    def getOptions(self):
        options = {}
        for button in self.options_list:
            options[self.builder.get_name(button)] = button.get_active()
        return options
            
        

    def getDefaults(self):
        defaults = {}
        default_values = {}
        #Get Application
        index = int(self.application_chooser.get_active())   
        defaults['application_chooser'] = index     
        model = self.application_chooser.get_model()
        default_values['application_chooser'] = model[index][0]
        #Get Notebook Location
        defaults['nbkloc_chooser'] = self.nbkloc_chooser.get_filename()
        #Get Backup Location
        defaults['bkploc_chooser'] = self.bkploc_chooser.get_filename()
        #Get Backup Command
        index = int(self.bkpcom_chooser.get_active())
        model = self.bkpcom_chooser.get_model()
        defaults['bkpcom_chooser'] = index
        default_values['bkpcom_chooser'] = model[index][0]
        return defaults, default_values
        
        

    def on_saveprefs_clicked(self, widget):
        errors = []
        self.pref_statusbar.push(self.status_id, "Saving....") 
        #Setup Preferences Directory 
        if os.path.exists(self.__preferencesdir__):
            shutil.rmtree(self.__preferencesdir__)
        os.mkdir(self.__preferencesdir__)
        default_conf = file(self.__preferencesdir__ + "/defaults.conf",'w')
        default_values_conf = file(self.__preferencesdir__ + "/default_values.conf",'w')
        options_conf = file(self.__preferencesdir__ + "/options.conf",'w')
        course_conf = file(self.__preferencesdir__ + "/course.conf",'w')
        defaults, default_values = self.getDefaults()
        options = self.getOptions()
        course = self.getCourse()
        #TestSanityBefore Saving?!
        default_conf.write(str(defaults))       
        default_values_conf.write(str(default_values))
        options_conf.write(str(options))
        course_conf.write(str(course))
        default_conf.close()
        default_values_conf.close()
        options_conf.close()
        course_conf.close()
        self.pref_statusbar.push(self.status_id, "Save Complete") 
        
        
        


        
        
        #Test to see if preferences file exists, if not, create it
        #Create 3 different files, one for each page. i.e. defaults.cfg, options.cfg, course.cfg
        #Pull active text from all preferences boxes and save to these files



