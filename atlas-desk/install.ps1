# Atlas Desk - installation de l'agent sur Windows, en une ligne.
#   irm https://atlasnexus.tech/atlas-desk/install.ps1 | iex
# Installe dans %LOCALAPPDATA%\AtlasDesk, ajoute un raccourci au demarrage de
# session, lance l'agent et affiche son identifiant a 9 chiffres.
# Aucun droit administrateur requis.

$Version = 'v0.10.0'
$Asset   = 'atlas-desk-agent-windows-amd64.zip'
$Url     = "https://github.com/AtlasNexusTech/atlas-desk/releases/download/$Version/$Asset"
$Signal  = 'wss://signal.atlasnexus.tech/ws'
$Dir     = Join-Path $env:LOCALAPPDATA 'AtlasDesk'
$LnkName = 'Atlas Desk Agent.lnk'

function Say($m) { Write-Host "* $m" -ForegroundColor Cyan }
function Warn($m){ Write-Host "  $m" -ForegroundColor Yellow }
function Bad($m) { Write-Host "x $m" -ForegroundColor Red; return }

if (-not [Environment]::Is64BitOperatingSystem) { Bad "Windows 64 bits requis."; return }

# --- 1. Telechargement -------------------------------------------------------
Say "Telechargement de l'agent ($Version)"
try {
  New-Item -ItemType Directory -Force -Path $Dir | Out-Null
  $Zip = Join-Path $env:TEMP 'atlas-desk-agent.zip'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  Invoke-WebRequest -Uri $Url -OutFile $Zip -UseBasicParsing -ErrorAction Stop
} catch { Bad "Telechargement impossible : $($_.Exception.Message)"; return }

# --- 2. Arret d'une instance precedente --------------------------------------
Get-Process -Name 'atlas-desk-agent*' -ErrorAction SilentlyContinue |
  Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 600

# --- 3. Extraction -----------------------------------------------------------
Say "Installation dans $Dir"
try {
  Expand-Archive -Path $Zip -DestinationPath $Dir -Force -ErrorAction Stop
  Remove-Item $Zip -Force -ErrorAction SilentlyContinue
} catch { Bad "Extraction impossible : $($_.Exception.Message)"; return }

$Exe = Get-ChildItem -Path $Dir -Filter '*.exe' -Recurse -ErrorAction SilentlyContinue |
       Select-Object -First 1
if (-not $Exe) { Bad "Executable introuvable dans l'archive."; return }

# --- 4. Demarrage automatique (raccourci, sans admin ni schtasks) ------------
Say "Configuration du demarrage automatique"
try {
  $Startup = [Environment]::GetFolderPath('Startup')
  $Lnk = Join-Path $Startup $LnkName
  $W = New-Object -ComObject WScript.Shell
  $S = $W.CreateShortcut($Lnk)
  $S.TargetPath       = $Exe.FullName
  $S.Arguments        = "-signal $Signal"
  $S.WorkingDirectory = $Dir
  $S.WindowStyle      = 7          # demarre reduit
  $S.Description      = 'Atlas Desk - agent de prise en main a distance'
  $S.Save()
} catch { Warn "Demarrage automatique non configure : $($_.Exception.Message)" }

# --- 5. Pare-feu (silencieux si pas admin) -----------------------------------
try {
  $fw = Get-Command New-NetFirewallRule -ErrorAction SilentlyContinue
  if ($fw) {
    New-NetFirewallRule -DisplayName 'Atlas Desk Agent' -Direction Inbound `
      -Program $Exe.FullName -Action Allow -Profile Any -ErrorAction SilentlyContinue | Out-Null
  }
} catch { }

# --- 6. Lancement ------------------------------------------------------------
Say "Demarrage de l'agent"
$Log = Join-Path $Dir 'agent.log'
$Err = Join-Path $Dir 'agent.err.log'
Remove-Item $Log,$Err -Force -ErrorAction SilentlyContinue
try {
  Start-Process -FilePath $Exe.FullName -ArgumentList "-signal $Signal" `
    -WorkingDirectory $Dir -WindowStyle Hidden `
    -RedirectStandardOutput $Log -RedirectStandardError $Err -ErrorAction Stop
} catch { Bad "Lancement impossible : $($_.Exception.Message)"; return }

# --- 7. Recuperation de l'identifiant ----------------------------------------
$Id = $null
foreach ($i in 1..12) {
  Start-Sleep -Milliseconds 800
  foreach ($file in @($Log, $Err)) {
    if (Test-Path $file) {
      $txt = Get-Content $file -Raw -ErrorAction SilentlyContinue
      if ($txt -and $txt -match '(\d{3}[ \-]?\d{3}[ \-]?\d{3})') { $Id = $Matches[1] }
    }
  }
  if ($Id) { break }
}

Write-Host ""
if ($Id) {
  Write-Host "  Votre identifiant Atlas Desk : $Id" -ForegroundColor Green
} else {
  Warn "Agent demarre, identifiant pas encore visible."
  Warn "Consultez : $Log"
}
Write-Host ""
Say "Connectez-vous depuis un navigateur :"
Write-Host "  https://atlasnexus.tech/atlas-desk/client/"
Write-Host ""
Write-Host "  Journal      : $Log"
Write-Host "  Arreter      : Get-Process atlas-desk-agent* | Stop-Process -Force"
Write-Host "  Desinstaller : Remove-Item -Recurse -Force '$Dir' ; Remove-Item '$([Environment]::GetFolderPath('Startup'))\$LnkName'"
