import maya.cmds as cmds
from validator.utils.validator_API import *

checkId = 100
checkLabel = "1.2 Check polycount"


class lodPolycount():
    # takes any amount of args
    def __init__(self, combination):  # here should be only "combination" array

        self.hull = None
        self.chassis = None
        self.turret = None
        self.gun = None

        for i in combination:
            if i.find("hull") != -1 or i.find("Hull") != -1:
                self.hull = i
            elif i.find("chassis") != -1 or i.find("Chassis") != -1:
                self.chassis = i
            elif i.find("turret") != -1 or i.find("Turret") != -1:
                self.turret = i
            elif i.find("gun") != -1 or i.find("Gun") != -1:
                self.gun = i

        self.lastFoundedHull = self.hull
        self.lastFoundedChassis = self.chassis
        self.lastFoundedTurret = self.turret  # None
        self.lastFoundedGun = self.gun

        self.polycount = self.getPolycount()  # get polycount of the current combination
        self.lastPolycount = self.polycount

    def getRelatives(self, obj):  # get geo (list or single)
        relList = []
        objInList = []
        relList = cmds.listRelatives(obj, type="transform", f=1)
        if relList:  # if we found transform relatives
            return relList
        else:  # if we found only shape - then return parent obj
            objInList.append(obj)
            return objInList

    def getPolycount(self):  # get polycount of a combination

        hullGEO = None
        chassisGEO = None
        turretGEO = None
        gunGEO = None

        geoList = []

        if self.hull:
            hullGEO = self.getRelatives(self.hull)
            geoList = geoList + hullGEO
        if self.chassis:
            chassisGEO = self.getRelatives(self.chassis)
            geoList = geoList + chassisGEO
        if self.turret:
            turretGEO = self.getRelatives(self.turret)
            geoList = geoList + turretGEO
        if self.gun:
            gunGEO = self.getRelatives(self.gun)
            geoList = geoList + gunGEO

        # geoList = hullGEO + chassisGEO + turretGEO + gunGEO
        pCount = 0
        for geo in geoList:
            if geo:
                tmpCount = 0
                try:
                    tmpCount = int(cmds.polyEvaluate(geo, t=1))
                except:
                    pass
                if tmpCount != 0:
                    pCount += tmpCount  # int(cmds.polyEvaluate(geo, t=1))
        return pCount

    def LFO_Polycount(self):  # get polycount of a combination

        hullGEO = None
        chassisGEO = None
        turretGEO = None
        gunGEO = None

        geoList = []

        if self.lastFoundedHull:
            hullGEO = self.getRelatives(self.lastFoundedHull)
            geoList = geoList + hullGEO
        if self.lastFoundedChassis:
            chassisGEO = self.getRelatives(self.lastFoundedChassis)
            geoList = geoList + chassisGEO
        if self.lastFoundedTurret:  # still None
            turretGEO = self.getRelatives(self.lastFoundedTurret)
            geoList = geoList + turretGEO
        if self.lastFoundedGun:
            gunGEO = self.getRelatives(self.lastFoundedGun)
            geoList = geoList + gunGEO

        # geoList = hullGEO + chassisGEO + turretGEO + gunGEO
        pCount = 0
        for geo in geoList:
            if geo:
                tmpCount = 0
                try:
                    tmpCount = int(cmds.polyEvaluate(geo, t=1))
                except:
                    pass
                if tmpCount != 0:
                    pCount += tmpCount  # int(cmds.polyEvaluate(geo, t=1))
        return pCount

    def checkNextLod(self, lodName):  # get the polycount of the combination in the next lod

        relatives = self.getRelatives(lodName)  # get transform relatives from lod1 lod2 lod3

        # here we find the same combination in the next lod
        chassisSearchName = None
        hullSearchName = None
        turretSearchName = None
        gunSearchName = None

        # here is the names of objects from lod0  (some of the names are None) - which we gonna use in search
        if self.chassis:
            chassisSearchName = self.chassis.split("|")[-1]
        if self.hull:
            hullSearchName = self.hull.split("|")[-1]
        if self.turret:
            turretSearchName = self.turret.split("|")[-1]
        if self.gun:
            gunSearchName = self.gun.split("|")[-1]

        for rel in relatives:  # for each relative in lod0
            if self.chassis:  # if chassis in lod0
                if rel.find(chassisSearchName) != -1 and rel.find("bsp") == -1:
                    self.lastFoundedChassis = rel

            if self.hull:  # if hull in lod0
                if rel.find(hullSearchName) != -1 and rel.find("bsp") == -1:
                    self.lastFoundedHull = rel

            if self.turret:  # if turret in lod0   (no, turret is None in lod0)
                if rel.find(turretSearchName) != -1 and rel.find(
                        "bsp") == -1:  # no turret in all lods - lastFoundedTurret = None
                    self.lastFoundedTurret = rel  # still None

            if self.gun:  # if gun in lod0
                if rel.find(gunSearchName) != -1 and rel.find("bsp") == -1:
                    self.lastFoundedGun = rel

        polycountResult = self.LFO_Polycount()

        # print 'WTF', polycountResult
        self.lod0_polycount = self.lastPolycount
        half_of_lastPolycount = self.lastPolycount / 2
        topPercentage = half_of_lastPolycount / 20

        # print 'WTF2', lodName, polycountResult

        if lodName.find("lod1") != -1:
            firstLod_policount = int(0.525 * self.lod0_polycount)
            # print 'Recomended LOD1', firstLod_policount
            # if polycountResult > half_of_lastPolycount + topPercentage:
            if polycountResult > firstLod_policount:
                message = ""
                if self.lastFoundedHull:
                    message = message + self.lastFoundedHull + " , "
                if self.lastFoundedChassis:
                    message = message + self.lastFoundedChassis + " , "
                if self.lastFoundedTurret:
                    message = message + self.lastFoundedTurret + " , "
                if self.lastFoundedGun:
                    message = message + self.lastFoundedGun + "\n    -"

                # message = self.lastFoundedHull + " , "  +  self.lastFoundedChassis + " , " +  self.lastFoundedTurret + " , " + self.lastFoundedGun + "\n    -"
                message = message + "Out of range with " + str(polycountResult) + " tris > max polycount: " + str(
                    firstLod_policount) + "\n"
                # self.lastPolycount = firstLod_policount
                return message
            else:
                # self.lastPolycount = firstLod_policount
                return False

        elif lodName.find("lod2") != -1:
            secondLod_policount = int(0.2756 * self.lod0_polycount)
            # print 'Recomended LOD2', secondLod_policount
            # if polycountResult > half_of_lastPolycount + topPercentage:
            if polycountResult > secondLod_policount:
                message = ""
                if self.lastFoundedHull:
                    message = message + self.lastFoundedHull + " , "
                if self.lastFoundedChassis:
                    message = message + self.lastFoundedChassis + " , "
                if self.lastFoundedTurret:
                    message = message + self.lastFoundedTurret + " , "
                if self.lastFoundedGun:
                    message = message + self.lastFoundedGun + "\n    -"

                # message = self.lastFoundedHull + " , " +  self.lastFoundedChassis + " , " +  self.lastFoundedTurret + " , " + self.lastFoundedGun + "\n    -"
                message = message + "Out of range with " + str(polycountResult) + " tris > max polycount: " + str(
                    secondLod_policount) + "\n"
                # self.lastPolycount = polycountResult
                return message
            else:
                # self.lastPolycount = polycountResult
                return False

        elif lodName.find("lod3") != -1:
            thirdLod_policount = int(0.14469 * self.lod0_polycount)
            # print 'Recomended LOD3', thirdLod_policount
            # if polycountResult > half_of_lastPolycount + topPercentage:
            if polycountResult > thirdLod_policount:
                message = ""
                if self.lastFoundedHull:
                    message = message + self.lastFoundedHull + " , "
                if self.lastFoundedChassis:
                    message = message + self.lastFoundedChassis + " , "
                if self.lastFoundedTurret:
                    message = message + self.lastFoundedTurret + " , "
                if self.lastFoundedGun:
                    message = message + self.lastFoundedGun + "\n    -"

                # message = self.lastFoundedHull + " , " +  self.lastFoundedChassis + " , " +  self.lastFoundedTurret + " , " + self.lastFoundedGun + "\n    -"
                message = message + "Out of range with " + str(polycountResult) + " tris > max polycount: " + str(
                    thirdLod_policount) + "\n"
                # self.lastPolycount = polycountResult
                return message
            else:
                # self.lastPolycount = polycountResult
                return False


