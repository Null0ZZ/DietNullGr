$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path $PSScriptRoot -Parent
$uiPath = Join-Path $projectRoot 'resource_pack_qewqRv3q\ui\thirst_hud.json'
$ui = Get-Content -Raw $uiPath | ConvertFrom-Json

function Assert-Equal($actual, $expected, $message) {
    if ($actual -ne $expected) {
        throw "${message}: expected $expected, actual $actual"
    }
}

# 原版状态图标宽 9px、步进 8px，10 格的最终可见宽度为 81px。
Assert-Equal $ui.thirst_slot.size[0] 8 'slot step width'
Assert-Equal $ui.thirst_bar.size[0] 81 'visible bar width'
Assert-Equal $ui.thirst_bar.controls[0].slots.size[0] 80 'grid width'

$expectedLayouts = @(
    @('desktop_classic', '#hud_visible_centered', 49.5, -45, 'bottom_middle', 'bottom_middle'),
    @('desktop_touch', '#hud_visible_centered_touch', 59.5, -45, 'bottom_middle', 'bottom_middle'),
    @('pocket', '#hud_visible_not_centered', -2, 12, 'top_right', 'top_right')
)

for ($index = 0; $index -lt $expectedLayouts.Count; $index++) {
    $expected = $expectedLayouts[$index]
    $layoutName = $expected[0]
    $layout = $ui.root.controls[$index].$layoutName
    $survival = $layout.controls[0].survival
    $bar = $survival.controls[0].'bar@thirst_hud.thirst_bar'

    Assert-Equal $layout.bindings[0].binding_name $expected[1] "${layoutName} visibility binding"
    Assert-Equal $layout.bindings[0].binding_type 'global' "${layoutName} binding type"
    Assert-Equal $survival.bindings[0].binding_name '#show_survival_ui' "${layoutName} survival binding"
    Assert-Equal $bar.offset[0] $expected[2] "${layoutName} offset x"
    Assert-Equal $bar.offset[1] $expected[3] "${layoutName} offset y"
    Assert-Equal $bar.anchor_from $expected[4] "${layoutName} anchor from"
    Assert-Equal $bar.anchor_to $expected[5] "${layoutName} anchor to"
}

Write-Output 'Thirst HUD layout regression test passed'
