import hou
import os
import shutil
import json
from datetime import datetime

MEELIB = os.environ['MEELIB']
cfg_file = MEELIB + '/config.json'

def display_message(type, text):
    now = datetime.now()
    time = f'[{now.strftime("%H:%M:%S")}] - '
    sev = hou.severityType.Message
    ask = 1
    if type == 0:
        message = 'meeLib : ' + text
    elif type == 1:
        sev = hou.severityType.Error
        message = 'meeLib Error : ' + text
    elif type == 2:
        message = 'meeLib : ' + text
    else:
        raise hou.Error('Error: type not found')
    
    if type != 2:
        ask = hou.ui.displayMessage(message, 
                             buttons=('OK', 'Send to Console'), 
                             severity=sev, 
                             title='meeLib Error') == 1

    if ask == 1 or type == 2:
        print(time + message)

def get_cfg_data():
    if os.path.isfile(cfg_file):
        with open(cfg_file, 'r') as file:
            return json.load(file)
    else:
        display_message(1, 'Config file not found.')
        return None
    
def write_cfg_data(cfg):
    if os.path.isfile(cfg_file) and type(cfg) is dict:
        with open(cfg_file, 'w') as file:
            json.dump(cfg, file, indent=4)
    else:
        display_message(1, 'Unable to write Config file.')
        return None
    
def open_folder(path):
    if os.path.exists(path):
        hou.ui.showInFileBrowser(path)
        return True
    else:
        display_message(0, 'Output dir does not exist')
        return False
    
def clean_temp_folder(hip):
    path = os.path.dirname(hip) + '/meeLib_temp/'
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors = False)
        return True
    else:
        return False
    
def add_credits_to_hda(node):
    cfg = get_cfg_data()
    parm_template = node.parmTemplateGroup()
    parm_list = []
    label_list = []
    # fill column_labels list to align text to left 
    for i in range(16):
        label_list.append('')
    for key in cfg:
        parm = ''
        value = cfg[key]
        if key == 'Tools':
            parm_list.append(hou.SeparatorParmTemplate(f'credits_{key}_sep', 
                                                       tags={'sidefx::layout_height': 'medium', 'sidefx::look': 'blank'}))
            continue
        elif key == 'Socials':
            parm_list.append(hou.SeparatorParmTemplate(f'credits_{key}_sep', 
                                                       tags={'sidefx::layout_height': 'medium', 'sidefx::look': 'blank'}))
            for link in value:
                if value[link] != None:
                    parm = hou.ButtonParmTemplate(f'credits_button_{link}',
                                                  link,
                                                  join_with_next=True, 
                                                  script_callback='exec("""\nimport webbrowser\n\nwebbrowser.open(\'' + value[link] + '\')\n""")',
                                                  script_callback_language=hou.scriptLanguage.Python)
                    parm_list.append(parm)
            parm_list.append(hou.LabelParmTemplate(f'credits_{key}_label_end', 
                                                   title, 
                                                   ()))
        else:
            label_list[0] = str(value)
            if key.startswith('About'):
                title = key[:-1] if key.endswith('1') else ' '
                parm = hou.LabelParmTemplate(f'credits_{key}', 
                                             title, 
                                             label_list)
            else:
                parm = hou.LabelParmTemplate(f'credits_{key}', 
                                             key, 
                                             label_list)
            parm_list.append(parm)
    credits_folder = hou.FolderParmTemplate('credits',
                                            'Credits',
                                            parm_templates = parm_list,
                                            folder_type = hou.folderType.Collapsible)
    parm_template.appendToFolder('Advanced', credits_folder)
    node.setParmTemplateGroup(parm_template)