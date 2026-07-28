# -*- coding: utf-8 -*-
"""疾病系统纯数据、资源与接线回归测试。"""

import ast
import json
import struct
import sys
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
behavior_root = project_root / "behavior_pack_XFwwevzL"
resource_root = project_root / "resource_pack_qewqRv3q"
sys.path.insert(0, str(behavior_root))

from Diet_NullGr.ModSys.Disease import Disease
from Diet_NullGr.ModSys.Disease import config


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_equal(actual, expected, message):
    if actual != expected:
        raise AssertionError("{}: expected {!r}, actual {!r}".format(message, expected, actual))


def assert_close(actual, expected, message, tolerance=0.000001):
    if abs(actual - expected) > tolerance:
        raise AssertionError("{}: expected {!r}, actual {!r}".format(message, expected, actual))


def make_snapshot(**overrides):
    values = {
        "fruits": 0.5,
        "grains": 0.5,
        "proteins": 0.5,
        "vegetables": 0.5,
        "sugars": 0.5,
        "thirst": 0.5,
    }
    values.update(overrides)
    return {
        "values": values,
        "tracking": {
            "fruits": True,
            "grains": True,
            "proteins": True,
            "vegetables": True,
            "sugars": True,
        },
        "thirstEnabled": True,
    }


def test_trigger_and_recovery_thresholds():
    assert_equal(config.diseaseOrder, [
        "hypoglycemia",
        "hyperglycemia",
        "constipation",
        "rickets",
        "fever",
        "mouth_ulcer",
        "scurvy",
    ], "seven configured diseases")

    cases = {
        "hypoglycemia": (
            make_snapshot(fruits=0.20, grains=0.15, sugars=0.20),
            make_snapshot(fruits=0.20, grains=0.151, sugars=0.20),
            make_snapshot(fruits=0.10, grains=0.35, sugars=0.10),
            make_snapshot(fruits=0.349, grains=0.349, sugars=0.349),
            1.0,
        ),
        "hyperglycemia": (
            make_snapshot(fruits=0.45, grains=0.45, proteins=0.45, vegetables=0.45, sugars=0.80),
            make_snapshot(fruits=0.451, grains=0.451, proteins=0.451, vegetables=0.451, sugars=0.80),
            make_snapshot(fruits=0.35, grains=0.35, proteins=0.10, vegetables=0.10, sugars=0.55),
            make_snapshot(fruits=0.35, grains=0.35, proteins=0.10, vegetables=0.10, sugars=0.551),
            1.0,
        ),
        "constipation": (
            make_snapshot(fruits=0.25, grains=0.25, vegetables=0.50, thirst=0.35),
            make_snapshot(fruits=0.25, grains=0.25, vegetables=0.50, thirst=0.351),
            make_snapshot(fruits=0.35, grains=0.35, vegetables=0.10, thirst=0.50),
            make_snapshot(fruits=0.35, grains=0.35, vegetables=0.10, thirst=0.499),
            1.0,
        ),
        "rickets": (
            make_snapshot(fruits=0.35, grains=0.35, proteins=0.15, vegetables=0.10),
            make_snapshot(fruits=0.35, grains=0.35, proteins=0.151, vegetables=0.10),
            make_snapshot(proteins=0.45),
            make_snapshot(proteins=0.449),
            1.0,
        ),
        "fever": (
            make_snapshot(fruits=0.15, grains=0.15, proteins=0.15, vegetables=0.50, thirst=0.25),
            make_snapshot(fruits=0.15, grains=0.15, proteins=0.15, vegetables=0.50, thirst=0.251),
            make_snapshot(fruits=0.30, grains=0.30, proteins=0.30, vegetables=0.10, thirst=0.50),
            make_snapshot(fruits=0.30, grains=0.30, proteins=0.30, vegetables=0.10, thirst=0.499),
            1.0,
        ),
        "mouth_ulcer": (
            make_snapshot(grains=0.20, proteins=0.20, sugars=0.60),
            make_snapshot(grains=0.201, proteins=0.20, sugars=0.60),
            make_snapshot(grains=0.40, proteins=0.30),
            make_snapshot(grains=0.399, proteins=0.30),
            2.0,
        ),
        "scurvy": (
            make_snapshot(fruits=0.10, grains=0.35, proteins=0.10, vegetables=0.15),
            make_snapshot(fruits=0.101, grains=0.35, proteins=0.10, vegetables=0.15),
            make_snapshot(fruits=0.40, vegetables=0.10),
            make_snapshot(fruits=0.399, vegetables=0.449),
            1.0,
        ),
    }

    for disease_id in config.diseaseOrder:
        trigger, outside_trigger, recovery, outside_recovery, expected_multiplier = cases[disease_id]
        assert_close(
            Disease.getTriggerMultiplier(disease_id, trigger),
            expected_multiplier,
            "{} trigger boundary".format(disease_id),
        )
        assert_close(
            Disease.getTriggerMultiplier(disease_id, outside_trigger),
            0.0,
            "{} outside trigger boundary".format(disease_id),
        )
        assert_true(
            Disease.isRecoveryConditionMet(disease_id, recovery),
            "{} recovery boundary".format(disease_id),
        )
        assert_true(
            not Disease.isRecoveryConditionMet(disease_id, outside_recovery),
            "{} outside recovery boundary".format(disease_id),
        )

    low_sugar_mouth_ulcer = make_snapshot(grains=0.20, proteins=0.20, sugars=0.59)
    assert_close(Disease.getTriggerMultiplier("mouth_ulcer", low_sugar_mouth_ulcer), 1.0, "mouth ulcer normal rate")
    dry_fiber_shortage = make_snapshot(fruits=0.15, grains=0.15, vegetables=0.15, thirst=0.80)
    assert_close(Disease.getTriggerMultiplier("constipation", dry_fiber_shortage), 0.5, "constipation fiber-only rate")


