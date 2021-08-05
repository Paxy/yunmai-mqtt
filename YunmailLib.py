#!/usr/bin/env python
""" generated source for module YunmaiLib """
#  Copyright (C) 2018  olie.xdev <olie.xdev@googlemail.com>
#  *
#  *    This program is free software: you can redistribute it and/or modify
#  *    it under the terms of the GNU General Public License as published by
#  *    the Free Software Foundation, either version 3 of the License, or
#  *    (at your option) any later version.
#  *
#  *    This program is distributed in the hope that it will be useful,
#  *    but WITHOUT ANY WARRANTY; without even the implied warranty of
#  *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  *    GNU General Public License for more details.
#  *
#  *    You should have received a copy of the GNU General Public License
#  *    along with this program.  If not, see <http://www.gnu.org/licenses/>
#  

import math 


class YunmaiLib(object):
    """ generated source for class YunmaiLib """
    sex = int()

    #  male = 1; female = 0
    height = float()
    fitnessBodyType = bool()

    def __init__(self, sex, height, active):
        """ generated source for method __init__ """
        self.sex = sex
        self.height = height
        self.fitnessBodyType = active

    def getWater(self, bodyFat):
        """ generated source for method getWater """
        return ((100.0 - bodyFat) * 0.726 * 100.0 + 0.5) / 100.0

    def getFat(self, age, weight, resistance):
        """ generated source for method getFat """
        #  for < 0x1e version devices
        fat = float()
        r = (resistance - 100.0) / 100.0
        h = self.height / 100.0
        if r >= 1:
            r = (math.sqrt(r))
        fat = (weight * 1.5 / h / h) + (age * 0.08)
        if self.sex == 1:
            fat -= 10.8
        fat = (fat - 7.4) + r
        if fat < 5.0 or fat > 75.0:
            fat = 0.0
        return fat

    def getMuscle(self, bodyFat):
        """ generated source for method getMuscle """
        muscle = float()
        muscle = (100.0 - bodyFat) * 0.67
        if self.fitnessBodyType:
            muscle = (100.0 - bodyFat) * 0.7
        muscle = ((muscle * 100.0) + 0.5) / 100.0
        return muscle

    def getSkeletalMuscle(self, bodyFat):
        """ generated source for method getSkeletalMuscle """
        muscle = float()
        muscle = (100.0 - bodyFat) * 0.53
        if self.fitnessBodyType:
            muscle = (100.0 - bodyFat) * 0.6
        muscle = ((muscle * 100.0) + 0.5) / 100.0
        return muscle

    def getBoneMass(self, muscle, weight):
        """ generated source for method getBoneMass """
        boneMass = float()
        h = self.height - 170.0
        if self.sex == 1:
            boneMass = ((weight * (muscle / 100.0) * 4.0) / 7.0 * 0.22 * 0.6) + (h / 100.0)
        else:
            boneMass = ((weight * (muscle / 100.0) * 4.0) / 7.0 * 0.34 * 0.45) + (h / 100.0)
        boneMass = ((boneMass * 10.0) + 0.5) / 10.0
        return boneMass

    def getLeanBodyMass(self, weight, bodyFat):
        """ generated source for method getLeanBodyMass """
        return weight * (100.0 - bodyFat) / 100.0

    def getVisceralFat(self, bodyFat, age):
        """ generated source for method getVisceralFat """
        f = bodyFat
        a = 18 if (age < 18 or age > 120) else age
        vf = float()
        if not self.fitnessBodyType:
            if self.sex == 1:
                if a < 40:
                    f -= 21.0
                elif a < 60:
                    f -= 22.0
                else:
                    f -= 24.0
            else:
                if a < 40:
                    f -= 34.0
                elif a < 60:
                    f -= 35.0
                else:
                    f -= 36.0
            if f > 0.0:
                d = 1.1
            vf = (f / d) + 9.5
            if vf < 1.0:
                return 1.0
            if vf > 30.0:
                return 30.0
            return vf
        else:
            if bodyFat > 15.0:
                vf = (bodyFat - 15.0) / 1.1 + 12.0
            else:
                vf = -1 * (15.0 - bodyFat) / 1.4 + 12.0
            if vf < 1.0:
                return 1.0
            if vf > 9.0:
                return 9.0
            return vf

