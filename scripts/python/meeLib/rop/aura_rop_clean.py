'''

        */meeLib.rop.aura_rop_clean
            Post-Render .py script to use with ROP and TOP

'''
import hou
from meeLib import config

def clean():
    '''
    Clean the temp folder
    '''
    hip = hou.hipFile.path()
    debug = hou.pwd().node('../../').evalParm('adv_debug_mode')
    if config.clean_temp_folder(hip) and debug == 1:
        config.display_message(2, f'VDB to AUR : Cleaning temp files : Done 🧹')
        
clean()