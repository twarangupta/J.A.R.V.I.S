import winreg

def copy_key(src_key, dest_key):
    # Copy values
    try:
        i = 0
        while True:
            val_name, val_data, val_type = winreg.EnumValue(src_key, i)
