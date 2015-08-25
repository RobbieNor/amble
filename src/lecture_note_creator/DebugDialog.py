# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from gi.repository import Gtk # pylint: disable=E0611

from lecture_note_creator_lib.helpers import get_builder

import gettext, DebugDialog, os
from gettext import gettext as _
gettext.textdomain('lecture-note-creator')

class DebugDialog(Gtk.Dialog):
    __gtype_name__ = "DebugDialog"
    __programdir__ = os.path.expanduser("~") + "/Documents/Programs/Git Repositories/lecture-note-creator"
    __preferencesdir__ = __programdir__ + "/preferences"
    __config__ = __preferencesdir__ + "/config.json"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated DebugDialog object.
        """
        builder = get_builder('DebugDialog')
        new_object = builder.get_object('debug_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a DebugDialog object with it in order to
        finish initializing the start of the new DebugDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

        self.debug_log_textview = self.builder.get_object("debug_log_textview")
        self.debug_config_textview = self.builder.get_object("debug_config_textview")


        #Initialise Log Dialog Box
        '''
        fin = open(self.__preferencesdir__ + "/defaults.conf","r")
        text = fin.read()
        fin.close()
        self.debug_defaults_textview.set_sensitive(False)
        buff = self.debug_defaults_textview.get_buffer()
        buff.set_text(text)
        buff.set_modified(False)
        self.debug_defaults_textview.set_sensitive(True)'''

        #Initialise Settings Dialog Box
        fin = open(self.__config__,"r")
        text = fin.read()
        fin.close()
        self.debug_config_textview.set_sensitive(False)
        buff = self.debug_config_textview.get_buffer()
        buff.set_text(text)
        buff.set_modified(False)
        self.debug_config_textview.set_sensitive(True)


    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns Gtk.ResponseType.CANCEL for run()
        """
        pass


if __name__ == "__main__":
    dialog = DebugDialog()
    dialog.show()
    Gtk.main()
