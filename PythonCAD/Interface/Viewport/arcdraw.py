#
# Copyright (c) 2005, 2006 Art Haas
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
# code for adding graphical methods to drawing entities
#

import types
from math import pi
_dtr = (pi/180.0)

import pygtk
pygtk.require('2.0')
import gtk
import pango

from PythonCAD.Generic import color
#from PythonCAD.Generic import point
#from PythonCAD.Generic import segment
#from PythonCAD.Generic import circle
#from PythonCAD.Generic import arc
#from PythonCAD.Generic import leader
#from PythonCAD.Generic import polyline
#from PythonCAD.Generic import segjoint
#from PythonCAD.Generic import conobject
#from PythonCAD.Generic import hcline
#from PythonCAD.Generic import vcline
#from PythonCAD.Generic import acline
#from PythonCAD.Generic import cline
#from PythonCAD.Generic import ccircle
#from PythonCAD.Generic import text
#from PythonCAD.Generic import dimension
#from PythonCAD.Generic import layer
#
#from PythonCAD.Interface.Gtk import gtkimage


#----------------------------------------------------------------------------------------------------
def _draw_arc(self, gimage, col=None):
    if not isinstance(gimage, gtkimage.GTKImage):
        raise TypeError, "Invalid GTKImage: " + `type(gimage)`
    _col = col
    if _col is not None and not isinstance(_col, color.Color):
        raise TypeError, "Invalid Color: " + `type(_col)`
    _layer = self.getParent()
    if _layer is None:
        raise RuntimeError, "No parent Layer for Arc"
    _cp = self.getCenter()
    _x, _y = _cp.getCoords()
    _r = self.getRadius()
    _sa = self.getStartAngle()
    _ea = self.getEndAngle()
    _px, _py = gimage.coordToPixTransform(_x, _y)
    _rx, _ry = gimage.coordToPixTransform((_x + _r), _y)
    _rad = _rx - _px
    if _col is None:
        _col = self.getColor()
    _dlist = self.getLinetype().getList()
    _lw = self.getThickness()#/gimage.getUnitsPerPixel()
    _ctx = gimage.getCairoContext()
    if _ctx is not None:
        _ctx.save()
        _r, _g, _b = _col.getColors()
        _ctx.set_source_rgb((_r/255.0), (_g/255.0), (_b/255.0))
        if _dlist is not None:
            _ctx.set_dash(_dlist)
        _ctx.set_line_width(_lw)
        _rsa = _sa * _dtr
        _rea = _ea * _dtr
        #
        # arc drawing relies on Cairo transformations
        #
        _ctx.scale(1.0, -1.0)
        _ctx.translate(_px, -(_py))
        if abs(_sa - _ea) < 1e-10:
            _ctx.arc(0, 0, _rad, _rsa, (_rsa + (2.0 * pi)))
        else:
            _ctx.arc(0, 0, _rad, _rsa, _rea)
        _ctx.stroke()
        _ctx.restore()
    else:
        _gc = gimage.getGC()
        for _ep in self.getEndpoints():
            _ex, _ey = _ep
            _pts = _layer.find('point', _ex, _ey)
            if len(_pts) == 0:
                raise RuntimeError, "No Arc endpoint at: " + str(_ep)
            _ept = None
            for _pt in _pts:
                for _user in _pt.getUsers():
                    if _user is self:
                        _ept = _pt
                        break
                if _ept is not None:
                    break
            if abs(_sa - _ea) < 1e-10:
                break
        _pxmin = _px - _rad
        _pymin = _py - _rad
        _cw = _ch = _rad * 2
        _set_gc_values(_gc, _dlist, gimage.getColor(_col), _lw)
        if abs(_sa - _ea) < 1e-10:
            _sweep = 360.0
        elif _sa > _ea:
            _sweep = 360.0 - (_sa - _ea)
        else:
            _sweep = _ea - _sa
        gimage.getPixmap().draw_arc(_gc, False,
                                    _pxmin, _pymin,
                                    _cw, _ch,
                                    int(round(_sa * 64)),
                                    int(round(_sweep * 64)))

#----------------------------------------------------------------------------------------------------
def _erase_arc(self, gimage):
    self.draw(gimage, gimage.image.getOption('BACKGROUND_COLOR'))
    