def test_new_player_protection():
    data = Disease.createDefaultData()
    trigger = make_snapshot(fruits=0.20, grains=0.15, sugars=0.20)
    neutral = make_snapshot()
    for _ in range(config.minimumValidEatCount - 1):
        Disease.recordValidEat(data, neutral)
    result = Disease.advanceMetabolism(data, 100.0, trigger)
    assert_equal(result["diagnosed"], [], "four meals cannot diagnose")
    assert_true(all(value == 0.0 for value in data["progress"].values()), "protected progress reset")

    Disease.recordValidEat(data, neutral)
    assert_equal(data["validEatCount"], 5, "five valid meals enable disease")
    result = Disease.advanceMetabolism(data, config.diseases["hypoglycemia"]["triggerPoints"], trigger)
    assert_equal(result["diagnosed"], ["hypoglycemia"], "fifth meal unlocks diagnosis")


def test_two_slots_and_half_progress_cap():
    data = Disease.createDefaultData()
    data["validEatCount"] = config.minimumValidEatCount
    assert_true(Disease.diagnoseDisease(data, "fever"), "first slot diagnosis")
    assert_true(Disease.diagnoseDisease(data, "rickets"), "second slot diagnosis")
    assert_true(not Disease.diagnoseDisease(data, "scurvy"), "third slot rejected")

    scurvy_trigger = make_snapshot(
        fruits=0.10,
        grains=0.35,
        proteins=0.40,
        vegetables=0.15,
        sugars=0.40,
        thirst=0.20,
    )
    Disease.advanceMetabolism(data, 30.0, scurvy_trigger)
    expected_half = config.diseases["scurvy"]["triggerPoints"] * config.fullSlotProgressRatio
    assert_close(data["progress"]["scurvy"], expected_half, "third disease half progress cap")
    assert_equal(len(data["active"]), 2, "active disease slot cap")

    Disease.cureDisease(data, "rickets", useProtection=False)
    result = Disease.advanceMetabolism(data, expected_half, scurvy_trigger)
    assert_true("scurvy" in result["diagnosed"], "half-capped disease needs remaining half cycle")
    assert_equal(len(data["active"]), 2, "slot refilled without exceeding cap")


def test_blood_sugar_mutual_exclusion():
    data = Disease.createDefaultData()
    data["progress"]["hyperglycemia"] = 3.0
    assert_true(Disease.diagnoseDisease(data, "hypoglycemia"), "hypoglycemia diagnosis")
    assert_close(data["progress"]["hyperglycemia"], 0.0, "diagnosis clears conflicting candidate")
    assert_true(not Disease.diagnoseDisease(data, "hyperglycemia"), "hyperglycemia blocked by active hypoglycemia")
    assert_true(not ("hypoglycemia" in data["active"] and "hyperglycemia" in data["active"]), "blood sugar diseases never coexist")

    Disease.cureDisease(data, "hypoglycemia")
    assert_true(
        data["protectionSeconds"]["hyperglycemia"] >= config.bloodSugarConversionProtectionSeconds,
        "cure adds conversion protection",
    )
    assert_true(not Disease.diagnoseDisease(data, "hyperglycemia"), "conversion protection blocks immediate switch")

    reverse = Disease.createDefaultData()
    assert_true(Disease.diagnoseDisease(reverse, "hyperglycemia"), "hyperglycemia diagnosis")
    assert_true(not Disease.diagnoseDisease(reverse, "hypoglycemia"), "hypoglycemia blocked by active hyperglycemia")


