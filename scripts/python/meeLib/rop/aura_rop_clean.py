import hou
from meeLib import config

def clean():
    hip = hou.hipFile.path()
    debug = hou.pwd().node('../../').evalParm('adv_debug_mode')
    if config.clean_temp_folder(hip) and debug == 1:
        config.display_message(2, f'VDB to AUR : Cleaning temp files : Done 🧹')
        
clean()