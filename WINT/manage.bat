if not "%1" == "am_admin" (powershell start -verb runas '%0' am_admin & exit ) 
@echo on

CALL C:\Users\Jinu\PycharmProjects\WEB\venv\Scripts\activate.bat


start "manage"               /MIN /d "C:\Users\Jinu\PycharmProjects\WEB\WINT"  python manage.py runserver
