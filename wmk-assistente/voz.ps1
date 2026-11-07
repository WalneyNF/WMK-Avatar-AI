param([string]$TextoArquivo,[string]$WavArquivo,[string]$Voz='')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Speech
$texto=[System.IO.File]::ReadAllText($TextoArquivo,[System.Text.Encoding]::UTF8)
$synth=New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
  if($Voz){$synth.SelectVoice($Voz)}
  else {
    $pt=$synth.GetInstalledVoices() | Where-Object {$_.VoiceInfo.Culture.Name -eq 'pt-BR'} | Select-Object -First 1
    if($pt){$synth.SelectVoice($pt.VoiceInfo.Name)}
  }
  $synth.SetOutputToWaveFile($WavArquivo)
  $synth.Speak($texto)
  $synth.SetOutputToNull()
} finally {$synth.Dispose()}
