$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$dietConfigPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\config.py'
$thirstConfigPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'

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

$designFiles = @(Get-ChildItem -LiteralPath $projectRoot -File -Filter 'FarmerDelight*.md')
Assert-Equal $designFiles.Count 1 'FarmerDelight design file count'
$designPath = $designFiles[0].FullName
$dietText = Get-Content -LiteralPath $dietConfigPath -Raw -Encoding UTF8
$thirstText = Get-Content -LiteralPath $thirstConfigPath -Raw -Encoding UTF8
$designText = Get-Content -LiteralPath $designPath -Raw -Encoding UTF8

$groupOrder = @('fruits', 'grains', 'proteins', 'vegetables', 'sugars')

$dietTableMatch = [regex]::Match(
    $dietText,
    'farmerDelightFoodGroups\s*=\s*\{(?<body>[\s\S]*?)\r?\n\}'
)
Assert-True $dietTableMatch.Success 'FarmerDelight nutrition table exists'

$dietEntryMatches = [regex]::Matches(
    $dietTableMatch.Groups['body'].Value,
    '(?m)^\s{4}"(?<id>farmer_delight_nullgr:[^"]+)":\s*\[(?<groups>[^\]]+)\],?\s*$'
)
Assert-Equal $dietEntryMatches.Count 78 'FarmerDelight nutrition item count'

$dietValues = @{}
foreach ($entryMatch in $dietEntryMatches) {
    $itemName = $entryMatch.Groups['id'].Value
    Assert-True (-not $dietValues.ContainsKey($itemName)) "duplicate nutrition item $itemName"
    $groups = @(
        [regex]::Matches($entryMatch.Groups['groups'].Value, '"(?<group>[^"]+)"') |
            ForEach-Object { $_.Groups['group'].Value }
    )
    Assert-True ($groups.Count -gt 0) "empty nutrition groups for $itemName"
    $lastIndex = -1
    foreach ($groupId in $groups) {
        $groupIndex = [array]::IndexOf($groupOrder, $groupId)
        Assert-True ($groupIndex -ge 0) "unknown nutrition group $groupId for $itemName"
        Assert-True ($groupIndex -gt $lastIndex) "unordered or duplicate nutrition group $groupId for $itemName"
        $lastIndex = $groupIndex
    }
    $dietValues[$itemName] = $groups
}

Assert-True ($dietText -match 'foodGroups\.update\(farmerDelightFoodGroups\)') 'FarmerDelight nutrition merge'
Assert-True (-not $dietValues.ContainsKey('farmer_delight_nullgr:cathartic_bottle')) 'cathartic bottle has no nutrition'

$designRows = [regex]::Matches(
    $designText,
    '(?m)^\| `(?<id>farmer_delight_nullgr:[^`]+)` \| (?<name>[^|]+) \| (?<groups>[^|]+) \| (?<thirst>\d+) \|'
)
Assert-Equal $designRows.Count 79 'FarmerDelight reviewed food row count'

$designValues = @{}
$designThirstValues = @{}
foreach ($designRow in $designRows) {
    $itemName = $designRow.Groups['id'].Value
    Assert-True (-not $designValues.ContainsKey($itemName)) "duplicate design item $itemName"
    $designValues[$itemName] = $designRow.Groups['groups'].Value.Trim()
    $thirstValue = [int]$designRow.Groups['thirst'].Value
    if ($thirstValue -gt 0) {
        $designThirstValues[$itemName] = '{0}.0' -f $thirstValue
    }
}

Assert-True ($designValues.ContainsKey('farmer_delight_nullgr:cathartic_bottle')) 'cathartic bottle appears in design'
foreach ($itemName in $dietValues.Keys) {
    Assert-True ($designValues.ContainsKey($itemName)) "nutrition item missing from design $itemName"
}
foreach ($itemName in $designValues.Keys) {
    if ($itemName -eq 'farmer_delight_nullgr:cathartic_bottle') {
        continue
    }
    Assert-True ($dietValues.ContainsKey($itemName)) "designed food missing from nutrition config $itemName"
}

$drinkTableMatch = [regex]::Match(
    $thirstText,
    'foodDrinkDefaultValues\s*=\s*\{(?<body>[\s\S]*?)\r?\n\}'
)
Assert-True $drinkTableMatch.Success 'external thirst table exists'

$farmerDrinkMatches = [regex]::Matches(
    $drinkTableMatch.Groups['body'].Value,
    '(?m)^\s{4}"(?<id>farmer_delight_nullgr:[^"]+)":\s*(?<value>\d+\.0),\s*$'
)
Assert-Equal $farmerDrinkMatches.Count 15 'FarmerDelight thirst item count'
Assert-Equal $designThirstValues.Count 15 'FarmerDelight designed thirst item count'

$drinkValues = @{}
foreach ($drinkMatch in $farmerDrinkMatches) {
    $itemName = $drinkMatch.Groups['id'].Value
    Assert-True (-not $drinkValues.ContainsKey($itemName)) "duplicate thirst item $itemName"
    $drinkValues[$itemName] = $drinkMatch.Groups['value'].Value
}
foreach ($itemName in $designThirstValues.Keys) {
    Assert-True ($drinkValues.ContainsKey($itemName)) "designed thirst item missing from config $itemName"
    Assert-Equal $drinkValues[$itemName] $designThirstValues[$itemName] "thirst value matches design for $itemName"
}
foreach ($itemName in $drinkValues.Keys) {
    Assert-True ($designThirstValues.ContainsKey($itemName)) "thirst config item missing from design $itemName"
}

Write-Output 'FarmerDelight food and thirst data regression test passed'
