import sys
import os
import subprocess as sproc

pipe_outputs = { 'stdout' : sproc.PIPE, 
                 'stderr' : sproc.PIPE}

## requires pyinstaller <= 4.6
res = sproc.run([ "pyinstaller"
                    , "--version"
                ], **pipe_outputs)

if res.returncode != 0:
    print("pyinstaller not found on PATH")
    sys.exit(1)

res = sproc.run([ "pyinstaller"
                    , "--add-data"
                    , "../client/assets/*" + (";" if os.name == 'nt' else ":") + "assets"
                    , "--clean"
                    , "--noconfirm"
                    , "--noconsole"
                    , "--onefile"
                    , "--windowed"
                    , "--name", "SnowballSlingers"
                    , "--icon=icon.ico"
                    , "../client/main.py"
                ], **pipe_outputs)

if res.returncode != 0:
    print(res.stderr.decode("UTF-8"))
