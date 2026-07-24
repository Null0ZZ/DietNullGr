$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'
$dataPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst.py'
$serverPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst_ss.py'
$clientPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst_cs.py'

function Assert-Regex($text, $pattern, $message) {
    if ($text -notmatch $pattern) {
        throw "Assertion failed: $message"
    }
}

$configText = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8
$dataText = Get-Content -LiteralPath $dataPath -Raw -Encoding UTF8
$serverText = Get-Content -LiteralPath $serverPath -Raw -Encoding UTF8
$clientText = Get-Content -LiteralPath $clientPath -Raw -Encoding UTF8

Assert-Regex -text $configText -pattern '"minecraft:milk_bucket"\s*:\s*8\.0' -message 'milk hydration data'
Assert-Regex -text $configText -pattern 'dehydrationDamageIntervalTick\s*=\s*80' -message 'four-second dehydration interval'
Assert-Regex -text $configText -pattern 'dehydrationDamage\s*=\s*1\.0' -message 'dehydration damage amount'
Assert-Regex -text $configText -pattern 'easyDehydrationMinHealth\s*=\s*10\.0' -message 'easy health floor'
Assert-Regex -text $configText -pattern 'normalDehydrationMinHealth\s*=\s*1\.0' -message 'normal health floor'

Assert-Regex -text $serverText -pattern '"PlayerEatFoodServerEvent"' -message 'verified milk completion listener'
Assert-Regex -text $serverText -pattern "itemName\s*=\s*itemDict\['newItemName'\][\s\S]*itemName\s+not\s+in\s+config\.drinkItemValues" -message 'configured drink lookup'
Assert-Regex -text $serverText -pattern "self\.addThirstValue\(playerId,\s*config\.drinkItemValues\[itemName\]\)" -message 'drink hydration settlement'

Assert-Regex -text $dataText -pattern "'dehydrationTicks':\s*0" -message 'dehydration timer initialization'
Assert-Regex -text $dataText -pattern "'sprintLimited':\s*False" -message 'sprint restriction initialization'
Assert-Regex -text $serverText -pattern 'GetGameDiffculty\(\)' -message 'difficulty query'
Assert-Regex -text $serverText -pattern 'gameDifficultyEnum\.Peaceful' -message 'peaceful filter'
Assert-Regex -text $serverText -pattern 'gameDifficultyEnum\.Easy' -message 'easy difficulty branch'
Assert-Regex -text $serverText -pattern 'gameDifficultyEnum\.Normal' -message 'normal difficulty branch'
Assert-Regex -text $serverText -pattern 'actorDamageCause\.Starve' -message 'starvation damage cause'
Assert-Regex -text $serverText -pattern 'health\s*-\s*minHealth' -message 'difficulty health floor clipping'
Assert-Regex -text $serverText -pattern "not data\['enabled'\][\s\S]*gameDifficulty\s*==\s*gameDifficultyEnum\.Peaceful[\s\S]*gameType\s*==\s*gameTypeEnum\.Creative[\s\S]*gameType\s*==\s*gameTypeEnum\.Spectator" -message 'live mode filters before dehydration damage'

Assert-Regex -text $clientText -pattern '"OnScriptTickClient"' -message 'client tick listener'
Assert-Regex -text $clientText -pattern "self\.thirstData\['sprintLimited'\]" -message 'synced sprint restriction check'
Assert-Regex -text $clientText -pattern 'CreateActorMotion\(clientApi\.GetLocalPlayerId\(\)\)[\s\S]*EndSprinting\(\)' -message 'low thirst sprint cancellation'

Write-Output 'Thirst hydration and penalty regression test passed'
