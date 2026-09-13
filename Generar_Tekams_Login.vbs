Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

'Obtener la ruta de la carpeta actual
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

'Crear archivo batch temporal
strBatchFile = strPath & "\temp_run.bat"
Set objFile = objFSO.CreateTextFile(strBatchFile, True)
objFile.WriteLine("@echo off")
objFile.WriteLine("cd /d """ & strPath & """")
objFile.WriteLine("python GENERAR_TEKAMS_LOGIN.py")
objFile.WriteLine("del """ & strBatchFile & """")
objFile.Close()

'Ejecutar el batch
objShell.Run """" & strBatchFile & """"