def test_constipation_squat_and_timeout_cure():
    data = Disease.createDefaultData()
    assert_true(Disease.diagnoseDisease(data, "constipation"), "constipation diagnosis")
    for index in range(config.constipationSquatRequired - 1):
        assert_true(not Disease.recordConstipationSquat(data), "squat {} cannot cure early".format(index + 1))
    assert_equal(data["constipationSquatCount"], 11, "eleven squat count")
    assert_true(Disease.recordConstipationSquat(data), "twelfth squat cures")
    assert_true("constipation" not in data["active"], "constipation removed after twelve squats")
    assert_equal(data["constipationSquatCount"], 0, "squat count resets after cure")

    for disease_id in config.diseaseOrder:
        timed = Disease.createDefaultData()
        assert_true(Disease.diagnoseDisease(timed, disease_id), "{} timeout setup".format(disease_id))
        maximum = config.diseases[disease_id]["maxActiveSeconds"]
        assert_equal(Disease.advanceSeconds(timed, maximum - 1), [], "{} survives before timeout".format(disease_id))
        assert_equal(Disease.advanceSeconds(timed, 1), [disease_id], "{} auto-cures at timeout".format(disease_id))
        assert_true(disease_id not in timed["active"], "{} removed at timeout".format(disease_id))
        assert_equal(
            timed["protectionSeconds"][disease_id],
            config.diseases[disease_id]["protectionSeconds"],
            "{} timeout protection".format(disease_id),
        )


def test_recovery_transactions():
    for disease_id in config.diseaseOrder:
        if disease_id == "rickets":
            continue
        recovery_values = {
            "hypoglycemia": make_snapshot(grains=0.35, fruits=0.10, sugars=0.10),
            "hyperglycemia": make_snapshot(fruits=0.35, grains=0.35, proteins=0.10, vegetables=0.10, sugars=0.55),
            "constipation": make_snapshot(fruits=0.35, grains=0.35, vegetables=0.10, thirst=0.50),
            "fever": make_snapshot(fruits=0.30, grains=0.30, proteins=0.30, vegetables=0.10, thirst=0.50),
            "mouth_ulcer": make_snapshot(grains=0.40, proteins=0.30),
            "scurvy": make_snapshot(fruits=0.40, vegetables=0.10),
        }
        data = Disease.createDefaultData()
        Disease.diagnoseDisease(data, disease_id)
        cured = Disease.applyNutritionRecovery(data, 0.0, recovery_values[disease_id])
        assert_equal(cured, [disease_id], "{} immediate dietary recovery".format(disease_id))

    rickets = Disease.createDefaultData()
    Disease.diagnoseDisease(rickets, "rickets")
    recovery = make_snapshot(proteins=0.45)
    assert_equal(Disease.applyNutritionRecovery(rickets, 2.0, recovery), [], "rickets requires three metabolic points")
    assert_close(rickets["recoveryProgress"]["rickets"], 2.0, "rickets recovery progress")
    assert_equal(Disease.applyNutritionRecovery(rickets, 1.0, recovery), ["rickets"], "rickets cures at third point")


def read_png_size(path):
    data = path.read_bytes()
    assert_equal(data[:8], b"\x89PNG\r\n\x1a\n", "{} PNG signature".format(path.name))
    return struct.unpack(">II", data[16:24])


