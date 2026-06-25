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
