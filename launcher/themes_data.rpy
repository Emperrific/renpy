init 1 python:

    # This is a list of (theme name, theme function, theme exemplar) tuples.
    themes = [
        ("Roundrect", "roundrect", "Basic Blue"),
        ("Bordered", "bordered", "Dramatic Flesh"),
        ("Diamond", "diamond", "Colorblind"),
        ("Regal", "regal", "Fine China"),
        ("Austen", "austen", "White Chocolate"),
        ("TV", "tv", "Old Polaroid"),
        ("3D", "threeD", "Colorblind"),
        ("Glow", "glow", "Really Red"),
        ("Marker", "marker", "Creamsicle"),
        ("Crayon", "crayon", "First Valentines"),
        ]

    # This is a map from theme function to template text that sensibly calls
    # that function.
    theme_templates = { }
    
    theme_templates["roundrect"] = """\
    theme.roundrect(
        # Color scheme: %(name)s
                                    
        ## The color of an idle widget face.
        widget = "%(widget)s",

        ## The color of a focused widget face.
        widget_hover = "%(widget_hover)s",

        ## The color of the text in a widget.
        widget_text = "%(widget_text)s",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        widget_selected = "%(widget_selected)s",

        ## The color of a disabled widget face. 
        disabled = "%(disabled)s",

        ## The color of disabled widget text.
        disabled_text = "%(disabled_text)s",

        ## The color of informational labels.
        label = "%(label)s",

        ## The color of a frame containing widgets.
        frame = "%(frame)s",

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        mm_root = "%(mm_root)s",

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        gm_root = "%(gm_root)s",

        ## If this is True, the in-game window is rounded. If False,
        ## the in-game window is square.
        rounded_window = False,

        ## And we're done with the theme. The theme will customize
        ## various styles, so if we want to change them, we should
        ## do so below.            
        )"""

    theme_templates["bordered"] = theme_templates["roundrect"].replace("roundrect", "bordered")
    theme_templates["diamond"] = theme_templates["roundrect"].replace("roundrect", "diamond")
    theme_templates["tv"] = theme_templates["roundrect"].replace("roundrect", "tv")
    theme_templates["glow"] = theme_templates["roundrect"].replace("roundrect", "glow")
    theme_templates["regal"] = theme_templates["roundrect"].replace("roundrect", "regal")
    theme_templates["crayon"] = theme_templates["roundrect"].replace("roundrect", "crayon")
    theme_templates["threeD"] = theme_templates["roundrect"].replace("roundrect", "threeD")
    theme_templates["marker"] = theme_templates["roundrect"].replace("roundrect", "marker")
    theme_templates["austen"] = theme_templates["roundrect"].replace("roundrect", "austen")
    
    # This is a map from theme name to the code needed to implement that
    # theme.
    theme_data = {
        'Basic Blue': {'disabled': '#404040',
                       'disabled_text': '#c8c8c8',
                       'frame': '#6496c8',
                       'gm_root': '#dcebff',
                       'label': '#ffffff',
                       'mm_root': '#dcebff',
                       'widget': '#003c78',
                       'widget_hover': '#0050a0',
                       'widget_selected': '#ffffc8',
                       'widget_text': '#c8ffff'},
        'Bloody Mary': {'disabled': '#400000',
                        'disabled_text': '#260000',
                        'frame': '#400808',
                        'gm_root': '#000000',
                        'label': '#ffffff',
                        'mm_root': '#000000',
                        'widget': '#000000',
                        'widget_hover': '#830000',
                        'widget_selected': '#ffffff',
                        'widget_text': '#C2C2C2'},
        'Colorblind': {'disabled': '#898989',
                       'disabled_text': '#666666',
                       'frame': '#252525',
                       'gm_root': '#393939',
                       'label': '#c2c2c2',
                       'mm_root': '#393939',
                       'widget': '#898989',
                       'widget_hover': '#464646',
                       'widget_selected': '#F2F2F2',
                       'widget_text': '#CCCCCC'},
        'Cotton Candy': {'disabled': '#C8AFA1',
                         'disabled_text': '#E1D4C9',
                         'frame': '#FCF5F2',
                         'gm_root': '#D0B4BA',
                         'label': '#805C40',
                         'mm_root': '#D0B4BA',
                         'widget': '#ECC7D0',
                         'widget_hover': '#E1D4C9',
                         'widget_selected': '#805C40',
                         'widget_text': '#805C40'},
        'Creamsicle': {'disabled': '#FFECBF',
                       'disabled_text': '#ffffff',
                       'frame': '#FFECBF',
                       'gm_root': '#FDF5E3',
                       'label': '#502F13',
                       'mm_root': '#FDF5E3',
                       'widget': '#D96B00',
                       'widget_hover': '#FD9B1C',
                       'widget_selected': '#ffffff',
                       'widget_text': '#FCE6B1'},
        'Dramatic Flesh': {'disabled': '#ab6038',
                           'disabled_text': '#BF7C51',
                           'frame': '#49271b',
                           'gm_root': '#2a201f',
                           'label': '#ffffff',
                           'mm_root': '#2a201f',
                           'widget': '#BF7C51',
                           'widget_hover': '#dda570',
                           'widget_selected': '#ffffff',
                           'widget_text': '#E5DFDF'},
        'Easter Baby': {'disabled': '#DDE9FF',
                        'disabled_text': '#A6AFBF',
                        'frame': '#CCF8DC',
                        'gm_root': '#FBF9DF',
                        'label': '#698071',
                        'mm_root': '#FBF9DF',
                        'widget': '#F5D4EE',
                        'widget_hover': '#F0DDFF',
                        'widget_selected': '#000000',
                        'widget_text': '#698071'},
        'Favorite Jeans': {'disabled': '#919994',
                           'disabled_text': '#B6BFB9',
                           'frame': '#6f7571',
                           'gm_root': '#b0b8ba',
                           'label': '#ffffff',
                           'mm_root': '#b0b8ba',
                           'widget': '#8699a7',
                           'widget_hover': '#9eb1ad',
                           'widget_selected': '#ffffff',
                           'widget_text': '#dcdfd6'},
        'Fine China': {'disabled': '#ADB9CC',
                       'disabled_text': '#DFBA14',
                       'frame': '#ADB9CC',
                       'gm_root': '#F7F7FA',
                       'label': '#39435E',
                       'mm_root': '#F7F7FA',
                       'widget': '#6A7183',
                       'widget_hover': '#1A2B47',
                       'widget_selected': '#E3E3E4',
                       'widget_text': '#C9C9CB'},
        'First Valentines': {'disabled': '#F8F2D0',
                             'disabled_text': '#BFA1A1',
                             'frame': '#F8F2D0',
                             'gm_root': '#D98989',
                             'label': '#5D1010',
                             'mm_root': '#D98989',
                             'widget': '#F09898',
                             'widget_hover': '#D6C5BB',
                             'widget_selected': '#B31E1E',
                             'widget_text': '#593131'},
        'Ice Queen': {'disabled': '#F0F2F2',
                      'disabled_text': '#FBFBFB',
                      'frame': '#ffffff',
                      'gm_root': '#E6E6E6',
                      'label': '#D9D9D9',
                      'mm_root': '#E6E6E6',
                      'widget': '#D9D9D9',
                      'widget_hover': '#F0F2F2',
                      'widget_selected': '#737373',
                      'widget_text': '#ffffff'},
        'Mocha Latte': {'disabled': '#614D3A',
                        'disabled_text': '#80654D',
                        'frame': '#926841',
                        'gm_root': '#1A140E',
                        'label': '#F1EBE5',
                        'mm_root': '#1A140E',
                        'widget': '#4D3B29',
                        'widget_hover': '#996E45',
                        'widget_selected': '#ffffff',
                        'widget_text': '#B99D83'},
        'Muted Horror': {'disabled': '#73735C',
                         'disabled_text': '#8C8C70',
                         'frame': '#555544',
                         'gm_root': '#1A0001',
                         'label': '#1A0001',
                         'mm_root': '#1A0001',
                         'widget': '#777777',
                         'widget_hover': '#73735C',
                         'widget_selected': '#000000',
                         'widget_text': '#404033'},
        'Old Polaroid': {'disabled': '#A89E7D',
                         'disabled_text': '#CCC097',
                         'frame': '#49403E',
                         'gm_root': '#A84A3E',
                         'label': '#ffffff',
                         'mm_root': '#A84A3E',
                         'widget': '#A89E7D',
                         'widget_hover': '#8DB6B9',
                         'widget_selected': '#ffffff',
                         'widget_text': '#49403E'},
        'Really Red': {'disabled': '#404040',
                       'disabled_text': '#c8c8c8',
                       'frame': '#e17373',
                       'gm_root': '#ffd0d0',
                       'label': '#ffffff',
                       'mm_root': '#ffd0d0',
                       'widget': '#963232',
                       'widget_hover': '#c83232',
                       'widget_selected': '#ffffc8',
                       'widget_text': '#ffffff'},
        'Summer Sky': {'disabled': '#6074BF',
                       'disabled_text': '#7383BF',
                       'frame': '#6074BF',
                       'gm_root': '#B4CDD4',
                       'label': '#94C7D4',
                       'mm_root': '#B4CDD4',
                       'widget': '#F2E6AA',
                       'widget_hover': '#FCFCA4',
                       'widget_selected': '#1A5766',
                       'widget_text': '#7DA8B3'},
        'Swamp Critter': {'disabled': '#A2521D',
                          'disabled_text': '#753D00',
                          'frame': '#797C1C',
                          'gm_root': '#B09D5A',
                          'label': '#ffffff',
                          'mm_root': '#B09B4F',
                          'widget': '#753D00',
                          'widget_hover': '#B19A48',
                          'widget_selected': '#ffffff',
                          'widget_text': '#CCCAC2'},
        'Urban Sprawl': {'disabled': '#8F0000',
                         'disabled_text': '#333333',
                         'frame': '#8F0000',
                         'gm_root': '#000000',
                         'label': '#ffffff',
                         'mm_root': '#000000',
                         'widget': '#333333',
                         'widget_hover': '#000000',
                         'widget_selected': '#ffffff',
                         'widget_text': '#6C8A2F'},
        'Victorian Gingerbread': {'disabled': '#7A674F',
                                  'disabled_text': '#664F33',
                                  'frame': '#BF8A73',
                                  'gm_root': '#695640',
                                  'label': '#F2EDC4',
                                  'mm_root': '#695640',
                                  'widget': '#7A674F',
                                  'widget_hover': '#BDA77D',
                                  'widget_selected': '#FDFBEE',
                                  'widget_text': '#F2EDC4'},
        'Watermelon Pie': {'disabled': '#FABF46',
                           'disabled_text': '#FFE06D',
                           'frame': '#C3CD91',
                           'gm_root': '#F7F7C5',
                           'label': '#FCFCD7',
                           'mm_root': '#F7F7C5',
                           'widget': '#FFE06D',
                           'widget_hover': '#E38A4F',
                           'widget_selected': '#996600',
                           'widget_text': '#FAA700'},
        'White Chocolate': {'disabled': '#614D3A',
                            'disabled_text': '#80654D',
                            'frame': '#926841',
                            'gm_root': '#FBF9EA',
                            'label': '#F1EBE5',
                            'mm_root': '#FBF9EA',
                            'widget': '#33271C',
                            'widget_hover': '#ECE7C4',
                            'widget_selected': '#ffffff',
                            'widget_text': '#B99D83'},
        'Winter Mint': {'disabled': '#426143',
                        'disabled_text': '#819981',
                        'frame': '#245536',
                        'gm_root': '#e5f1e5',
                        'label': '#ffffff',
                        'mm_root': '#e5f1e5',
                        'widget': '#7AA27B',
                        'widget_hover': '#A3C7A3',
                        'widget_selected': '#ffffff',
                        'widget_text': '#CDE0CE'}}

