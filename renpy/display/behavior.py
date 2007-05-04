# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This contains various Displayables that handle events.


import renpy
from renpy.display.render import render

import pygame
from pygame.constants import *

def map_event(ev, name):
    """
    This looks up the name in the keymap, and uses it to determine if
    the given event was caused by one of the keys or mouse buttons
    mapped to the given name in config.keymap. If so, it returns
    True, otherwise it returns False.
    """
    
    keys = renpy.config.keymap.get(name, [ name ])

    if ev.type == MOUSEBUTTONDOWN:
        if ( "mousedown_" + str(ev.button) ) in keys:
            return True
        else:
            return False

    if ev.type == MOUSEBUTTONUP:
        if ( "mouseup_" + str(ev.button) ) in keys:
            return True
        else:
            return False

    if ev.type == KEYDOWN:
        for key in keys:
            if key == ev.unicode or ev.key == getattr(pygame.constants, key, None):
                return True

        return False

    if ev.type == renpy.display.core.JOYEVENT and ev.press:
        for key in keys:
            if renpy.game.preferences.joymap.get(key, None) == ev.press:
                return True

    return False

def map_keyup(ev, name):

    keys = renpy.config.keymap[name]
    
    if ev.type == KEYUP:
        for key in keys:
            if ev.key == getattr(pygame.constants, key, None):
                return True

    if ev.type == renpy.display.core.JOYEVENT and ev.release:
        for key in keys:
            if renpy.game.preferences.joymap.get(key, None) == ev.release:
                return True
            
    return False
    
        
def is_pressed(pressed, name):
    """
    This looks the given name up in the keymap. For each binding of the
    form K_whatever, it checks to see if the given key is pressed, and if
    so, returns the keycode of the pressed key. Otherwise, returns False.
    """

    keys = renpy.config.keymap[name]

    for key in keys:
        code = getattr(pygame.constants, key)
        if pressed[code]:
            return code

    return False

def skipping(ev):
    """
    This handles setting skipping in response to the press of one of the
    CONTROL keys. The library handles skipping in response to TAB.
    """

    if map_event(ev, "skip"):
        renpy.config.skipping = "slow"
        renpy.exports.restart_interaction()

    if map_keyup(ev, "skip"):
        renpy.config.skipping = None
        renpy.exports.restart_interaction()

    return

class Keymap(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, **keymap):
        super(Keymap, self).__init__(style='default')
        self.keymap = keymap

    def event(self, ev, x, y, st):

        for name, action in self.keymap.iteritems():
            if map_event(ev, name):
                rv = action()
                
                if rv is not None:
                    return rv
                
                raise renpy.display.core.IgnoreEvent()


class RollForward(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to functions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, value):
        super(RollForward, self).__init__(style='default')
        self.value = value

        
    def event(self, ev, x, y, st):
        
        if map_event(ev, "rollforward"):
            renpy.game.interface.suppress_transition = True
            renpy.game.after_rollback = True
            return self.value

class PauseBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the Pause behavior, which is to
    return a value after a certain amount of time has elapsed.
    """

    def __init__(self, delay, result=False):
        super(PauseBehavior, self).__init__()

        self.delay = delay
        self.result = result 


    def event(self, ev, x, y, st):

        if self.delay is not None and st >= self.delay:
            return self.result

        renpy.game.interface.timeout(self.delay - st)

class SayBehavior(renpy.display.layout.Null):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    focusable = True

    def __init__(self, default=True, afm=None, dismiss=[ 'dismiss' ], allow_dismiss=None, **properties):
        super(SayBehavior, self).__init__(default=default, **properties)

        if not isinstance(dismiss, (list, tuple)):
            dismiss = [ dismiss ]

        if afm is not None:
            self.afm_length = len(afm)
        else:
            self.afm_length = None

        # What keybindings lead to dismissal?
        self.dismiss = dismiss

        self.allow_dismiss = allow_dismiss
        
    def set_afm_length(self, afm_length):
        self.afm_length = afm_length
              
    def event(self, ev, x, y, st):

        skip_delay = renpy.config.skip_delay / 1000.0

        if renpy.config.allow_skipping and renpy.config.skipping and \
           st >= skip_delay:

            if renpy.game.preferences.skip_unseen:
                return True
            elif renpy.config.skipping == "fast":
                return True
            elif renpy.game.context().seen_current(True):
                return True

        if renpy.config.allow_skipping and renpy.config.skipping and \
           st < skip_delay:
            renpy.game.interface.timeout(skip_delay - st)

        if self.afm_length and renpy.game.preferences.afm_time:
                                                          
            afm_delay = ( 1.0 * ( renpy.config.afm_bonus + self.afm_length ) / renpy.config.afm_characters ) * renpy.game.preferences.afm_time

            if renpy.game.preferences.text_cps:
                afm_delay += 1.0 / renpy.game.preferences.text_cps * self.afm_length

            if st > afm_delay:
                if renpy.config.afm_callback:
                    if renpy.config.afm_callback():
                        return True
                    else:
                        renpy.game.interface.timeout(0.1)
                else:
                    return True
            else:
                renpy.game.interface.timeout(afm_delay - st)

        for dismiss in self.dismiss:

            if map_event(ev, dismiss) and self.is_focused():

                if renpy.config.skipping:
                    renpy.config.skipping = None
                    renpy.exports.restart_interaction()
                    raise renpy.display.core.IgnoreEvent()

                if self.allow_dismiss:
                    if not self.allow_dismiss():
                        raise renpy.display.core.IgnoreEvent()

                return True
                    
                

        # if map_event(ev, "rollforward"):
        #    if renpy.game.context().seen_current(False):
        #         return True
            
        return None
        
class Button(renpy.display.layout.Window):

    def __init__(self, child, style='button', clicked=None,
                 hovered=None, unhovered=None, role='',
                 **properties):

        super(Button, self).__init__(child, style=style, **properties)

        self.activated = False
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.focusable = clicked is not None
        self.role = role
        self.stoff = -self.style.initial_time_offset
        
    def render(self, width, height, st, at):

        if self.stoff is None:
            self.stoff = st

        st -= self.stoff
        
        rv = super(Button, self).render(width, height, st, at)

        if self.clicked:

            rect = self.style.focus_rect
            if rect is not None:
                fx, fy, fw, fh = rect
            else:
                fx = self.style.left_margin
                fy = self.style.top_margin
                fw = rv.width - self.style.right_margin
                fh = rv.height - self.style.bottom_margin

            mask = self.style.focus_mask

            if mask is True:
                mask = rv
            elif mask is not None:
                mask = renpy.easy.displayable(mask)
                mask = renpy.display.render.render(mask, rv.width, rv.height, st, at)

            if mask is not None:
                fmx = 0
                fmy = 0
            else:
                fmx = None
                fmy = None
                
            rv.add_focus(self, None,
                         fx, fy, fw, fh,
                         fmx, fmy, mask)
            
        return rv


    def focus(self, default=False):
        super(Button, self).focus(default)

        if not default:
            self.stoff = None

        if self.hovered and not default:
            return self.hovered()


    def unfocus(self):
        super(Button, self).unfocus()

        self.stoff = None
        
        if self.unhovered:
            self.unhovered()

    def per_interact(self):
        if not self.clicked:
            self.set_style_prefix(self.role + "insensitive_")

    def event(self, ev, x, y, st):

        # We deactivate on an event.
        if self.activated:
            self.activated = False

            if self.focusable:
                if self.is_focused():
                    self.set_style_prefix(self.role + 'hover_')
                else:
                    self.set_style_prefix(self.role + 'idle_')
            else:
                self.set_style_prefix(self.role + 'insensitive_')

        # If not focused, ignore all events.
        if not self.is_focused():
            return None

        
        # If clicked, 
        if map_event(ev, "button_select") and self.clicked:

            self.activated = True

            renpy.audio.sound.play(self.style.activate_sound)

            rv = self.clicked()

            if rv is not None:
                return rv
            else:
                raise renpy.display.core.IgnoreEvent()
                    
        return None


# Reimplementation of the TextButton widget as a Button and a Text
# widget.
def TextButton(text, style='button', text_style='button_text',
               clicked=None, **properties):

    text = renpy.display.text.Text(text, style=text_style)
    return Button(text, style=style, clicked=clicked, **properties)

                
class Input(renpy.display.text.Text):
    """
    This is a Displayable that takes text as input.
    """

    def __init__(self, default, length=None,
                 style='input_text',
                 allow=None,
                 exclude=None,
                 **properties):

        super(Input, self).__init__(default.replace("{", "{{") + "_", style=style, **properties)

        self.content = unicode(default)
        self.length = length

        self.allow = allow
        self.exclude = exclude

    def event(self, ev, x, y, st):

        if map_event(ev, "input_backspace"):
            if self.content:
                self.content = self.content[:-1]

            self.set_text(self.content.replace("{", "{{") + "_")
            renpy.display.render.redraw(self, 0)

        elif map_event(ev, "input_enter"):
            return self.content

        elif ev.type == KEYDOWN and ev.unicode:
            if ord(ev.unicode[0]) < 32:
                return None
                
            if self.length and len(self.content) >= self.length:
                raise renpy.display.core.IgnoreEvent()

            if self.allow and ev.unicode not in self.allow:
                raise renpy.display.core.IgnoreEvent()

            if self.exclude and ev.unicode in self.exclude:
                raise renpy.display.core.IgnoreEvent()

            self.content += ev.unicode

            self.set_text(self.content.replace("{", "{{") + "_")
            renpy.display.render.redraw(self, 0)

            raise renpy.display.core.IgnoreEvent()
                

class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """
    
    def __init__(self, range, value, width=None, height=None,
                 changed=None, style='bar', **properties):

        if width is not None:
            properties['xmaximum'] = width

        if height is not None:
            properties['ymaximum'] = height

        super(Bar, self).__init__(style=style, **properties)

        self.range = range
        self.value = value
        self.changed = changed
        self.focusable = changed is not None

    def visit(self):
        return [ self.style.left_bar, self.style.right_bar ]
        
    def render(self, width, height, st, at):

        # Store the width and height for the event function to use.
        self.width = width
        self.height = height

        if self.style.bar_invert:
            value = self.range - self.value
        else:
            value = self.value

        if self.style.bar_vertical:

            tgutter = self.style.top_gutter
            bgutter = self.style.bottom_gutter

            zone_height = height - tgutter - bgutter

            bottom_height = zone_height * value // self.range
            top_height = zone_height - bottom_height

            top_height += tgutter
            bottom_height += bgutter

            rv = renpy.display.render.Render(width, height)

            tsurf = render(self.style.top_bar, width, height, st, at)
            bsurf = render(self.style.bottom_bar, width, height, st, at)

            if self.style.thumb_shadow:
                surf = render(self.style.thumb_shadow, width, height, st, at)
                rv.blit(surf, (0, top_height + self.style.thumb_offset))

            rv.blit(tsurf.subsurface((0, 0, width, top_height)), (0, 0))
            rv.blit(bsurf.subsurface((0, top_height, width, bottom_height)),
                    (0, top_height))

            if self.style.thumb:
                surf = render(self.style.thumb, width, height, st, at)
                rv.blit(surf, (0, top_height + self.style.thumb_offset))

            if self.changed:
                rv.add_focus(self, None, 0, 0, width, height)

        else:

            lgutter = self.style.left_gutter
            rgutter = self.style.right_gutter

            zone_width = width - lgutter - rgutter

            left_width = zone_width * value // self.range
            right_width = zone_width - left_width

            left_width += lgutter
            right_width += rgutter

            rv = renpy.display.render.Render(width, height)

            lsurf = render(self.style.left_bar, width, height, st, at)
            rsurf = render(self.style.right_bar, width, height, st, at)

            if self.style.thumb_shadow:
                surf = render(self.style.thumb_shadow, width, height, st, at)
                rv.blit(surf, (left_width + self.style.thumb_offset, 0))

            rv.blit(lsurf.subsurface((0, 0, left_width, height)), (0, 0))
            rv.blit(rsurf.subsurface((left_width, 0, right_width, height)),
                    (left_width, 0))

            if self.style.thumb:
                surf = render(self.style.thumb, width, height, st, at)
                rv.blit(surf, (left_width + self.style.thumb_offset, 0))

            if self.changed:
                rv.add_focus(self, None, 0, 0, width, height)

        return rv
        
    def event(self, ev, x, y, st):

        if not self.changed:
            return

        if not self.is_focused():
            return

        old_value = self.value

        value = self.value
        if self.style.bar_invert:
            value = self.range - value

        grabbed = (renpy.display.focus.get_grab() is self)
        just_grabbed = False
            
        if not grabbed and map_event(ev, "bar_activate"):
            renpy.display.focus.set_grab(self)
            just_grabbed = True
            grabbed = True

        if grabbed:

            if map_event(ev, "bar_decrease"):
                value -= 1

            if map_event(ev, "bar_increase"):
                value += 1

            if ev.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):

                if self.style.bar_vertical:

                    tgutter = self.style.left_gutter
                    bgutter = self.style.right_gutter
                    zone_width = self.height - tgutter - bgutter

                    value = (self.height - bgutter - y) * self.range / zone_width

                else:
                    lgutter = self.style.left_gutter
                    rgutter = self.style.right_gutter
                    zone_width = self.width - lgutter - rgutter
                
                    value = (x - lgutter) * self.range / zone_width

            if isinstance(self.range, int):
                value = int(value)
                    
            if value < 0:
                value = 0

            if value > self.range:
                value = self.range

            if self.style.bar_invert:
                value = self.range - value

            self.value = value


        if grabbed and not just_grabbed and map_event(ev, "bar_deactivate"):
            renpy.display.focus.set_grab(None)

        if self.value != old_value:
            renpy.display.render.redraw(self, 0)
            return self.changed(self.value)

        return
        
     
class Conditional(renpy.display.layout.Container):
    """
    This class renders its child if and only if the condition is
    true. Otherwise, it renders nothing. (Well, a Null). 

    Warning: the condition MUST NOT update the game state in any
    way, as that would break rollback.
    """

    def __init__(self, condition, *args):
        super(Conditional, self).__init__(*args)

        self.condition = condition
        self.null = renpy.display.layout.Null()

        self.state = eval(self.condition, vars(renpy.store))

    def render(self, width, height, st, at):
        if self.state:
            return render(self.child, width, height, st, at)
        else:
            return render(self.null, width, height, st, at)

    def event(self, ev, x, y, st):

        state = eval(self.condition, vars(renpy.store))

        if state != self.state:
            renpy.display.render.redraw(self, 0)

        self.state = state

        if state:
            return self.child.event(ev, x, y, st)
        
            
