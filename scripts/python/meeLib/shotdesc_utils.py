"""

*/meeLib.shotdesc
    shot description management functions of the meeLib library

"""

import datetime
import getpass
from pathlib import Path

import hou

from meeLib import config_utils


# region ShotDesc
class ShotDesc:
    def __init__(self, node: hou.Node = None):
        if node is None:
            node = self.get_shotdesc_node()
        self.node = node

    @property
    def project(self) -> str:
        return self.node.parm("project").evalAsString() if self.node else ""

    @property
    def shot(self) -> str:
        return self.node.parm("shot").evalAsString() if self.node else ""

    @property
    def sequence(self) -> str:
        return self.node.parm("sequence").evalAsString() if self.node else ""

    @property
    def shot_range(self) -> list:
        return self.node.parmTuple("shot_range").evalAsInts() if self.node else []

    @property
    def shot_handles(self) -> list:
        return self.node.parmTuple("shot_handles").evalAsInts() if self.node else []

    @property
    def resolution(self) -> list:
        return self.node.parmTuple("resolution").evalAsInts() if self.node else []

    @property
    def fps(self) -> int:
        return hou.getEnvConfigValue("FPS")

    @property
    def user(self) -> str:
        return getpass.getuser()

    @property
    def root_folder(self) -> str:
        return Path(hou.hipFile.path()).parent.as_posix()

    @property
    def timenow(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_shotdesc_node() -> hou.Node:
        return next((node for node in hou.node("/obj").children() if node.type().name() == "meelib_shotdesc"), None)

    def as_dict(self) -> dict:
        return {
            name: getattr(self, name)
            for name in dir(self.__class__)
            if isinstance(getattr(self.__class__, name), property)
        }


# endregion


# region Main
def set_framerange(shotdesc_node: hou.Node = None):
    shotdesc = ShotDesc(node=shotdesc_node)

    # clean old bookmark
    hou.anim.removeBookmarks(
        list(
            [
                bookmark
                for bookmark in hou.anim.bookmarks()
                if bookmark.comment() == config_utils.CFG["bookmark_comment"]
            ]
        )
    )

    # set frame range
    hou.playbar.setFrameRange(
        shotdesc.shot_range[0] - shotdesc.shot_handles[0], shotdesc.shot_range[1] + shotdesc.shot_handles[1]
    )

    # set current frame at start frame
    hou.setFrame(shotdesc.shot_range[0] - shotdesc.shot_handles[0])

    # create bookmark
    shotrange_bookmark = hou.anim.newBookmark(
        f"{shotdesc.sequence} - {shotdesc.shot}", shotdesc.shot_range[0], shotdesc.shot_range[1]
    )
    shotrange_bookmark.setColor(hou.Color(config_utils.CFG["colors"]["cyan"]))
    shotrange_bookmark.setComment(config_utils.CFG["bookmark_comment"])


# endregion
