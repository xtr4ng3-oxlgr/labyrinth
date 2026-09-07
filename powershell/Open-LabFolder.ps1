param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

# xtr4ng3: convenience helper only.
if (Test-Path $Path) {
    Invoke-Item $Path
} else {
    Write-Host "Path not found: $Path"
}
