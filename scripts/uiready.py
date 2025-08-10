"""

*/meeLib.123
    Houdini will find any files matching this pattern in the Houdini path and run them at startup.
    Houdini runs this script (if it exists) very early in the startup sequence,
    before the UI is available and before assets are loaded.

"""

from meeLib.config_utils import HoudiniStartup

HoudiniStartup.uiready()
