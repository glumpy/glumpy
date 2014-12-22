# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


class Unit(object):
    """ """

    dpi  = 72
    size = [512,512]

    def __init__(self, value=1.0, scale=1.0, unit='em'):
        self._value = float(value)
        if type(scale) in [int,float]:
            self._scale = float(scale)
        else:
            self._scale = scale
        self._unit = unit

    @property
    def scale(self):
        s = self._scale
        if type(s) is float:
            return s
        else:
            return self._scale()

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value


    def __add__(self,other):
        """ x.__add__(y) <==> x+y """

        # Convert to default unit if none given
        if type(other) in [int,float]:
            other = Unit(other, default_unit.scale, default_unit._value)
        v = self._value*self.scale + other._value*other.scale
        return Unit( v/self.scale, self.scale, self._unit)


    def __radd__(self,other):
        """ x.__radd__(y) <==> y+x """

        if type(other) in [int,float]:
            return Unit(self._value*self.scale + other, self.scale, self._unit)

        # All other operations are forbidden
        raise UnitException('Forbidden operation')


    def __sub__(self,other):
        """ x.__sub__(y) <==> x-y """

        # Convert to default unit if none given
        if type(other) in [int,float]:
            other = Unit(other, default_unit.scale, default_unit._value)
        v = self._value*self.scale - other._value*other._scale
        return Unit( v/self.scale, self.scale, self._unit)


    def __rsub__(self,other):
        """ x.__rsub__(y) <==> y-x """

        if type(other) in [int,float]:
            return Unit(other - self._value*self.scale, self.scale, self._unit)

        # All other operations are forbidden
        raise UnitException('Forbidden operation')


    def __mul__(self,other):
        """ x.__mul__(y) <==> x*y """

        # Regular multiplication with a scalar
        if type(other) in [int,float]:
            return Unit(self._value*other, self.scale, self._unit)

        # Conversion to another unit
        elif other in units:
            v = self._value*self.scale * other._value
            return Unit(v/other.scale, other.scale, other._unit)

        # All other operations are forbidden
        raise UnitException('Forbidden operation')

    def __rmul__(self,other):
        """ x.__rmul__(y) <==> y*x """

        # Regular multiplication with a scalar
        if type(other) in [int,float]:
            return Unit(self._value*other, self.scale, self._unit)

        # All other operations are forbidden
        raise UnitException('Forbidden operation')


    def __div__(self,other):
        """ x.__div__(y) <==> x/y """

        # Regular division with a scalar
        if type(other) in [int,float]:
            return Unit(self._value/other, self.scale, self._unit)

        # All other operations are forbidden
        raise UnitException('Forbidden operation')


    def __rdiv__(self,other):
        """ x.__rdiv__(y) <==> y/x """

        # All such operations are forbidden
        raise UnitException('Forbidden operation')


    def __float__(self):
        return float(self._value*self.scale)


    def __int__(self):
        return int(self._value*self.scale)


    def __str__(self):
        v = self._value
        if abs(int(v)-v) < 1e-10:
            return "%d %s" % (self._value,self._unit)
        else:
            return "%.3f %s" % (self._value,self._unit)


Unit.dpi   = 72.0
Unit.size = [512,512]
px    = Unit(1,1,'px')
em    = Unit(1, lambda: min(Unit.size[0],Unit.size[1]),'em')
pc    = Unit(1, lambda: min(Unit.size[0],Unit.size[1])/100.0,'%')
inch  = Unit(1, lambda: Unit.dpi/1.000,'in')
cm    = Unit(1, lambda: Unit.dpi/2.540,'cm')
mm    = Unit(1, lambda: Unit.dpi/25.40,'mm')

length ::= number (~"em" | ~"ex" | ~"px" | ~"in" | ~"cm" | ~"mm" | ~"pt" | ~"pc")?

units = [em, pc, px, cm, mm, inch]
default_unit = px



# -----------------------------------------------------------------------------
if __name__ == '__main__':

    print "Regular conversions"
    print "-------------------"
    print "1 em =", (1*em  )*px
    print "1 %  =", (1*pc  )*px
    print "1 in =", (1*inch)*px
    print "1 cm =", (1*cm  )*px
    print "1 mm =", (1*mm  )*px
    print "1 px =", (1*px  )*px
    print

    print "Operations"
    print "----------"
    print "2*px + 3   =", 2*px+3
    print "3 + 2*px   =", 3+2*px
    print "2*px - 3   =", 2*px-3
    print "3 - 2*px   =", 3-2*px
    print "3 * (2*px) =", 3*(2*px)
    print "(2*px) * 3 =", (2*px)*3
    print "(2*px) / 3 =", (2*px)/3
    print

    print "Relative units"
    print "--------------"
    print "1 em =", (1*em  )*px
    Unit.size = 200, 200
    print "1 em =", (1*em  )*px
