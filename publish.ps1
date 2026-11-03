# 1. Set variables and navigate to the blog folder
$BlogDir = "$env:USERPROFILE\Documents\EchoNomad26.github.io"
Set-Location $BlogDir

# 2. Generate today's filename (e.g., 2026-11-03-thought.md)
$DateStr = Get-Date -Format "yyyy-MM-dd"
$FileName = "blog/$DateStr-thought.md"
$FilePath = "content/$FileName"

# 3. Create the file if it doesn't already exist today
if (-not (Test-Path $FilePath)) {
    hugo new $FileName
    # Automatically set draft to false
    (Get-Content $FilePath) -replace 'draft: true', 'draft: false' | Set-Content $FilePath
}

# 4. Open Notepad and pause the script until you close it
Write-Host "Opening Notepad. Write your thought, save (Ctrl+S), and close Notepad when finished..." -ForegroundColor Cyan
Start-Process notepad.exe -ArgumentList $FilePath -Wait

# 5. Push to GitHub automatically
Write-Host "Publishing to GitHub..." -ForegroundColor Yellow
git add .
git commit -m "Daily thought: $DateStr"
git push origin main

Write-Host "Success! Your thought will be live on echonomad26.github.io in ~45 seconds." -ForegroundColor Green
Start-Sleep -Seconds 5