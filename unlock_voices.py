import winreg

def copy_key(src_key, dest_key):
    # Copy values
    try:
        i = 0
        while True:
            val_name, val_data, val_type = winreg.EnumValue(src_key, i)
            winreg.SetValueEx(dest_key, val_name, 0, val_type, val_data)
            i += 1
    except OSError:
        pass # No more values
        
    # Copy subkeys recursively
    try:
        i = 0
        while True:
            subkey_name = winreg.EnumKey(src_key, i)
            src_subkey = winreg.OpenKey(src_key, subkey_name)
            dest_subkey = winreg.CreateKey(dest_key, subkey_name)
            copy_key(src_subkey, dest_subkey)
            winreg.CloseKey(src_subkey)
            winreg.CloseKey(dest_subkey)
            i += 1
    except OSError:
        pass # No more subkeys

def unlock():
    one_core_path = r"SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
    sapi5_user_path = r"SOFTWARE\Microsoft\Speech\Voices\Tokens"
    
    try:
        src_root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, one_core_path)
