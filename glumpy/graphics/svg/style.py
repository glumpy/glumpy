# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from . color import Color
from . length import Length

_converters = {
    "color":             Color,
    "fill":              Color,
    "stroke":            Color,
    "stroke-width":      Length
}


# ------------------------------------------------------------------- Style ---
class Style(object):
    """
    SVG uses styling properties to describe many of its document
    parameters. Styling properties define how the graphics elements in the SVG
    content are to be rendered. SVG uses styling properties for the following:

    * Parameters which are clearly visual in nature and thus lend themselves to
      styling. Examples include all attributes that define how an object is
      "painted," such as fill and stroke colors, linewidths and dash styles.

    * Parameters having to do with text styling such as font family and size.

    * Parameters which impact the way that graphical elements are rendered,
      such as specifying clipping paths, masks, arrowheads, markers and filter
      effects.
    """

    def __init__(self, description=None):

        self.fill = None
        self.stroke = None
        self.color = None
        self.stroke_width = Length("2.0")

        if description:
            self.parse(description)


    def parse(self, description):
        """ Parse an SVG style description """

        items = description.strip().split(";")
	attributes = dict([item.strip().split(":") for item in items if item])

        for key,value in attributes.items():
            if key in _converters:
                key_ = key.replace("-","_")
                self.__setattr__(key_, _converters[key](value))





# -----------------------------------------------------------------------------
if __name__ == '__main__':
    style = Style("""fill: #ffffff;
                     stroke: #000000;
                     stroke-width:0.172;""")
    print style.fill.rgba
    print style.stroke.rgba
    print style.stroke_width
