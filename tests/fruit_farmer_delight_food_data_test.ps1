$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$dietConfigPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\config.py'
$thirstConfigPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'
$sourceRoot = Join-Path (Split-Path -Parent $projectRoot) 'FruitFarmerDelight'

function Assert-Equal($actual, $expected, $message) {
    if ($actual -ne $expected) {
        throw "Assertion failed: $message; actual $actual; expected $expected"
    }
}

function Assert-True($condition, $message) {
    if (-not $condition) {
        throw "Assertion failed: $message"
    }
}

$dietText = Get-Content -LiteralPath $dietConfigPath -Raw -Encoding UTF8
$thirstText = Get-Content -LiteralPath $thirstConfigPath -Raw -Encoding UTF8
$designFiles = @(Get-ChildItem -LiteralPath $projectRoot -File -Filter 'FruitFarmerDelight*.md')
Assert-Equal $designFiles.Count 1 'FruitFarmerDelight design file count'
$designPath = $designFiles[0].FullName
$designText = Get-Content -LiteralPath $designPath -Raw -Encoding UTF8
$groupOrder = @('fruits', 'grains', 'proteins', 'vegetables', 'sugars')

$dietTableMatch = [regex]::Match(
    $dietText,
    'fruitFarmerDelightFoodGroups\s*=\s*\{(?<body>[\s\S]*?)\r?\n\}'
)
Assert-True $dietTableMatch.Success 'FruitFarmerDelight nutrition table exists'

$dietEntryMatches = [regex]::Matches(
    $dietTableMatch.Groups['body'].Value,
    '(?m)^\s{4}"(?<id>fruitfarmersdelight_nullgr:[^"]+)":\s*\[(?<groups>[^\]]+)\],?\s*$'
)
Assert-Equal $dietEntryMatches.Count 347 'FruitFarmerDelight nutrition item count'

$dietValues = @{}
foreach ($entryMatch in $dietEntryMatches) {
    $itemName = $entryMatch.Groups['id'].Value
    Assert-True (-not $dietValues.ContainsKey($itemName)) "duplicate nutrition item $itemName"
    $foodGroups = @(
        [regex]::Matches($entryMatch.Groups['groups'].Value, '"(?<group>[^"]+)"') |
            ForEach-Object { $_.Groups['group'].Value }
    )
    Assert-True ($foodGroups.Count -gt 0) "empty nutrition groups for $itemName"
    $lastIndex = -1
    foreach ($groupId in $foodGroups) {
        $groupIndex = [array]::IndexOf($groupOrder, $groupId)
        Assert-True ($groupIndex -ge 0) "unknown nutrition group $groupId for $itemName"
        Assert-True ($groupIndex -gt $lastIndex) "unordered or duplicate nutrition group $groupId for $itemName"
        $lastIndex = $groupIndex
    }
    $dietValues[$itemName] = $foodGroups
}

Assert-True ($dietText -match 'foodGroups\.update\(fruitFarmerDelightFoodGroups\)') 'FruitFarmerDelight nutrition merge'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:fruit_juice_banana'] -join ',') 'fruits,sugars' 'banana juice includes its sugar crafting route'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:fruit_juice_blueberry'] -join ',') 'fruits' 'juicer-only blueberry juice has no added sugar'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:icecream_banana'] -join ',') 'fruits' 'ice cream follows the actual fruit and ice recipe'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:jam_banana'] -join ',') 'fruits' 'jam recipe contains fruit without added sugar'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:jellydrops_grape'] -join ',') 'fruits,proteins' 'gelatin jelly includes protein without invented sugar'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:wine_grape'] -join ',') 'fruits,grains' 'wine keeps fruit and wheat recipe groups'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:banana_beef'] -join ',') 'fruits,proteins,vegetables' 'banana beef cooking-pot composition'
Assert-Equal ($dietValues['fruitfarmersdelight_nullgr:strawberry_egg_tart'] -join ',') 'fruits,grains,proteins' 'egg tart extraction route has no added sugar'

