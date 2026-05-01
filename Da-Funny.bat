@echo off
setlocal EnableDelayedExpansion

cd /D "%~dp0"
set tag=[USED]

:begin
title Options list
color 0F
cls
echo.
echo Select a number:
echo.
echo [1] Decode   %~1
echo.
echo [2] Randomize   %~2
echo.
echo [3] Encode   %~3
echo.
echo [4] Acquire Usernames and Ids   %~4
echo.
echo [5] Open the Map Editor   %~5
echo.
echo [6] Exit
echo.

choice /c 123456 /n /m "Enter your choice:"
if errorlevel 6 goto :end

if errorlevel 5 (
    title Map Editor
    cls
    echo.
    echo ^(5^) Open the Map Editor
    echo.
    echo SENT: * * * editMap * * * * *
    python randomizer.py None None None editMap None None None None None
    pause
    call :begin "" "" "" "" "!tag!"
)

if errorlevel 4 (
    title Acquire Usernames and Ids
    cls
    echo.
    echo ^(4^) Acquire Usernames and Ids
    echo.
    echo SENT: * * * acquireUsernames * * * * *
    python randomizer.py None None None acquireUsernames None None None None None
    set "filename3=userlist.txt"
    pause
    call :begin "" "" "" "!tag!"
)

if errorlevel 3 (
    title Encode
    cls
    echo.
    echo ^(3^) Encode
    set /p filename1="Enter the output filename: "
    if "!filename1!"=="" call :error "The file name can not be empty" "" "3"
    echo.
    echo SENT: * * * encode * !filename1! * * *
    python randomizer.py None None None encode None !filename1! None None None
    call :begin "" "" "!tag!"
)

if errorlevel 2 (
    title Randomize
    cls
    if not exist "output.json" (
        call :error "Error: output.json not found." "Please run the Decode option first to generate this file." "2"
    )

    echo.
    echo ^(2^) Randomize
    set /p option="Use data, or bullets (bullet randomization is not yet implemented): "

    if /I "!option!" EQU "data" (
        echo.
        echo Usernames and IDs from userlist.txt:

        if not exist "userlist.txt" (
            call :error "Error: userlist.txt not found." "Please run the Acquire Usernames and Ids option first to generate this file." "2"
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

        if !id! EQU "" (
            call :error "Invalid username!" "Try option 4, then enter the correct username" "2"
        )

        python randomizer.py None None None getMinMax None None !coloumn! None

        for /f "tokens=1,2 delims=:" %%a in (minmax.txt) do (
            if "%%a"=="Min" set "min=(min %%b)"
            if "%%a"=="Max" set "max=(max %%b)"
        )

        set /p minval="Enter minimum random value !min!: "
        set /p maxval="Enter maximum random value !max!: "
    )

    if /I "!option!" NEQ "data" (
        if /I "!option!" NEQ "bullets" (
            call :error "Invalid option!" "Try either data or bullets" "2"
        )
    )

    echo.
    echo SENT: !option! !minval! !maxval! randomize * * !coloumn! !id!
    python randomizer.py !option! !minval! !maxval! randomize None None !coloumn! !id!
    pause
    call :begin "" "!tag!"
)

if errorlevel 1 (
    title Decode
    cls
    echo.
    echo ^(1^) Decode
    set /p "filename2=Enter the target filename: "
    set /p "prepri=Pretty-print the JSON output? (yes/no [default: no]): "
    if /I "!prepri!" NEQ "yes" if /I "!prepri!" NEQ "no" set "prepri=no"
    echo.
    echo SENT: * * * decode !prepri! !filename2! * * *
    python randomizer.py None None None decode !prepri! "!filename2!" None None None
    call :begin "!tag!"
)

:error
cls
echo.
color 40
if %1 EQU nul (
    echo You might be here because of a bad input selection.
    echo Perhaps try another input.
) else (
    echo %1
    echo %2
)

timeout 3 >nul
if %3 EQU "1" call :begin !tag!
if %3 EQU "2" call :begin "" !tag!
if %3 EQU "3" call :begin "" "" !tag! 
if %3 EQU "4" call :begin "" "" "" !tag! 
if %3 EQU "5" call :begin "" "" "" "" !tag! 
call :begin "" "" "" "" ""

:end
title Exiting...
cls
color
echo.
echo Exiting...
timeout 2 >nul
exit