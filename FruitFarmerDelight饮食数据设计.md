# FruitFarmerDelight 饮食数据设计

## 审查范围

- 数据接入目标：当前 Diet 项目；不修改外部模组的食物属性和配方。
- 道具来源：`D:\MCStudioDownload\work\qq2951029182@126.com\Cpp\AddOn\FruitFarmerDelight`。
- 源码快照：`9939171ed62199c106eb1d0aba248e72d44b0fff`。
- 同时复核的 FarmerDelight 来源仍为 `8337dcdb00e28fbea0fd3f0379faa994a2810372`，其 78 项营养数据和 15 项口渴数据继续使用 `FarmerDelight饮食数据设计.md` 中的既有逐项结论。
- FruitFarmerDelight 行为包共有 430 个道具 JSON，其中有 347 个启用 `minecraft:food` 的道具；这 347 个最终食物 ID 全部显式写入 `fruitFarmerDelightFoodGroups`。
- 配方来源同时覆盖 330 个工作台/熔炉配方、烹饪锅配置、榨汁机配置、整块甜点切片链路、果酒工作台路线和酿酒桶路线，不能只按文件名猜测。

营养组沿用水果、谷物、蛋白质、蔬菜、糖分五组。配置只确定食物属于哪些组；实际增长量仍由食物自身的 `nutrition`、饱和品质和营养组数量计算，不改动外部模组数值。

口渴值沿用 20 点上限量纲。本次登记 143 个确实具有饮品、冰制品、浓流食或炖品形态的道具；未登记表示不额外补水。果酱即使装瓶也属于浓缩食物，水果沙拉、普通水果和固体甜点也不因为含水果而自动补水。

## 逐项审查原则

- 每个最终食物 ID 都独立核对；脚本只用于提取清单、检查漏项和验证配置集合，没有用公式生成营养组或口渴值。
- 同一配方族只有在逐个 JSON 的原料结构相同后才采用相同结论；任何不同路线均单独处理。
- 香蕉果汁另有“香蕉、糖、玻璃瓶”的工作台路线，因此登记水果、糖分；其余榨汁机果汁只使用实际水果，不虚构糖分。
- 所有果酱配方都是两份水果加玻璃瓶，没有糖，所以只登记水果；瓶子也不使果酱成为饮品。
- 所有冰淇淋配方实际只有水果、冰和碗，没有奶和糖，所以只登记水果；冰制份量提供 4 点口渴值。
- 软糖由水果和两份明胶烹制，登记水果、蛋白质，不因“软糖”名称虚构配方中不存在的糖。
- 果酒当前工作台路线含水果、小麦和水瓶，同时支持果浆酿造；营养登记水果、谷物，口渴值按项目既有酒类标准设为 2。
- `fruit_juice_pean`、`forzen_sucker_*`、`send_*_slice` 等拼写是外部模组真实 ID，内置数据原样保留，不能擅自纠正。
- `milkshake_avocado` 启用了食物组件并在进食回收表中返还玻璃瓶，但没有本地化和获取配方。为保证命令获取或后续启用时兼容，按其奶昔数据契约登记水果、蛋白质、糖分和 4 点口渴，并明确标记为休眠占位项。

## 已逐项核对的同构配方族

下表的数量均是最终可食用 ID 数量。每一个 ID 仍在 Python 内置表中逐行列出，回归测试会把 347 个配置 ID 与外部行为包逐项做集合比对。

