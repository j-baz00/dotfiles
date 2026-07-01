# ~/.config/qtile/config.py

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess

#login items
@hook.subscribe.startup_once
def autostart():
    #background, display, input
    subprocess.Popen(["feh", "--bg-fill", "/home/julian/pictures/mtn.jpg"])
    subprocess.Popen(["xrandr", "--output", "HDMI-1", "--primary"])
    subprocess.Popen(["picom", "--daemon"])
    #subprocess.Popen(["xset", "r", "rate", "200", "50"  ])

    #lock screen and suspend
    subprocess.Popen(["xset", "s", "600"]) 
    subprocess.Popen(["xss-lock", "--", "/home/julian/.config/qtile/lock.sh"])
    subprocess.Popen(["xset", "+dpms"])
    subprocess.Popen(["xset", "dpms", "0", "0", "900"])

    #notifications daemon, polkit, other backend stuff you want running
    subprocess.Popen(["dunst"])
    subprocess.Popen(["/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1"])

COLORS = {
    "bg":      "#0d1117",  
    "bg_alt":  "#161b22",  # the bar
    "bg_high": "#21262d",  # hovers, active-group fill
    "fg":      "#c9d1d9",  # primary text
    "fg_dim":  "#8b949e",  # muted text / inactive
    "border":  "#30363d",  # inactive window border
    "blue":    "#58a6ff",
    "green":   "#3fb950",
    "yellow":  "#d29922",
    "orange":  "#ffa657",
    "red":     "#f85149",
    "purple":  "#bc8cff",
    "cyan":    "#39c5cf",
    "pink":    "#f778ba",
}

FONT      = "JetBrains Mono"   
FONT_BOLD = "JetBrains Mono Bold"
FONT_SIZE = 13

BAR_HEIGHT  = 30
BAR_MARGIN  = [0, 0, 0, 0]     # [top, right, bottom, left]
GAP         = 8                
BORDER      = 2                

ACTIVE_BORDER   = COLORS["blue"]
INACTIVE_BORDER = COLORS["border"]

TERMINAL = "alacritty"        
MOD      = "mod4"   

# ──────────────────────────────────────────────────────────────────────────
# KEYBINDINGS
# ──────────────────────────────────────────────────────────────────────────

