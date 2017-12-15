import ctypes
import mmap
import os
from tkFileDialog import askdirectory


JPG = b'\xff\xd8\xff'


class FileProvider(object):

    def __init__(self):
        self.folder = askdirectory()

    def get_files(self):
        return self.folder



class HeaderRepair(object):

    def __init__(self, provider):
        self.repaired_files = []
        self.folder = provider.get_files()

    def header_repair(self):

        for subdir, dirs, files in os.walk(self.folder):
            for item in files:
                filepath = subdir + os.sep + item
                if not (not filepath.endswith(".jpg") and not filepath.endswith(".JPG")):
                    f = open(filepath, 'r+b')
                    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
                    loc = s.find(JPG)
                    if loc:
                        self.repaired_files.append(filepath)
                        f.write(s[loc:])
                        f.close()
                    else:
                        f.close()
        return self.repaired_files



    # tracks results of repair function
class DisplayResults(object):

    IDYES = 6
    
    def __init__(self):
        _user32 = ctypes.WinDLL('user32', use_last_error=True)
        self._MessageBoxW = _user32.MessageBoxW
        

    def MessageBoxW(title, text, style):
        result = self._MessageBoxW(0, text, title, style)
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        return result

    def display_results(self, rep_files):
        if rep_files:
            try:
                result = self.MessageBoxW("Results", str(len(rep_files)) +
                                    " files have been repaired.\nWould you like to view the file names?", 4)
                if result == IDYES:
                    self.MessageBoxW("Results", """{}""".format("\n".join(rep_files[1:])), 0)
            except WindowsError as win_err:
                print("An error occurred:\n{}".format(win_err))
        else:
            try:
                self.MessageBoxW("Results", "No bad headers were found", 0)
            except WindowsError as win_err:
                print("An error occurred:\n{}".format(win_err))