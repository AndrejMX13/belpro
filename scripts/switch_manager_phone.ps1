param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("volunteer", "manager")]
    [string]$Mode
)

$fakePhone = "38600000000"
$realPhone = "38630369632"
$apiUrl = "http://localhost:8100/api/managers/me"
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("manager:`;FX~:7SMJKpT2n."))

if ($Mode -eq "volunteer") {
    $phone = $fakePhone
    Write-Host "Switching to FAKE ($phone) - your phone is VOLUNTEER"
} else {
    $phone = $realPhone
    Write-Host "Switching to REAL ($phone) - your phone is MANAGER"
}

$body = "{""phone"":""$phone""}"
try {
    $result = Invoke-RestMethod -Uri $apiUrl -Method PATCH -Body $body `
        -ContentType "application/json" `
        -Headers @{Authorization="Basic $cred"}
    Write-Host "Done. Manager phone: $($result.phone)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
