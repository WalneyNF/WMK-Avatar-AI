Add-Type -AssemblyName System.Speech
$s=New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.GetInstalledVoices() | ForEach-Object { Write-Output ($_.VoiceInfo.Name + ' / ' + $_.VoiceInfo.Culture.Name) }
$s.Dispose()