def parse_language_file(path):
    values = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def test_resources_and_languages():
    effect_root = behavior_root / "netease_effects"
    icon_root = resource_root / "textures" / "ui"
    effect_files = sorted(effect_root.glob("diet_nullgr_*.json"))
    assert_equal(len(effect_files), 7, "seven custom effect JSON files")
    expected_files = {"diet_nullgr_{}.json".format(disease_id) for disease_id in config.diseaseOrder}
    assert_equal({path.name for path in effect_files}, expected_files, "custom effect JSON names")

    languages = json.loads((resource_root / "texts" / "languages.json").read_text(encoding="utf-8-sig"))
    assert_equal(languages, ["zh_CN"], "language registration")
    translations = parse_language_file(resource_root / "texts" / "zh_CN.lang")

    for disease_id in config.diseaseOrder:
        disease_config = config.diseases[disease_id]
        effect_path = effect_root / "diet_nullgr_{}.json".format(disease_id)
        effect_data = json.loads(effect_path.read_text(encoding="utf-8-sig"))
        assert_equal(effect_data["format_version"], "1.10", "{} effect format".format(disease_id))
        effect = effect_data["minecraft:effect"]
        assert_equal(effect["description"]["identifier"], disease_config["customEffect"], "{} effect identifier".format(disease_id))
        icon_key = effect["components"]["minecraft:icon"]
        assert_equal(
            disease_config["icon"],
            "textures/ui/{}_effect".format(icon_key),
            "{} configured icon path".format(disease_id),
        )
        icon_path = icon_root / "{}_effect.png".format(icon_key)
        assert_true(icon_path.is_file(), "{} icon exists".format(disease_id))
        assert_equal(read_png_size(icon_path), (18, 18), "{} icon size".format(disease_id))
        particle_color = effect["components"]["minecraft:particle_color"]
        assert_true(len(particle_color) == 3 and all(isinstance(value, int) and 0 <= value <= 255 for value in particle_color), "{} particle color".format(disease_id))
        assert_equal(translations[disease_config["customEffect"]], disease_config["name"], "{} language key".format(disease_id))
        assert_true(disease_config["symptom"], "{} symptom text".format(disease_id))
        assert_true(disease_config["uiGroups"], "{} highlighted nutrition groups".format(disease_id))

    animation_path = resource_root / "animations" / "diet_disease.animation.json"
    animation_data = json.loads(animation_path.read_text(encoding="utf-8-sig"))
    animation = animation_data["animations"][config.playerScaleAnimation]
    assert_true(animation["loop"], "disease scale animation loops")
    assert_equal(animation["bones"]["body"]["scale"], [config.bodyScaleQuery] * 3, "body scale query")
    compensated_head_scale = "{} / {}".format(config.headScaleQuery, config.bodyScaleQuery)
    assert_equal(animation["bones"]["head"]["scale"], [compensated_head_scale] * 3, "head scale compensates body parent")
    assert_equal(set(animation["bones"]), {"body", "head"}, "hat inherits compensated head without duplicate scaling")

    for json_path in list(effect_root.glob("*.json")) + list((resource_root / "animations").glob("*.json")) + list((resource_root / "ui").glob("*.json")):
        json.loads(json_path.read_text(encoding="utf-8-sig"))


def find_named_control(value, target):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.split("@", 1)[0] == target:
                return child
            result = find_named_control(child, target)
            if result is not None:
                return result
    elif isinstance(value, list):
        for child in value:
            result = find_named_control(child, target)
            if result is not None:
                return result
    return None