keys = [
    # Focus
    Key([MOD], "h", lazy.layout.left(), desc="Focus left"),
    Key([MOD], "l", lazy.layout.right(), desc="Focus right"),
    Key([MOD], "j", lazy.layout.down(), desc="Focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Focus next window"),
    Key([MOD], "period", lazy.next_screen(), desc="Focus next monitor"),
    Key([MOD], "comma", lazy.prev_screen(), desc="Focus previous monitor"),

    # Move windows
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move up"),

    # Resize 
    Key([MOD, "control"], "l", lazy.layout.grow_main(), desc="Grow main pane"),
    Key([MOD, "control"], "h", lazy.layout.shrink_main(), desc="Shrink main pane"),
    Key([MOD, "control"], "k", lazy.layout.grow(), desc="Grow window"),
    Key([MOD, "control"], "j", lazy.layout.shrink(), desc="Shrink window"),
    Key([MOD], "r", lazy.layout.reset(), desc="Reset window size"), 
    Key([MOD, "shift"], "space", lazy.layout.flip(), desc="Flip main pane to the other side"),

    # Layout / window management
    Key([MOD], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([MOD], "q", lazy.window.kill(), desc="Close window"),
    Key([MOD], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([MOD], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key(["mod1"], "Tab", lazy.spawn("rofi -show window"), desc="Window switcher (all groups)"),

    # Launchers
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Open terminal"),
    Key([MOD], "d", lazy.spawn("rofi -show drun"), desc="App launcher"),
    Key([MOD], "p", lazy.spawn("rofi -show run"), desc="Run command"),
    Key([MOD], "e", lazy.spawn("rofi -modi emoji -show emoji"), desc="Emoji picker"),
    Key([MOD], "w", lazy.spawn("helium-browser"), desc="Launch web browser"),

    # Media / volume / brightness (uses pactl + brightnessctl)
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86MonBrightnessUp",   lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Session
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Quit qtile"),

    #lock screen
    Key([MOD, "shift"], "x", lazy.spawn("loginctl lock-session"), desc="Lock screen with blur"),

    #screenshot
    Key([MOD, "shift"], "s",
    lazy.spawn("sh -c 'maim -s ~/pictures/screenshots/screenshot-$(date +%Y%m%d-%H%M%S).png'"),
    desc="Screenshot (select region)"),
]

# ──────────────────────────────────────────────────────────────────────────
# GROUPS (workspaces)
# ──────────────────────────────────────────────────────────────────────────

groups = [Group(name) for name in "1234"]

for g in groups:
    keys.extend([
        # MOD + number → switch to group
        Key([MOD], g.name, lazy.group[g.name].toscreen(),
            desc=f"Switch to group {g.name}"),
        # MOD + shift + number → move focused window to group
        Key([MOD, "shift"], g.name, lazy.window.togroup(g.name),
            desc=f"Move window to group {g.name}"),
    ])

# ──────────────────────────────────────────────────────────────────────────
# LAYOUTS
# ──────────────────────────────────────────────────────────────────────────

layout_theme = {
    "border_width": BORDER,
    "border_focus": ACTIVE_BORDER,
    "border_normal": INACTIVE_BORDER,
    "margin": GAP,
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    #layout.Columns(**layout_theme, border_on_single=True),
    # Uncomment to add more:
    # layout.MonadWide(**layout_theme),  # MonadTall rotated 90° (main on top)
    # layout.Bsp(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.Floating(**layout_theme),
]

# ──────────────────────────────────────────────────────────────────────────
# WIDGET BAR
# ──────────────────────────────────────────────────────────────────────────

widget_defaults = dict(
    font=FONT,
    fontsize=FONT_SIZE,
    padding=8,
    foreground=COLORS["fg"],
    background=COLORS["bg_alt"],
)
extension_defaults = widget_defaults.copy()


def sep():
    """A subtle vertical divider between widget groups."""
    return widget.Sep(
        linewidth=1,
        padding=12,
        foreground=COLORS["border"],
        background=COLORS["bg_alt"],
    )

def label(text, color):
    """A small bright accent label, e.g. CPU / RAM / VOL."""
    return widget.TextBox(
        text=text,
        font=FONT_BOLD,
        foreground=color,
        padding=4,
    )

def build_widgets():
    return [
        widget.Spacer(length=6),

        widget.GroupBox(
            font=FONT_BOLD,
            fontsize=FONT_SIZE,
            margin_y=4,
            margin_x=0,
            padding_y=6,
            padding_x=8,
            borderwidth=2,
            rounded=False,                       # sharp corners
            highlight_method="line",             # underline the active group
            highlight_color=[COLORS["bg_high"], COLORS["bg_high"]],
            active=COLORS["fg"],                 # group with windows
            inactive=COLORS["fg_dim"],           # empty group
            this_current_screen_border=COLORS["blue"],
            urgent_border=COLORS["red"],
            urgent_text=COLORS["red"],
            disable_drag=True,
        ),

        sep(),

        widget.CurrentLayout(foreground=COLORS["purple"], padding=8),

        sep(),

        widget.WindowName(
            foreground=COLORS["fg"],
            empty_group_string="desktop",
            max_chars=120,
            padding=4,
        ),

        # ── right side ──
        widget.Spacer(),

        label("CPU", COLORS["green"]),
        widget.CPU(format="{load_percent:>4.0f}%", update_interval=2.0),

        sep(),

        label("RAM", COLORS["cyan"]),
        widget.Memory(format="{MemPercent:>4.0f}%", update_interval=2.0),

        sep(),

        label("TEMP", COLORS["orange"]),
        widget.ThermalSensor(
            tag_sensor="Tctl",
            format="{temp:.0f}{unit}",
            update_interval=2.0,
            foreground=COLORS["fg"],
            foreground_alarm=COLORS["red"],
            threshold=80.0,
        ),

        sep(),

        label("VOL", COLORS["yellow"]),
        widget.PulseVolume(
            fmt="{}",
            scroll_step=5,
            mouse_callbacks={"Button1": lazy.spawn("pavucontrol")},
        ),
        sep(),

        # Comment out the next two lines on a desktop without a battery.
        #label("BAT", COLORS["orange"]),
        #widget.Battery(
        #    format="{percent:2.0%}",
        #    low_percentage=0.15,
        #    low_foreground=COLORS["red"],
        #    notify_below=15,
        #    update_interval=30,
        #),

        #sep(),

        widget.Clock(
            format="%a %d %b  %H:%M",
            foreground=COLORS["blue"],
            font=FONT_BOLD,
        ),

        widget.Spacer(length=6),

        widget.Systray(padding=8, icon_size=18),

        widget.Spacer(length=6),
    ]

def build_widgets_secondary():
    """Same bar as the primary, minus the system tray.
    The tray can only live on one screen, so the second monitor's bar
    omits it (everything else is identical)."""
    return [
        w for w in build_widgets()
        if not isinstance(w, (widget.StatusNotifier, widget.Systray))
    ]



def make_bar(widgets):
    """Build a bar with your standard styling from a widget list."""
    return bar.Bar(
        widgets,
        BAR_HEIGHT,
        background=COLORS["bg_alt"],
        margin=BAR_MARGIN,
        border_width=[0, 0, 1, 0],            # thin bottom hairline
        border_color=COLORS["border"],
    )


screens = [
    Screen(top=make_bar(build_widgets())),            # primary monitor (with tray)
    Screen(top=make_bar(build_widgets_secondary())),  # secondary monitor (no tray)
]

# ──────────────────────────────────────────────────────────────────────────
# MOUSE
# ──────────────────────────────────────────────────────────────────────────

mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

# ──────────────────────────────────────────────────────────────────────────
# MISC / RULES
# ──────────────────────────────────────────────────────────────────────────

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    border_width=BORDER,
    border_focus=ACTIVE_BORDER,
    border_normal=INACTIVE_BORDER,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="pavucontrol"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
        Match(wm_class="Mail"),
        Match(wm_class="discord"),
    ],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"  # helps some Java apps behave
