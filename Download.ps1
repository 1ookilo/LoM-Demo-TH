param(
    [string]$Authorization
)

$ErrorFile = "./Error.txt"
if ((Test-Path -Path $ErrorFile)) {
    Remove-Item $ErrorFile
}
else {
    
    git config --global user.name 'github-actions[bot]'
    git config --global user.email 'github-actions[bot]@users.noreply.github.com'
    git rm Localize/utf8/Localize.json
    git commit -m "Remove Localize.json before download"

    $url = "https://paratranz.cn/api/projects/8038/artifacts/download"
    $headers = @{
        "Authorization" = "$Authorization"
        "accept" = "*/*"
    }
    $response = Invoke-WebRequest -Uri $url -Headers $headers -Method Get
    [IO.File]::WriteAllBytes("test.zip", $response.Content)

    # Unzip the file to the desired directory
    $destinationPath = "Localize"  # Specify the destination directory here
    Expand-Archive -Path "test.zip" -DestinationPath $destinationPath -Force
    

    git add Localize/*
    $commitMessage = $(Get-Date -Format "MM-dd")+" ParaToGitWrok"
    git commit -m $commitMessage
    git push https://github-actions[bot]:${ secrets.GH_TOKEN }@github.com/1ookilo/LoM-Demo-TH
}