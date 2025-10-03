@echo off
setlocal EnableDelayedExpansion

cd /D "%~dp0"
title Options list

:begin
color 0F
cls
echo.
echo Select a number:
echo.
echo [1] Decode
echo.
echo [2] Randomize
echo.
echo [3] Encode
echo.
echo [4] exit
echo.

choice /c 1234 /n /m "Enter your choice:"
if errorlevel 4 goto :end

if errorlevel 3 (
    cls
    echo.
    echo ^(2^) Encode
    set /p filename1="Enter the filename (without .btnks extension): "
    if "!filename1!"=="" goto :error
    if /I "!filename1:~-6!"==".btnks" goto :error
    echo.
    echo SENT: * * * encode * !filename1! *
    python randomizer.py None None None encode None "!filename1!" None
    goto begin
)

if errorlevel 2 (
    cls
    echo.
    echo ^(3^) Randomize
    set /p option="Use data (Still testing), aim (Your aim only), or bullets (bullets not yet implemented): "
    set /p minval="Enter minimum random value (negative integer): "
    set /p maxval="Enter maximum random value (positive integer): "
    set /p coloumn="Column to randomize (1-13, not 4): "
    if /I "!option!" NEQ "data" if /I "!option!" NEQ "aim" if /I "!option!" NEQ "bullets" goto :error
    echo.
    echo SENT: !option! !minval! !maxval! randomize * * !coloumn!
    python randomizer.py !option! !minval! !maxval! randomize None None !coloumn!
    pause
    goto begin
)

if errorlevel 1 (
    cls
    echo.
    echo ^(1^) Decode
    set /p "filename2=Enter the filename (with .btnks extension): "
    set /p "prepri=Pretty-print the JSON output? (yes/no [default: no]): "
    if /I "!filename2:~-6!" NEQ ".btnks" goto :error
    if /I "!prepri!" NEQ "yes" if /I "!prepri!" NEQ "no" set "prepri=no"
    echo.
    echo SENT: * * * decode !prepri! !filename2! *
    python randomizer.py None None None decode !prepri! "!filename2!" None
    goto begin
)

:error
cls
echo.
color 40
echo You might be here because of a bad input selection.
echo Perhaps try another input.
timeout 3 >nul
goto begin

:end
cls
color
echo.
echo Exiting...
timeout 2 >nul
exit