def test_system_registration_and_ui_bindings():
    disease_config_path = behavior_root / "Diet_NullGr" / "ModSys" / "Disease" / "config.py"
    com_path = behavior_root / "Diet_NullGr" / "com.py"
    mod_main_path = behavior_root / "Diet_NullGr" / "modMain.py"
    server_path = behavior_root / "Diet_NullGr" / "ModSys" / "Disease" / "Disease_ss.py"
    client_path = behavior_root / "Diet_NullGr" / "ModSys" / "Disease" / "Disease_cs.py"
    diet_client_path = behavior_root / "Diet_NullGr" / "Diet_main_cs.py"
    diet_server_path = behavior_root / "Diet_NullGr" / "Diet_main_ss.py"
    thirst_server_path = behavior_root / "Diet_NullGr" / "ModSys" / "Thirst" / "Thirst_ss.py"
    diet_ui_logic_path = behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "DietUI.py"
    diet_ui_path = resource_root / "ui" / "diet_screen.json"

    assert_equal(config.serverSysKey[config.ssname], config.ssPath, "disease server config registration")
    assert_equal(config.clientSysKey[config.csname], config.csPath, "disease client config registration")
    assert_true(server_path.is_file() and client_path.is_file() and disease_config_path.is_file(), "disease module files exist")

    com_text = com_path.read_text(encoding="utf-8-sig")
    assert_true("serverSysKey.update(diseaseConfig.serverSysKey)" in com_text, "server registry includes disease")
    assert_true("clientSysKey.update(diseaseConfig.clientSysKey)" in com_text, "client registry includes disease")
    mod_main_text = mod_main_path.read_text(encoding="utf-8-sig")
    assert_true("serverApi.RegisterSystem(com.modName, key, com.serverSysKey[key])" in mod_main_text, "server registry is executed")
    assert_true("clientApi.RegisterSystem(com.modName, key, com.clientSysKey[key])" in mod_main_text, "client registry is executed")

    server_text = server_path.read_text(encoding="utf-8-sig")
    for required_event in (
        "AddServerPlayerEvent",
        "DelServerPlayerEvent",
        "PlayerDieEvent",
        "PlayerRespawnFinishServerEvent",
        "OnPlayerActionServerEvent",
        "ActuallyHurtServerEvent",
        "ActorHurtServerEvent",
        "OnScriptTickServer",
    ):
        assert_true('"{}"'.format(required_event) in server_text, "disease server listens {}".format(required_event))
    assert_true("damage_f" not in server_text, "current 3.9 hurt events do not expose damage_f")
    assert_true("args['damage'] = float(damage) * config.ricketsFallDamageMultiplier" in server_text,
                "rickets modifies the official mutable damage field")
    assert_true("customTag = args['customTag']" in server_text, "hurt and death callbacks bind customTag")
    assert_true("visualPlayerId not in onlinePlayers" in server_text, "visual ready event validates target player")
    assert_true("self._finishDiseaseChanges(playerId, data, [diseaseId], cured)" in server_text,
                "blood sugar command removes the conflicting effect")
    assert_true("debugCommandEnabled = False" in disease_config_path.read_text(encoding="utf-8-sig"),
                "disease management command is disabled in production by default")
    assert_true("if not config.debugCommandEnabled:" in server_text,
                "disease management command requires explicit development opt-in")
    assert_true("gameType == gameTypeEnum.Creative or gameType == gameTypeEnum.Spectator" in server_text,
                "rickets jump damage excludes unrestricted game modes")
    assert_true("footBlockName in config.invalidBodyBlocks" in server_text,
                "constipation squat rejects water at the player's feet")
    assert_true("playerActionType.StartSwimming" in server_text and "playerActionType.StopSwimming" in server_text,
                "constipation squat tracks swimming state")

    diet_server_text = diet_server_path.read_text(encoding="utf-8-sig")
    for call_name in ("recordFoodEat", "queueMetabolism", "hasActiveDisease", "isSugarRushPaused"):
        assert_true("diseaseSys.{}(".format(call_name) in diet_server_text, "Diet integration {}".format(call_name))
    assert_true(diet_server_text.index("diseaseSys.recordFoodEat(") < diet_server_text.index("if not gainValues:"),
                "all successful food events reach disease symptoms before unclassified food exits")
    thirst_server_text = thirst_server_path.read_text(encoding="utf-8-sig")
    assert_true("diseaseSys.getThirstConsumptionMultiplier(playerId)" in thirst_server_text, "thirst multiplier integration")
    assert_true("def setSprintLimitSource(" in thirst_server_text, "shared sprint restriction source")

    ui_data = json.loads(diet_ui_path.read_text(encoding="utf-8-sig"))
    ui_text = diet_ui_path.read_text(encoding="utf-8-sig")
    logic_text = diet_ui_logic_path.read_text(encoding="utf-8-sig")
    client_text = client_path.read_text(encoding="utf-8-sig")
    assert_true('"RemovePlayerAOIClientEvent"' in client_text, "disease client listens AOI removal")
    assert_true("def RemovePlayerAOIClientEvent(" in client_text, "disease client clears stale visual injection")
    assert_true("self.AddPlayerCreatedClientEvent({'playerId': playerId})" in client_text,
                "UI initialization restores local player render injection after addon reload")
    assert_true("not self.postProcessComp.CheckGaussianBlurEnabled()" in client_text,
                "active disease restores blur after another screen disables it")
    assert_true("self.renderedVisualData" in client_text and "config.visualScaleFadeTick" in client_text,
                "bone scale changes interpolate on the client")
    assert_true("clientApi.GetUI(com.modName, dietConfig.uiKey)" in client_text and
                "uiNode.UpdateDiseaseData(self.diseaseData)" in client_text,
                "disease sync only refreshes a live diet screen")
    for audio_text in (client_text, diet_client_path.read_text(encoding="utf-8-sig")):
        assert_true("CreateCustomAudio(levelId)" in audio_text and "PlayCustomMusic(" in audio_text,
                    "current custom audio API is used")
        assert_true("CreateAudio(" not in audio_text and "PlayPlayerSound" not in audio_text,
                    "removed audio API remains absent")
    assert_true("actorDamageCause.Magic" in server_text,
                "symptom damage uses a Hurt-compatible no-attacker damage cause")
    assert_true("actorDamageCause.Custom" not in server_text,
                "unsupported Custom damage cause is not reintroduced")
    binding_names = ["disease_healthy_visible"]
    for slot_index in range(2):
        for field_name in ("visible", "icon", "name", "duration", "progress", "symptom", "cause", "relief"):
            binding_names.append("disease_slot_{}_{}".format(slot_index, field_name))
    for binding_name in binding_names:
        full_name = "#diet_screen.{}".format(binding_name)
        assert_true(full_name in ui_text, "UI declares {}".format(full_name))
        assert_true(full_name in logic_text, "Python binds {}".format(full_name))
    assert_true("#diet_screen.effects" not in ui_text and "#diet_screen.effects" not in logic_text, "removed effects binding remains absent")
    assert_true("def UpdateDiseaseData(" in logic_text, "DietUI disease update entry")
    assert_true("diseaseClientSys.diseaseData" in logic_text, "DietUI reads cached disease data")
    assert_true("UpdateDiseaseData(self.diseaseData)" in client_text, "Disease client refreshes open DietUI")

    root = find_named_control(ui_data["main"], "root")
    nutrition_grid = find_named_control(root, "rows_grid")
    healthy_label = find_named_control(root, "disease_healthy")
    assert_true(root["size"][1] >= 292, "expanded Diet panel height")
    assert_equal(nutrition_grid["grid_dimensions"], [1, 5], "five nutrition rows remain")
    assert_equal(nutrition_grid["maximum_grid_items"], 5, "nutrition row limit")
    assert_equal(healthy_label["text"], "当前身体状况良好", "healthy state text")
    assert_true(find_named_control(root, "disease_grid") is None and "disease_rows" not in ui_text,
                "disease cards avoid a second collection grid")
    for slot_index in range(2):
        template_name = "disease_slot_{}".format(slot_index)
        assert_true(find_named_control(root, template_name) is not None, "disease slot {} instance".format(slot_index))
        assert_true(template_name in ui_data, "disease slot {} template".format(slot_index))
        assert_true(find_named_control(ui_data[template_name], "symptom") is not None,
                    "disease slot {} shows symptoms".format(slot_index))
    assert_true("refreshDiseaseGroupFlags" in logic_text and "diseaseRelated" in logic_text and
                "diseaseGroupHighlightColor" in logic_text,
                "nutrition rows highlight precomputed disease-related groups")


