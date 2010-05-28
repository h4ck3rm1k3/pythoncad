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
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This  module PROVIDE ALL GLOBAL VARIABLE NEEDE TO THE SCENE
#
from Interface.Entity.segment   import Segment
from Interface.Entity.arc       import Arc
from Interface.Entity.text      import Text
from Interface.Entity.ellipse   import Ellipse
from Interface.Entity.polyline   import Polyline

SCENE_SUPPORTED_TYPE=["SEGMENT",
                        "ARC",
                        "TEXT", 
                        "ELLIPSE", 
                        "POLYLINE"]

SCANE_OBJECT_TYPE=dict(zip(SCENE_SUPPORTED_TYPE, 
                       (
                        Segment, 
                        Arc, 
                        Text, 
                        Ellipse, 
                        Polyline
                       )))