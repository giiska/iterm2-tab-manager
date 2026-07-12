#!/usr/bin/env python3

from __future__ import annotations

import iterm2


async def main(connection: iterm2.Connection) -> None:
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window
    if window is None:
        print("No active iTerm2 window found")
        return

    current_tab = window.current_tab
    if current_tab is None:
        print("No active iTerm2 tab found")
        return

    source_session = current_tab.current_session
    if source_session is None:
        print("No active iTerm2 session found")
        return

    source_profile = await source_session.async_get_profile()

    customizations = None
    if getattr(source_profile, "use_tab_color", False):
        customizations = iterm2.LocalWriteOnlyProfile()
        customizations.set_tab_color(source_profile.tab_color)
        customizations.set_use_tab_color(True)

    new_tab = await window.async_create_tab(profile_customizations=customizations)
    if new_tab is None:
        print("Failed to create a new tab")
        return

    if customizations is not None:
        print("Created a new tab and copied the tab color")
    else:
        print("Created a new tab")


if __name__ == "__main__":
    iterm2.run_until_complete(main)
