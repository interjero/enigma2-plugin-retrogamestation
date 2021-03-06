from Components.config import config, ConfigSubsection, ConfigDirectory

from ..Emulator import EmulationHelper
from ..plugin import emulators

config.plugins.retrogamestation.dgen = ConfigSubsection()
config.plugins.retrogamestation.dgen.romlocation = ConfigDirectory(default="/media/")

class Dgen(EmulationHelper):
	name = _("Dgen")
	description = _("Sega Genesis")
	location = config.plugins.retrogamestation.dgen.romlocation
	pattern = "^.*\.(MD|md|ZIP|zip|32x|32X)"
	cmd = "/usr/bin/dgen-start"
	icon = "dgen/dgen.png"
	packageName = "dgen"

emulators.append(Dgen())
