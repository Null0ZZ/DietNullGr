# -*- coding: utf-8 -*-
"""桌面离线检查：乡村乐事食品映射、补水与既有计算边界。"""
import ast
import json
from pathlib import Path
import runpy
import subprocess
import sys

repo = Path(__file__).resolve().parents[1]
rustic = repo.parent / 'd8753542db664be7a6ae72cf84cfeccc'
behavior = repo / 'behavior_pack_XFwwevzL'
sys.path.insert(0, str(behavior))
base = '3e99a10297203293d2a2b09c05c39149f443f8cc'
dietPath = 'behavior_pack_XFwwevzL/Diet_NullGr/ModSys/Diet/config.py'
thirstPath = 'behavior_pack_XFwwevzL/Diet_NullGr/ModSys/Thirst/config.py'


# 读取任务前已提交数据，断言其他模组分类、疾病、收益公式没有随联动变动。
def readBaseline(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', base + ':' + path]).decode('utf-8-sig')


diet = runpy.run_path(str(repo / dietPath))
oldDiet = {}
exec(compile(readBaseline(dietPath), dietPath, 'exec'), oldDiet)
foods = diet['foodGroups']
expected = json.loads((rustic / 'tools/port_171_existing.json').read_text(encoding='utf-8'))['foods']
assert set(expected) <= set(foods)
newItems = set()
for batch in range(1, 5):
    data = json.loads((rustic / ('tools/port_171_batch_%s.json' % batch)).read_text(encoding='utf-8'))
    newItems.update(data['items'])
newFoods = newItems & set(expected)
assert len(newFoods) == 42, len(newFoods)
assert 'rusticdelight_nullgr:coffee_beans' not in foods
for name in ('coffee', 'dark_coffee', 'cooking_oil'):
    assert foods['rusticdelight_nullgr:' + name] == []
for color in ('red', 'green', 'yellow', 'orange', 'white', 'pink', 'blue', 'purple', 'black'):
    for prefix in ('bell_pepper_', 'bell_pepper_slice_', 'roasted_bell_pepper_', 'cook_bell_pepper_slice_'):
        assert foods['rusticdelight_nullgr:' + prefix + color] == ['vegetables']
    for prefix in ('stuffed_bell_pepper_', 'bell_pepper_roll_'):
        assert foods['rusticdelight_nullgr:' + prefix + color] == ['grains', 'vegetables']
for name, groups in oldDiet['foodGroups'].items():
    if not name.startswith('rusticdelight_nullgr:') or name.split(':')[1] in (
            'batter', 'calamari', 'cooked_calamari', 'spring_rolls', 'potato_slices', 'baked_potato_slices'):
        assert foods[name] == groups, name
for key in ('dietEffects', 'dietPenalties', 'groups', 'targetDietValue', 'nutritionPenaltyValue'):
    assert diet[key] == oldDiet[key], key
thirst = runpy.run_path(str(repo / thirstPath))
oldThirst = {}
exec(compile(readBaseline(thirstPath), thirstPath, 'exec'), oldThirst)
addedDrinks = {'rusticdelight_nullgr:' + name for name in ('pumpkin_coffee', 'cherry_blossom_coffee', 'calamari_soup')}
assert set(thirst['drinkItemValues']) - set(oldThirst['drinkItemValues']) == addedDrinks
for name in addedDrinks:
    assert thirst['drinkItemValues'][name] == {'defaultValue': 4.0, 'event': 'PlayerEatFoodServerEvent', 'auxValues': {}}
assert all(thirst['drinkItemValues'][name] == value for name, value in oldThirst['drinkItemValues'].items())
for path in ('ModSys/Diet/Diet.py', 'ModSys/Disease/config.py', 'ModSys/Disease/Disease_ss.py',
             'ModSys/Thirst/Thirst.py', 'ModSys/Thirst/Thirst_ss.py'):
    name = 'behavior_pack_XFwwevzL/Diet_NullGr/' + path
    assert (repo / name).read_text(encoding='utf-8-sig') == readBaseline(name).replace('\r\n', '\n'), name
for relative in (dietPath, thirstPath, 'behavior_pack_XFwwevzL/Diet_NullGr/Diet_main_ss.py'):
    current = ast.parse((repo / relative).read_text(encoding='utf-8-sig'))
    previous = ast.parse(readBaseline(relative))
    imports = lambda tree: {ast.dump(node) for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))}
    assert imports(current) <= imports(previous), '新增导入必须另行核对白名单'
main = (behavior / 'Diet_NullGr/Diet_main_ss.py').read_text(encoding='utf-8-sig')
assert main.count('"RusticDelightFoodConsumed", self, self.PlayerEatFoodServerEvent') == 1
print('PASS: 97 种现有食品、42 种新品、3 个补水条目；共享分类、计算和疾病规则未改；无新增导入。')
