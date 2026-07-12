#!/usr/bin/env python3

from __future__ import annotations

from random import randint

import iterm2


def random_color() -> iterm2.Color:
    return iterm2.Color(randint(0, 255), randint(0, 255), randint(0, 255))


async def main(connection: iterm2.Connection) -> None:
    app = await iterm2.async_get_app(connection)

    async def create_tab_impl(session_id: str | None, use_random_color: bool) -> None:
        session = app.get_session_by_id(session_id) if session_id else None
        if session is None:
            window = app.current_terminal_window
            if window is None:
                print("No active iTerm2 window found")
                return
            current_tab = window.current_tab
            if current_tab is None or current_tab.current_session is None:
                print("No active iTerm2 session found")
                return
            session = current_tab.current_session

        profile = await session.async_get_profile()
        customizations = None

        if use_random_color:
            customizations = iterm2.LocalWriteOnlyProfile()
            customizations.set_tab_color(random_color())
            customizations.set_use_tab_color(True)
        elif getattr(profile, "use_tab_color", False):
            customizations = iterm2.LocalWriteOnlyProfile()
            customizations.set_tab_color(profile.tab_color)
            customizations.set_use_tab_color(True)

        window = session.tab.window
        if window is None:
            print("No window found for the active session")
            return

        new_tab = await window.async_create_tab(profile_customizations=customizations)
        if new_tab is None:
            print("Failed to create a new tab")

    @iterm2.RPC
    async def create_tab(session_id=iterm2.Reference("id?")):
        await create_tab_impl(session_id, False)

    @iterm2.RPC
    async def create_tab_with_random_color(session_id=iterm2.Reference("id?")):
        await create_tab_impl(session_id, True)

    await create_tab.async_register(connection)
    await create_tab_with_random_color.async_register(connection)


iterm2.run_forever(main)
