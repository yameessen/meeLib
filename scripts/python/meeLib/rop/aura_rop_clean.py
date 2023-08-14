import hou
from meeLib import config

hip = hou.hipFile.path()
config.clean_temp_folder(hip)