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
echo [4] Acqiure Usernames and Ids
echo.
echo [5] exit
echo.

choice /c 12345 /n /m "Enter your choice:"
if errorlevel 5 goto :end

if errorlevel 4 (
    cls
    echo.
    echo ^(4^) Acqiure Usernames and Ids
    echo.
    echo SENT: * * * acqiureUsernames * * * * *
    python randomizer.py None None None acqiureUsernames None None None None None
    set "filename3=userlist.txt"
    pause
    goto begin
)

if errorlevel 3 (
    cls
    echo.
    echo ^(2^) Encode
    set /p filename1="Enter the filename (without .btnks extension): "
    if "!filename1!"=="" goto :error
    if /I "!filename1:~-6!"==".btnks" goto :error
    echo.
    echo SENT: * * * encode * !filename1! * * *
    python randomizer.py None None None encode None "!filename1!" None None None
    goto begin
)

if errorlevel 2 (
    cls
    if not exist "output.json" (
        echo.
        echo Error: output.json not found. Please run the Decode option first to generate this file.
        pause
        goto begin
    )
    echo.
    echo ^(3^) Randomize
    set /p option="Use data (Still testing), or bullets (bullets not yet implemented): "
    if /I "!option!" EQU "data" (
        echo.
        echo Usernames and IDs from userlist.txt:
        if not exist "userlist.txt" (
            echo Error: userlist.txt not found. Please run the Acqiure Usernames and Ids option first to generate this file.
            pause
            goto begin
        ) else (
            if not defined !filename3! if "!filename!"=="" set "filename3=userlist.txt"
        )
        set i=0
        for /f "tokens=1-2 delims=," %%a in (!filename3!) do (
            set /a i+=1
            set "usernames!i!=%%a"
            set "userID!i!=%%b"
            echo Username: %%a, ID: %%b
        )
        echo.
        set /p "username=Enter the username or id to randomize them (case-insensitive): "
        set /p "coloumn=Column to randomize (1-7): "
        set "id="
        for %%a in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do (
            set "username=!username:%%a=%%a!"
        )
        set /a isNumeric=!username! 2>nul
        if /I !isNumeric! equ !username! (
            for /L %%i in (1,1,!i!) do (
                if "!username!"=="!userID%%i!" set "id=!userID%%i!"
            )
        ) else (
            for /L %%i in (1,1,!i!) do (
                if "!username!"=="!usernames%%i!" set "id=!userID%%i!"
            )
        )
    )
    if /I "!option!" EQU "data" (
        python randomizer.py None None None getMinMax None None !coloumn! None
        for /f "tokens=1,2 delims=:" %%a in (minmax.txt) do (
            if "%%a"=="Min" set "min=(min %%b)"
            if "%%a"=="Max" set "max=(max %%b)"
        )
    ) else ( rem Aim
        set "min= (min 0)"
        set "max= (max 360)"
    )
    set /p minval="Enter minimum random value!min!: "
    set /p maxval="Enter maximum random value!max!: "
    if /I "!option!" NEQ "data" if /I "!option!" NEQ "bullets" goto :error
    echo.
    echo SENT: !option! !minval! !maxval! randomize * * !coloumn! !id!
    python randomizer.py !option! !minval! !maxval! randomize None None !coloumn! !id!
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
    echo SENT: * * * decode !prepri! !filename2! * * *
    python randomizer.py None None None decode !prepri! "!filename2!" None None None
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