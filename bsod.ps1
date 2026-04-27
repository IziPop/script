Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms

# 1. Lancement du compte à rebours système (600 secondes = 10 minutes)
# -r (restart), -t 600 (délai), -f (force la fermeture des applis)
shutdown -r -t 600 -f

# 2. Configuration de l'interface graphique
$w = [Windows.Window]::new()
$w.WindowStyle = 'None'
$w.WindowState = 'Maximized'
$w.Background = [Windows.Media.Brushes]::Blue
$w.Topmost = $true

$stack = [Windows.Controls.StackPanel]::new()
$stack.VerticalAlignment = "Center"
$stack.HorizontalAlignment = "Center"

# Texte d'erreur
$t = [Windows.Controls.TextBlock]::new()
$t.Text = "Your PC ran into a problem and needs to restart.`n`n:(`n`nSTOP CODE: CRITICAL_PROCESS_DIED"
$t.Foreground = [Windows.Media.Brushes]::White
$t.FontSize = 30
$t.TextAlignment = "Center"

# Affichage du Timer visuel
$timerLabel = [Windows.Controls.TextBlock]::new()
$timerLabel.Text = "`n`nRestarting in 600 seconds..."
$timerLabel.Foreground = [Windows.Media.Brushes]::White
$timerLabel.FontSize = 20
$timerLabel.TextAlignment = "Center"

$stack.Children.Add($t)
$stack.Children.Add($timerLabel)
$w.Content = $stack

# 3. Logique du compte à rebours dans l'interface
$secondsLeft = 600
$timer = [Windows.Threading.DispatcherTimer]::new()
$timer.Interval = [TimeSpan]::FromSeconds(1)
$timer.Add_Tick({
    $script:secondsLeft--
    $timerLabel.Text = "`n`nRestarting in $script:secondsLeft seconds..."
    if ($script:secondsLeft -le 0) { $timer.Stop(); $w.Close() }
})

$timer.Start()
$w.ShowDialog()
