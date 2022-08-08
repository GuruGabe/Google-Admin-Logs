@echo off
Title Retrieving Google Admin logs
cls
echo Retrieving Google Admin logs
echo.

::Grabs current date and converts it to Google fomat. For those systems that has the day of week in the short date, makes the correct adjustment.
set rundate1=
set rundate1=%date:~-4%-%date:~0,2%-%date:~3,2%
echo %rundate1%
echo %rundate1%|findstr /i [a-z] > nul
echo %errorlevel%
if %errorlevel% NEQ 0 set rundate1=%date:~-4%-%date:~0,2%-%date:~3,2%T11:59:59.999Z
if %errorlevel% EQU 0 set rundate1=%date:~-4%-%date:~4,2%-%date:~7,2%T11:59:59.999Z

::The AddDays(-1) will get yesterday's date and then I convert it to Google format
set rundate2=
FOR /F "usebackq tokens=*" %%t IN (`powershell -NoProfile -Command "(Get-Date).AddDays(-1).ToString('yyyy-MM-dd')"`) DO (SET "rundate2=%%t")
set rundate2=%rundate2%T11:59:59.999Z

::Gets current date for file name. Redundant, but I like to keep thing seperate sometimes.
set rundate3=
set rundate3=%date:~0,2%/%date:~3,2%/%date:~-4%
echo %rundate3%
echo %rundate3%|findstr /r "[^a-zA-Z]" > nul
if %errorlevel% NEQ 1 set rundate3=%date:~4,2%/%date:~7,2%/%date:~-4%

gam report admin todrive user <AdminEmailAddress> start %rundate2% end %rundate1% todrive tdparent id:<GoogleFolderID> tdtitle "<AdminName> %rundate3%"
