#!/usr/bin/python -Es

#imports
#{{{
from configobj import ConfigObj
from validate import Validator
import sys

#}}}



# global constants
# {{{
CFG_DEF_DYNAMIC_TUNING = True
CFG_DEF_SLEEP_INTERVAL = 1
CFG_DEF_UPDATE_INTERVAL = 10
GLOBAL_CONFIG_FILE = "tuned-main.conf"

global_config_spec =    ["dynamic_tuning = boolean(default=%s)" % CFG_DEF_DYNAMIC_TUNING,
                        "sleep_interval = integer(default=%s)" % CFG_DEF_SLEEP_INTERVAL,
                        "update_interval = integer(default=%s)" % CFG_DEF_UPDATE_INTERVAL]
#}}}

#   tab_1
#           -------------------------------------
#           | code name | profile   | priority  |
#           -------------------------------------
#           | media     | balanced  |   10      |
#           -------------------------------------
#           | media     | desktop   |   5       |
#           -------------------------------------
#

# class Conf
# load configuration and validate 
#{{{
class Conf(object):
    def __init__(self,conf_name=GLOBAL_CONFIG_FILE):
        self.config = self._load_global_config(conf_name)
        self.tab_1 = []
        self.read_config()

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


    def read_config(self):
        self.keys = self.config.keys()
        print(self.config.get("autoswitch"))
        for item in self.keys:
            if item not in ["dynamic_tuning", "sleep_interval", "update_interval","autoswitch", "changing"]:
                self.read_section(item)

    def read_section(self, section_name):
        section = self.config[section_name]
        for item in section:
            value = section.get(item)
            prirad = [section_name,item, value]
            self.tab_1.append(prirad)
        self.print_tab()

    def print_tab(self):
        while self.tab_1:
            item = self.tab_1.pop()
            print(item)

#}}}

config = Conf()
