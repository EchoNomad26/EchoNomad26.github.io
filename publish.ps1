# 1. Set variables and navigate to the blog folder
$BlogDir = "$env:USERPROFILE\Documents\EchoNomad26.github.io"
Set-Location $BlogDir

# 2. Generate today's filename
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

# 5. Start Hugo local server silently in the background
Write-Host "Generating local preview..." -ForegroundColor Yellow
$HugoProc = Start-Process hugo -ArgumentList "server -D" -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 2 # Give the server a moment to start

# 6. Open the default web browser directly to the new post
$PreviewUrl = "http://localhost:1313/blog/$DateStr-thought/"
Start-Process $PreviewUrl

# 7. Ask for user confirmation
Write-Host "`nPreview opened in your browser!" -ForegroundColor Cyan
$Response = Read-Host "Do you want to publish this post live? (Y/N)"

# 8. Stop the hidden Hugo server so it doesn't run forever
Stop-Process -Id $HugoProc.Id -Force -ErrorAction SilentlyContinue

# 9. Execute based on your choice
if ($Response -match "^[yY]") {
    Write-Host "Publishing to GitHub..." -ForegroundColor Yellow
    git add .
    git commit -m "Daily thought: $DateStr"
    git push origin main
    Write-Host "Success! Your thought will be live on echonomad26.github.io in ~45 seconds." -ForegroundColor Green
    Start-Sleep -Seconds 4
} else {
    Write-Host "Publish canceled. Your draft is saved locally on your computer." -ForegroundColor Red
    Start-Sleep -Seconds 4
}