$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$clientPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\Diet_main_cs.py'
$configPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'

$script:failures = @()

function Assert-Regex($text, $pattern, $message) {
    if ($text -notmatch $pattern) {
        $script:failures += $message
    }
}

function Assert-NotRegex($text, $pattern, $message) {
    if ($text -match $pattern) {
        $script:failures += $message
    }
}

$clientText = Get-Content -LiteralPath $clientPath -Raw -Encoding UTF8
$configText = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8

# 饮品配置合并不能复用口渴初始值变量名，否则模块加载后会把 20 覆盖成某个饮品补水量。

Assert-Regex $configText 'defaultValue\s*=\s*20\.0' '口渴初始值必须保持为 20.0'
Assert-Regex $configText 'for\s+itemName,\s*drinkDefaultValue\s+in\s+foodDrinkDefaultValues\.items\(\):' '饮品合并必须使用独立的循环变量'
Assert-Regex $configText '"defaultValue"\s*:\s*drinkDefaultValue' '饮品条目必须引用独立的补水量变量'
Assert-NotRegex $configText 'for\s+itemName,\s*defaultValue\s+in\s+foodDrinkDefaultValues\.items\(\):' '饮品合并不能覆盖口渴初始值'

# 通用设置下拉框回传的是选项索引，发送服务端前必须映射为配置中的样式字符串。

Assert-Regex $clientText 'CreateDietSettingCallback\(settingDef\)' '设置回调必须绑定完整设置定义'
Assert-Regex $clientText 'def\s+CreateDietSettingCallback\(self,\s*settingDef\):' '设置回调必须接收完整设置定义'
Assert-Regex $clientText 'settingKey\s*=\s*settingDef\[''key''\]' '设置回调必须从设置定义读取 key'
Assert-Regex $clientText 'if\s+settingDef\[''control''\]\s*==\s*config\.controlDropDown:[\s\S]*value\s*=\s*settingDef\[''options''\]\[int\(value\)\]' '下拉框索引必须映射为选项值'
Assert-Regex $clientText 'NotifyDietSettingChanged\(settingKey,\s*value\)' '映射后的设置值必须发送到服务端'

if ($script:failures.Count -gt 0) {
    throw "Assertion failed:`n- $($script:failures -join "`n- ")"
}

Write-Output 'Thirst initialization and style regression test passed'
