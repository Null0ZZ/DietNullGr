# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import Diet_NullGr.com as com


@Mod.Binding(name="Diet_NullGr", version="0.0.1")
class DietNullGrMod(object):
    def __init__(self):
        pass

    @Mod.InitServer()
    def DietNullGrServerInit(self):
        for key in com.serverSysKey:
            serverApi.RegisterSystem(com.modName, key, com.serverSysKey[key])
        print("[DietNullGr] server systems registered")

    @Mod.DestroyServer()
    def DietNullGrServerDestroy(self):
        pass

    @Mod.InitClient()
    def DietNullGrClientInit(self):
        for key in com.clientSysKey:
            clientApi.RegisterSystem(com.modName, key, com.clientSysKey[key])
        print("[DietNullGr] client systems registered")

    @Mod.DestroyClient()
    def DietNullGrClientDestroy(self):
        pass
