$repo = "C:\Users\User\Desktop\mirae\backroom"
Set-Location $repo

while ($true) {
    try {
        git pull origin main 2>&1 | Out-Null
    } catch {
        # ignore errors
    }
    Start-Sleep -Seconds 120
}
