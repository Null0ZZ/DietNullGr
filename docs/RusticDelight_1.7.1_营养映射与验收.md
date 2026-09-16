# RusticDelight 1.7.1 联动更新

基准：Java `05f12ae`。保留共享和隐藏兼容食品约定，覆盖 97 种 Rustic 专属食品（含 42 种上一轮新品）及 6 个隐藏兼容条目。

放置煎饼的 `RusticDelightFoodConsumed` 复用原生进食结算。奶咖啡通过 `GetFoodCureProtectedEffects` 排除当前营养奖惩、疾病及疾病派生状态；营养算法、最低收益、连续食物衰减、疾病配置不变。

南瓜咖啡、樱花咖啡、鱿鱼汤各补水 4 点。普通咖啡、黑咖啡、食用油明确不分配营养；生咖啡豆不再是食品。可选肉馅不改变所有酿椒的固定分类。

## 食品映射

| 物品 ID | 营养类别 |
| --- | --- |
| `rusticdelight_nullgr:baked_potato_slices` | 蔬菜 |
| `rusticdelight_nullgr:batter` | 主食、蛋白质 |
| `rusticdelight_nullgr:bell_pepper_black` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_blue` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_green` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_orange` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_pasta` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_pink` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_purple` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_red` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_black` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_blue` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_green` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_orange` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_pink` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_purple` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_red` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_white` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_roll_yellow` | 主食、蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_black` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_blue` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_green` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_orange` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_pink` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_purple` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_red` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_white` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_slice_yellow` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_soup` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_white` | 蔬菜 |
| `rusticdelight_nullgr:bell_pepper_yellow` | 蔬菜 |
| `rusticdelight_nullgr:calamari` | 蛋白质 |
| `rusticdelight_nullgr:calamari_roll` | 主食、蛋白质 |
| `rusticdelight_nullgr:calamari_slice` | 蛋白质 |
| `rusticdelight_nullgr:calamari_soup` | 蛋白质、蔬菜 |
| `rusticdelight_nullgr:cherry_blossom_cheesecake_slic` | 主食、蛋白质、糖分 |
| `rusticdelight_nullgr:cherry_blossom_coffee` | 蛋白质 |
| `rusticdelight_nullgr:cherry_blossom_cookie` | 主食 |
| `rusticdelight_nullgr:cherry_blossom_pancake` | 主食、蛋白质 |
| `rusticdelight_nullgr:cherry_blossom_roll` | 主食 |
| `rusticdelight_nullgr:chocolate_coffee` | 蛋白质、糖分 |
| `rusticdelight_nullgr:chocolate_pancake` | 主食、蛋白质、糖分 |
| `rusticdelight_nullgr:coffee` | 无 |
| `rusticdelight_nullgr:coffee_braised_beef` | 蛋白质、蔬菜 |
| `rusticdelight_nullgr:coffee_cheesecake_slice` | 主食、蛋白质、糖分 |
| `rusticdelight_nullgr:coffee_cookie` | 主食 |
| `rusticdelight_nullgr:coffee_pancake` | 主食、蛋白质 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_black` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_blue` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_green` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_orange` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_pink` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_purple` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_red` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_white` | 蔬菜 |
| `rusticdelight_nullgr:cook_bell_pepper_slice_yellow` | 蔬菜 |
| `rusticdelight_nullgr:cooked_calamari` | 蛋白质 |
| `rusticdelight_nullgr:cooked_calamari_slice` | 蛋白质 |
| `rusticdelight_nullgr:cooking_oil` | 无 |
| `rusticdelight_nullgr:dark_coffee` | 无 |
| `rusticdelight_nullgr:fried_calamari` | 主食、蛋白质、蔬菜 |
| `rusticdelight_nullgr:fried_chicken` | 主食、蛋白质、蔬菜 |
| `rusticdelight_nullgr:fried_dough` | 主食 |
| `rusticdelight_nullgr:fried_dumplings` | 主食、蛋白质、蔬菜 |
| `rusticdelight_nullgr:fried_fish` | 主食、蛋白质 |
| `rusticdelight_nullgr:fried_mushrooms` | 蔬菜 |
| `rusticdelight_nullgr:fruit_beignet` | 水果、主食、糖分 |
| `rusticdelight_nullgr:golden_coffee_beans` | 蔬菜 |
| `rusticdelight_nullgr:honey_coffee` | 蛋白质、糖分 |
| `rusticdelight_nullgr:honey_pancake` | 主食、蛋白质、糖分 |
| `rusticdelight_nullgr:milk_coffee` | 蛋白质 |
| `rusticdelight_nullgr:pancake` | 主食、蛋白质、糖分 |
| `rusticdelight_nullgr:potato_salad` | 蛋白质、蔬菜 |
| `rusticdelight_nullgr:potato_slices` | 蔬菜 |
| `rusticdelight_nullgr:pumpkin_coffee` | 蛋白质、蔬菜 |
| `rusticdelight_nullgr:pumpkin_pancake` | 主食、蛋白质、蔬菜、糖分 |
| `rusticdelight_nullgr:roasted_bell_pepper_black` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_blue` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_green` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_orange` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_pink` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_purple` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_red` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_white` | 蔬菜 |
| `rusticdelight_nullgr:roasted_bell_pepper_yellow` | 蔬菜 |
| `rusticdelight_nullgr:roasted_coffee_beans` | 蔬菜 |
| `rusticdelight_nullgr:spring_rolls` | 主食、蛋白质、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_black` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_blue` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_green` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_orange` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_pink` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_purple` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_red` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_white` | 主食、蔬菜 |
| `rusticdelight_nullgr:stuffed_bell_pepper_yellow` | 主食、蔬菜 |
| `rusticdelight_nullgr:sweet_salad` | 水果、蔬菜、糖分 |
| `rusticdelight_nullgr:syrup` | 糖分 |
| `rusticdelight_nullgr:syrup_cheesecake_slice` | 主食、蛋白质、糖分 |
| `rusticdelight_nullgr:syrup_coffee` | 蛋白质、糖分 |
| `rusticdelight_nullgr:syrup_cookie` | 主食、糖分 |
| `rusticdelight_nullgr:syrup_sandwich` | 主食、糖分 |
| `rusticdelight_nullgr:vegetable_pancake` | 主食、蛋白质、蔬菜 |

## 验收记录

- `py -3 -B tools/verify_rustic_171.py`：97 种食品、42 种新品、3 个补水条目覆盖通过；其他模组及共享分类、收益/疾病代码不变；无新增运行时导入。
- MCDK 专用测试世界：放置咖啡煎饼和原生鼠标长按食用单张，均使主食、蛋白质从 50% 增至 53.5%；旧阶段重复事件不增加营养。
- MCDK 真实口渴系统：三个新品分别从 10 补至 14。
- 调低营养触发保护条件后，巧克力咖啡清除中毒，保留虚弱、缓慢；随后仍施加咖啡自身效果。
- 重进保存及与成就、杯垫联动的整体检查记录在 Rustic 主项目交付文档。
