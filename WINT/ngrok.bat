if not "%1" == "am_admin" (powershell start -verb runas '%0' am_admin & exit ) 
@echo on

start "ngrok"               /MIN /d "C:\Users\Jinu\PycharmProjects\WEB\WINT\"   ngrok.exe http 8000

CALL C:\Users\Jinu\PycharmProjects\WEB\venv\Scripts\activate.bat


start "ng"           /MIN /d "C:\Users\Jinu\PycharmProjects\WEB\WINT\"    python ng.py
