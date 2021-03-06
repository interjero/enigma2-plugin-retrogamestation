from Components.config import config, ConfigSubsection, ConfigDirectory
from Components.Language import language

from ..Emulator import EmulationHelper
from ..plugin import emulators

config.plugins.retrogamestation.snes = ConfigSubsection()
config.plugins.retrogamestation.snes.romlocation = ConfigDirectory(default="/media/")

class Snes(EmulationHelper):
	name = _("Snes9x")
	description = _("Super Nintendo")
	location = config.plugins.retrogamestation.snes.romlocation
	pattern = "^.*\.(zip|smc|SMC|sfc|SFC)"
	cmd = "/usr/bin/snes9x-start"
	icon = "snes/snes.svg"
	packageName = "snes9x-sdl"

emulators.append(Snes())

""" INIT """
from os import path as os_path
from os import mkdir as os_mkdir
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, copyfile
if not os_path.exists("/root/.snes9x/snes9x.conf"):
	print "[Snes]: config  /root/.snes9x/snes9x.conf not found creating defaults..."
	if not os_path.exists("/root/.snes9x"):
		os_mkdir("/root/.snes9x")
		os_mkdir("/root/.snes9x/rom")
	copyfile(resolveFilename(SCOPE_PLUGINS, "Extensions/RetroGameStation/snes/snes9x.conf.default"), "/root/.snes9x/snes9x.conf")
