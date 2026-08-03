$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$configPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'
$configText = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8

function Assert-Equal($actual, $expected, $message) {
    if ($actual -ne $expected) {
        throw "Assertion failed: $message; actual $actual; expected $expected"
    }
}

$tableMatch = [regex]::Match($configText, 'foodDrinkDefaultValues\s*=\s*\{(?<body>[\s\S]*?)\r?\n\}')
if (-not $tableMatch.Success) {
    throw 'Assertion failed: external drink table'
}

$entryMatches = [regex]::Matches(
    $tableMatch.Groups['body'].Value,
    '(?m)^\s{4}"(?<id>[^"]+)":\s*(?<value>\d+\.0),\s*$'
)
Assert-Equal $entryMatches.Count 423 'external drink item count'

$values = @{}
foreach ($entryMatch in $entryMatches) {
    $itemName = $entryMatch.Groups['id'].Value
    $defaultValue = $entryMatch.Groups['value'].Value
    if ($values.ContainsKey($itemName)) {
        throw "Assertion failed: duplicate external drink item $itemName"
    }
    if ($defaultValue -notin '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '8.0') {
        throw "Assertion failed: invalid hydration value $defaultValue for $itemName"
    }
    $values[$itemName] = $defaultValue
}

Assert-Equal ($values.Values | Where-Object { $_ -eq '1.0' }).Count 11 '1.0 hydration count'
Assert-Equal ($values.Values | Where-Object { $_ -eq '2.0' }).Count 29 '2.0 hydration count'
Assert-Equal ($values.Values | Where-Object { $_ -eq '3.0' }).Count 150 '3.0 hydration count'
Assert-Equal ($values.Values | Where-Object { $_ -eq '4.0' }).Count 114 '4.0 hydration count'
Assert-Equal ($values.Values | Where-Object { $_ -eq '5.0' }).Count 110 '5.0 hydration count'
Assert-Equal ($values.Values | Where-Object { $_ -eq '6.0' }).Count 7 '6.0 hydration count'
Assert-Equal ($values.Values | Where-Object { $_ -eq '8.0' }).Count 2 '8.0 hydration count'

Assert-Equal $values['tea_delight_nullgr:ceramic_teacup_red_tea'] '3.0' 'small teacup tea value'
Assert-Equal $values['dragon_boat_festival_nullgr:soy_milk'] '6.0' 'plant milk value'
Assert-Equal $values['farmer_delight_nullgr:apple_cider'] '5.0' 'FarmerDelight fruit drink value'
Assert-Equal $values['farmer_delight_nullgr:beef_stew'] '3.0' 'FarmerDelight thick stew value'
Assert-Equal $values['farmer_delight_nullgr:bone_broth'] '4.0' 'FarmerDelight clear broth value'
Assert-Equal $values['farmer_delight_nullgr:milk_bottle'] '6.0' 'FarmerDelight milk bottle value'
Assert-Equal $values['hearthandharvest_nullgr:red_grape_wine'] '2.0' 'wine value'
Assert-Equal $values['vintage_delight_nullgr:pickle_soup'] '4.0' 'soup value'
Assert-Equal $values['foragersinsight_nullgr:seed_milk_bucket'] '8.0' 'large milk value'

if ($configText -notmatch 'for itemName, drinkDefaultValue in foodDrinkDefaultValues\.items\(\):[\s\S]*"event": playerEatDrinkEvent[\s\S]*"defaultValue": drinkDefaultValue[\s\S]*"auxValues": \{\}') {
    throw 'Assertion failed: external drink data merge'
}

Write-Output 'Thirst external drink data regression test passed'
