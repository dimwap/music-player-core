#!/usr/bin/python

import os, sys
from glob import glob
os.chdir(os.path.dirname(__file__))

def sysExec(cmd):
    print " ".join(cmd)
    r = os.system(" ".join(cmd))
    if r != 0: sys.exit(r)

sysExec(["mkdir","-p","build"])
os.chdir("build")

staticChromaprint = False

ffmpegFiles = ["../ffmpeg.c"] + \
	(glob("../chromaprint/*.cpp") if staticChromaprint else [])

sysExec(["gcc", "-c"] + ffmpegFiles +
	[
		"-DHAVE_CONFIG_H",
		"-I", "/System/Library/Frameworks/Python.framework/Headers/",
		"-g",
	] +
	(["-I", "../chromaprint"] if staticChromaprint else [])
)

sysExec(["libtool", "-dynamic", "-o", "../ffmpeg.so"] +
	[os.path.splitext(os.path.basename(fn))[0] + ".o" for fn in ffmpegFiles] +
	[
		"-framework", "Python",
		"-lavformat", "-lavutil", "-lavcodec", "-lswresample", "-lportaudio",
		"-lc", "-lstdc++",
	] +
	([] if staticChromaprint else ["-lchromaprint"])
)

sysExec(["gcc", "-c"] + ["../kyotocabinet.cc"] +
	[
		"-I", "/System/Library/Frameworks/Python.framework/Headers/",
		"-g",
	]
)

sysExec(["libtool", "-dynamic", "-o", "../kyotocabinet.so"] +
	["kyotocabinet.o"] +
	[
		"-framework", "Python",
		"-lkyotocabinet",
		"-lc", "-lstdc++",
	]
)

levelDbFiles = glob("../leveldb*.cc")

sysExec(["gcc", "-c"] + levelDbFiles +
	[
		"-I", "/System/Library/Frameworks/Python.framework/Headers/",
		"-g",
	]
)

sysExec(["libtool", "-dynamic", "-o", "../leveldb.so"] +
	[os.path.splitext(os.path.basename(fn))[0] + ".o" for fn in levelDbFiles] +
	[
		"-framework", "Python",
		"-lleveldb", "-lsnappy",
		"-lc", "-lstdc++",
	]
)
