import winreg

def copy_key(src_key, dest_key):
    # Copy values
    try:
        i = 0
        while True:
