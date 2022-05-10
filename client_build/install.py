import sys
import os
import subprocess as sproc

pipe_outputs = { 'stdin' : sproc.PIPE,
                 'stdout' : sproc.PIPE, 
                 'stderr' : sproc.PIPE}

## requires pyinstaller <= 4.6
res = sproc.run([ "pyinstaller"
                    , "--version"
                ], **pipe_outputs)

if res.returncode != 0:
    print("pyinstaller not found on PATH")
    sys.exit(1)

res = sproc.Popen(["pyinstaller", "--add-data", "../client/assets/*" + (";" if os.name == 'nt' else ":") + "assets", "--noconsole", "--onefile", "--windowed", "--name", "SnowballSlingers", "--icon=icon.ico", "../client/main.py"], **pipe_outputs)

outs, errs = res.communicate()

if res.returncode != 0:
    print(errs.decode("UTF-8"))
