'''

        */meeLib.rop.aura_rop_convert
            Post-Write .py script to use with ROP and TOP
            This generate the cache-converter.exe command from the HDA parameters

'''
import hou
import subprocess as sp
from meeLib import aura
from scripts.python.meeLib import config_utils

def convert():
    '''
    Generate and execute the command to convert the .vdb to .aur
    '''
    frame = hou.intFrame()
    try:
        debug = hou.pwd().node('../../').evalParm('adv_debug_mode')
    except:
        debug = hou.pwd().node('../../../../').evalParm('adv_debug_mode')
    debug = 1
    if debug == 1:
        config_utils.display_message(2, f'VDB to AUR : Exporting frame {frame} : Starting ⏳')

    node = hou.pwd().node('../../EXPORT')
    if node == None:
        node = hou.pwd().node('../../../../EXPORT')
    geo = node.geometry()

    exe = aura.install_path_get()

    framerange = geo.attribValue('_aura_framerange')
    quality = geo.attribValue('_aura_quality')
    dst = '.'.join([geo.attribValue('_aura_dst'), f'{frame:04}', 'aur'])
    import_type = geo.attribValue('_aura_import_type')
    try:
        src = hou.pwd().node('../temp_vdb').evalParm('sopoutput')
    except:
        src = hou.pwd().evalParm('sopoutput')
    si = sp.STARTUPINFO()
    si.dwFlags |= sp.STARTF_USESHOWWINDOW
    sp.call(f'"{exe}" -srcfile "{src}" -dstfile "{dst}" -storagequality {quality}', startupinfo=si)

    if debug == 1:
        config_utils.display_message(2, f'VDB to AUR : Exporting frame {frame} : Success ✔️')

convert()