def getLodList():
    lodList = []
    lodList = cmds.ls("*lod*", type="transform", l=1)
    return lodList


def getRelatives(obj):  # return relatives or obj (if it has no relatives)
    relList = []
    objInList = []
    relList = cmds.listRelatives(obj, type="transform", f=1)
    if relList:  # if we found transform relatives
        return relList
    else:  # if we found only shape - then return parent obj
        objInList.append(obj)
        return objInList


def wg_getPolycount(list, limit):
    result = 0
    for i in list:
        rel = cmds.ls(cmds.listRelatives(i, type="transform", f=1), l=1)
        if rel:
            for j in rel:
                # print 'RESULT ', cmds.polyEvaluate(j, t=1), j
                if type(cmds.polyEvaluate(j, t=1)) is int:
                    result += cmds.polyEvaluate(j, t=1)
        else:
            result += cmds.polyEvaluate(i, t=1)
    if result > limit:
        message = ""
        for i in list:
            message += i + " , "
        message = message + "\n    -"
        message = message + "Out of range with " + str(result) + " tris > max polycount: " + str(limit) + "\n"
        return message
    else:
        return None


def main():
    returnList = []
    lodList = getLodList()

    if lodList:
        for lod in lodList:
            if lod.find("lod0") != -1:  # we found lod0

                relatives = getRelatives(lod)
                chassisList = [0]
                hullList = [0]
                turretList = [0]
                gunList = [0]

                for i in relatives:
                    if (i.find("hull") != -1 or i.find("Hull") != -1) and i.find("bsp") == -1:
                        hullList.append(i)
                    elif (i.find("chassis") != -1 or i.find("Chassis") != -1) and i.find("bsp") == -1:
                        chassisList.append(i)
                    elif (i.find("turret") != -1 or i.find("Turret") != -1) and i.find("bsp") == -1:
                        turretList.append(i)
                    elif (i.find("gun") != -1 or i.find("Gun") != -1) and i.find("bsp") == -1:
                        gunList.append(i)

                lists = 0

                if len(hullList) > 1:
                    lists += 1
                if len(chassisList) > 1:
                    lists += 1
                if len(turretList) > 1:
                    lists += 1
                if len(gunList) > 1:
                    lists += 1

                combinations_lod0 = []

                for h in hullList:
                    for c in chassisList:
                        for t in turretList:
                            for g in gunList:
                                tmpList = []
                                if h != 0:
                                    tmpList.append(h)
                                if c != 0:
                                    tmpList.append(c)
                                if t != 0:
                                    tmpList.append(t)
                                if g != 0:
                                    tmpList.append(g)

                                if tmpList and len(tmpList) == lists:
                                    combinations_lod0.append(tmpList)

                for comb in combinations_lod0:
                    # print comb
                    foundedCombination = lodPolycount(comb)
                    pcount = wg_getPolycount(comb, 50000)
                    if pcount != None:
                        tmp = []
                        tmp.append(pcount)
                        tmp.append(pcount)
                        returnList.append(tmp)
                        # print pcount

                    for index, lodet in enumerate(lodList):  # for each lod: lod1-lod3
                        if (index != 0 and index != 4):
                            result = foundedCombination.checkNextLod(
                                lodet)  # if checkNextLod returned false (in case current lod's polycount doesn't match the condition)
                            if result:
                                tmp = []
                                tmp.append(result)
                                tmp.append(result)
                                returnList.append(tmp)
                                # print result
                                # here we need to form a message for the returnList with selection (turret and gun comb)

            # here check other lods from 1 to 3 <!-not done yet->

            # check lod4
            if lod.find("lod4") != -1:
                relatives = getRelatives(lod)
                chassisList = [0]
                hullList = [0]
                turretList = [0]
                gunList = [0]

                for i in relatives:
                    if (i.find("hull") != -1 or i.find("Hull") != -1) and i.find("bsp") == -1:
                        hullList.append(i)
                    elif (i.find("chassis") != -1 or i.find("Chassis") != -1) and i.find("bsp") == -1:
                        chassisList.append(i)
                    elif (i.find("turret") != -1 or i.find("Turret") != -1) and i.find("bsp") == -1:
                        turretList.append(i)
                    elif (i.find("gun") != -1 or i.find("Gun") != -1) and i.find("bsp") == -1:
                        gunList.append(i)

                lists = 0
                if len(hullList) > 1:
                    lists += 1
                if len(chassisList) > 1:
                    lists += 1
                if len(turretList) > 1:
                    lists += 1
                if len(gunList) > 1:
                    lists += 1

                combinationsLod4 = []

                for h in hullList:
                    for c in chassisList:
                        for t in turretList:
                            for g in gunList:
                                tmpList = []
                                if h != 0:
                                    tmpList.append(h)
                                if c != 0:
                                    tmpList.append(c)
                                if t != 0:
                                    tmpList.append(t)
                                if g != 0:
                                    tmpList.append(g)

                                if tmpList and len(tmpList) == lists:
                                    combinationsLod4.append(tmpList)

                for comb in combinationsLod4:
                    pcount = wg_getPolycount(comb, 400)
                    if pcount != None:
                        tmp = []
                        tmp.append(pcount)
                        tmp.append(pcount)
                        returnList.append(tmp)
                        # print pcount

    return returnList
