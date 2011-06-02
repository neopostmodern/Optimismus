#!/usr/bin/env python
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <mrs_sheep@web.de> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you
# think
# this stuff is worth it, you can buy me a beer in return mrs_sheep
# ----------------------------------------------------------------------------
#

#    This file is part of Optimismus.
#
#    Optimismus is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Optimismus is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#   
#    You should have received a copy of the GNU General Public License
#    along with Optimismus.  If not, see <http://www.gnu.org/licenses/>.
#


import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import subprocess
import os.path

#configuration
path = ""
arch = ""

class AppIndicatorExample:
    def __init__(self):
        readconf() # get settings
        
	print("STARTING OPTIMISMUS by MRS_SHEEP based on BUMBLEBEE by MrMEEE")
        self.ind = appindicator.Indicator ("bumblebee-applet",
                "indicator-messages", appindicator.CATEGORY_HARDWARE)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon ("indicator-messages-new")
        self.ind.set_icon("../bin/icon/nvidia.png")

        

        # create a menu
        self.menu = gtk.Menu()

        # create items for the menu:

        gpu = gtk.CheckMenuItem("Discrete Graphics") #switch on/off
        gpu.show()
        gpu.connect("activate", self.switch)
        self.menu.append(gpu)

        submenu = gtk.Menu() #prefered apps
        subitem = gtk.MenuItem("glxgears")
        subitem.connect("activate", self.glxgears)
        subitem.show()
        submenu.append(subitem)
        for i in range(0, 10):
            subitem = gtk.MenuItem("Preferred App #%d" % (i+1))
            subitem.show()
            submenu.append(subitem)
        submenu.show()
        appmenu = gtk.MenuItem("Preferred Apps")
        appmenu.set_submenu(submenu)
        appmenu.show()
        self.menu.append(appmenu)

	
        about = gtk.MenuItem("Preferences/About")
	about.connect("activate", self.about_box)
        about.show()
        self.menu.append(about)

        quit = gtk.ImageMenuItem(gtk.STOCK_QUIT) #quit-item
        quit.connect("activate", self.quit)
        quit.show()
        self.menu.append(quit)

        self.menu.show()

        self.ind.set_menu(self.menu)

    def quit(self, widget, data=None):
        gtk.main_quit()

    def switch(self, widget, data=None):
        if widget.get_active():
            subprocess.call(["bash " + path + "bumblebee-enablecard",""],shell=True)
        else :
            subprocess.call(["bash " + path + "bumblebee-disablecard",""],shell=True)

    def glxgears(self, widget, data=None):
        subprocess.call(["optirun64 glxgears", ""],shell=True)

    def about_box(self, widget, data=None):
	dialog = gtk.MessageDialog(None, type=gtk.MESSAGE_INFO,buttons=gtk.BUTTONS_NONE,message_format="Preferences/About")
	dialog.format_secondary_text("This is Optimus by mrs_sheep. \n It is based on bumblebee by MrMEEE. \n The configuration can (by now) only be set thorugh the config file!")
	dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
	dialog.run()
	dialog.destroy()

def readconf():
    print "read config..."
    conf = open('../optimismus.conf', 'r')
    conf.readline() 					#skip introduction
    conf.readline() 					#skip title
    arch = conf.readline() 				#read architecture
    arch = arch.replace("\r","")			#remove linebreak
    arch = arch.replace("\n","")
    if ((arch == "64") or (arch == "32")):		#check architecure
    	print "architecture set to " + arch +  " [OK]"
    else:
	print "corrupt architecture: " + arch + " [failed]"
    conf.readline() 					#skip title
    path = conf.readline() 				#read path to bumblebee
    path = path.replace("\r","")			#remove linebreak
    path = path.replace("\n","")
    if (os.path.isfile(path + "optirun32")): 		#check if folder is correct
	print "bumblebee-path is set to " + path + " [OK]"
    else:
        print "bumblebee-path is corrupt (" + path + ") [failed]"
    conf.close()


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    indicator = AppIndicatorExample()
    main()
