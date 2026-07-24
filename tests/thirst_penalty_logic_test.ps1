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

function Assert-NotRegex($text, $pattern, $message) {
    if ($text -match $pattern) {
        throw "Assertion failed: $message"
    }
}

$configText = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8
$dataText = Get-Content -LiteralPath $dataPath -Raw -Encoding UTF8
$serverText = Get-Content -LiteralPath $serverPath -Raw -Encoding UTF8
$clientText = Get-Content -LiteralPath $clientPath -Raw -Encoding UTF8

Assert-Regex -text $configText -pattern 'playerEatDrinkEvent\s*=\s*"PlayerEatFoodServerEvent"' -message 'food completion event source'
Assert-Regex -text $configText -pattern 'actorUseDrinkEvent\s*=\s*"ActorUseItemServerEvent"' -message 'item-use completion event source'
Assert-Regex -text $configText -pattern '"minecraft:milk_bucket"\s*:\s*\{[\s\S]*?"event"\s*:\s*playerEatDrinkEvent[\s\S]*?"defaultValue"\s*:\s*8\.0' -message 'milk hydration data'
Assert-Regex -text $configText -pattern '"minecraft:potion"\s*:\s*\{[\s\S]*?"event"\s*:\s*actorUseDrinkEvent[\s\S]*?"defaultValue"\s*:\s*4\.0[\s\S]*?"auxValues"\s*:\s*\{\s*0\s*:\s*6\.0' -message 'water bottle and potion hydration data'
Assert-Regex -text $configText -pattern 'dehydrationDamageIntervalTick\s*=\s*80' -message 'four-second dehydration interval'
Assert-Regex -text $configText -pattern 'dehydrationDamage\s*=\s*1\.0' -message 'dehydration damage amount'
Assert-Regex -text $configText -pattern 'easyDehydrationMinHealth\s*=\s*10\.0' -message 'easy health floor'
Assert-Regex -text $configText -pattern 'normalDehydrationMinHealth\s*=\s*1\.0' -message 'normal health floor'

Assert-Regex -text $serverText -pattern '"PlayerEatFoodServerEvent"' -message 'verified milk completion listener'
Assert-Regex -text $serverText -pattern '"ActorUseItemServerEvent"\s*,\s*self\s*,\s*self\.ActorUseItemServerEvent' -message 'potion completion listener'
Assert-Regex -text $dataText -pattern "def\s+getDrinkItemValue\(itemName,\s*itemAuxValue\):[\s\S]*itemAuxValue\s+in\s+drinkData\['auxValues'\][\s\S]*return\s+drinkData\['defaultValue'\]" -message 'aux-specific hydration lookup with default fallback'
Assert-Regex -text $serverText -pattern "def\s+ActorUseItemServerEvent\(self,\s*args\):[\s\S]*playerId\s*=\s*args\['playerId'\][\s\S]*itemDict\s*=\s*args\['itemDict'\][\s\S]*stackSize\s*=\s*args\['stackSize'\][\s\S]*itemName\s*=\s*args\['itemName'\][\s\S]*itemAuxValue\s*=\s*args\['auxValue'\][\s\S]*useMethod\s*=\s*args\['useMethod'\]" -message 'official item-use event parameters'
Assert-Regex -text $serverText -pattern "def\s+ActorUseItemServerEvent[\s\S]*drinkData\['event'\]\s*!=\s*config\.actorUseDrinkEvent[\s\S]*self\.addThirstValue\(playerId,\s*Thirst\.getDrinkItemValue\(itemName,\s*itemAuxValue\)\)" -message 'potion hydration settlement on item-use completion'
Assert-Regex -text $serverText -pattern "def\s+PlayerEatFoodServerEvent[\s\S]*itemAuxValue\s*=\s*itemDict\['newAuxValue'\][\s\S]*drinkData\['event'\]\s*!=\s*config\.playerEatDrinkEvent[\s\S]*self\.addThirstValue\(playerId,\s*Thirst\.getDrinkItemValue\(itemName,\s*itemAuxValue\)\)" -message 'milk hydration settlement on food completion'
Assert-NotRegex -text $serverText -pattern 'Codex(Actor|Inventory|Item|OnCarried|ServerItem)' -message 'temporary event probes removed'

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
