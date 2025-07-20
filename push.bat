$commitmsg = Read-Host "Enter commit message"
git add .
git commit -m "$commitmsg"
git push
Write-Output "Changes pushed!"
