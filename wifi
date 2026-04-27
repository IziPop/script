$profiles = (netsh wlan show profiles) | Select-String "Profil Tous les utilisateurs" | ForEach-Object {
    ($_ -split ":")[1].Trim()
}

$lines = @()
$lines += "=== MOTS DE PASSE WIFI ==="
$lines += ""

foreach ($profile in $profiles) {
    $details = netsh wlan show profile name="$profile" key=clear
    $pass = ($details | Select-String "Contenu de la cl")
    if ($pass) {
        $pass = ($pass.ToString() -split ":")[1].Trim()
    } else {
        $pass = "Pas de mot de passe"
    }
    $lines += "Reseau : $profile"
    $lines += "Mot de passe : $pass"
    $lines += ""
}

$result = $lines -join [Environment]::NewLine

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show($result, "WiFi Passwords", 0, 64)
