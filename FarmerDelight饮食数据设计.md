# FarmerDelight 饮食数据设计

## 审查范围

- 道具来源：`D:\MCStudioDownload\work\qq2951029182@126.com\Cpp\AddOn\FarmerDelight`
- 源码快照：`8337dcdb00e28fbea0fd3f0379faa994a2810372`
- 审查对象：行为包 `netease_items_beh` 中真正启用 `minecraft:food` 的 79 个道具。
- 腐败的番茄只保留了已注释的食物组件，当前是投掷物，不纳入进食数据。
- 腹泻药剂虽然借用食物组件完成饮用，但属于功能药剂，不提供任何营养或补水。

营养设计沿用 Diet 的水果、谷物、蛋白质、蔬菜、糖分五组。配置只决定道具属于哪些营养组；每组实际增长量继续由道具原有饥饿值、饱和品质和营养组数量计算，不篡改 FarmerDelight 的食物属性。

口渴值使用现有 20 点上限量纲。`0` 表示不登记到补水表，而不是额外扣水。每个道具均结合实际配方、形态、份量和功能单独判断，没有按容器或名称批量套值。

## 逐项设计

| 道具 | 名称 | 营养组 | 口渴值 | 逐项依据 |
|---|---|---|---:|---|
| `farmer_delight_nullgr:apple_cider` | 苹果酒 | 水果、糖分 | 5 | 两个苹果和糖制成，源码没有酒精惩罚，按完整瓶装果饮处理。 |
| `farmer_delight_nullgr:apple_pie_slice` | 苹果派切片 | 水果、谷物、糖分 | 0 | 整派以苹果、小麦、糖和派皮制成，切片继承三类主要成分。 |
| `farmer_delight_nullgr:bacon` | 生培根 | 蛋白质 | 0 | 由生猪肉切分，属于单一生肉原料。 |
| `farmer_delight_nullgr:bacon_and_eggs` | 培根鸡蛋 | 蛋白质 | 0 | 主要成分只有熟培根和煎蛋，碗不计营养。 |
| `farmer_delight_nullgr:bacon_sandwich` | 培根三明治 | 谷物、蛋白质、蔬菜 | 0 | 面包、熟培根、卷心菜叶和番茄共同构成完整三明治。 |
| `farmer_delight_nullgr:baked_cod_stew` | 烘焙鳕鱼炖 | 蛋白质、蔬菜 | 3 | 鳕鱼、鸡蛋、番茄和马铃薯组成浓炖物，补水低于清汤。 |
| `farmer_delight_nullgr:barbecue_stick` | 烧烤串 | 蛋白质、蔬菜 | 0 | 牛肉、鸡肉、洋葱和番茄同串，木棍不计营养。 |
| `farmer_delight_nullgr:beef_patty` | 牛肉饼 | 蛋白质 | 0 | 由熟牛肉切分，仍是单一肉类。 |
| `farmer_delight_nullgr:beef_stew` | 牛肉炖 | 蛋白质、蔬菜 | 3 | 牛肉馅、胡萝卜和马铃薯组成浓炖物。 |
| `farmer_delight_nullgr:bone_broth` | 大骨汤 | 蛋白质、蔬菜 | 4 | 骨头和红蘑菇熬成清汤，液体比例高于炖菜。 |
| `farmer_delight_nullgr:cabbage` | 卷心菜 | 蔬菜 | 0 | 完整叶菜原料。 |
| `farmer_delight_nullgr:cabbage_leaf` | 卷心菜叶 | 蔬菜 | 0 | 卷心菜切分后的叶菜份量。 |
| `farmer_delight_nullgr:cabbage_rolls` | 菜叶卷 | 蛋白质、蔬菜 | 0 | 卷心菜叶、洋葱和煎蛋制成，不含谷物外皮。 |
| `farmer_delight_nullgr:cake_slice` | 蛋糕切片 | 谷物、糖分 | 0 | 由原版蛋糕切分，保持原版蛋糕的谷物和糖分分类。 |
| `farmer_delight_nullgr:cathartic_bottle` | 腹泻药剂 | 无 | 0 | 配方和代码均把它定位为清除状态并重置饥饿的药剂，不作为食物或饮水。 |
| `farmer_delight_nullgr:chicken_cuts` | 生鸡肉丁 | 蛋白质 | 0 | 由生鸡肉切分。 |
| `farmer_delight_nullgr:chicken_sandwich` | 鸡肉三明治 | 谷物、蛋白质、蔬菜 | 0 | 面包、熟鸡肉、卷心菜叶和胡萝卜组成。 |
| `farmer_delight_nullgr:chicken_soup` | 鸡肉汤 | 蛋白质、蔬菜 | 4 | 鸡肉、胡萝卜、叶菜和洋葱熬成汤，液体占比高。 |
| `farmer_delight_nullgr:chocolate_pie_slice` | 巧克力派切片 | 谷物、蛋白质、糖分 | 0 | 巧克力派使用派皮、三份牛奶、可可和糖，奶制馅料是主要部分。 |
| `farmer_delight_nullgr:cod_roll` | 鳕鱼寿司 | 谷物、蛋白质 | 0 | 鳕鱼片与米饭组合。 |
| `farmer_delight_nullgr:cod_slice` | 生鳕鱼片 | 蛋白质 | 0 | 由生鳕鱼切分。 |
| `farmer_delight_nullgr:cooked_bacon` | 熟培根 | 蛋白质 | 0 | 生培根或熟猪肉加工后的肉类。 |
| `farmer_delight_nullgr:cooked_chicken_cuts` | 熟鸡肉丁 | 蛋白质 | 0 | 熟鸡肉切分后的肉类。 |
| `farmer_delight_nullgr:cooked_cod_slice` | 熟鳕鱼片 | 蛋白质 | 0 | 熟鳕鱼切分后的鱼肉。 |
| `farmer_delight_nullgr:cooked_mutton_chops` | 熟羊排 | 蛋白质 | 0 | 熟羊肉切分后的肉类。 |
| `farmer_delight_nullgr:cooked_rice` | 米饭 | 谷物 | 0 | 单一稻米主食；盛装用碗不计营养。 |
| `farmer_delight_nullgr:cooked_salmon_slice` | 熟鲑鱼片 | 蛋白质 | 0 | 熟鲑鱼切分后的鱼肉。 |
| `farmer_delight_nullgr:dumplings` | 饺子 | 谷物、蛋白质、蔬菜 | 0 | 面团或意面、鸡肉、卷心菜和洋葱共同组成。 |
| `farmer_delight_nullgr:egg_sandwich` | 鸡蛋三明治 | 谷物、蛋白质 | 0 | 面包和两份煎蛋组成。 |
| `farmer_delight_nullgr:fish_stew` | 鱼肉炖 | 蛋白质、蔬菜 | 3 | 鱼肉、洋葱和番茄组成浓炖物。 |
| `farmer_delight_nullgr:fried_egg` | 煎鸡蛋 | 蛋白质 | 0 | 单一鸡蛋料理。 |
| `farmer_delight_nullgr:fried_rice` | 炒饭 | 谷物、蛋白质、蔬菜 | 0 | 稻米、鸡蛋、胡萝卜和洋葱共同组成。 |
| `farmer_delight_nullgr:fruit_salad` | 水果沙拉 | 水果、蛋白质、蔬菜、糖分 | 0 | 苹果、西瓜、甜浆果为主体，另含南瓜片和牛奶；甜浆果同时计糖分。 |
| `farmer_delight_nullgr:gleaming_salad` | 碗装发光沙拉 | 水果、蔬菜、糖分 | 0 | 发光浆果、蜂蜜、番茄、金胡萝卜、甜菜根和卷心菜组成。 |
| `farmer_delight_nullgr:glow_berry_custard` | 发光浆果蛋奶沙司 | 水果、蛋白质、糖分 | 3 | 发光浆果、鸡蛋、牛奶和糖组成稠厚蛋奶甜品。 |
| `farmer_delight_nullgr:grilled_salmon` | 香烤鲑鱼 | 水果、蛋白质、蔬菜 | 0 | 鲑鱼、甜浆果、卷心菜叶和洋葱共同装盘。 |
| `farmer_delight_nullgr:ham` | 火腿 | 蛋白质 | 0 | 可继续切成培根的整块肉类。 |
| `farmer_delight_nullgr:hamburger` | 汉堡包 | 谷物、蛋白质、蔬菜 | 0 | 面包、牛肉饼、卷心菜叶、番茄和洋葱组成。 |
| `farmer_delight_nullgr:honey_cookie` | 蜂蜜曲奇 | 谷物、糖分 | 0 | 小麦、蜂蜜、糖和可可制成。 |
| `farmer_delight_nullgr:honey_glazed_ham` | 盘装蜜汁火腿 | 水果、谷物、蛋白质、蔬菜、糖分 | 0 | 装盘配方含火腿、米、甜浆果和洋葱，整份烤制配方另含蜂蜜，覆盖五组且会受多组收益折减。 |
| `farmer_delight_nullgr:hot_cocoa` | 热可可 | 蛋白质、糖分 | 4 | 牛奶、可可和糖制成的稠厚热饮，补水低于果汁和纯奶。 |
| `farmer_delight_nullgr:kelp_roll` | 海带寿司卷 | 谷物、蔬菜 | 0 | 稻米、胡萝卜和海带组成，不含鱼肉。 |
| `farmer_delight_nullgr:kelp_roll_slice` | 海带寿司切片 | 谷物、蔬菜 | 0 | 由海带寿司卷切分，营养组成不变。 |
| `farmer_delight_nullgr:melon_juice` | 西瓜汁 | 水果、糖分 | 5 | 四片西瓜和糖制成完整瓶装果汁。 |
| `farmer_delight_nullgr:melon_popsicle` | 西瓜冰棍 | 水果 | 4 | 西瓜与冰制成，虽为固体但冰制份量能明确补水。 |
| `farmer_delight_nullgr:milk_bottle` | 奶瓶 | 蛋白质 | 6 | 完整瓶装牛奶，补水量低于奶桶、高于普通稠饮。 |
| `farmer_delight_nullgr:minced_beef` | 牛肉馅 | 蛋白质 | 0 | 由生牛肉切分。 |
| `farmer_delight_nullgr:mixed_salad` | 混合沙拉 | 蔬菜、糖分 | 0 | 卷心菜、洋葱、番茄和甜菜根等蔬菜搭配糖制调味。 |
| `farmer_delight_nullgr:mushroom_rice` | 蘑菇饭 | 谷物、蔬菜 | 0 | 稻米、红蘑菇、棕蘑菇和胡萝卜组成。 |
| `farmer_delight_nullgr:mutton_chops` | 生羊排 | 蛋白质 | 0 | 由生羊肉切分。 |
| `farmer_delight_nullgr:mutton_wrap` | 羊肉卷 | 谷物、蛋白质、蔬菜 | 0 | 面包、熟羊肉、卷心菜叶和洋葱组成。 |
| `farmer_delight_nullgr:nether_salad` | 下界沙拉 | 蔬菜 | 0 | 绯红菌和诡异菌组成，沿用菌类蔬菜分类。 |
| `farmer_delight_nullgr:noodle_soup` | 面条汤 | 谷物、蛋白质、蔬菜 | 4 | 意面、鸡蛋、培根和干海带组成有汤面的完整一碗。 |
| `farmer_delight_nullgr:onion` | 洋葱 | 蔬菜 | 0 | 单一根茎蔬菜。 |
| `farmer_delight_nullgr:onion_soup` | 洋葱汤 | 谷物、蛋白质、蔬菜 | 3 | 两份洋葱、面包和牛奶组成偏稠的奶香汤。 |
| `farmer_delight_nullgr:pasta_with_meatballs` | 肉丸意面 | 谷物、蛋白质、蔬菜 | 0 | 意面、牛肉、番茄和洋葱组成。 |
| `farmer_delight_nullgr:pasta_with_mutton_chop` | 羊排意面 | 谷物、蛋白质、蔬菜 | 0 | 意面、羊肉、番茄和洋葱组成。 |
| `farmer_delight_nullgr:pie_crust` | 馅饼酥皮 | 谷物、蛋白质 | 0 | 三份小麦和一瓶牛奶组成，尚未加入甜味馅料。 |
| `farmer_delight_nullgr:pumpkin_slice` | 南瓜片 | 蔬菜 | 0 | 南瓜切分后的蔬菜份量。 |
| `farmer_delight_nullgr:pumpkin_soup` | 南瓜汤 | 蛋白质、蔬菜 | 3 | 南瓜、培根、卷心菜和鸡蛋组成的浓汤。 |
| `farmer_delight_nullgr:ratatouille` | 蔬菜杂烩 | 蔬菜 | 0 | 胡萝卜、甜菜根、卷心菜、洋葱和番茄组成纯蔬菜杂烩。 |
| `farmer_delight_nullgr:raw_pasta` | 生意面 | 谷物 | 0 | 主配方和面团切制路线均以小麦为主体；鸡蛋仅是可选替代配方。 |
| `farmer_delight_nullgr:roast_chicken` | 盘装烤鸡 | 蛋白质、蔬菜、糖分 | 0 | 烤鸡整份配方含鸡肉、洋葱、胡萝卜和糖。 |
| `farmer_delight_nullgr:roasted_mutton_chops` | 烤羊排 | 谷物、蛋白质、蔬菜 | 0 | 熟羊排、稻米、甜菜根和番茄共同装盘。 |
| `farmer_delight_nullgr:salmon_roll` | 鲑鱼寿司 | 谷物、蛋白质 | 0 | 鲑鱼片与米饭组合。 |
| `farmer_delight_nullgr:salmon_slice` | 生鲑鱼片 | 蛋白质 | 0 | 由生鲑鱼切分。 |
| `farmer_delight_nullgr:shepherds_pie_item` | 盘装牧羊人派 | 蛋白质、蔬菜 | 0 | 整派以羊排、烤马铃薯、洋葱和牛奶制成，不含谷物派皮。 |
| `farmer_delight_nullgr:smoked_ham` | 烟熏火腿 | 蛋白质 | 0 | 火腿烟熏后的肉类成品。 |
| `farmer_delight_nullgr:squid_ink_pasta` | 鱿鱼墨面 | 谷物、蛋白质、蔬菜 | 0 | 意面、鱼肉、墨囊、洋葱和番茄组成。 |
| `farmer_delight_nullgr:steak_and_potatoes` | 牛排土豆盖饭 | 谷物、蛋白质、蔬菜 | 0 | 米饭、牛排、烤马铃薯和洋葱组成。 |
| `farmer_delight_nullgr:stuffed_potato` | 填馅马铃薯 | 蛋白质、蔬菜 | 0 | 烤马铃薯、牛肉饼、胡萝卜和牛奶组成。 |
| `farmer_delight_nullgr:stuffed_pumpkin` | 碗装填馅南瓜 | 水果、谷物、蛋白质、蔬菜、糖分 | 0 | 道具配方含牛肉与多种蔬菜，整南瓜出餐路线另含米和甜浆果；按全部合法来源登记五组并接受多组折减。 |
| `farmer_delight_nullgr:sweet_berry_cheesecake_slice` | 甜浆果芝士派切片 | 水果、谷物、蛋白质、糖分 | 0 | 整派由大量甜浆果、奶制馅料和派皮组成；甜浆果同时计糖分。 |
| `farmer_delight_nullgr:sweet_berry_cookie` | 甜浆果曲奇 | 水果、谷物、糖分 | 0 | 甜浆果、小麦、糖和可可制成。 |
| `farmer_delight_nullgr:tomato` | 番茄 | 蔬菜 | 0 | 本玩法沿用料理语义，把番茄归入蔬菜。 |
| `farmer_delight_nullgr:tomato_sauce` | 番茄酱 | 蔬菜、糖分 | 0 | 番茄和糖熬制的调味酱，不因液态外观作为饮水。 |
| `farmer_delight_nullgr:vegetable_noodles` | 蔬菜面 | 谷物、蔬菜 | 0 | 意面、胡萝卜、蘑菇、卷心菜和洋葱组成。 |
| `farmer_delight_nullgr:vegetable_soup` | 蔬菜汤 | 蔬菜 | 4 | 马铃薯、胡萝卜、卷心菜、洋葱和甜菜根熬成清汤。 |
| `farmer_delight_nullgr:wheat_dough` | 面团 | 谷物 | 0 | 小麦面团属于未烘焙谷物原料，配方用水不等于成品可饮用。 |

## 口渴值汇总

| 口渴值 | 道具 |
|---:|---|
| 6 | 奶瓶 |
| 5 | 苹果酒、西瓜汁 |
| 4 | 大骨汤、鸡肉汤、热可可、西瓜冰棍、面条汤、蔬菜汤 |
| 3 | 烘焙鳕鱼炖、牛肉炖、鱼肉炖、发光浆果蛋奶沙司、洋葱汤、南瓜汤 |
| 0 | 其余道具不登记到补水表 |
