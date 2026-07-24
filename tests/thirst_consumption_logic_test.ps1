$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'
$dataPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst.py'
$serverPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst_ss.py'

function Assert-Regex($text, $pattern, $message) {
    if ($text -notmatch $pattern) {
        throw "Assertion failed: $message"
    }
}

function Assert-Approx($actual, $expected, $message) {
    if ([Math]::Abs($actual - $expected) -gt 0.000001) {
        throw "Assertion failed: $message; actual $actual; expected $expected"
    }
}

$configText = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8
$dataText = Get-Content -LiteralPath $dataPath -Raw -Encoding UTF8
$serverText = Get-Content -LiteralPath $serverPath -Raw -Encoding UTF8

Assert-Regex -text $configText -pattern 'baseDecayIntervalTick\s*=\s*20' -message 'base decay interval'
Assert-Regex -text $configText -pattern 'baseDecayPerSecond\s*=\s*1\.0\s*/\s*180\.0' -message 'base decay rate'
Assert-Regex -text $configText -pattern 'hungerDecayFactor\s*=\s*0\.2' -message 'hunger decay factor'
Assert-Regex -text $configText -pattern 'dataSaveIntervalTick\s*=\s*600' -message 'batched save interval'
Assert-Regex -text $configText -pattern 'respawnValue\s*=\s*20\.0' -message 'respawn value'
Assert-Approx (20.0 / (1.0 / 180.0) / 3600.0) 1.0 'one-hour idle depletion'

Assert-Regex -text $dataText -pattern "'dirty':\s*False" -message 'dirty state initialization'
Assert-Regex -text $serverText -pattern 'PlayerHungerChangeServerEvent' -message 'hunger event listener'
Assert-Regex -text $serverText -pattern '\(hungerBefore\s*-\s*hunger\)\s*\*\s*config\.hungerDecayFactor' -message 'activity decay formula'
Assert-Regex -text $serverText -pattern 'GetPlayerGameType\(playerId\)' -message 'game type query'
Assert-Regex -text $serverText -pattern 'gameTypeEnum\.Creative' -message 'creative mode filter'
Assert-Regex -text $serverText -pattern 'gameTypeEnum\.Spectator' -message 'spectator mode filter'
Assert-Regex -text $serverText -pattern "data\['dirty'\]\s*=\s*True" -message 'automatic decay dirty mark'
Assert-Regex -text $serverText -pattern "if data\['dirty'\]:[\s\S]*Thirst\.savePlayerData[\s\S]*data\['dirty'\]\s*=\s*False" -message 'dirty batch save and clear'
Assert-Regex -text $serverText -pattern 'PlayerRespawnFinishServerEvent' -message 'respawn event listener'
Assert-Regex -text $serverText -pattern 'config\.respawnValue' -message 'configured respawn reset'

Write-Output 'Thirst consumption regression test passed'
