$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$buttonUiPath = Join-Path $projectRoot 'resource_pack_qewqRv3q\ui\diet_button.json'
$dietUiPath = Join-Path $projectRoot 'resource_pack_qewqRv3q\ui\diet_screen.json'
$thirstUiPath = Join-Path $projectRoot 'resource_pack_qewqRv3q\ui\thirst_hud.json'
$buttonLogicPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\DietButtonUI.py'
$dietLogicPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\DietUI.py'
$dietDataPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Diet\Diet.py'
$thirstConfigPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\config.py'
$thirstDataPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst.py'
$thirstServerPath = Join-Path $projectRoot 'behavior_pack_XFwwevzL\Diet_NullGr\ModSys\Thirst\Thirst_ss.py'
$textureDir = Join-Path $projectRoot 'resource_pack_qewqRv3q\textures\ui\thirst_nullgr'

function Assert-True($condition, $message) {
    if (-not $condition) {
        throw "Assertion failed: $message"
    }
}

function Assert-Match($text, $pattern, $message) {
    if ($text -notmatch $pattern) {
        throw "Assertion failed: $message"
    }
}

$buttonUiText = Get-Content -LiteralPath $buttonUiPath -Raw -Encoding UTF8
$buttonUi = $buttonUiText | ConvertFrom-Json
$dietUiText = Get-Content -LiteralPath $dietUiPath -Raw -Encoding UTF8
$dietUi = $dietUiText | ConvertFrom-Json
$thirstUiText = Get-Content -LiteralPath $thirstUiPath -Raw -Encoding UTF8
$thirstUi = $thirstUiText | ConvertFrom-Json
$buttonLogicText = Get-Content -LiteralPath $buttonLogicPath -Raw -Encoding UTF8
$dietLogicText = Get-Content -LiteralPath $dietLogicPath -Raw -Encoding UTF8
$dietDataText = Get-Content -LiteralPath $dietDataPath -Raw -Encoding UTF8
$thirstConfigText = Get-Content -LiteralPath $thirstConfigPath -Raw -Encoding UTF8
$thirstDataText = Get-Content -LiteralPath $thirstDataPath -Raw -Encoding UTF8
$thirstServerText = Get-Content -LiteralPath $thirstServerPath -Raw -Encoding UTF8

# 新版按钮位于 screen 根节点，逻辑必须继续绑定同一实际路径并注册完整触摸链路。
Assert-True ($buttonUi.main.controls[0].PSObject.Properties.Name -contains 'open_button@common.button') 'redesigned open button exists'
Assert-Match $buttonUiText '"is_handle_button_move_event"\s*:\s*true' 'open button move events enabled'
Assert-Match $buttonLogicText "GetBaseUIControl\('/open_button'\)" 'open button control path'
Assert-Match $buttonLogicText 'SetButtonTouchDownCallback[\s\S]*SetButtonTouchMoveCallback[\s\S]*SetButtonTouchUpCallback[\s\S]*SetButtonTouchCancelCallback' 'open button touch callbacks'
Assert-Match $buttonLogicText 'buttonLayoutVersionKey[\s\S]*buttonLayoutVersion' 'open button position layout migration'

# 主界面暂时保持普通 screen，避免重新引入 common.base_screen 后阻断 UI 编辑器编辑。
Assert-True ($dietUi.main.type -eq 'screen') 'diet main is a plain screen'
Assert-True ($dietUiText -notmatch '"main@common\.base_screen"') 'diet main does not inherit base screen'
Assert-True ($null -ne $dietUi.main.controls[0].netease_editor_root_panel_base_screen0) 'editable root panel remains in main tree'

# 关闭按钮沿用编辑器生成的 common.button 外观，只恢复原有绑定事件；底部效果标签删除后不再生成或同步专用文本。
Assert-Match $dietUiText '"button@common\.button"' 'redesigned close button exists'
Assert-Match $dietUiText '"to_button_id"\s*:\s*"#diet_screen\.close"' 'redesigned close button mapping'
Assert-Match $dietLogicText 'BF_ButtonClickUp,\s*"#diet_screen\.close"[\s\S]*clientApi\.PopScreen\(\)' 'close button binding'
Assert-True ($dietUiText -notmatch '#diet_screen\.effects') 'removed effects label binding'
Assert-True ($dietLogicText -notmatch 'effectsText|bindEffectsText|#diet_screen\.effects') 'removed effects UI logic'
Assert-True ($dietDataText -notmatch 'effectsText|buildEffectsText') 'removed effects text sync data'

# 两种外观复用同一套状态绑定，只切换贴图容器，避免切换样式时改变口渴数值与闪烁逻辑。
Assert-True ($thirstUi.thirst_slot.controls[0].PSObject.Properties.Name -contains 'water_drop@thirst_hud.thirst_icon_style') 'water drop style control'
Assert-True ($thirstUi.thirst_slot.controls[1].PSObject.Properties.Name -contains 'square@thirst_hud.thirst_icon_style') 'square style control'
Assert-Match $thirstUiText '#thirst_hud\.water_drop_style_visible' 'water drop style binding'
Assert-Match $thirstUiText '#thirst_hud\.square_style_visible' 'square style binding'
Assert-Match $thirstUiText 'textures/ui/thirst_nullgr/thirst_square_full' 'square full texture path'

Add-Type -AssemblyName System.Drawing
$textureNames = @(
    'thirst_square_background.png',
    'thirst_square_blink.png',
    'thirst_square_flash_full.png',
    'thirst_square_flash_half.png',
    'thirst_square_full.png',
    'thirst_square_half.png'
)
foreach ($textureName in $textureNames) {
    $texturePath = Join-Path $textureDir $textureName
    Assert-True (Test-Path -LiteralPath $texturePath) "texture exists: $textureName"
    $image = [System.Drawing.Bitmap]::new($texturePath)
    Assert-True ($image.Width -eq 9 -and $image.Height -eq 9) "texture size: $textureName"
    Assert-True ($image.GetPixel(0, 0).A -eq 0) "texture transparent margin: $textureName"
    Assert-True ($image.GetPixel(1, 1).A -eq 255) "texture visible square border: $textureName"
    $image.Dispose()
}

# 样式选择由服务端持久化并同时同步 HUD 与通用设置，重进世界后仍保留玩家选择。
Assert-Match $thirstConfigText 'settingStyleKey\s*=\s*"thirst_style"' 'style setting key'
Assert-Match $thirstConfigText 'styleOptions\s*=\s*\[styleWaterDrop,\s*styleSquare\]' 'style dropdown options'
Assert-Match $thirstDataText "SetAttr\(config\.attrStyle,\s*data\['style'\]" 'style persistence'
Assert-Match $thirstDataText "'style':\s*data\['style'\]" 'style HUD sync data'
Assert-Match $thirstServerText "settingKey\s*!=\s*config\.settingStyleKey[\s\S]*data\['style'\]\s*=\s*value[\s\S]*_saveAndSync\(playerId,\s*True,\s*True\)" 'style setting update transaction'

Write-Output 'UI integration and thirst style regression test passed'
