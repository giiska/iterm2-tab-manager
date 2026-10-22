#!/usr/bin/env python3

from __future__ import annotations

from random import randint

import iterm2

_COLOR_DISTANCE_THRESHOLD = 40
_COLOR_PICK_MAX_TRIES = 500


def _color_distance(a: iterm2.Color, b: iterm2.Color) -> float:
    dr = a.red - b.red
    dg = a.green - b.green
    db = a.blue - b.blue
    return (dr * dr + dg * dg + db * db) ** 0.5


def _is_too_close(candidate: iterm2.Color, used: list[iterm2.Color]) -> bool:
    return any(_color_distance(candidate, c) <= _COLOR_DISTANCE_THRESHOLD for c in used)


def random_color(used_colors: list[iterm2.Color]) -> iterm2.Color:
    if not used_colors:
        return iterm2.Color(randint(0, 255), randint(0, 255), randint(0, 255))

    for _ in range(_COLOR_PICK_MAX_TRIES):
        candidate = iterm2.Color(randint(0, 255), randint(0, 255), randint(0, 255))
        if not _is_too_close(candidate, used_colors):
            return candidate

    best, best_dist = used_colors[0], -1.0
    for _ in range(_COLOR_PICK_MAX_TRIES):
        candidate = iterm2.Color(randint(0, 255), randint(0, 255), randint(0, 255))
        min_dist = min(_color_distance(candidate, c) for c in used_colors)
        if min_dist > best_dist:
            best, best_dist = candidate, min_dist
    return best


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

        window = session.tab.window
        if window is None:
            print("No window found for the active session")
            return

        customizations = None

        if use_random_color:
            used_colors: list[iterm2.Color] = []
            for tab in window.tabs:
                tab_session = tab.current_session
                if tab_session is None:
                    continue
                tab_profile = await tab_session.async_get_profile()
                if tab_profile.use_tab_color:
                    used_colors.append(tab_profile.tab_color)

            customizations = iterm2.LocalWriteOnlyProfile()
            customizations.set_tab_color(random_color(used_colors))
            customizations.set_use_tab_color(True)
        else:
            profile = await session.async_get_profile()
            if profile.use_tab_color:
                customizations = iterm2.LocalWriteOnlyProfile()
                customizations.set_tab_color(profile.tab_color)
                customizations.set_use_tab_color(True)

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
