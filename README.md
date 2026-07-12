# iTerm2 Tab Manager

Small Python utility scaffold for iTerm2 scripting work.

Planned feature set:

- create a new tab in the current iTerm2 window
- optionally copy selected profile settings to the new session
- grow into additional tab/session management actions

## Layout

- `src/iterm2_tab_manager/` - package code
- `scripts/create_tab.py` - script entry point for iTerm2

## Status

This is a fresh development folder. The first utility being built here is tab creation and profile cloning.

## Hotkey setup

Bind `Cmd+Shift+T` in iTerm2 to call the registered RPC directly.

Recommended setup:

1. Open iTerm2 settings and go to the key bindings section.
2. Add a new key mapping for `Cmd+Shift+T`.
3. Set the action to `Invoke Script Function...`.
4. Enter this function call: `create_tab(session_id: id)`
5. Put this file into iTerm2's AutoLaunch Scripts folder: `scripts/AutoLaunch/create_tab_rpc.py`.
6. Restart iTerm2 once so the daemon registers the RPC.

For a random tab color instead, use:

`create_tab_with_random_color(session_id: id)`

The script creates a new tab in the current window and copies the active session's tab color when the current profile uses one.

If you do not know where iTerm2's Scripts folder is, use `Scripts -> Manage -> Reveal Scripts in Finder` from the menu bar.

If the old menu-item binding is still active, remove it. That path goes through the Scripts menu and is slower because iTerm2 has to launch the script through the menu item rather than calling the registered RPC directly.
