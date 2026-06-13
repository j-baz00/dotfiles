# ~/.config/qtile/config.py
#
# A clean, extensible qtile config:
#   - Sharp corners (no rounding), thin crisp borders
#   - JetBrains Mono everywhere
#   - GitHub/Google-style dark theme: gray surfaces, bright accent colors
#
# Almost everything you'd want to change lives in the THEME section below.
# Add widgets in `build_widgets()`, add keybinds in the KEYS section.

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# ──────────────────────────────────────────────────────────────────────────
# THEME  (edit this block to restyle everything)
# ──────────────────────────────────────────────────────────────────────────

# GitHub Dark inspired palette: grayscale surfaces + bright accents.
COLORS = {
    "bg":      "#0d1117",  # desktop / deepest background
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

FONT      = "JetBrains Mono"   # use "JetBrainsMono Nerd Font" if you want glyph icons
FONT_BOLD = "JetBrains Mono Bold"
FONT_SIZE = 13

BAR_HEIGHT  = 30
BAR_MARGIN  = [0, 0, 0, 0]     # [top, right, bottom, left] — set e.g. [6,8,4,8] for a floating bar
GAP         = 8                # window gap (margin). Set 0 for no gaps.
BORDER      = 2                # window border width. Set 0 to remove borders.

ACTIVE_BORDER   = COLORS["blue"]
INACTIVE_BORDER = COLORS["border"]

TERMINAL = "alacritty"         # change to kitty / wezterm / foot / etc.
MOD      = "mod4"              # mod4 = Super/Windows key

# ──────────────────────────────────────────────────────────────────────────
# KEYBINDINGS
# ──────────────────────────────────────────────────────────────────────────

keys = [
    # Focus
    Key([MOD], "h", lazy.layout.left(),  desc="Focus left"),
    Key([MOD], "l", lazy.layout.right(), desc="Focus right"),
    Key([MOD], "j", lazy.layout.down(),  desc="Focus down"),
    Key([MOD], "k", lazy.layout.up(),    desc="Focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Focus next window"),

    # Move windows
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(),  desc="Move left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(),  desc="Move down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(),    desc="Move up"),

    # Resize  (MonadTall: h/l size the MAIN pane, j/k size the focused window)
    Key([MOD, "control"], "l", lazy.layout.grow_main(),   desc="Grow main pane"),
    Key([MOD, "control"], "h", lazy.layout.shrink_main(), desc="Shrink main pane"),
    Key([MOD, "control"], "k", lazy.layout.grow(),        desc="Grow window"),
    Key([MOD, "control"], "j", lazy.layout.shrink(),      desc="Shrink window"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset window sizes"),
    Key([MOD], "m", lazy.layout.maximize(),  desc="Toggle maximize window"),
    Key([MOD, "shift"], "space", lazy.layout.flip(),
        desc="Flip main pane to the other side"),

    # Layout / window management
    Key([MOD], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([MOD], "w", lazy.window.kill(), desc="Close window"),
    Key([MOD], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([MOD], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([MOD, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle split/stack"),

    # Launchers
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Open terminal"),
    Key([MOD], "r", lazy.spawn("rofi -show drun"), desc="App launcher"),
    Key([MOD], "p", lazy.spawn("rofi -show run"), desc="Run command"),

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
]

# ──────────────────────────────────────────────────────────────────────────
# GROUPS (workspaces)
# ──────────────────────────────────────────────────────────────────────────

groups = [Group(name) for name in "123456789"]

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
    # MonadTall is the default: one large "main" pane on the left,
    # remaining windows stacked on the right.
    layout.MonadTall(
        **layout_theme,
        ratio=0.55,                 # main pane takes 55% of the screen width
        single_border_width=BORDER, # keep a border even with one window
    ),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme, border_on_single=True),
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
    """Return the ordered list of bar widgets. Add/remove freely."""
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

        label("VOL", COLORS["yellow"]),
        widget.Volume(fmt="{}"),

        sep(),

        # Comment out the next two lines on a desktop without a battery.
        label("BAT", COLORS["orange"]),
        widget.Battery(
            format="{percent:2.0%}",
            low_percentage=0.15,
            low_foreground=COLORS["red"],
            notify_below=15,
            update_interval=30,
        ),

        sep(),

        widget.Clock(
            format="%a %d %b  %H:%M",
            foreground=COLORS["blue"],
            font=FONT_BOLD,
        ),

        widget.Spacer(length=6),

        widget.Systray(padding=8, icon_size=18),

        widget.Spacer(length=6),
    ]


screens = [
    Screen(
        top=bar.Bar(
            build_widgets(),
            BAR_HEIGHT,
            background=COLORS["bg_alt"],
            margin=BAR_MARGIN,
            border_width=[0, 0, 1, 0],            # thin bottom hairline
            border_color=COLORS["border"],
        ),
    ),
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
    ],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"  # helps some Java apps behave
