@echo off
:: ==========================================
:: Git Push Script (Batch file for Windows)
:: ==========================================

:: Ask for a commit message
set /p commitmsg="Enter commit message: "

:: Stage all changes
git add .

:: Commit with message
git commit -m "%commitmsg%"

:: Push to remote
git push

:: Confirm push
echo.
echo Changes pushed successfully!
pause
