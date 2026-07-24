# -*- coding: utf-8 -*-

import Diet_NullGr.ModSys.Diet.config as config
import Diet_NullGr.ModSys.Thirst.config as thirstConfig

modName = "diet_nullgr"
ssname = "Diet_nullgr_ServerSys"
csname = "Diet_nullgr_ClientSys"
ssPath = "Diet_NullGr.Diet_main_ss.DietServerSystem"
csPath = "Diet_NullGr.Diet_main_cs.DietClientSystem"

serverSysKey = {
    ssname: ssPath
}
serverSysKey.update(config.serverSysKey)
serverSysKey.update(thirstConfig.serverSysKey)

clientSysKey = {
    csname: csPath
}
clientSysKey.update(config.clientSysKey)
clientSysKey.update(thirstConfig.clientSysKey)