| 配方族 | 数量 | 营养组 | 口渴值 | 实际配方依据 |
|---|---:|---|---:|---|
| 水果曲奇 `biscuit_*` | 25 | 水果、谷物、蛋白质、糖分 | 0 | 每个变体均由对应水果、两份小麦、两份鸡蛋、牛奶和糖制成。 |
| 水果蛋糕/起司蛋糕切片 | 20 | 水果、谷物、蛋白质、糖分 | 0 | 每个整块甜点均含对应水果、蛋、奶、小麦、面包和糖，再经切片链路得到食物。百香果切片使用独立文件但组成相同。 |
| 水果冰棍 `forzen_sucker_*` | 26 | 水果 | 4 | 每个变体均为对应水果加一块冰和木棍，不含奶、谷物或糖。 |
| 榨汁机果汁 | 25 | 水果；香蕉果汁另含糖分 | 5 | 榨汁机逐种消耗 1 至 3 份对应水果装瓶；香蕉果汁另有显式加糖工作台路线。 |
| 水果冰淇淋 | 26 | 水果 | 4 | 每个变体均为对应水果、冰和碗；源码配方没有奶和糖。 |
| 水果果酱 | 26 | 水果 | 0 | 每个变体均为两份对应水果和玻璃瓶；源码配方没有糖。 |
| 水果软糖 | 23 | 水果、蛋白质 | 0 | 每个变体均由对应水果和两份明胶在烹饪锅制成。 |
| 水果奶昔 | 27 | 水果、蛋白质、糖分 | 4 | 26 个可制作变体均为对应水果、奶瓶和糖；另含一个已说明的牛油果休眠占位项。 |
| 水果慕斯切片 | 3 | 水果、谷物、蛋白质、糖分 | 0 | 蓝莓、芒果、火龙果整块慕斯均含水果、蛋、奶、小麦、面包和糖。 |
| 水果松饼 | 20 | 水果、谷物、蛋白质、糖分 | 0 | 每个变体均含对应水果、两份鸡蛋、两份小麦、糖和派皮。 |
| 水果派切片 `send_*_slice` | 25 | 水果、谷物、蛋白质、糖分 | 0 | 每个整派均含三份对应水果、三瓶奶、派皮和糖，再切成食物。 |
| 水果千层切片 | 2 | 水果、谷物、蛋白质、糖分 | 0 | 榴莲和覆盆子千层均含水果、蛋、奶、小麦、面包和糖。 |
| 水果酒 | 25 | 水果、谷物 | 2 | 工作台路线逐项使用对应水果、两份小麦和水瓶；酿酒桶使用同类水果果浆，不改变成品的果酒定位。 |

## 非同构道具逐项结论

