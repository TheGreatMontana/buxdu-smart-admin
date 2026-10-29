
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# 1. Get CSRF token from login page
$loginPage = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/login/" -SessionVariable session -UseBasicParsing
$csrfMatch = [regex]::Match($loginPage.Content, 'name="csrfmiddlewaretoken" value="([^"]+)"')
$csrfToken = $csrfMatch.Groups[1].Value

# 2. Login as admin
$postBody = @{
    csrfmiddlewaretoken = $csrfToken
    username = "admin"
    password = "admin123"
    next = "/admin/news/article/1/change/"
}
$loginResp = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/login/" -Method POST -Body $postBody -WebSession $session -UseBasicParsing

# 3. Access article 1 change form
$articlePage = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/news/article/1/change/" -WebSession $session -UseBasicParsing
Write-Output "Status: $($articlePage.StatusCode)"
Write-Output "Contains 'BuxDU Smart Assistant': $($articlePage.Content.Contains('BuxDU Smart Assistant'))"
Write-Output "Contains 'btn-auto-translate': $($articlePage.Content.Contains('btn-auto-translate'))"
Write-Output "Contains 'btn-transliterate-new': $($articlePage.Content.Contains('btn-transliterate-new'))"
