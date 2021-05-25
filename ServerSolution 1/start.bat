@echo off

:restart

cls

copy "serverlogic2.py" "serverlogic.py" > nul

python "Server.py"

goto restart

pause
