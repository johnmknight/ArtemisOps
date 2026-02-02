Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Check if server is running on port 8080
Set objExec = WshShell.Exec("cmd /c netstat -ano | findstr "":8080.*LISTENING""")
strOutput = objExec.StdOut.ReadAll()

If Len(Trim(strOutput)) = 0 Then
    ' Server not running - start it
    WshShell.CurrentDirectory = "C:\Users\john_\ArtemisOps\server"
    WshShell.Run "cmd /c .\venv\Scripts\python.exe main.py", 0, False
    WScript.Sleep 3000
End If

' Open Chrome to ArtemisOps
WshShell.Run "chrome.exe http://localhost:8080", 1, False
