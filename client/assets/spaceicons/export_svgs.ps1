$dir = "C:\Users\john_\dev\ArtemisOps\client\assets\spaceicons\svg-clean"
$files = Get-ChildItem "$dir\*.svg"
foreach ($f in $files) {
    $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($f.FullName))
    Write-Output "###FILE:$($f.Name)###"
    Write-Output $b64
    Write-Output "###END###"
}
