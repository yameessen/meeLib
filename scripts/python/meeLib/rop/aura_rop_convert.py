import hou
import subprocess as sp
from meeLib import aura
from meeLib import config

#node_debug = hou.pwd().node('../../')
#if node_debug == None:
#    node_debug = hou.pwd().node('../../../../')
#debug = node_debug.evalParm('adv_debug_mode')

try:
    debug = hou.pwd().node('../../').evalParm('adv_debug_mode')
except:
    debug = hou.pwd().node('../../../../').evalParm('adv_debug_mode')
debug = 1
frame = hou.intFrame()
if debug == 1:
    config.display_message(2, f'VDB to AUR : Exporting frame {frame} : Starting ⏳')

node = hou.pwd().node('../../EXPORT')
if node == None:
    node = hou.pwd().node('../../../../EXPORT')
geo = node.geometry()

exe = aura.install_path_get()

# bad solution to get attribs, pyLance doesn't like that
'''
attrib_list = []
for attrib in geo.globalAttribs():
    if attrib.name().startswith('_aura'):
        attrib_list.append(attrib)
        
for attrib in attrib_list:
    exec(f"{attrib.name()[-6:]} = '{geo.attribValue(attrib)}'")
'''

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
    config.display_message(2, f'VDB to AUR : Exporting frame {frame} : Success ✔️')