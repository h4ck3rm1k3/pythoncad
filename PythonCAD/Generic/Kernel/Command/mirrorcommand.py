#!/usr/bin/env python
#
# Copyright (c) 2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public Licensesegmentcmd.py
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#This module provide a class for the polyline command
#

from Kernel.exception               import *
from Kernel.Command.basecommand     import *
from Kernel.GeoEntity.point            import Point

class MirrorCommand(BaseCommand):
    """
        this class rappresent the mirror command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception=[ExcText,
                        ExcText]
        self.message=[  "Give Me Entity ID use , for more enitt ES: 4,10,5", 
                        "Give me the reference line (Segmento or CLine)"]
                        
    def performMirror(self):
        """
            perform the mirror of all the entity selected
        """
        mirrorRef=self.document.getEntity(self.value[1])
        geoMirrorRef=self.document.convertToGeometricalEntity(mirrorRef)
        outEnt=[]
        updEnts=[]
        for id in str(self.value[0]).split(','):
            dbEnt=self.document.getEntity(id)
            geoEnt=self.document.convertToGeometricalEntity(dbEnt)
            geoEnt.mirror(geoMirrorRef)
            dbEnt.setConstructionElements(geoEnt.getConstructionElements())
            outEnt.append(dbEnt)
        return outEnt
        
    def applyCommand(self):
        """
            perform the write of the entity
        """
        if len(self.value)!=2:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        try:
            self.document.startMassiveCreation()
            for _ent in self.performMirror():
                self.document.saveEntity(_ent)
        finally:
            self.document.stopMassiveCreation()