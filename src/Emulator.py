from enigma import eConsoleAppContainer, eDBoxLCD, eRCInput, fbClass

from Components.Language import language
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen
from Screens.ServiceStopScreen import ServiceStopScreen
from Tools.Log import Log

from os import path as os_path
from subprocess import check_output
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_PLUGINS
from Components.Ipkg import IpkgComponent
from Screens.Ipkg import Ipkg


class EmulatorSummary(Screen):
	def __init__(self, session, parent):
		Screen.__init__(self, session, parent=parent)
		self.skinName = ["EmulatorSummary"]

class EmulationHelper(object):
	installed_packages = []
	fileMode = True
	name = None
	description = None
	cmd = None
	pattern = None
	location = None
	icon = None
	packageName = None
	version = ""
	png = None

	@staticmethod
	def updatePackages():
		EmulationHelper.installed_packages = []
		try:
			out = check_output(["dpkg", "-l"])
			lines = out.split("\n")[5:] #strip dpkg header
			for line in lines:
				packageData = [x.strip() for x in line.split("  ") if x]
				if len(packageData) >= 3:
					EmulationHelper.installed_packages.append(packageData)
		except Exception as e:
			Log.w(e)

	def install(self, session, callback):
		cmdList = [(IpkgComponent.CMD_INSTALL, { "package": self.packageName })]
		session.openWithCallback(callback, Ipkg, cmdList = cmdList)

	def remove(self, session, callback):
		cmdList = [(IpkgComponent.CMD_REMOVE, { "package": self.packageName, "autoremove" : True })]
		session.openWithCallback(callback, Ipkg, cmdList = cmdList)

	def __init__(self):
		pass

	def getRunCmd(self, rom=None):
		if rom:
			return "%s '%s';" % (self.cmd, rom)
		else:
			return self.cmd

	def check(self):
		if not self.packageName:
			return True
		if not EmulationHelper.installed_packages:
			EmulationHelper.updatePackages()
		"""
		items of installed_packages look like this:
		['ii', 'advancemame', '3.2+git0+7f7abff1dd-r1.1', 'armhf', 'advancemame version 3.2+gitAUTOINC+7f7abff1dd-r1']
		"""
		for package in EmulationHelper.installed_packages:
			if package[1] == self.packageName:
				self.version = package[2]
				Log.w(self.version)
				return package[0] == "ii"
		return False # MISS!

	def toList(self):
		if not self.png:
			if self.icon:
				path = resolveFilename(SCOPE_PLUGINS, "Extensions/RetroGameStation/%s" %(self.icon,))
				Log.w("%s" %(path,))
				self.png = LoadPixmap(path)
			else:
				self.png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/icons/plugin.png"))

		installed = self.check()
		name = self.name if installed else _("Press OK to install...")

		return (
			self,
			name,
			self.description,
			self.packageName,
			self.version,
			self.png,
			installed,
		)

class Emulator(Screen, ServiceStopScreen):
	def __init__(self, session, emulationHelper, rom=None):
		Screen.__init__(self, session, emulationHelper.name)
		ServiceStopScreen.__init__(self)
		self._emulationHelper = emulationHelper
		self.__rom = rom
		if rom:
			self["lcdinfo"] = StaticText(os_path.basename(self.__rom))
		else:
			self["lcdinfo"] = StaticText(emulationHelper.name)
		self.__container = eConsoleAppContainer()
		self.__appClosed_conn = self.__container.appClosed.connect(self.__runFinished)
		self.stopService()
		self.__runEmu(self.__rom)

	def __runEmu(self, rom=None):
		Log.i(rom)
		eDBoxLCD.getInstance().lock()
		eRCInput.getInstance().lock()
		fbClass.getInstance().lock()
		cmd = "export LANG=" + language.getLanguage() + ".UTF-8;%s" % (self._emulationHelper.getRunCmd(rom),)
		Log.w(cmd)
		self.__container.execute(cmd)

	def __runFinished(self, retval=1):
		Log.i(retval)
		eDBoxLCD.getInstance().unlock()
		fbClass.getInstance().unlock()
		eRCInput.getInstance().unlock()
		self.close()

	def createSummary(self):
		return EmulatorSummary
