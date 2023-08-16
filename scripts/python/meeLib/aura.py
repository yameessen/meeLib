from meeLib import config
import hou
import os
from pathlib import Path

def install_path_get():
    cfg = config.get_cfg_data()
    path = cfg['Tools']['pfd_path']
    if os.path.isfile(path):
        return Path(path)
    else:
        return '//None//'

def install_path_exist(silent):
    path = install_path_get()
    if os.path.isfile(path):
        if silent == 0:
            config.display_message(0, 'Install found!')
        return True
    else:
        if silent == 0:
            config.display_message(1, 'PhoenixFD "cache_converter.exe" is not found !')
        return False
    
def install_path_ask():
    hou.ui.displayMessage('You have to select "cache_converter.exe" of your PhoenixFD Installation folder inside the "bin" folder.', buttons=('Roger that',), severity=hou.severityType.ImportantMessage, title='meeLib Reminder', details='Path is usualy "C:/Program Files/Chaos Group/Phoenix FD/3ds Max 2024 for x64/bin". \nDCC name depends on the version of PhoenixFD you installed. \nAny DCC version will work.', details_label='More infos', details_expanded=False)
    path = hou.ui.selectFile(start_directory='C:/Program Files/', title="meeLib Find cache_converter.exe", collapse_sequences=False, file_type=hou.fileType.Any, pattern='cache_converter.exe', default_value=None, multiple_select=False, image_chooser=None, chooser_mode=hou.fileChooserMode.Read)
    if path.endswith('cache_converter.exe'):
        return Path(path)
    else:
        config.display_message(1, 'cache_converter.exe had been wrongly selected.')

def install_path_write():
    predict_path = ''
    custom_path = True
    for key, value in os.environ.items():
        if key.startswith('PHX') and key.endswith('BIN'):
            predict_path = Path(value + '/cache_converter.exe')
            
    if predict_path:
        if hou.ui.displayCustomConfirmation('A version of PhoenixFD has been found ! Do you want to use it ?', buttons=('Yes', 'No'), severity=hou.severityType.Message, help=None, title='meeLib Confirmation', details=str(predict_path), details_label='Show path') == 0:
            custom_path = False
    
    if custom_path == True:
        input = install_path_ask()
        if input:
            new_path = input
        else:
            raise hou.Error('Cancel by User')
    else:
        new_path = predict_path
    
    print(f'New PhoenixFD install path : [{new_path}]')
    cfg = config.get_cfg_data()
    cfg['Tools']['pfd_path'] = str(new_path)
    config.write_cfg_data(cfg)   