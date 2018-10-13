# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    dist_name = "pyload-ng"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

import builtins
import sys
from os import chdir, makedirs, path
from os.path import join
from sys import argv, platform

builtins._ = lambda x: x  # TODO: remove

builtins.pyreq = None  # TODO: remove
builtins.addonManager = None  # TODO: remove

builtins.owd = path.abspath("")  # original working directory
builtins.pypath = pypath = path.abspath(path.join(__file__, "..", ".."))

sys.path.append(join(pypath, "pyload", "lib"))

homedir = ""

if platform == "nt":
    homedir = path.expanduser("~")
    if homedir == "~":
        import ctypes

        CSIDL_APPDATA = 26
        _SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathW
        _SHGetFolderPath.argtypes = [
            ctypes.wintypes.HWND,
            ctypes.c_int,
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.LPCWSTR,
        ]

        path_buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        result = _SHGetFolderPath(0, CSIDL_APPDATA, 0, 0, path_buf)
        homedir = path_buf.value
else:
    homedir = path.expanduser("~")

builtins.homedir = homedir

args = " ".join(argv[1:])

# dirty method to set configdir from commandline arguments
if "--configdir=" in args:
    pos = args.find("--configdir=")
    end = args.find("-", pos + 12)

    if end == -1:
        configdir = args[pos + 12 :].strip()
    else:
        configdir = args[pos + 12 : end].strip()
elif path.exists(path.join(pypath, "pyload", "config", "configdir")):
    with open(path.join(pypath, "pyload", "config", "configdir"), "rb") as f:
        c = f.read().strip()
    configdir = path.join(pypath, c)
else:
    if platform in ("posix", "linux2"):
        configdir = path.join(homedir, ".pyload")
    else:
        configdir = path.join(homedir, "pyload")

if not path.exists(configdir):
    makedirs(configdir, 0o700)

builtins.configdir = configdir
chdir(configdir)

# print("Using {} as working directory.".format(configdir))
