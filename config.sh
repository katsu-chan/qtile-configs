#!/usr/bin/env bash

systemctl --user import-environment WAYLAND_DISPLAY XDG_SESSION_DESKTOP XDG_CURRENT_DESKTOP XDG_SESSION_TYPE DISPLAY XAUTHORITY

if command -v dbus-update-activation-environment >/dev/null 2>&1; then
    dbus-update-activation-environment WAYLAND_DISPLAY XDG_SESSION_DESKTOP XDG_CURRENT_DESKTOP XDG_SESSION_TYPE DISPLAY XAUTHORITY
fi
