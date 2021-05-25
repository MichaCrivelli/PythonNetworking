@echo off

:restart

cls
echo "server restart"

copy "serverlogic2.py" "serverlogic.py"

python "Server.pyw"

goto restart

pause
