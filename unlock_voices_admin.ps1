# Run this script as Administrator to unlock premium Windows OneCore voices (including George - Male) in standard SAPI5 applications.
$source = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$destination = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"

if (-not (Test-Path $source)) {
    Write-Host "OneCore voices path not found. Exiting." -ForegroundColor Red
    exit
}

Get-ChildItem -Path $source | ForEach-Object {
    $name = $_.PSChildName
    $destPath = Join-Path $destination $name
    if (-not (Test-Path $destPath)) {
        Write-Host "Unlocking voice: $name" -ForegroundColor Green
        Copy-Item -Path $_.PSPath -Destination $destination -Recurse -Force
    } else {
        Write-Host "Voice $name is already unlocked." -ForegroundColor Yellow
    }
}
Write-Host "Done! Please restart Jarvis." -ForegroundColor Green
