@echo off
echo Starting Game Content Generation Process...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
pip show fal-client >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Run the generation script with async music generation
python generate_and_merge.py --generate-music --async --music-duration 6

pause 