def test_modsdk_import_whitelist():
    python_paths = [
        behavior_root / "Diet_NullGr" / "com.py",
        behavior_root / "Diet_NullGr" / "Diet_main_cs.py",
        behavior_root / "Diet_NullGr" / "Diet_main_ss.py",
        behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "Diet.py",
        behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "DietUI.py",
        behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "config.py",
        behavior_root / "Diet_NullGr" / "ModSys" / "Thirst" / "Thirst.py",
        behavior_root / "Diet_NullGr" / "ModSys" / "Thirst" / "Thirst_ss.py",
    ]
    python_paths.extend((behavior_root / "Diet_NullGr" / "ModSys" / "Disease").glob("*.py"))
    allowed_roots = {"mod", "Diet_NullGr", "typing", "operator"}
    for python_path in python_paths:
        tree = ast.parse(python_path.read_text(encoding="utf-8-sig"), filename=str(python_path))
        for node in ast.walk(tree):
            imported_modules = []
            if isinstance(node, ast.Import):
                imported_modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules = [node.module]
            for module_name in imported_modules:
                module_root = module_name.split(".", 1)[0]
                assert_true(
                    module_root in allowed_roots,
                    "non-whitelisted import {} in {}".format(module_name, python_path.relative_to(project_root)),
                )


def main():
    tests = [
        test_trigger_and_recovery_thresholds,
        test_new_player_protection,
        test_two_slots_and_half_progress_cap,
        test_blood_sugar_mutual_exclusion,
        test_constipation_squat_and_timeout_cure,
        test_recovery_transactions,
        test_resources_and_languages,
        test_system_registration_and_ui_bindings,
        test_modsdk_import_whitelist,
    ]
    for test in tests:
        test()
        print("PASS {}".format(test.__name__))
    print("Disease system regression test passed: {} groups".format(len(tests)))


if __name__ == "__main__":
    main()
