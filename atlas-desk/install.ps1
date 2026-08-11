# Atlas Desk - installation de l'agent sur Windows, en une ligne.
#   irm https://atlasnexus.tech/atlas-desk/install.ps1 | iex
# Telecharge le binaire, l'installe dans %LOCALAPPDATA%\AtlasDesk, cree une tache
# planifiee au demarrage de session, puis affiche l'identifiant a 9 chiffres.

$ErrorActionPreference = 'Stop'
$Version = 'v0.10.0'
$Asset   = 'atlas-desk-agent-windows-amd64.zip'
$Url     = "https://github.com/AtlasNexusTech/atlas-desk/releases/download/$Version/$Asset"
$Signal  = 'wss://signal.atlasnexus.tech/ws'
$Dir     = Join-Path $env:LOCALAPPDATA 'AtlasDesk'
$Task    = 'AtlasDeskAgent'

function Say($m) { Write-Host "* $m" -ForegroundColor Cyan }
function Bad($m) { Write-Host "x $m" -ForegroundColor Red; exit 1 }

if ([Environment]::Is64BitOperatingSystem -eq $false) { Bad "Windows 64 bits requis." }

Say "Telechargement de l'agent ($Version)"
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$Zip = Join-Path $env:TEMP 'atlas-desk-agent.zip'
try   { Invoke-WebRequest -Uri $Url -OutFile $Zip -UseBasicParsing }
catch { Bad "Telechargement impossible : $($_.Exception.Message)" }

Say "Installation dans $Dir"
Expand-Archive -Path $Zip -DestinationPath $Dir -Force
Remove-Item $Zip -Force -ErrorAction SilentlyContinue

$Exe = Get-ChildItem -Path $Dir -Filter '*.exe' -Recurse | Select-Object -First 1
if (-not $Exe) { Bad "Executable introuvable dans l'archive." }

# Autorise l'agent dans le pare-feu (silencieux si deja present ou sans droits admin)
try {
  New-NetFirewallRule -DisplayName 'Atlas Desk Agent' -Direction Inbound `
    -Program $Exe.FullName -Action Allow -Profile Any -ErrorAction SilentlyContinue | Out-Null
} catch { }

Say "Creation du demarrage automatique"
schtasks /Query /TN $Task *> $null
if ($LASTEXITCODE -eq 0) { schtasks /Delete /TN $Task /F *> $null }
$Cmd = "`"$($Exe.FullName)`" -signal $Signal"
schtasks /Create /TN $Task /TR $Cmd /SC ONLOGON /RL LIMITED /F *> $null
if ($LASTEXITCODE -ne 0) { Write-Host "  (tache planifiee non creee : lancement manuel requis)" -ForegroundColor Yellow }

Say "Demarrage de l'agent"
$Log = Join-Path $Dir 'agent.log'
Start-Process -FilePath $Exe.FullName -ArgumentList "-signal $Signal" `
  -WindowStyle Hidden -RedirectStandardOutput $Log -RedirectStandardError (Join-Path $Dir 'agent.err.log')

Start-Sleep -Seconds 4
$Id = $null
if (Test-Path $Log) {
  $Id = (Select-String -Path $Log -Pattern '\d{3}[ -]?\d{3}[ -]?\d{3}' -AllMatches |
         ForEach-Object { $_.Matches } | Select-Object -Last 1).Value
}

Write-Host ""
if ($Id) {
  Write-Host "  Votre identifiant Atlas Desk : $Id" -ForegroundColor Green
} else {
  Write-Host "  Agent demarre. Identifiant visible dans : $Log" -ForegroundColor Yellow
}
Write-Host ""
Say "Connectez-vous depuis un navigateur :"
Write-Host "  https://atlasnexus.tech/atlas-desk/client/"
Write-Host ""
Write-Host "  Arreter      : schtasks /End /TN $Task"
Write-Host "  Desinstaller : schtasks /Delete /TN $Task /F ; Remove-Item -Recurse '$Dir'"