| 道具 | 名称 | 营养组 | 口渴值 | 逐项依据 |
|---|---|---|---:|---|
| `fruitfarmersdelight_nullgr:a_mangosteen` | 山竹果肉 | 水果 | 0 | 山竹拆分出的单份果肉。 |
| `fruitfarmersdelight_nullgr:a_segment_of_orange` | 一瓣橘子 | 水果 | 0 | 橘子拆分出的单瓣果肉。 |
| `fruitfarmersdelight_nullgr:baked_pear` | 烤梨 | 水果 | 0 | 梨直接烘烤，原料类别不变。 |
| `fruitfarmersdelight_nullgr:banana` | 香蕉 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:banana_beef` | 蕉叶包牛肉 | 水果、蛋白质、蔬菜 | 0 | 两份牛肉馅、香蕉、洋葱和番茄组成完整肉菜。 |
| `fruitfarmersdelight_nullgr:banana_egg_roll` | 香蕉蛋卷 | 水果、谷物、蛋白质 | 0 | 香蕉、鸡蛋和小麦制成，配方没有糖。 |
| `fruitfarmersdelight_nullgr:blueberry` | 蓝莓 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:blueberry_yam` | 蓝莓山药 | 水果、蛋白质、蔬菜、糖分 | 0 | 蓝莓、马铃薯、牛奶和糖盛于碗中。 |
| `fruitfarmersdelight_nullgr:braised_pineapple_meat` | 菠萝咕咾肉 | 水果、蛋白质、蔬菜、糖分 | 0 | 菠萝、肉、洋葱和蜂蜜共同烹制。 |
| `fruitfarmersdelight_nullgr:cake_passion_slice` | 百香果蛋糕切片 | 水果、谷物、蛋白质、糖分 | 0 | 百香果整块蛋糕含蛋、奶、小麦、面包和糖；该切片因文件名前缀不同单独列出。 |
| `fruitfarmersdelight_nullgr:cherry` | 车厘子 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:cherry_custard` | 车厘子沙司 | 水果、蛋白质、糖分 | 3 | 车厘子、鸡蛋、奶和糖制成的瓶装稠厚蛋奶品。 |
| `fruitfarmersdelight_nullgr:dried_persimmon` | 柿饼 | 水果 | 0 | 柿子直接干制，没有添加糖。 |
| `fruitfarmersdelight_nullgr:durian_meat` | 榴莲肉 | 水果 | 0 | 榴莲拆分出的果肉。 |
| `fruitfarmersdelight_nullgr:durian_pizza_slice` | 榴莲披萨 | 水果、谷物、蛋白质、糖分 | 0 | 榴莲肉、面团、奶酪和糖制成整块披萨后切片。 |
| `fruitfarmersdelight_nullgr:fruit_juice_pean` | 梨汁 | 水果 | 5 | 榨汁机消耗两只梨装满一瓶，源码 ID 保留 `pean` 拼写。 |
| `fruitfarmersdelight_nullgr:grape` | 葡萄 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:grape_custard` | 葡萄沙司 | 水果、蛋白质、糖分 | 3 | 葡萄、鸡蛋、奶和糖制成的瓶装稠厚蛋奶品。 |
| `fruitfarmersdelight_nullgr:grape_tiramisu` | 葡萄提拉米苏 | 水果、谷物、蛋白质、糖分 | 0 | 葡萄果酱、蜂蜜、奶、糖、鸡蛋和小麦制成三份。 |
| `fruitfarmersdelight_nullgr:half_a_kiwi` | 奇异果切片 | 水果 | 0 | 奇异果切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:half_a_mango` | 芒果片 | 水果 | 0 | 芒果切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:half_a_papaya` | 番木瓜切片 | 水果 | 0 | 番木瓜切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:half_a_passion_fruit` | 百香果切片 | 水果 | 0 | 百香果切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:half_a_pitaya` | 火龙果切片 | 水果 | 0 | 火龙果切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:hami_melon_fire_sb_bowl` | 碗装填馅哈密瓜 | 水果、谷物、蔬菜 | 0 | 哈密瓜盛装链路结合米饭、洋葱和菠萝；木棍与碗不计营养。 |
| `fruitfarmersdelight_nullgr:hami_melon_piece` | 哈密瓜切片 | 水果 | 0 | 哈密瓜切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:haw_sheets` | 果丹皮 | 水果、糖分 | 0 | 三份山楂和糖制成三份果丹皮。 |
| `fruitfarmersdelight_nullgr:hawaiian_pizza_slice` | 山楂披萨 | 水果、谷物、蛋白质、糖分 | 0 | 实际配方是山楂、面团、奶酪和糖；以本地化名称与源码原料为准。 |
| `fruitfarmersdelight_nullgr:hawthorn` | 山楂 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:hawthorn_skewers` | 冰糖葫芦 | 水果、糖分 | 0 | 三份山楂和糖制成两串。 |
| `fruitfarmersdelight_nullgr:honey_peach` | 水蜜桃 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:icecream_blueberry` | 蓝莓冰淇淋 | 水果 | 4 | 蓝莓、冰和碗制成，源码没有奶和糖。 |
| `fruitfarmersdelight_nullgr:icecream_grape` | 葡萄冰淇淋 | 水果 | 4 | 葡萄、冰和碗制成，源码没有奶和糖。 |
| `fruitfarmersdelight_nullgr:icecream_mulberry` | 桑葚冰淇淋 | 水果 | 4 | 桑葚、冰和碗制成，源码没有奶和糖。 |
| `fruitfarmersdelight_nullgr:jellydrops_blueberry` | 蓝莓软糖 | 水果、蛋白质 | 0 | 蓝莓和两份明胶制成，配方没有糖。 |
| `fruitfarmersdelight_nullgr:jellydrops_grape` | 葡萄软糖 | 水果、蛋白质 | 0 | 葡萄和两份明胶制成，配方没有糖。 |
| `fruitfarmersdelight_nullgr:kiwi_fruit` | 奇异果 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:lemon` | 柠檬 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:lemon_chicken_chop` | 柠檬浇汁鸡柳 | 水果、蛋白质、糖分 | 0 | 两份柠檬片、鸡肉、柠檬酒和糖构成浇汁鸡柳，酒只作调味，不把成品当饮品。 |
| `fruitfarmersdelight_nullgr:lemon_slice` | 柠檬片 | 水果 | 0 | 柠檬切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:litchi_chicken` | 盘装荔枝鸡 | 水果、蛋白质、蔬菜、糖分 | 0 | 鸡肉、荔枝、荔枝果酱、洋葱、浆果和糖制成。 |
| `fruitfarmersdelight_nullgr:liulian_stewed_chicken` | 榴莲鸡肉炖 | 水果、蛋白质 | 3 | 榴莲肉、鸡肉和鸡蛋组成一碗浓炖品。 |
| `fruitfarmersdelight_nullgr:longan` | 龙眼 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:loquat` | 枇杷 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:luxurious_fruit_salad` | 豪华水果沙拉 | 水果、蛋白质、糖分 | 0 | 多种水果、牛奶和蜂蜜组成；沙拉不是饮品。 |
| `fruitfarmersdelight_nullgr:lychee` | 荔枝 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:mango` | 芒果 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:mango_cake` | 芒果饼 | 水果、谷物、糖分 | 0 | 芒果、糖和面团烹制，配方没有蛋奶。 |
| `fruitfarmersdelight_nullgr:mango_custard` | 芒果沙司 | 水果、蛋白质、糖分 | 3 | 芒果、鸡蛋、奶和糖制成的瓶装稠厚蛋奶品。 |
| `fruitfarmersdelight_nullgr:mango_milk` | 芒果双皮奶 | 水果、蛋白质、糖分 | 3 | 芒果、奶和糖制成稠厚奶制甜品，低于奶昔的补水量。 |
| `fruitfarmersdelight_nullgr:mangosteen` | 山竹 | 水果 | 0 | 完整水果原料。 |
| `fruitfarmersdelight_nullgr:matcha_strawberry` | 草莓抹茶卷 | 水果、谷物、蛋白质、糖分 | 0 | 草莓、茶叶、奶、糖和面团制成；茶叶是调味，不作为一份蔬菜。 |
| `fruitfarmersdelight_nullgr:milkshake_grape` | 葡萄奶昔 | 水果、蛋白质、糖分 | 4 | 葡萄、奶瓶和糖制成。 |
| `fruitfarmersdelight_nullgr:milkshake_kiwifruit` | 奇异果奶昔 | 水果、蛋白质、糖分 | 4 | 奇异果、奶瓶和糖制成。 |
| `fruitfarmersdelight_nullgr:milkshake_passion_fruit` | 百香果奶昔 | 水果、蛋白质、糖分 | 4 | 百香果、奶瓶和糖制成。 |
| `fruitfarmersdelight_nullgr:mulberry` | 桑葚 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:papaya_milk` | 木瓜双皮奶 | 水果、蛋白质、糖分 | 3 | 木瓜、奶和糖制成稠厚奶制甜品。 |
| `fruitfarmersdelight_nullgr:passion_fruit` | 百香果 | 水果 | 0 | 完整水果原料。 |
| `fruitfarmersdelight_nullgr:passion_fruit_chicken` | 百香果浇汁鸡肉 | 水果、蛋白质、蔬菜 | 0 | 鸡肉、马铃薯、百香果和洋葱组成碗装主菜。 |
| `fruitfarmersdelight_nullgr:passion_fruit_pasta` | 百香果拌面 | 水果、谷物、糖分 | 0 | 百香果、意面和蜂蜜组成，碗不计营养。 |
| `fruitfarmersdelight_nullgr:passion_fruit_trout` | 百香果浇汁鲑鱼 | 水果、蛋白质 | 0 | 三份百香果与熟鲑鱼组成。 |
| `fruitfarmersdelight_nullgr:pawpaw` | 番木瓜 | 水果 | 0 | 完整水果原料。 |
| `fruitfarmersdelight_nullgr:pear` | 梨子 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:persimmon` | 柿子 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:pineapple_drumstick_fort` | 菠萝鸡腿堡 | 水果、谷物、蛋白质、蔬菜 | 0 | 熟鸡肉、菠萝、两份面包和卷心菜叶组成。 |
| `fruitfarmersdelight_nullgr:pineapple_rice` | 菠萝饭 | 水果、谷物、蛋白质、蔬菜 | 0 | 米饭、菠萝、鸡蛋和洋葱组成。 |
| `fruitfarmersdelight_nullgr:pineapple_slice` | 菠萝片 | 水果 | 0 | 菠萝切分后的食用份量。 |
| `fruitfarmersdelight_nullgr:pineapple_strand` | 菠萝串 | 水果 | 0 | 两份菠萝片穿串，配方没有糖。 |
| `fruitfarmersdelight_nullgr:pitaya_dragon_fruit` | 火龙果 | 水果 | 0 | 完整水果原料。 |
| `fruitfarmersdelight_nullgr:raspberry` | 覆盆子 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:roasted_durian` | 烤榴莲肉 | 水果 | 0 | 榴莲肉直接烘烤，原料类别不变。 |
| `fruitfarmersdelight_nullgr:shaddock_slice` | 西柚果肉 | 水果 | 0 | 西柚拆分出的食用份量。 |
| `fruitfarmersdelight_nullgr:steamed_eggs_with_oranges` | 橘子蒸蛋 | 水果、蛋白质、糖分 | 0 | 鸡蛋、蜂蜜和橘子制成。 |
| `fruitfarmersdelight_nullgr:stewed_beef_with_hawthorn` | 山楂牛肉炖 | 水果、蛋白质、蔬菜 | 3 | 牛肉馅、甜菜根、番茄、山楂和洋葱组成浓炖品。 |
| `fruitfarmersdelight_nullgr:stewed_beef_with_red_wine` | 红酒炖牛肉 | 水果、谷物、蛋白质、蔬菜 | 3 | 牛肉、马铃薯、洋葱和整瓶葡萄酒组成；葡萄酒的有效路线含水果和小麦。 |
| `fruitfarmersdelight_nullgr:stewed_pear_with_apple` | 苹果炖梨 | 水果、蛋白质、糖分 | 3 | 梨、另一种水果、奶和糖组成稠厚甜炖品。 |
| `fruitfarmersdelight_nullgr:stewed_pear_with_loquat` | 龙眼雪梨炖 | 水果、蛋白质、糖分 | 3 | 梨、龙眼、奶和糖组成稠厚甜炖品。 |
| `fruitfarmersdelight_nullgr:strawberry` | 草莓 | 水果 | 0 | 单一水果原料。 |
| `fruitfarmersdelight_nullgr:strawberry_boo` | 草莓爆珠 | 水果、蛋白质、蔬菜 | 3 | 草莓、奶和马铃薯制成碗装稠食，源码配方没有糖。 |
| `fruitfarmersdelight_nullgr:strawberry_custard` | 草莓沙司 | 水果、蛋白质、糖分 | 3 | 草莓、鸡蛋、奶和糖制成的瓶装稠厚蛋奶品。 |
| `fruitfarmersdelight_nullgr:strawberry_egg_tart` | 草莓蛋挞 | 水果、谷物、蛋白质 | 0 | 草莓、鸡蛋和奶烹制后用派皮取出；源码配方没有糖。 |
| `fruitfarmersdelight_nullgr:tangerine` | 橘子 | 水果 | 0 | 完整水果原料。 |
| `fruitfarmersdelight_nullgr:tangerine_custard` | 橘子沙司 | 水果、蛋白质、糖分 | 3 | 橘子、鸡蛋、奶和糖制成的瓶装稠厚蛋奶品。 |
| `fruitfarmersdelight_nullgr:three_colour_custard` | 三彩沙司 | 水果、蛋白质、糖分 | 3 | 橘子、樱桃、山竹果肉、奶、鸡蛋和糖制成。 |

## 口渴值汇总

| 口渴值 | 数量 | 设计对象 |
|---:|---:|---|
| 5 | 25 | 全部瓶装果汁。 |
| 4 | 79 | 26 个冰棍、26 个冰淇淋、27 个奶昔。 |
| 3 | 14 | 6 个蛋奶沙司、2 个双皮奶、5 个浓炖品和 1 个草莓爆珠。 |
| 2 | 25 | 全部果酒，沿用项目现有酒类低补水标准。 |
| 0 | 204 | 其余固体水果、甜点、果酱和正餐不登记到补水表。 |

总计 347 个营养映射、143 个口渴映射。`tests/fruit_farmer_delight_food_data_test.ps1` 校验内置表数量、营养组顺序、关键差异项、口渴分布，并在同级外部源码存在时逐 ID 比对全部启用食物。
