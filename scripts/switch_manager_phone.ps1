param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("volunteer", "manager")]
    [string]$Mode
)

$fakePhone = if ($env:TEST_VOLUNTEER_PHONE) { $env:TEST_VOLUNTEER_PHONE } else { "38600000000" }
$realPhone = $env:TEST_MANAGER_PHONE
if (-not $realPhone) {
    Write-Host "ERROR: TEST_MANAGER_PHONE not set in environment" -ForegroundColor Red
    exit 1
}

$password = $env:MANAGER_PASSWORD
if (-not $password) {
    Write-Host "ERROR: MANAGER_PASSWORD not set in environment" -ForegroundColor Red
    exit 1
}

$apiUrl = "http://localhost:8100/api/managers/me"
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("manager:$password"))

if ($Mode -eq "volunteer") {
    $phone = $fakePhone
    Write-Host "Switching to TEST phone ($phone) - your phone is VOLUNTEER"
} else {
    $phone = $realPhone
    Write-Host "Switching to REAL phone ($phone) - your phone is MANAGER"
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
