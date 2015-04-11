#!/usr/bin/python -Es

#imports
#{{{
from configobj import ConfigObj
from validate import Validator
import sys
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gi.repository.GLib
#import gobject

#}}}



# global constants
# {{{
PROFILES = "Profiles"
NAMES = "names"
CHANGING = "changing"
PRIORITY = "priority"
PARENT = "parent"

CFG_DEF_DYNAMIC_TUNING = True
CFG_DEF_SLEEP_INTERVAL = 1
CFG_DEF_UPDATE_INTERVAL = 10
GLOBAL_CONFIG_FILE = "tuned-main.conf"

global_config_spec =    ["dynamic_tuning = boolean(default=%s)" % CFG_DEF_DYNAMIC_TUNING,
                        "sleep_interval = integer(default=%s)" % CFG_DEF_SLEEP_INTERVAL,
                        "update_interval = integer(default=%s)" % CFG_DEF_UPDATE_INTERVAL]
#}}}


# class Conf
# load configuration and validate 
#{{{
class Conf(object):
    def __init__(self,conf_name):
        self.config = self._load_global_config(conf_name)


    def _load_global_config(self, file_name = GLOBAL_CONFIG_FILE):
        """
        Loads global configuration file.
        """
#        log.debug("reading and parsing global configuration file '%s'" % GLOBAL_CONFIG_FILE)
    
        try:
            config = ConfigObj(file_name, configspec=global_config_spec, raise_errors = True, file_error = True)
        except IOError as e:
            raise TunedException("Global tuned configuration file '%s' not found." % file_name)
        except ConfigObjError as e:
            raise TunedException("Error parsing global tuned configuration file '%s'." % file_name)
    
        vdt = Validator()
    
        if (not config.validate(vdt, copy=True)):
            raise TunedException("Global tuned configuration file '%s' is not valid." % file_name)
    
        return config
#}}}


#class Autoswitch
#parse configuration and create table_1
#        ------------------------------------
#tab_1   | Code-name | Priority | Parent    |
#        ------------------------------------
#        | String    | Integer  | List      |
#        ------------------------------------
#{{{
class Autoswitch(object):
    def __init__(self, conf=None):
        self._config = conf
        self._tab_1 = []
        self._pos = -1
        self._load_default_values()
        if self._config is not None:
            self._load_values()

    def _load_default_values(self):
        self._sleep_interval = int(CFG_DEF_SLEEP_INTERVAL)
        self._update_interval = int(CFG_DEF_UPDATE_INTERVAL)
        self._dynamic_tuning = CFG_DEF_DYNAMIC_TUNING

    def _load_values(self):
        self._sleep_interval = int(self._config["sleep_interval"])
        self._update_interval = int(self._config.get("update_interval", CFG_DEF_UPDATE_INTERVAL))

        self._dynamic_tuning = self._config.get("dynamic_tuning", CFG_DEF_DYNAMIC_TUNING)
        self._profile_names = self._config[PROFILES][NAMES]
        
        for item in self._profile_names:
            self._pos += 1
            self._tab_1.append([])
            self._tab_1[self._pos].append(item)
            self._tab_1[self._pos].append(self._config[item][PRIORITY])
            self._tab_1[self._pos].append(self._config[item][PARENT])
        
        
#}}}

#class Dbus
#{{{

# DBUS connection
class Connection(object): #{{{
    def __init__(self,bus_name,interface_name,object_name):
        self._bus_name = bus_name
        self._bus_interface = interface_name
        self._object_name = object_name
        self._proxy = None
#        self.__init_proxy()

 #   def __init_proxy(self):
#        if self._proxy is None:
 #           #bus = dbus.SystemBus()
  #          bus = dbus.SessionBus()
   #         name = dbus.service.BusName(DBUS_BUS,bus)
            #self._proxy = bus.get_object(self._bus_name, self._bus_interface, self._object_name)

    def _call(self, method_name, *args, **kwargs):
        self.__init_proxy()
        method = self._proxy.get_dbus_method(method_name)
        return method(*args, **kwargs)
#}}}



#main{{{
#definice globalnich promenych
DBUS_BUS="com.redhat.tuned"
DBUS_OBJECT="/Tuned"
DBUS_INTERFACE="com.redhat.tuned.control"


conf = Conf("tuned-main.conf")
auto = Autoswitch(conf.config)


DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
name = dbus.service.BusName(DBUS_BUS,session_bus)

control = Connection(DBUS_BUS, DBUS_OBJECT, DBUS_INTERFACE)

mainloop = gi.repository.GLib.MainLoop()

mainloop.run()


sys.exit(0)
#}}}
