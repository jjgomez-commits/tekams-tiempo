Set objShell = CreateObject("WScript.Shell")
Dim pythonScript
pythonScript = "C:\Users\Jose J. Gomez\AppData\Roaming\Claude\local-agent-mode-sessions\45997731-6d35-4f60-84af-00b65211ddac\a39b206f-47a6-4fb5-b04c-4599015c17dd\local_e7034798-53ad-4f92-9cef-d2b4ccdcb33b\outputs\process_tekams.py"
objShell.Run "python """ & pythonScript & """", 1, True
