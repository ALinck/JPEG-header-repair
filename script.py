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
    # tracks files that were repaired
    if len(rep_files) > 0:
        i = 0
        print(str(len(rep_files)) + " files have been repaired.\n")
        while i < len(rep_files):
            print(rep_files[i])
            i += 1
