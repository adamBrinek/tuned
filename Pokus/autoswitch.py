#!/usr/bin/python -Es

from configobj import ConfigObj

tab_1 = []
pos = -1
PROFILES = "Profiles"
NAMES = "names"
CHANGING = "changing"
PRIORITY = "priority"
PARENT = "parent"

global_config_spec =    ["dynamic_tuning = boolean(default=%s)" % consts.CFG_DEF_DYNAMIC_TUNING,
                        "sleep_interval = integer(default=%s)" % consts.CFG_DEF_SLEEP_INTERVAL,
                        "update_interval = integer(default=%s)" % consts.CFG_DEF_UPDATE_INTERVAL]

class Conf(object):
    def __init__(self,conf_name):
        self.config = self._load_global_config()


    def _load_global_config(self, file_name = consts.GLOBAL_CONFIG_FILE):
        """
        Loads global configuration file.
        """
        log.debug("reading and parsing global configuration file '%s'" % consts.GLOBAL_CONFIG_FILE)
    
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

class Autoswitch(object):
    def __init__(self, conf):
        self._config = conf


#        ------------------------------------
#tab_1   | Code-name | Priority | Parent    |
#        ------------------------------------
#        | String    | Integer  | List      |
#        ------------------------------------



config = ConfigObj('tuned-main.conf')
profiles = config[PROFILES][NAMES]
for item in profiles:
    pos += 1
    tab_1.append([])
    tab_1[pos].append(item)
    tab_1[pos].append(config[item][PRIORITY])
    tab_1[pos].append(config[item][PARENT])

print (tab_1)


self._sleep_interval = int(consts.CFG_DEF_SLEEP_INTERVAL)
self._update_interval = int(consts.CFG_DEF_UPDATE_INTERVAL)
self._dynamic_tuning = consts.CFG_DEF_DYNAMIC_TUNING

if config is not None:
    self._sleep_interval = int(config.get("sleep_interval", consts.CFG_DEF_SLEEP_INTERVAL))
    self._update_interval = int(config.get("update_interval", consts.CFG_DEF_UPDATE_INTERVAL))
    self._dynamic_tuning = config.get("dynamic_tuning", consts.CFG_DEF_DYNAMIC_TUNING)





conf = Conf("tuned-main.conf")
auto = Autoswitch(conf)
