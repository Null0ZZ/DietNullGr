$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$dietConfigPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\config.py'
$dietLogicPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\Diet.py'
$dietUiLogicPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\DietUI.py'
$dietUiPath = Join-Path $projectRoot 'resource_pack_qewqRv3q\ui\diet_screen.json'

function Assert-Match($text, $pattern, $message) {
    if ($text -notmatch $pattern) {
        throw "Assertion failed: $message"
    }
}

$dietConfigText = Get-Content -LiteralPath $dietConfigPath -Raw -Encoding UTF8
$dietLogicText = Get-Content -LiteralPath $dietLogicPath -Raw -Encoding UTF8
$dietUiLogicText = Get-Content -LiteralPath $dietUiLogicPath -Raw -Encoding UTF8
$dietUiText = Get-Content -LiteralPath $dietUiPath -Raw -Encoding UTF8

# 五类颜色按配置块逐项锁定，同时检查服务端确实把该配置字段写入客户端同步数据。
$expectedColors = [ordered]@{ fruits = @(238, 102, 119); grains = @(204, 187, 68); proteins = @(68, 119, 170); vegetables = @(34, 136, 51); sugars = @(170, 51, 119) }
foreach ($groupId in $expectedColors.Keys) {
    $color = $expectedColors[$groupId]
    $pattern = '(?s)"' + [Regex]::Escape($groupId) + '"\s*:\s*\{[^}]*"color"\s*:\s*\[\s*' + $color[0] + '\s*,\s*' + $color[1] + '\s*,\s*' + $color[2] + '\s*\]'
    Assert-Match $dietConfigText $pattern "$groupId palette color"
}
Assert-Match $dietConfigText 'groupOrder\s*=\s*\["fruits", "grains", "proteins", "vegetables", "sugars"\]' 'nutrition group order stays unchanged'
Assert-Match $dietLogicText "'color':\s*groupConfig\['color'\]" 'server client-data color source'

# 名称和营养条必须继续复用同一个颜色转换函数，关闭追踪时仍分别使用既有灰色。
Assert-Match $dietUiLogicText '(?ms)^    def getGroupDisplayColor\(self, index\):.*?^        color = self\.getGroupData\(index\)\[''color''\].*?^        return \(color\[0\] / 255\.0, color\[1\] / 255\.0, color\[2\] / 255\.0\)' 'shared 0-255 to 0-1 color conversion'
Assert-Match $dietUiLogicText '(?ms)^    def bindRowNameColor\(self, index\):.*?^        return self\.getGroupDisplayColor\(index\)' 'nutrition names use the palette'
Assert-Match $dietUiLogicText '(?ms)^    def bindRowBarColor\(self, index\):.*?^        return self\.getGroupDisplayColor\(index\)' 'nutrition bars use the palette'
Assert-Match $dietUiLogicText '(?ms)^    def bindRowNameColor\(self, index\):.*?^            return \(0\.48, 0\.48, 0\.48\)' 'disabled nutrition name gray stays unchanged'
Assert-Match $dietUiLogicText '(?ms)^    def bindRowBarColor\(self, index\):.*?^            return \(0\.22, 0\.22, 0\.22\)' 'disabled nutrition bar gray stays unchanged'
Assert-Match $dietUiText '"color"\s*:\s*"#diet_screen\.row_name_color"' 'nutrition name JSON color binding'
Assert-Match $dietUiText '"color"\s*:\s*"#diet_screen\.row_bar_color"' 'nutrition bar JSON color binding'

# 百分比告警和疾病高低描边是独立视觉层，本任务不得跟随营养分类色变化。
Assert-Match $dietConfigText 'percentColorHealthy\s*=\s*\(0\.96, 0\.96, 0\.96\)' 'healthy percentage color stays unchanged'
Assert-Match $dietConfigText 'percentColorCaution\s*=\s*\(1\.0, 0\.92, 0\.18\)' 'caution percentage color stays unchanged'
Assert-Match $dietConfigText 'percentColorWarning\s*=\s*\(1\.0, 0\.55, 0\.08\)' 'warning percentage color stays unchanged'
Assert-Match $dietConfigText 'percentColorDanger\s*=\s*\(1\.0, 0\.16, 0\.12\)' 'danger percentage color stays unchanged'
Assert-Match $dietConfigText 'diseaseHighOutlineColor\s*=\s*\(1\.0, 0\.2509803921568627, 0\.1019607843137255\)' 'high disease outline stays #ff401a'
Assert-Match $dietConfigText 'diseaseLowOutlineColor\s*=\s*\(0\.3058823529411765, 0\.9098039215686274, 1\.0\)' 'low disease outline stays #4ee8ff'
Assert-Match $dietUiText '"color"\s*:\s*"#diet_screen\.row_bar_outline_color"' 'disease outline JSON color binding'

Write-Output 'Nutrition palette regression test passed'
