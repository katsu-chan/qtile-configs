# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.backend.wayland import InputConfig
from libqtile.backend.wayland.inputs import CLICK_METHODS
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os


@lazy.function
def brightness(qtile, val=16, increase=False):
    with open("/sys/class/backlight/amdgpu_bl1/brightness", "w+") as f:
        f.write(
            str(int(f.readline()) + val * (int(increase) * 2 - 1))
        )  # increase ? read + val : read - val


mod = "mod4"
# terminal = guess_terminal()
terminal = "wezterm"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key(
        ["mod1", "control"],
        "F1",
        lazy.core.change_vt(1),
        desc="Go to virtual console 1",
    ),
    Key(
        ["mod1", "control"],
        "F2",
        lazy.core.change_vt(2),
        desc="Go to virtual console 2",
    ),
    Key(
        ["mod1", "control"],
        "F3",
        lazy.core.change_vt(3),
        desc="Go to virtual console 3",
    ),
    Key(
        ["mod1", "control"],
        "F4",
        lazy.core.change_vt(4),
        desc="Go to virtual console 4",
    ),
    Key(
        ["mod1", "control"],
        "F5",
        lazy.core.change_vt(5),
        desc="Go to virtual console 5",
    ),
    Key(
        ["mod1", "control"],
        "F6",
        lazy.core.change_vt(6),
        desc="Go to virtual console 6",
    ),
    Key(
        ["mod1", "control"],
        "F7",
        lazy.core.change_vt(7),
        desc="Go to virtual console 7",
    ),
    Key(
        ["mod1", "control"],
        "F8",
        lazy.core.change_vt(8),
        desc="Go to virtual console 8",
    ),
    Key(
        ["mod1", "control"],
        "F9",
        lazy.core.change_vt(9),
        desc="Go to virtual console 9",
    ),
    # Run xeyes
    Key([mod], "y", lazy.spawn("xeyes")),
    # Brightness
    Key([], 232, brightness(), desc="brightness--"),
    Key([], 233, brightness(increase=True), desc="brightness++"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

layouts = [
    layout.VerticalTile(),
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    floating_layout,
    # layout.Floating(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="roboto",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

ticker = widget.CryptoTicker(
    crypto="TON",
    currency="USDT",
    api="binance",
    update_interval=1,
    #    mouse_callbacks={"Button1": ticker.force_update},
    format="{crypto}: {symbol}{amount:,.3f}",
)

ticker.add_callbacks({"Button1": ticker.force_update})

battery = widget.Battery()

battery.add_callbacks({"Button1": battery.force_update})

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.LaunchBar(),
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                # widget.TaskList(),
                widget.WindowName(format="{state}{name}"),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Sep(),
                widget.KeyboardLayout(
                    configured_keyboards=["us colemak", "ru rulemak", "us"]
                ),
                widget.Sep(),
                battery,
                widget.Sep(),
                ticker,
                widget.Sep(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                # widget.Spacer(length=4),
                widget.Sep(),
                widget.QuickExit(
                    default_text="[X]", countdown_format="[{}]", foreground="#d75f5f"
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        wallpaper="/home/eve/wallpaper",
        wallpaper_mode="stretch",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

keys.extend(
    [
        Key(
            [mod],
            "space",
            lazy.widget["keyboardlayout"].next_keyboard(),
            desc="Next keyboard layout",
        )
    ]
)

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "*": InputConfig(tap=True, natural_scroll=True),
    #    "type:touchpad": InputConfig(tap=False, click_method="button_areas"),
}

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

os.environ["XDG_SESSION_DESKTOP"] = "wlroots"
os.environ["XDG_CURRENT_DESKTOP"] = "wlroots"

from subprocess import call, DEVNULL

call("/home/eve/.config/qtile/config.sh", stdout=DEVNULL, stderr=DEVNULL)
