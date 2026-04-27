# Plus besoin de param($url)
$url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRm2KkGlWZXuzaK1lOLy9dDEo4Jl_wpJYTFPg&s"
$img = "$env:TEMP\sys_cache_04.jpg"

try {
    Invoke-WebRequest -Uri $url -OutFile $img -ErrorAction SilentlyContinue
    $c = @"
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@
    if (-not ([System.Management.Automation.PSTypeName]"Wallpaper").Type) {
        Add-Type -TypeDefinition $c -ErrorAction SilentlyContinue
    }
    [Wallpaper]::SystemParametersInfo(20, 0, $img, 0x01 -bor 0x02) | Out-Null
} catch { exit }
