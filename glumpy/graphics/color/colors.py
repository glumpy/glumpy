from collections import OrderedDict

colors = OrderedDict( {

    # Colors from Material design by Google
    # http://www.google.com/design/spec/material-design/introduction.html
    "material" : {

        "red":  OrderedDict([
            (  "50" , "#ffebee"),
            ( "100" , "#ffcdd2"),
            ( "200" , "#ef9a9a"),
            ( "300" , "#e57373"),
            ( "400" , "#ef5350"),
            ( "500" , "#f44336"),
            ( "600" , "#e53935"),
            ( "700" , "#d32f2f"),
            ( "800" , "#c62828"),
            ( "900" , "#b71c1c"),
            ( "accent", OrderedDict([
                ("100" , "#ff8a80"),
                ("200" , "#ff5252"),
                ("400" , "#ff1744"),
                ("700" , "#d50000")]))]),

        "pink" : OrderedDict([
            (  "50" , "#fce4ec"),
            ( "100" , "#f8bbd0"),
            ( "200" , "#f48fb1"),
            ( "300" , "#f06292"),
            ( "400" , "#ec407a"),
            ( "500" , "#e91e63"),
            ( "600" , "#d81b60"),
            ( "700" , "#c2185b"),
            ( "800" , "#ad1457"),
            ( "900" , "#880e4f"),
            ( "accent", OrderedDict([
                ("100" , "#ff80ab"),
                ("200" , "#ff4081"),
                ("400" , "#f50057"),
                ("700" , "#c51162")]))]),

        "purple" : OrderedDict([
            (  "50" , "#f3e5f5"),
            ( "100" , "#e1bee7"),
            ( "200" , "#ce93d8"),
            ( "300" , "#ba68c8"),
            ( "400" , "#ab47bc"),
            ( "500" , "#9c27b0"),
            ( "600" , "#8e24aa"),
            ( "700" , "#7b1fa2"),
            ( "800" , "#6a1b9a"),
            ( "900" , "#4a148c"),
            ( "accent", OrderedDict([
                ("100" , "#ea80fc"),
                ("200" , "#e040fb"),
                ("400" , "#d500f9"),
                ("700" , "#aa00ff")]))]),

        "deeppurple" :OrderedDict([
            (  "50" , "#ede7f6"),
            ( "100" , "#d1c4e9"),
            ( "200" , "#b39ddb"),
            ( "300" , "#9575cd"),
            ( "400" , "#7e57c2"),
            ( "500" , "#673ab7"),
            ( "600" , "#5e35b1"),
            ( "700" , "#512da8"),
            ( "800" , "#4527a0"),
            ( "900" , "#311b92"),
            ( "accent", OrderedDict([
                ("100" , "#b388ff"),
                ("200" , "#7c4dff"),
                ("400" , "#651fff"),
                ("700" , "#6200ea")]))]),

        "indigo" : OrderedDict([
            (  "50" , "#e8eaf6"),
            ( "100" , "#c5cae9"),
            ( "200" , "#9fa8da"),
            ( "300" , "#7986cb"),
            ( "400" , "#5c6bc0"),
            ( "500" , "#3f51b5"),
            ( "600" , "#3949ab"),
            ( "700" , "#303f9f"),
            ( "800" , "#283593"),
            ( "900" , "#1a237e"),
            ( "accent", OrderedDict([
                ("100" , "#8c9eff"),
                ("200" , "#536dfe"),
                ("400" , "#3d5afe"),
                ("700" , "#304ffe")]))]),

        "blue" : OrderedDict([
            (  "50" , "#e3f2fd"),
            ( "100" , "#bbdefb"),
            ( "200" , "#90caf9"),
            ( "300" , "#64b5f6"),
            ( "400" , "#42a5f5"),
            ( "500" , "#2196f3"),
            ( "600" , "#1e88e5"),
            ( "700" , "#1976d2"),
            ( "800" , "#1565c0"),
            ( "900" , "#0d47a1"),
            ( "accent", OrderedDict([
                ("100" , "#82b1ff"),
                ("200" , "#448aff"),
                ("400" , "#2979ff"),
                ("700" , "#2962ff")]))]),

        "lightblue" : OrderedDict( [
            (  "50" , "#e1f5fe"),
            ( "100" , "#b3e5fc"),
            ( "200" , "#81d4fa"),
            ( "300" , "#4fc3f7"),
            ( "400" , "#29b6f6"),
            ( "500" , "#03a9f4"),
            ( "600" , "#039be5"),
            ( "700" , "#0288d1"),
            ( "800" , "#0277bd"),
            ( "900" , "#01579b"),
            ( "accent", OrderedDict([
                ("100" , "#80d8ff"),
                ("200" , "#40c4ff"),
                ("400" , "#00b0ff"),
                ("700" , "#0091ea")]))]),

        "cyan" : OrderedDict([
            (  "50" , "#e0f7fa"),
            ( "100" , "#b2ebf2"),
            ( "200" , "#80deea"),
            ( "300" , "#4dd0e1"),
            ( "400" , "#26c6da"),
            ( "500" , "#00bcd4"),
            ( "600" , "#00acc1"),
            ( "700" , "#0097a7"),
            ( "800" , "#00838f"),
            ( "900" , "#006064"),
            ( "accent", OrderedDict([
                ("100" , "#84ffff"),
                ("200" , "#18ffff"),
                ("400" , "#00e5ff"),
                ("700" , "#00b8d4")]))]),

        "teal" : OrderedDict( [
            (  "50" , "#e0f2f1"),
            ( "100" , "#b2dfdb"),
            ( "200" , "#80cbc4"),
            ( "300" , "#4db6ac"),
            ( "400" , "#26a69a"),
            ( "500" , "#009688"),
            ( "600" , "#00897b"),
            ( "700" , "#00796b"),
            ( "800" , "#00695c"),
            ( "900" , "#004d40"),
            ( "accent", OrderedDict([
                ("100" , "#a7ffeb"),
                ("200" , "#64ffda"),
                ("400" , "#1de9b6"),
                ("700" , "#00bfa5")]))]),

        "green" : OrderedDict( [
            (  "50" , "#e8f5e9"),
            ( "100" , "#c8e6c9"),
            ( "200" , "#a5d6a7"),
            ( "300" , "#81c784"),
            ( "400" , "#66bb6a"),
            ( "500" , "#4caf50"),
            ( "600" , "#43a047"),
            ( "700" , "#388e3c"),
            ( "800" , "#2e7d32"),
            ( "900" , "#1b5e20"),
            ( "accent", OrderedDict([
                ("100" , "#b9f6ca"),
                ("200" , "#69f0ae"),
                ("400" , "#00e676"),
                ("700" , "#00c853")]))]),

        "lightgreen" :  OrderedDict([
            (  "50" , "#f1f8e9"),
            ( "100" , "#dcedc8"),
            ( "200" , "#c5e1a5"),
            ( "300" , "#aed581"),
            ( "400" , "#9ccc65"),
            ( "500" , "#8bc34a"),
            ( "600" , "#7cb342"),
            ( "700" , "#689f38"),
            ( "800" , "#558b2f"),
            ( "900" , "#33691e"),
            ( "accent", OrderedDict([
                ("100" , "#ccff90"),
                ("200" , "#b2ff59"),
                ("400" , "#76ff03"),
                ("700" , "#64dd17")]))]),

        "lime" : OrderedDict([
            (  "50" , "#f9fbe7"),
            ( "100" , "#f0f4c3"),
            ( "200" , "#e6ee9c"),
            ( "300" , "#dce775"),
            ( "400" , "#d4e157"),
            ( "500" , "#cddc39"),
            ( "600" , "#c0ca33"),
            ( "700" , "#afb42b"),
            ( "800" , "#9e9d24"),
            ( "900" , "#827717"),
            ( "accent", OrderedDict([
                ("100" , "#f4ff81"),
                ("200" , "#eeff41"),
                ("400" , "#c6ff00"),
                ("700" , "#aeea00")]))]),

        "yellow" : OrderedDict([
            (  "50" , "#fffde7"),
            ( "100" , "#fff9c4"),
            ( "200" , "#fff59d"),
            ( "300" , "#fff176"),
            ( "400" , "#ffee58"),
            ( "500" , "#ffeb3b"),
            ( "600" , "#fdd835"),
            ( "700" , "#fbc02d"),
            ( "800" , "#f9a825"),
            ( "900" , "#f57f17"),
            ( "accent", OrderedDict([
                ("100" , "#ffff8d"),
                ("200" , "#ffff00"),
                ("400" , "#ffea00"),
                ("700" , "#ffd600")]))]),

        "amber" : OrderedDict([
            (  "50" , "#fff8e1"),
            ( "100" , "#ffecb3"),
            ( "200" , "#ffe082"),
            ( "300" , "#ffd54f"),
            ( "400" , "#ffca28"),
            ( "500" , "#ffc107"),
            ( "600" , "#ffb300"),
            ( "700" , "#ffa000"),
            ( "800" , "#ff8f00"),
            ( "900" , "#ff6f00"),
            ( "accent", OrderedDict([
                ("100" , "#ffe57f"),
                ("200" , "#ffd740"),
                ("400" , "#ffc400"),
                ("700" , "#ffab00")]))]),

        "orange" : OrderedDict( [
            (  "50" , "#fff3e0"),
            ( "100" , "#ffe0b2"),
            ( "200" , "#ffcc80"),
            ( "300" , "#ffb74d"),
            ( "400" , "#ffa726"),
            ( "500" , "#ff9800"),
            ( "600" , "#fb8c00"),
            ( "700" , "#f57c00"),
            ( "800" , "#ef6c00"),
            ( "900" , "#e65100"),
            ( "accent", OrderedDict([
                ("100" , "#ffd180"),
                ("200" , "#ffab40"),
                ("400" , "#ff9100"),
                ("700" , "#ff6d00")]))]),

        "deeporange" : OrderedDict([
            (  "50" , "#fbe9e7"),
            ( "100" , "#ffccbc"),
            ( "200" , "#ffab91"),
            ( "300" , "#ff8a65"),
            ( "400" , "#ff7043"),
            ( "500" , "#ff5722"),
            ( "600" , "#f4511e"),
            ( "700" , "#e64a19"),
            ( "800" , "#d84315"),
            ( "900" , "#bf360c"),
            ( "accent", OrderedDict([
                ("100" , "#ff9e80"),
                ("200" , "#ff6e40"),
                ("400" , "#ff3d00"),
                ("700" , "#dd2c00")]))]),

        "brown" : OrderedDict([
            ( "50" , "#efebe9"),
            ("100" , "#d7ccc8"),
            ("200" , "#bcaaa4"),
            ("300" , "#a1887f"),
            ("400" , "#8d6e63"),
            ("500" , "#795548"),
            ("600" , "#6d4c41"),
            ("700" , "#5d4037"),
            ("800" , "#4e342e"),
            ("900" , "#3e2723")]),

        "grey" : OrderedDict( [
            (" 50" , "#fafafa"),
            ("100" , "#f5f5f5"),
            ("200" , "#eeeeee"),
            ("300" , "#e0e0e0"),
            ("400" , "#bdbdbd"),
            ("500" , "#9e9e9e"),
            ("600" , "#757575"),
            ("700" , "#616161"),
            ("800" , "#424242"),
            ("900" , "#212121")]),

        "bluegrey" : OrderedDict([
            (" 50" , "#eceff1"),
            ("100" , "#cfd8dc"),
            ("200" , "#b0bec5"),
            ("300" , "#90a4ae"),
            ("400" , "#78909c"),
            ("500" , "#607d8b"),
            ("600" , "#546e7a"),
            ("700" , "#455a64"),
            ("800" , "#37474f"),
            ("900" , "#263238")]),

        "black" : "#000000",
        "white" : "#ffffff",
    },

    # Basic color keywords from W3C
    # http://www.w3.org/TR/css3-color/#html4
    "web" : {
        "black":   "#000000",
        "silver":  "#c0c0c0",
        "gray":    "#808080",
        "white":   "#ffffff",
        "maroon":  "#800000",
        "red":     "#ff0000",
        "purple":  "#800080",
        "fuchsia": "#ff00ff",
        "green":   "#008000",
        "lime":    "#00ff00",
        "olive":   "#808000",
        "yellow":  "#ffff00",
        "navy":    "#000080",
        "blue":    "#0000ff",
        "teal":    "#008080",
        "aqua":    "#00ffff"
    },


    # SVG color keywords from W3C
    # http://www.w3.org/TR/css3-color/#svg-color
    "svg" : {
        "aliceblue":            "#f0f8ff",
        "antiquewhite":         "#faebd7",
        "aqua":                 "#00ffff",
        "aquamarine":           "#7fffd4",
        "azure":                "#f0ffff",
        "beige":                "#f5f5dc",
        "bisque":               "#ffe4c4",
        "black":                "#000000",
        "blanchedalmond":       "#ffebcd",
        "blue":                 "#0000ff",
        "blueviolet":           "#8a2be2",
        "brown":                "#a52a2a",
        "burlywood":            "#deb887",
        "cadetblue":            "#5f9ea0",
        "chartreuse":           "#7fff00",
        "chocolate":            "#d2691e",
        "coral":                "#ff7f50",
        "cornflowerblue":       "#6495ed",
        "cornsilk":             "#fff8dc",
        "crimson":              "#dc143c",
        "cyan":                 "#00ffff",
        "darkblue":             "#00008b",
        "darkcyan":             "#008b8b",
        "darkgoldenrod":        "#b8860b",
        "darkgray":             "#a9a9a9",
        "darkgrey":             "#a9a9a9",
        "darkgreen":            "#006400",
        "darkkhaki":            "#bdb76b",
        "darkmagenta":          "#8b008b",
        "darkolivegreen":       "#556b2f",
        "darkorange":           "#ff8c00",
        "darkorchid":           "#9932cc",
        "darkred":              "#8b0000",
        "darksalmon":           "#e9967a",
        "darkseagreen":         "#8fbc8f",
        "darkslateblue":        "#483d8b",
        "darkslategray":        "#2f4f4f",
        "darkslategrey":        "#2f4f4f",
        "darkturquoise":        "#00ced1",
        "darkviolet":           "#9400d3",
        "deeppink":             "#ff1493",
        "deepskyblue":          "#00bfff",
        "dimgray":              "#696969",
        "dimgrey":              "#696969",
        "dodgerblue":           "#1e90ff",
        "firebrick":            "#b22222",
        "floralwhite":          "#fffaf0",
        "forestgreen":          "#228b22",
        "fuchsia":              "#ff00ff",
        "gainsboro":            "#dcdcdc",
        "ghostwhite":           "#f8f8ff",
        "gold":                 "#ffd700",
        "goldenrod":            "#daa520",
        "gray":                 "#808080",
        "grey":                 "#808080",
        "green":                "#008000",
        "greenyellow":          "#adff2f",
        "honeydew":             "#f0fff0",
        "hotpink":              "#ff69b4",
        "indianred":            "#cd5c5c",
        "indigo":               "#4b0082",
        "ivory":                "#fffff0",
        "khaki":                "#f0e68c",
        "lavender":             "#e6e6fa",
        "lavenderblush":        "#fff0f5",
        "lawngreen":            "#7cfc00",
        "lemonchiffon":         "#fffacd",
        "lightblue":            "#add8e6",
        "lightcoral":           "#f08080",
        "lightcyan":            "#e0ffff",
        "lightgoldenrodyellow": "#fafad2",
        "lightgray":            "#d3d3d3",
        "lightgrey":            "#d3d3d3",
        "lightgreen":           "#90ee90",
        "lightpink":            "#ffb6c1",
        "lightsalmon":          "#ffa07a",
        "lightseagreen":        "#20b2aa",
        "lightskyblue":         "#87cefa",
        "lightslategray":       "#778899",
        "lightslategrey":       "#778899",
        "lightsteelblue":       "#b0c4de",
        "lightyellow":          "#ffffe0",
        "lime":                 "#00ff00",
        "limegreen":            "#32cd32",
        "linen":                "#faf0e6",
        "magenta":              "#ff00ff",
        "maroon":               "#800000",
        "mediumaquamarine":     "#66cdaa",
        "mediumblue":           "#0000cd",
        "mediumorchid":         "#ba55d3",
        "mediumpurple":         "#9370d8",
        "mediumseagreen":       "#3cb371",
        "mediumslateblue":      "#7b68ee",
        "mediumspringgreen":    "#00fa9a",
        "mediumturquoise":      "#48d1cc",
        "mediumvioletred":      "#c71585",
        "midnightblue":         "#191970",
        "mintcream":            "#f5fffa",
        "mistyrose":            "#ffe4e1",
        "moccasin":             "#ffe4b5",
        "navajowhite":          "#ffdead",
        "navy":                 "#000080",
        "oldlace":              "#fdf5e6",
        "olive":                "#808000",
        "olivedrab":            "#6b8e23",
        "orange":               "#ffa500",
        "orangered":            "#ff4500",
        "orchid":               "#da70d6",
        "palegoldenrod":        "#eee8aa",
        "palegreen":            "#98fb98",
        "paleturquoise":        "#afeeee",
        "palevioletred":        "#d87093",
        "papayawhip":           "#ffefd5",
        "peachpuff":            "#ffdab9",
        "peru":                 "#cd853f",
        "pink":                 "#ffc0cb",
        "plum":                 "#dda0dd",
        "powderblue":           "#b0e0e6",
        "purple":               "#800080",
        "red":                  "#ff0000",
        "rosybrown":            "#bc8f8f",
        "royalblue":            "#4169e1",
        "saddlebrown":          "#8b4513",
        "salmon":               "#fa8072",
        "sandybrown":           "#f4a460",
        "seagreen":             "#2e8b57",
        "seashell":             "#fff5ee",
        "sienna":               "#a0522d",
        "silver":               "#c0c0c0",
        "skyblue":              "#87ceeb",
        "slateblue":            "#6a5acd",
        "slategray":            "#708090",
        "slategrey":            "#708090",
        "snow":                 "#fffafa",
        "springgreen":          "#00ff7f",
        "steelblue":            "#4682b4",
        "tan":                  "#d2b48c",
        "teal":                 "#008080",
        "thistle":              "#d8bfd8",
        "tomato":               "#ff6347",
        "turquoise":            "#40e0d0",
        "violet":               "#ee82ee",
        "wheat":                "#f5deb3",
        "white":                "#ffffff",
        "whitesmoke":           "#f5f5f5",
        "yellow":               "#ffff00",
        "yellowgreen":          "#9acd32"
    }
} )


def get(name):
    """
    get("white")
    get("svg:white")
    get("material:red:100")
    get("material:red:accent:100")
    get("material:red:*")
    """

    def flatten(d):
        values = []
        if isinstance(d, dict):
            for value in d.values():
                values.extend(flatten(value))
        else:
            values.append(d)
        return values

    name = name.lower().strip()
    name = name.replace(' ','')
    name = name.replace('-','')

    items = name.split(":")
    if len(items) == 1:
        domain = colors['svg']
    elif len(items) == 2:
        domain = colors[items[0]]
        name = items[1]
    elif len(items) == 3:
        domain = colors[items[0]][items[1]]
        name = items[2]
    elif len(items) == 4:
        domain = colors[items[0]][items[1]][items[2]]
        name = items[3]

    if name != '*':
        return domain[name]
    else:
        return flatten(domain)
