def header_repair():
    import mmap
    import os
    from tkinter.filedialog import askdirectory
    filename = askdirectory()
    headers = {"jpg": b'\xff\xd8\xff'}
    rep_files = []
    for subdir, dirs, files in os.walk(filename):
        for file in files:
            filepath = subdir + os.sep + file
            if not (not filepath.endswith(".jpg") and not filepath.endswith(".JPG")):
                f = open(filepath, 'r+b')
                s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
                loc = s.find(headers["jpg"])
                if loc != -1 and loc != 0:
                    rep_files.append(filepath)
                    f.write(s[loc:])
                    f.close()
                else:
                    f.close()

    def results():
        import ctypes
        _user32 = ctypes.WinDLL('user32', use_last_error=True)
        _MessageBoxW = _user32.MessageBoxW
        IDYES = 6
        
        def MessageBoxW(title, text, style):
                result = _MessageBoxW(0, text, title, style)
                if not result:
                    raise ctypes.WinError(ctypes.get_last_error())
                return result
                
        if len(rep_files) > 0:
            def main():
                try:
                    result = MessageBoxW("Results", str(len(rep_files)) +
                    " files have been repaired.\nWould you like to view the file names?", 4)
                    if result == IDYES:
                        i = 0
                        while i < len(rep_files):
                            print(rep_files[i])
                            i += 1
                except WindowsError as win_err:
                    print("An error occurred:\n{}".format(win_err))

            main()

        else:
            def main():
                try:
                    MessageBoxW("Results", "No bad headers were found", 0)
                except WindowsError as win_err:
                    print("An error occurred:\n{}".format(win_err))

            main()

    results()