$drinkTableMatch = [regex]::Match(
    $thirstText,
    'foodDrinkDefaultValues\s*=\s*\{(?<body>[\s\S]*?)\r?\n\}'
)
Assert-True $drinkTableMatch.Success 'external thirst table exists'

$drinkEntryMatches = [regex]::Matches(
    $drinkTableMatch.Groups['body'].Value,
    '(?m)^\s{4}"(?<id>fruitfarmersdelight_nullgr:[^"]+)":\s*(?<value>\d+\.0),\s*$'
)
Assert-Equal $drinkEntryMatches.Count 143 'FruitFarmerDelight thirst item count'

$drinkValues = @{}
foreach ($entryMatch in $drinkEntryMatches) {
    $itemName = $entryMatch.Groups['id'].Value
    Assert-True (-not $drinkValues.ContainsKey($itemName)) "duplicate thirst item $itemName"
    Assert-True ($dietValues.ContainsKey($itemName)) "thirst item missing from nutrition config $itemName"
    $drinkValues[$itemName] = $entryMatch.Groups['value'].Value
}

Assert-Equal ($drinkValues.Values | Where-Object { $_ -eq '2.0' }).Count 25 'FruitFarmerDelight wine count'
Assert-Equal ($drinkValues.Values | Where-Object { $_ -eq '3.0' }).Count 14 'FruitFarmerDelight dense liquid meal count'
Assert-Equal ($drinkValues.Values | Where-Object { $_ -eq '4.0' }).Count 79 'FruitFarmerDelight ice and milkshake count'
Assert-Equal ($drinkValues.Values | Where-Object { $_ -eq '5.0' }).Count 25 'FruitFarmerDelight juice count'
Assert-Equal $drinkValues['fruitfarmersdelight_nullgr:wine_grape'] '2.0' 'wine hydration value'
Assert-Equal $drinkValues['fruitfarmersdelight_nullgr:fruit_juice_grape'] '5.0' 'juice hydration value'
Assert-Equal $drinkValues['fruitfarmersdelight_nullgr:forzen_sucker_grape'] '4.0' 'ice pop hydration value'
Assert-Equal $drinkValues['fruitfarmersdelight_nullgr:milkshake_grape'] '4.0' 'milkshake hydration value'
Assert-Equal $drinkValues['fruitfarmersdelight_nullgr:grape_custard'] '3.0' 'custard hydration value'
Assert-True (-not $drinkValues.ContainsKey('fruitfarmersdelight_nullgr:jam_grape')) 'jam is not a drink'
Assert-True (-not $drinkValues.ContainsKey('fruitfarmersdelight_nullgr:luxurious_fruit_salad')) 'fruit salad is not a drink'

Assert-True ($designText -match '347') 'design records enabled food count'
Assert-True ($designText -match '143') 'design records hydration count'
Assert-True ($designText -match 'milkshake_avocado') 'design records dormant avocado milkshake'

# 外部源码存在时逐项核对，缺少同级仓库时仍验证内置数据.
if (Test-Path -LiteralPath $sourceRoot) {
    $sourceItemPath = Join-Path $sourceRoot 'FruitFarmerDelight_BP\netease_items_beh'
    $sourceFoodIds = @(
        Get-ChildItem -LiteralPath $sourceItemPath -File -Filter '*.json' |
            ForEach-Object {
                $itemJson = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
                $itemData = $itemJson.'minecraft:item'
                if ($null -ne $itemData.components.'minecraft:food') {
                    $itemData.description.identifier
                }
            }
    )
    Assert-Equal $sourceFoodIds.Count 347 'source enabled food count'
    $sourceFoodSet = @{}
    foreach ($itemName in $sourceFoodIds) {
        Assert-True (-not $sourceFoodSet.ContainsKey($itemName)) "duplicate source food $itemName"
        $sourceFoodSet[$itemName] = $true
        Assert-True ($dietValues.ContainsKey($itemName)) "source food missing from nutrition config $itemName"
    }
    foreach ($itemName in $dietValues.Keys) {
        Assert-True ($sourceFoodSet.ContainsKey($itemName)) "nutrition config item missing from source $itemName"
    }
}

Write-Output 'FruitFarmerDelight food and thirst data regression test passed'
