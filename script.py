import mmap
import os
from tkinter.filedialog import askdirectory

filename = askdirectory()
for subdir, dirs, files in os.walk(filename):
    for file in files:
        filepath = subdir + os.sep + file

        if not (not filepath.endswith(".jpg") and not filepath.endswith(".JPG")):
            header = b'\xff\xd8\xff'
            f = open(filepath, 'r+b')
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
            loc = s.find(header)
            if loc != -1:
                f.write(s[loc:])
                f.close()
