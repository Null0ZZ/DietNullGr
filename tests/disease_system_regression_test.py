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
from Diet_NullGr.ModSys.Diet import Diet
from Diet_NullGr.ModSys.Diet import config as diet_config
from Diet_NullGr.ModSys.TipMessage import TipMessage
from Diet_NullGr.ModSys.TipMessage import config as tip_message_config


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


def test_client_tips_contract():
    for disease_id in config.diseaseOrder:
        disease_config = config.diseases[disease_id]
        tips = disease_config["tips"]
        assert_true(isinstance(tips, str) and tips, "{} concise tips exist".format(disease_id))
        assert_true(len(tips) <= 20, "{} concise tips stay within 20 characters".format(disease_id))

        data = Disease.createDefaultData()
        assert_true(Disease.diagnoseDisease(data, disease_id), "{} client tips setup".format(disease_id))
        client_data = Disease.buildClientData(data)
        active_data = client_data["active"][0]
        assert_equal(active_data["tips"], tips, "{} client tips contract".format(disease_id))
        assert_equal(active_data["lowGroups"], disease_config["lowGroups"], "{} low outline groups".format(disease_id))
        assert_equal(active_data["highGroups"], disease_config["highGroups"], "{} high outline groups".format(disease_id))
        assert_true("groups" not in active_data, "{} removed generic highlight groups".format(disease_id))


def test_diet_tooltip_removal_contract():
    ui_path = resource_root / "ui" / "diet_screen.json"
    logic_path = behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "DietUI.py"
    ui_text = ui_path.read_text(encoding="utf-8-sig")
    logic_text = logic_path.read_text(encoding="utf-8-sig")
    assert_true("#diet_screen.row_tooltip" not in ui_text, "removed tooltip UI binding stays absent")
    assert_true("#diet_screen.row_tooltip" not in logic_text, "removed tooltip Python binding stays absent")

    data = {
        "active": True,
        "values": Diet.createInitialValues(),
        "tracking": Diet.createDefaultTracking(),
    }
    client_data = Diet.buildClientData(data)
    expected_fields = {"id", "name", "icon", "color", "value", "tracked"}
    for group_id in diet_config.groupOrder:
        assert_true("tooltip" not in diet_config.groups[group_id], "{} tooltip config removed".format(group_id))
    for group_data in client_data["groups"]:
        assert_equal(set(group_data), expected_fields, "{} client row fields".format(group_data["id"]))


def test_diet_initialization_persistence_and_death_boundary():
    class ModAttrStub(object):
        def __init__(self, values):
            self.values = values

        def GetAttr(self, key, default):
            return self.values[key] if key in self.values else default

        def SetAttr(self, key, value, needRestore=False):
            assert_true(needRestore, "diet values persist across death and re-entry")
            self.values[key] = value

    class CompFactoryStub(object):
        def __init__(self, values):
            self.modAttr = ModAttrStub(values)

        def CreateModAttr(self, player_id):
            return self.modAttr

    initial_data = Diet.loadPlayerData("new_player", CompFactoryStub({}))
    for group_id in diet_config.groupOrder:
        assert_close(initial_data["values"][group_id], 0.5, "{} first initialization is 50%".format(group_id))
        assert_close(diet_config.groups[group_id]["initialValue"], 0.5, "{} initial config is explicit".format(group_id))
        assert_true("defaultValue" not in diet_config.groups[group_id], "{} has no ambiguous default value".format(group_id))

    stored = {}
    comp_factory = CompFactoryStub(stored)
    persisted_values = {
        "fruits": 0.0,
        "grains": 0.125,
        "proteins": 0.25,
        "vegetables": 0.75,
        "sugars": 1.0,
    }
    initial_data["values"] = dict(persisted_values)
    Diet.savePlayerData("returning_player", initial_data, comp_factory)
    reloaded_data = Diet.loadPlayerData("returning_player", comp_factory)
    for group_id in diet_config.groupOrder:
        assert_close(
            reloaded_data["values"][group_id],
            persisted_values[group_id],
            "{} re-entry restores the stored value including zero".format(group_id),
        )

    Diet.applyDeathPenalty(reloaded_data)
    Diet.savePlayerData("returning_player", reloaded_data, comp_factory)
    respawned_data = Diet.loadPlayerData("returning_player", comp_factory)
    for group_id in diet_config.groupOrder:
        assert_close(respawned_data["values"][group_id], 0.0, "{} death result survives respawn and re-entry".format(group_id))

    reset_death_data = Diet.loadPlayerData("new_player", CompFactoryStub({}))
    reset_death_data["deathPenaltyMethod"] = diet_config.deathPenaltyMethodReset
    Diet.applyDeathPenalty(reset_death_data)
    for group_id in diet_config.groupOrder:
        assert_close(
            reset_death_data["values"][group_id],
            diet_config.deathResetValue,
            "{} death reset does not reuse the first initialization value".format(group_id),
        )

    command_result = Diet.handleCommand("/diet reset", respawned_data)
    assert_true(command_result["changed"], "explicit diet reset changes nutrition data")
    for group_id in diet_config.groupOrder:
        assert_close(respawned_data["values"][group_id], 0.5, "{} explicit reset returns to the initial value".format(group_id))


def test_disease_master_switch_state():
    class ModAttrStub(object):
        def __init__(self, values):
            self.values = values

        def GetAttr(self, key, default):
            return self.values[key] if key in self.values else default

        def SetAttr(self, key, value, needRestore=False):
            self.values[key] = value

    class CompFactoryStub(object):
        def __init__(self, values):
            self.modAttr = ModAttrStub(values)

        def CreateModAttr(self, player_id):
            return self.modAttr

    data = Disease.createDefaultData()
    assert_true(data["enabled"], "disease system defaults to enabled")
    data["validEatCount"] = 9
    assert_true(Disease.diagnoseDisease(data, "hypoglycemia"), "master switch setup first disease")
    assert_true(Disease.diagnoseDisease(data, "scurvy"), "master switch setup second disease")
    for disease_id in config.diseaseOrder:
        data["progress"][disease_id] = 1.0
        data["activeSeconds"][disease_id] = 2
        data["protectionSeconds"][disease_id] = 3
        data["recoveryProgress"][disease_id] = 4.0
    data["constipationSquatCount"] = 5
    data["enabled"] = False

    cleared = Disease.clearAllDiseaseState(data)

    assert_equal(cleared, ["hypoglycemia", "scurvy"], "master switch reports cleared diseases")
    assert_equal(data["active"], [], "master switch clears active diseases")
    assert_true(not Disease.diagnoseDisease(data, "fever"), "master switch blocks direct diagnosis")
    assert_equal(data["validEatCount"], 9, "master switch preserves onboarding progress")
    assert_equal(data["constipationSquatCount"], 0, "master switch clears constipation progress")
    for disease_id in config.diseaseOrder:
        assert_close(data["progress"][disease_id], 0.0, "master switch clears candidate progress")
        assert_equal(data["activeSeconds"][disease_id], 0, "master switch clears active duration")
        assert_equal(data["protectionSeconds"][disease_id], 0, "master switch clears protection")
        assert_close(data["recoveryProgress"][disease_id], 0.0, "master switch clears recovery progress")

    stored = {}
    comp_factory = CompFactoryStub(stored)
    Disease.savePlayerData("player", data, comp_factory)
    assert_true(stored[config.attrEnabled] is False, "master switch persists disabled state")
    loaded = Disease.loadPlayerData("player", comp_factory)
    assert_true(loaded["enabled"] is False and not loaded["active"], "master switch restores disabled clean state")
    default_loaded = Disease.loadPlayerData("new_player", CompFactoryStub({}))
    assert_true(default_loaded["enabled"], "missing master switch storage migrates to enabled")


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

    expected_outline_groups = {
        "hypoglycemia": (["fruits", "grains", "sugars"], []),
        "hyperglycemia": ([], ["sugars"]),
        "constipation": (["fruits", "grains", "vegetables"], []),
        "rickets": (["proteins"], []),
        "fever": (["fruits", "grains", "proteins", "vegetables"], []),
        "mouth_ulcer": (["grains", "proteins"], []),
        "scurvy": (["fruits", "vegetables"], []),
    }
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
        low_groups, high_groups = expected_outline_groups[disease_id]
        assert_equal(disease_config["lowGroups"], low_groups, "{} low outline group mapping".format(disease_id))
        assert_equal(disease_config["highGroups"], high_groups, "{} high outline group mapping".format(disease_id))
        outline_groups = low_groups + high_groups
        assert_true(outline_groups, "{} has abnormal nutrition groups".format(disease_id))
        assert_equal(len(outline_groups), len(set(outline_groups)), "{} outline groups do not overlap".format(disease_id))
        assert_true(all(group_id in diet_config.groupOrder for group_id in outline_groups),
                    "{} outline groups use visible nutrition IDs".format(disease_id))

    assert_equal(diet_config.diseaseHighOutlineColor,
                 (1.0, 0.2509803921568627, 0.1019607843137255),
                 "high outline color is #ff401a")
    assert_equal(diet_config.diseaseLowOutlineColor,
                 (0.3058823529411765, 0.9098039215686274, 1.0),
                 "low outline color is #4ee8ff")
    outline_path = resource_root / "textures" / "gui" / "diet_nullgr" / "outline.png"
    assert_true(outline_path.is_file(), "nutrition outline texture exists")
    assert_equal(read_png_size(outline_path), (141, 5), "nutrition outline texture matches bar size")

    animation_path = resource_root / "animations" / "diet_disease.animation.json"
    animation_data = json.loads(animation_path.read_text(encoding="utf-8-sig"))
    animation = animation_data["animations"][config.playerScaleAnimation]
    assert_true(animation["loop"], "disease scale animation loops")
    assert_equal(animation["bones"]["body"]["scale"], [config.bodyScaleQuery] * 3, "body scale query")
    compensated_head_scale = "{} / {}".format(config.headScaleQuery, config.bodyScaleQuery)
    assert_equal(animation["bones"]["head"]["scale"], [compensated_head_scale] * 3, "head scale compensates body parent")
    assert_equal(set(animation["bones"]), {"body", "head"}, "hat inherits compensated head without duplicate scaling")

    sound_definitions_path = resource_root / "sounds" / "sound_definitions.json"
    sound_definitions = json.loads(sound_definitions_path.read_text(encoding="utf-8-sig"))
    relief_sound = sound_definitions["sound_definitions"][config.constipationReliefSound]
    assert_equal(relief_sound["category"], "player", "constipation relief sound category")
    assert_equal(
        relief_sound["sounds"],
        [{
            "name": "sounds/diet_nullgr/constipation_relief",
            "load_on_low_memory": True,
        }],
        "constipation relief sound resource",
    )
    relief_sound_path = resource_root / "sounds" / "diet_nullgr" / "constipation_relief.ogg"
    assert_true(relief_sound_path.read_bytes().startswith(b"OggS"), "constipation relief sound is an Ogg file")
    fracture_sound = sound_definitions["sound_definitions"][config.ricketsFractureSound]
    assert_equal(fracture_sound["category"], "player", "rickets fracture sound category")
    assert_equal(
        fracture_sound["sounds"],
        [{
            "name": "sounds/diet_nullgr/rickets_fracture",
            "load_on_low_memory": True,
        }],
        "rickets fracture sound resource",
    )
    fracture_sound_path = resource_root / "sounds" / "diet_nullgr" / "rickets_fracture.ogg"
    fracture_sound_data = fracture_sound_path.read_bytes()
    assert_true(fracture_sound_data.startswith(b"OggS"), "rickets fracture sound is an Ogg file")
    first_packet_offset = 27 + fracture_sound_data[26]
    assert_equal(
        fracture_sound_data[first_packet_offset:first_packet_offset + 7],
        b"\x01vorbis",
        "rickets fracture sound uses Vorbis encoding",
    )
    # 网易打包错误码 33 检查 Vorbis 头中的标称码率，音效必须不超过 128 kbps。
    fracture_sound_bitrate = struct.unpack(
        "<i",
        fracture_sound_data[first_packet_offset + 20:first_packet_offset + 24],
    )[0]
    assert_true(
        0 < fracture_sound_bitrate <= 128000,
        "rickets fracture sound bitrate must not exceed 128 kbps: {}".format(fracture_sound_bitrate),
    )

    for json_path in list(effect_root.glob("*.json")) + list((resource_root / "animations").glob("*.json")) + list((resource_root / "ui").glob("*.json")) + [sound_definitions_path]:
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


def test_hypoglycemia_custom_postprocess_resources():
    post_process_path = resource_root / "graphics_settings" / "post_process.json"
    material_path = resource_root / "materials" / "postprocess.material"
    vertex_shader_path = resource_root / "shaders" / "glsl" / "diet_fullscreen.vertex"
    fragment_shader_path = resource_root / "shaders" / "glsl" / "diet_hypoglycemia_vision.fragment"

    for resource_path in (post_process_path, material_path, vertex_shader_path, fragment_shader_path):
        assert_true(resource_path.is_file(), "custom postprocess resource {}".format(resource_path.relative_to(project_root)))

    assert_equal(config.hypoglycemiaVisionPostProcess, "dietHypoglycemiaVision",
                 "hypoglycemia custom postprocess name")
    assert_equal(config.hypoglycemiaVisionStrengthParameter, "strength",
                 "hypoglycemia custom postprocess strength parameter")
    assert_close(config.hypoglycemiaVisionInitialStrength, 0.1,
                 "hypoglycemia custom postprocess initial strength")
    assert_close(config.hypoglycemiaVisionMaxStrength, 1.0,
                 "hypoglycemia custom postprocess maximum strength")
    assert_close(config.hypoglycemiaVisionGrowSeconds, 90.0,
                 "hypoglycemia custom postprocess growth duration")
    assert_equal(config.hypoglycemiaVisionFadeTick, 20,
                 "hypoglycemia custom postprocess fade duration")

    post_process_data = json.loads(post_process_path.read_text(encoding="utf-8-sig"))
    assert_equal(post_process_data["render_order"][-1], config.hypoglycemiaVisionPostProcess,
                 "hypoglycemia postprocess renders after the vanilla chain")
    assert_equal(post_process_data["render_order"].count(config.hypoglycemiaVisionPostProcess), 1,
                 "hypoglycemia postprocess appears once in render order")
    processes = {process["name"]: process for process in post_process_data["process_array"]}
    assert_equal(set(("bloom", "lensflare", "depthoffield", "gaussianblur", "coloradjustment",
                      "vignette", "lensstain", "oldtv", "scanmap")) - set(processes), set(),
                 "custom postprocess file preserves vanilla processes")
    assert_equal(processes[config.hypoglycemiaVisionPostProcess], {
        "name": "dietHypoglycemiaVision",
        "enable": False,
        "paras": [
            {"name": "strength", "value": 0.0, "range": [0.0, 1.0]},
            {"name": "blur_offset", "value": 0.008, "range": [0.0, 0.015]},
            {"name": "ghost_offset", "value": 0.018, "range": [0.0, 0.03]},
            {"name": "sway_speed", "value": 2.4, "range": [0.0, 6.0]},
        ],
        "pass_array": [{
            "render_target": {"width": 1.0, "height": 1.0},
            "material": "dietHypoglycemiaVisionMat",
        }],
    }, "hypoglycemia custom postprocess definition")

    material_data = json.loads(material_path.read_text(encoding="utf-8-sig"))
    assert_equal(material_data["dietHypoglycemiaVisionMat"], {
        "vertexShader": "shaders/diet_fullscreen.vertex",
        "fragmentShader": "shaders/diet_hypoglycemia_vision.fragment",
        "vertexFields": [{"field": "Position"}, {"field": "UV0"}],
        "samplerStates": [{
            "samplerIndex": 0,
            "textureWrap": "Clamp",
            "textureFilter": "Bilinear",
        }],
        "states": ["DisableDepthTest"],
        "msaaSupport": "Both",
    }, "hypoglycemia custom postprocess material")

    vertex_shader_text = vertex_shader_path.read_text(encoding="utf-8-sig")
    fragment_shader_text = fragment_shader_path.read_text(encoding="utf-8-sig")
    assert_true("// __multiversion__" in vertex_shader_text and "gl_Position" in vertex_shader_text and
                "uv = TEXCOORD_0" in vertex_shader_text,
                "custom postprocess vertex shader follows the official fullscreen pass")
    assert_true("// __multiversion__" in fragment_shader_text and
                '#include "uniformPerFrameConstants.h"' in fragment_shader_text and
                "uniform vec4 EXTRA_VECTOR1" in fragment_shader_text,
                "custom postprocess fragment shader exposes time and configured parameters")
    assert_equal(fragment_shader_text.count("texture(TEXTURE_0"), 7,
                 "custom postprocess uses exactly seven texture samples")
    assert_true("float symptomCycle = mod(TIME * 0.25, 1.0);" in fragment_shader_text and
                "float clearWindow = smoothstep(0.66, 0.74, symptomCycle)" in fragment_shader_text and
                "1.0 - smoothstep(0.82, 0.90, symptomCycle)" in fragment_shader_text,
                "custom postprocess provides a perceptible full-clear window every four seconds")
    assert_true("float blurPulse = 0.5 + 0.5 * sin(" in fragment_shader_text and
                "float symptomAmount = (0.68 + blurPulse * 0.32) * (1.0 - clearWindow);" in fragment_shader_text and
                "float blurOffset = baseBlurOffset * (0.45 + blurPulse * 0.55) * symptomAmount;" in fragment_shader_text,
                "custom postprocess continuously varies blur severity outside each clear window")
    assert_true("float shakeX = sin(TIME * swaySpeed * 3.20) * 0.65" in fragment_shader_text and
                "sin(TIME * swaySpeed * 5.70" in fragment_shader_text and
                "shakeX + separation" in fragment_shader_text and
                "shakeX - separation" in fragment_shader_text,
                "custom postprocess ghost pair shakes quickly and visibly from side to side")
    assert_true("positiveGhostOffset" in fragment_shader_text and
                "negativeGhostOffset" in fragment_shader_text and
                "doubleImageOffset" not in fragment_shader_text,
                "custom postprocess moves the two ghost images asymmetrically")
    assert_true("float baseBlurOffset = EXTRA_VECTOR1.y;" in fragment_shader_text and
                "float ghostOffset = EXTRA_VECTOR1.z;" in fragment_shader_text,
                "custom postprocess strength controls blending without suppressing ghost motion")
    assert_true("mix(sourceColor, ghostedColor, strength * symptomAmount)" in fragment_shader_text,
                "zero strength and clarity windows preserve the original image")
    assert_true("blurredColor * 0.30" in fragment_shader_text and
                "positiveGhostColor * 0.45" in fragment_shader_text and
                "negativeGhostColor * 0.25" in fragment_shader_text,
                "custom postprocess makes the rapidly moving ghost pair visually severe")


def test_system_registration_and_ui_bindings():
    disease_config_path = behavior_root / "Diet_NullGr" / "ModSys" / "Disease" / "config.py"
    com_path = behavior_root / "Diet_NullGr" / "com.py"
    mod_main_path = behavior_root / "Diet_NullGr" / "modMain.py"
    server_path = behavior_root / "Diet_NullGr" / "ModSys" / "Disease" / "Disease_ss.py"
    client_path = behavior_root / "Diet_NullGr" / "ModSys" / "Disease" / "Disease_cs.py"
    diet_client_path = behavior_root / "Diet_NullGr" / "Diet_main_cs.py"
    diet_server_path = behavior_root / "Diet_NullGr" / "Diet_main_ss.py"
    diet_config_path = behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "config.py"
    thirst_server_path = behavior_root / "Diet_NullGr" / "ModSys" / "Thirst" / "Thirst_ss.py"
    tip_message_server_path = behavior_root / "Diet_NullGr" / "ModSys" / "TipMessage" / "TipMessage_ss.py"
    diet_ui_logic_path = behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "DietUI.py"
    diet_ui_path = resource_root / "ui" / "diet_screen.json"

    assert_equal(config.serverSysKey[config.ssname], config.ssPath, "disease server config registration")
    assert_equal(config.clientSysKey[config.csname], config.csPath, "disease client config registration")
    assert_true(server_path.is_file() and client_path.is_file() and disease_config_path.is_file(), "disease module files exist")

    com_text = com_path.read_text(encoding="utf-8-sig")
    assert_true("serverSysKey.update(diseaseConfig.serverSysKey)" in com_text, "server registry includes disease")
    assert_true("serverSysKey.update(tipMessageConfig.serverSysKey)" in com_text,
                "server registry includes the shared tip service")
    assert_true("clientSysKey.update(diseaseConfig.clientSysKey)" in com_text, "client registry includes disease")
    assert_equal(
        tip_message_config.serverSysKey[tip_message_config.ssname],
        tip_message_config.ssPath,
        "tip message server config registration",
    )
    assert_true(tip_message_server_path.is_file(), "tip message server file exists")
    mod_main_text = mod_main_path.read_text(encoding="utf-8-sig")
    assert_true("serverApi.RegisterSystem(com.modName, key, com.serverSysKey[key])" in mod_main_text, "server registry is executed")
    assert_true("clientApi.RegisterSystem(com.modName, key, com.clientSysKey[key])" in mod_main_text, "client registry is executed")

    server_text = server_path.read_text(encoding="utf-8-sig")
    assert_equal(config.nauseaDuration, 4, "food-triggered constipation nausea remains four seconds")
    assert_equal(config.intermittentNauseaDuration, 10, "intermittent disease nausea lasts ten seconds")
    assert_equal(config.constipationMaximumBodyScale, 1.25, "constipation body scale remains unchanged")
    assert_equal(config.feverMaximumHeadScale, 2.5, "fever head scale reaches 2.5")
    assert_true("bodyScale += (config.constipationMaximumBodyScale - 1.0)" in server_text and
                "headScale += (config.feverMaximumHeadScale - 1.0)" in server_text,
                "server calculates constipation and fever visual limits independently")
    assert_equal(server_text.count("AddEffectToEntity('nausea', config.nauseaDuration"), 1,
                 "food-triggered nausea keeps its independent duration")
    assert_equal(server_text.count("AddEffectToEntity('nausea', config.intermittentNauseaDuration"), 1,
                 "intermittent nausea uses its dedicated duration")
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
    assert_true("ServerItemTryUseEvent" not in server_text and "debugItemEnabled" not in disease_config_path.read_text(encoding="utf-8-sig"),
                "temporary disease item shortcuts are removed")
    assert_equal(config.settingDef["key"], config.settingEnabledKey, "disease setting definition key")
    assert_true(config.settingDef["default"], "disease setting defaults to enabled")
    assert_true("config.settingEventUpdate" in server_text and "def DietSettingUpdate(" in server_text,
                "disease server listens to the shared setting event")
    assert_true("def _clearDiseaseSystemState(" in server_text and "Disease.clearAllDiseaseState(data)" in server_text,
                "disease setting closes persistent and runtime state together")
    assert_true("gameType == gameTypeEnum.Spectator" in server_text and
                "gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected" in server_text,
                "rickets symptoms follow the shared creative and spectator mode gate")
    assert_true("footBlockName in config.invalidBodyBlocks" in server_text,
                "constipation squat rejects water at the player's feet")
    assert_true("playerActionType.StartSwimming" in server_text and "playerActionType.StopSwimming" in server_text,
                "constipation squat tracks swimming state")
    assert_true("sneakingPlayers" not in server_text,
                "temporary sneak tracking is removed")
    assert_true("'sound': config.constipationReliefSound" in server_text,
                "successful constipation squat cure plays the configured sound")
    assert_true("tipMessageConfig.constipationProgressKey" in server_text and
                'serverApi.GenerateColor("GREEN") + "便秘缓解进度：{}/{}。"' in server_text and
                "self._queueTipMessage(" in server_text,
                "constipation squat progress enters the shared tip aggregation")
    assert_true("tipMessageSys.removeTip(playerId, tipMessageConfig.constipationProgressKey)" in server_text,
                "constipation cure removes stale pending squat progress")
    assert_true('_sendMessage(playerId, "便秘缓解进度' not in server_text,
                "constipation squat progress no longer fills chat")
    assert_true("'sound': config.ricketsFractureSound" in server_text and
                "'volume': config.ricketsFractureSoundVolume" in server_text and
                "'pitch': config.ricketsFractureSoundPitch" in server_text,
                "rickets jump injury plays the configured fracture sound")
    assert_true("mob.skeleton.hurt" not in server_text,
                "rickets no longer uses the vanilla skeleton hurt sound")
    assert_true("playerName = compFactory.CreateName(playerId).GetName()" in server_text and
                '"{}玩家拉了一坨大的".format(playerName)' in server_text and
                "for onlinePlayerId in serverApi.GetPlayerList():" in server_text and
                "tipMessageConfig.constipationBroadcastKeyPrefix + playerId" in server_text,
                "successful constipation squat cure queues one broadcast tip for every online player")

    feedback_source_text = "\n".join(
        path.read_text(encoding="utf-8-sig") for path in behavior_root.rglob("*.py")
    )
    for legacy_api in (
        "CreateMsg(",
        "NotifyOneMessage(",
        "SetNotifyMsg(",
        "SetTipMessage(",
        "SetOnePopupNotice(",
        "SetPopupNotice(",
    ):
        assert_true(legacy_api not in feedback_source_text,
                    "all player feedback removes legacy message API {}".format(legacy_api))
    assert_equal(feedback_source_text.count("SetOneTipMessage("), 1,
                 "all floating feedback shares one SetOneTipMessage output")
    tip_message_server_text = tip_message_server_path.read_text(encoding="utf-8-sig")
    assert_true("compGame.SetOneTipMessage(playerId, message)" in tip_message_server_text,
                "the aggregation service owns the only floating feedback output")

    diet_server_text = diet_server_path.read_text(encoding="utf-8-sig")
    diet_config_text = diet_config_path.read_text(encoding="utf-8-sig")
    diet_client_text = diet_client_path.read_text(encoding="utf-8-sig")
    assert_true("diseaseConfig.settingDef" in diet_config_text, "general settings include disease master switch")
    assert_true("settingKey in diseaseConfig.settingKeys" in diet_server_text,
                "Diet server delegates disease settings to the disease module")
    assert_true("diseaseConfig.ssname, config.settingEventSync" in diet_client_text,
                "general settings receive disease setting synchronization")
    for call_name in ("recordFoodEat", "queueMetabolism", "hasActiveDisease", "isSugarRushPaused"):
        assert_true("diseaseSys.{}(".format(call_name) in diet_server_text, "Diet integration {}".format(call_name))
    assert_true(diet_server_text.index("diseaseSys.recordFoodEat(") < diet_server_text.index("if not gainValues:"),
                "all successful food events reach disease symptoms before unclassified food exits")
    thirst_server_text = thirst_server_path.read_text(encoding="utf-8-sig")
    assert_true("diseaseSys.getThirstConsumptionMultiplier(playerId)" in thirst_server_text, "thirst multiplier integration")
    assert_true("def setSprintLimitSource(" in thirst_server_text, "shared sprint restriction source")
    assert_true("creativeModeAffected = False" in diet_config_text,
                "creative mode participation defaults to disabled")
    for mode_server_text, module_name in (
            (diet_server_text, "diet"),
            (thirst_server_text, "thirst"),
            (server_text, "disease")):
        assert_true('"GameTypeChangedServerEvent"' in mode_server_text,
                    "{} listens for immediate game mode cleanup".format(module_name))
        assert_true("gameTypeEnum.Spectator" in mode_server_text and
                    "creativeModeAffected" in mode_server_text,
                    "{} freezes spectator and optionally creative mode".format(module_name))
    assert_true("def _suspendPlayerRuntime(" in diet_server_text and
                "RemoveEffectFromEntity(effectName)" in diet_server_text,
                "diet mode cleanup removes configured rewards and penalties")
    assert_true("def _suspendDiseaseEffects(" in server_text and
                "clientData['active'] = []" in server_text and
                "'bodyScale': 1.0" in server_text and "'headScale': 1.0" in server_text,
                "disease mode cleanup suppresses symptoms and restores client visuals")
    assert_true("def setThirstValue(" in thirst_server_text and
                "gameType == gameTypeEnum.Creative and not dietConfig.creativeModeAffected" in thirst_server_text,
                "thirst public mutations honor the creative freeze")

    ui_data = json.loads(diet_ui_path.read_text(encoding="utf-8-sig"))
    ui_text = diet_ui_path.read_text(encoding="utf-8-sig")
    logic_text = diet_ui_logic_path.read_text(encoding="utf-8-sig")
    client_text = client_path.read_text(encoding="utf-8-sig")
    assert_true("thirstSys.setSprintLimitSource(" in server_text and
                "config.hypoglycemiaSprintLimitSource" in server_text,
                "hypoglycemia delegates sprint limiting to the shared thirst modifier")
    assert_true("EndSprinting" not in client_text,
                "hypoglycemia sprint limiting does not interrupt normal walking")
    assert_true("OnLocalPlayerActionClientEvent" not in client_text,
                "hypoglycemia does not maintain a separate client sprint interceptor")
    assert_true('"RemovePlayerAOIClientEvent"' in client_text, "disease client listens AOI removal")
    assert_true("def RemovePlayerAOIClientEvent(" in client_text, "disease client clears stale visual injection")
    assert_true("self.AddPlayerCreatedClientEvent({'playerId': playerId})" in client_text,
                "UI initialization restores local player render injection after addon reload")
    assert_true("SetEnableByName(" in client_text and "CheckEnabledByName(" in client_text and
                "SetParameter(" in client_text,
                "hypoglycemia uses the official custom postprocess control APIs")
    assert_true("config.hypoglycemiaVisionPostProcess" in client_text and
                "config.hypoglycemiaVisionStrengthParameter" in client_text,
                "hypoglycemia client controls the configured custom postprocess")
    assert_true("GaussianBlur" not in client_text and "gaussianBlur" not in disease_config_path.read_text(encoding="utf-8-sig"),
                "hypoglycemia no longer uses the built-in Gaussian blur")
    assert_true("self.renderedVisualData" in client_text and "config.visualScaleFadeTick" in client_text,
                "bone scale changes interpolate on the client")
    assert_true("('bodyScale', config.constipationMaximumBodyScale)" in client_text and
                "('headScale', config.feverMaximumHeadScale)" in client_text and
                "config.maximumBoneScale" not in client_text + server_text,
                "client interpolates each visual scale with its independent maximum")
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
    binding_names = (
        "title",
        "title_color",
        "row_bar_outline_visible",
        "row_bar_outline_color",
        "disease_button_visible",
        "disease_button_icon",
        "disease_button_click",
        "disease_panel_visible",
        "disease_icon",
        "disease_name",
        "disease_tips",
    )
    for binding_name in binding_names:
        full_name = "#diet_screen.{}".format(binding_name)
        assert_true(full_name in ui_text, "UI declares {}".format(full_name))
        assert_true(full_name in logic_text, "Python binds {}".format(full_name))
    assert_true('@ViewBinder.binding_collection(ViewBinder.BF_BindBool, "disease_grid", "#diet_screen.disease_button_visible")' in logic_text,
                "disease button visibility uses disease grid collection binding")
    assert_true('@ViewBinder.binding_collection(ViewBinder.BF_BindString, "disease_grid", "#diet_screen.disease_button_icon")' in logic_text,
                "disease button icon uses disease grid collection binding")
    assert_true('@ViewBinder.binding(ViewBinder.BF_ButtonClickUp, "#diet_screen.disease_button_click")' in logic_text and
                "args['#collection_index']" in logic_text,
                "disease button click receives its collection index")
    assert_true("self.selectedDiseaseId = ''" in logic_text and "if self.selectedDiseaseId == diseaseId:" in logic_text,
                "disease details default closed and toggle by disease ID")
    assert_true("self.selectedDiseaseData = self.emptyDiseaseData" in logic_text and
                "active[0]['id'] == self.selectedDiseaseId" in logic_text and
                "active[1]['id'] == self.selectedDiseaseId" in logic_text,
                "disease selection is precomputed by ID and closes when the selected disease disappears")
    assert_true("#diet_screen.effects" not in ui_text and "#diet_screen.effects" not in logic_text, "removed effects binding remains absent")
    assert_true("def UpdateDiseaseData(" in logic_text, "DietUI disease update entry")
    assert_true("diseaseClientSys.diseaseData" in logic_text, "DietUI reads cached disease data")
    assert_true("UpdateDiseaseData(self.diseaseData)" in client_text, "Disease client refreshes open DietUI")

    main = ui_data["main@common.base_screen"]
    screen_content = ui_data["netease_editor_root_panel_base_screen0"]
    root = find_named_control(screen_content, "root")
    title = find_named_control(root, "title")
    nutrition_grid = find_named_control(root, "rows_grid")
    disease_grid = find_named_control(root, "disease_grid")
    disease_panel = find_named_control(root, "disease_panel")
    disease_button = find_named_control(ui_data, "disease_button")
    disease_button_icon = find_named_control(disease_button, "image")
    bar_outline = find_named_control(ui_data, "bar_outline")
    disease_icon = find_named_control(disease_panel, "disease_icon")
    disease_name = find_named_control(disease_panel, "disease_name")
    disease_tips = find_named_control(disease_panel, "tips")

    assert_true("main" not in ui_data, "Diet main no longer uses a plain screen")
    assert_equal(main["$screen_content"], "diet_screen.netease_editor_root_panel_base_screen0",
                 "Diet main routes content through the base screen safe area")
    assert_true(main["$use_loading_bars"] is False, "Diet base screen disables loading bars")
    assert_equal(screen_content["type"], "panel", "Diet screen content remains a top-level panel")
    assert_equal(root["size"], [248, 148.0], "refactored Diet panel size remains unchanged")
    assert_equal(len(root["controls"]), 6, "refactored Diet panel control count remains unchanged")
    assert_equal(title["color"], [0.3058823529411765, 0.203921568627451, 0.1803921568627451],
                 "Diet title fallback color is deep brown #4E342E")
    assert_true("return (0.3058823529411765, 0.203921568627451, 0.1803921568627451)" in logic_text,
                "Diet title binding returns deep brown #4E342E")
    assert_equal(nutrition_grid["grid_dimensions"], [1, 5], "five nutrition rows remain")
    assert_equal(nutrition_grid["maximum_grid_items"], 5, "nutrition row limit")
    assert_equal(bar_outline["texture"], "textures/gui/diet_nullgr/outline", "nutrition outline texture")
    assert_equal(bar_outline["layer"], 2, "nutrition outline renders above the bar")
    assert_equal(bar_outline["visible"], "#diet_screen.row_bar_outline_visible", "nutrition outline visibility property")
    assert_equal(bar_outline["color"], "#diet_screen.row_bar_outline_color", "nutrition outline color property")
    assert_equal(bar_outline["bindings"], [
        {
            "binding_name_override": "#visible",
            "binding_collection_name": "diet_rows",
            "binding_condition": "always",
            "binding_type": "collection",
            "binding_name": "#diet_screen.row_bar_outline_visible",
        },
        {
            "binding_name_override": "#color",
            "binding_collection_name": "diet_rows",
            "binding_condition": "always",
            "binding_type": "collection",
            "binding_name": "#diet_screen.row_bar_outline_color",
        },
    ], "nutrition outline collection bindings")

    assert_equal(disease_grid["anchor_from"], "top_left", "disease grid source anchor remains unchanged")
    assert_equal(disease_grid["anchor_to"], "top_right", "disease grid target anchor remains unchanged")
    assert_equal(disease_grid["size"], [20.0, "default"], "disease grid size remains unchanged")
    assert_equal(disease_grid["layer"], 1, "disease grid layer remains unchanged")
    assert_equal(disease_grid["collection_name"], "disease_grid", "disease grid collection name")
    assert_equal(disease_grid["grid_dimensions"], [2, 2], "disease grid dimensions remain unchanged")
    assert_equal(disease_grid["grid_item_template"], "diet_screen.disease_button", "disease grid item template")
    assert_equal(disease_grid["grid_rescaling_type"], "horizontal", "disease grid rescaling remains unchanged")
    assert_equal(disease_grid["maximum_grid_items"], 2, "disease grid only exposes two disease icons")

    assert_equal(disease_button["size"], [20.0, 20.0], "disease button size remains unchanged")
    assert_equal(disease_button["layer"], 6, "disease button layer remains unchanged")
    assert_equal(len(disease_button["controls"]), 5, "disease button control count remains unchanged")
    assert_equal(disease_button["$pressed_button_name"], "#diet_screen.disease_button_click", "disease button click mapping")
    assert_true("button_mappings" not in disease_button, "disease button inherits common input mappings")
    assert_equal(disease_button["bindings"], [
        {
            "binding_type": "collection_details",
            "binding_collection_name": "disease_grid",
            "binding_condition": "always_when_visible",
        },
        {
            "binding_type": "collection",
            "binding_collection_name": "disease_grid",
            "binding_condition": "always",
            "binding_name": "#diet_screen.disease_button_visible",
            "binding_name_override": "#visible",
        },
    ], "disease button collection bindings")
    assert_equal(disease_button_icon["size"], [18.0, 18.0], "disease button icon size remains unchanged")
    assert_equal(disease_button_icon["layer"], 4, "disease button icon layer remains unchanged")
    assert_equal(disease_button_icon["bindings"], [{
        "binding_type": "collection",
        "binding_collection_name": "disease_grid",
        "binding_condition": "always",
        "binding_name": "#diet_screen.disease_button_icon",
        "binding_name_override": "#texture",
    }], "disease button icon collection binding")

    assert_equal(disease_panel["anchor_from"], "bottom_middle", "disease panel source anchor remains unchanged")
    assert_equal(disease_panel["anchor_to"], "top_middle", "disease panel target anchor remains unchanged")
    assert_equal(disease_panel["size"], ["100%+0px", 44.0], "disease panel size remains unchanged")
    assert_equal(disease_panel["layer"], 1, "disease panel layer remains unchanged")
    assert_equal(len(disease_panel["controls"]), 4, "disease panel control count remains unchanged")
    assert_equal(disease_panel["bindings"], [{
        "binding_condition": "always",
        "binding_name": "#diet_screen.disease_panel_visible",
        "binding_name_override": "#visible",
    }], "disease panel visibility binding")
    assert_equal([disease_icon["anchor_from"], disease_icon["anchor_to"], disease_icon["offset"], disease_icon["size"], disease_icon["layer"]],
                 ["top_left", "top_left", [5.0, 5.0], [18.0, 18.0], 2], "detail icon layout remains unchanged")
    assert_equal([disease_name["anchor_from"], disease_name["anchor_to"], disease_name["offset"], disease_name["layer"]],
                 ["top_left", "top_left", [25.0, 5.0], 4], "detail name layout remains unchanged")
    assert_equal([disease_tips["anchor_from"], disease_tips["anchor_to"], disease_tips["offset"], disease_tips["size"], disease_tips["layer"]],
                 ["top_left", "top_left", [5.0, 24.0], ["100%+-12px", 16.0], 5], "detail tips layout remains unchanged")
    full_icon_name = "#diet_screen.disease_icon"
    assert_equal(disease_icon["texture"], full_icon_name, "disease_icon display property binding")
    assert_equal(disease_icon["bindings"], [{
        "binding_condition": "always",
        "binding_name": full_icon_name,
        "binding_name_override": "#texture",
    }], "disease_icon detail binding")

    for control, binding_name in (
        (disease_name, "disease_name"),
        (disease_tips, "disease_tips"),
    ):
        full_name = "#diet_screen.{}".format(binding_name)
        assert_equal(control["text"], full_name, "{} display property binding".format(binding_name))
        assert_equal(control["bindings"], [{
            "binding_condition": "always",
            "binding_name": full_name,
        }], "{} detail binding".format(binding_name))

    for slot_index in range(2):
        template_name = "disease_slot_{}".format(slot_index)
        assert_true(template_name in ui_data, "disease slot {} template".format(slot_index))
        assert_true(find_named_control(root, template_name) is None,
                    "legacy disease slot {} template is not instantiated".format(slot_index))
    assert_true("refreshDiseaseOutlineStates" in logic_text and "diseaseOutline" in logic_text and
                "diseaseHighOutlineColor" in logic_text and "diseaseLowOutlineColor" in logic_text,
                "nutrition rows bind precomputed high and low disease outlines")
    assert_true("diseaseRelated" not in logic_text and "diseaseGroupHighlightColor" not in logic_text and
                "diseaseGroupTooltipColor" not in logic_text,
                "disease outlines do not recolor nutrition text or bar fill")


def test_disease_ui_detail_binding_reads_precomputed_selection():
    diet_ui_logic_path = behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "DietUI.py"
    source = diet_ui_logic_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(diet_ui_logic_path))
    diet_ui_class = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "DietUI")
    method_names = {
        "UpdateDiseaseData",
        "selectDiseaseButton",
        "bindDiseasePanelVisible",
        "bindDiseaseIcon",
        "bindDiseaseName",
        "bindDiseaseTips",
    }
    method_nodes = []
    for node in diet_ui_class.body:
        if isinstance(node, ast.FunctionDef) and node.name in method_names:
            node.decorator_list = []
            method_nodes.append(node)

    class ViewRequestStub(object):
        Nothing = "nothing"
        Refresh = "refresh"

    method_module = ast.Module(body=method_nodes, type_ignores=[])
    ast.fix_missing_locations(method_module)
    namespace = {"ViewRequest": ViewRequestStub}
    exec(compile(method_module, str(diet_ui_logic_path), "exec"), namespace)
    update_disease_data = namespace["UpdateDiseaseData"]
    select_disease_button = namespace["selectDiseaseButton"]
    bind_disease_panel_visible = namespace["bindDiseasePanelVisible"]
    bind_disease_icon = namespace["bindDiseaseIcon"]
    bind_disease_name = namespace["bindDiseaseName"]
    bind_disease_tips = namespace["bindDiseaseTips"]

    class UiState(object):
        def refreshDiseaseOutlineStates(self):
            self.outlineStatesRefreshed = True

        def UpdateScreen(self, force):
            self.screenRefreshForce = force

    first = {
        "id": "hypoglycemia",
        "icon": "textures/ui/diet_nullgr/disease/hypoglycemia_effect",
        "name": "低血糖",
        "tips": "能量不足；吃主食、水果或甜食",
    }
    second = {
        "id": "scurvy",
        "icon": "textures/ui/diet_nullgr/disease/scurvy_effect",
        "name": "坏血病",
        "tips": "水果蔬菜不足；补充水果或蔬菜",
    }
    state = UiState()
    state.emptyDiseaseData = {"id": ""}
    state.selectedDiseaseData = first
    state.selectedDiseaseId = "hypoglycemia"
    state.diseaseData = None
    assert_true(bind_disease_panel_visible(state), "selected disease opens the detail panel")
    assert_equal(bind_disease_icon(state), first["icon"], "detail icon reads the precomputed selection")
    assert_equal(bind_disease_name(state), first["name"], "detail name reads the precomputed selection")
    assert_equal(bind_disease_tips(state), first["tips"], "detail tips read the precomputed selection")

    state.selectedDiseaseId = "scurvy"
    state.selectedDiseaseData = second
    update_disease_data(state, {"active": [second, first]})
    assert_true(state.selectedDiseaseData is second and state.selectedDiseaseId == "scurvy",
                "selected disease survives a collection reorder by ID")
    update_disease_data(state, {"active": [first]})
    assert_true(state.selectedDiseaseData is state.emptyDiseaseData and state.selectedDiseaseId == "",
                "selected disease recovery closes details instead of switching rows")
    assert_true(state.outlineStatesRefreshed and state.screenRefreshForce,
                "disease synchronization refreshes outline states and bindings")

    state.diseaseData = {"active": [first, second]}
    assert_equal(select_disease_button(state, {"#collection_index": 0}), ViewRequestStub.Refresh,
                 "first disease button requests a binding refresh")
    assert_true(state.selectedDiseaseData is first and state.selectedDiseaseId == "hypoglycemia",
                "first disease button selects its disease ID and row")
    select_disease_button(state, {"#collection_index": 1})
    assert_true(state.selectedDiseaseData is second and state.selectedDiseaseId == "scurvy",
                "second disease button switches details directly")
    select_disease_button(state, {"#collection_index": 1})
    assert_true(state.selectedDiseaseData is state.emptyDiseaseData and state.selectedDiseaseId == "",
                "clicking the selected disease again closes details")


def test_disease_nutrition_outline_state():
    diet_ui_logic_path = behavior_root / "Diet_NullGr" / "ModSys" / "Diet" / "DietUI.py"
    source = diet_ui_logic_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(diet_ui_logic_path))
    diet_ui_class = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "DietUI")
    method_names = {
        "getGroupData",
        "refreshDiseaseOutlineStates",
        "bindRowBarOutlineVisible",
        "bindRowBarOutlineColor",
    }
    method_nodes = []
    for node in diet_ui_class.body:
        if isinstance(node, ast.FunctionDef) and node.name in method_names:
            node.decorator_list = []
            method_nodes.append(node)
    method_module = ast.Module(body=method_nodes, type_ignores=[])
    ast.fix_missing_locations(method_module)
    namespace = {"config": diet_config}
    exec(compile(method_module, str(diet_ui_logic_path), "exec"), namespace)
    refresh_outline_states = namespace["refreshDiseaseOutlineStates"]

    class UiState(object):
        getGroupData = namespace["getGroupData"]

    state = UiState()
    state.dietData = {
        "groups": [
            {"id": "fruits", "tracked": True, "diseaseOutline": "stale"},
            {"id": "grains", "tracked": True, "diseaseOutline": "stale"},
            {"id": "proteins", "tracked": True, "diseaseOutline": "stale"},
            {"id": "vegetables", "tracked": True, "diseaseOutline": "stale"},
            {"id": "sugars", "tracked": True, "diseaseOutline": "stale"},
        ]
    }
    state.diseaseData = {
        "active": [
            {"lowGroups": ["fruits", "grains"], "highGroups": []},
            {"lowGroups": ["proteins"], "highGroups": ["sugars"]},
        ]
    }
    refresh_outline_states(state)
    assert_equal(
        [group["diseaseOutline"] for group in state.dietData["groups"]],
        ["low", "low", "low", "", "high"],
        "two diseases merge low and high nutrition outline states",
    )
    assert_true(namespace["bindRowBarOutlineVisible"](state, 0), "low disease outline is visible")
    assert_equal(namespace["bindRowBarOutlineColor"](state, 0),
                 diet_config.diseaseLowOutlineColor,
                 "low disease outline uses #4ee8ff")
    assert_true(namespace["bindRowBarOutlineVisible"](state, 4), "high disease outline is visible")
    assert_equal(namespace["bindRowBarOutlineColor"](state, 4),
                 diet_config.diseaseHighOutlineColor,
                 "high disease outline uses #ff401a")
    assert_true(not namespace["bindRowBarOutlineVisible"](state, 3), "unrelated nutrition outline stays hidden")

    state.dietData["groups"][4]["tracked"] = False
    assert_true(not namespace["bindRowBarOutlineVisible"](state, 4), "disabled nutrition outline stays hidden")

    state.diseaseData = {"active": []}
    refresh_outline_states(state)
    assert_true(
        all(not group["diseaseOutline"] for group in state.dietData["groups"]),
        "healthy state hides every nutrition outline",
    )


def test_low_penalty_effect_message():
    class EffectStub(object):
        def __init__(self):
            self.calls = []

        def AddEffectToEntity(self, name, duration, amplifier, show_particles):
            self.calls.append((name, duration, amplifier, show_particles))

    class CompFactoryStub(object):
        def __init__(self):
            self.effect = EffectStub()

        def CreateEffect(self, player_id):
            return self.effect

    data = {
        "values": {
            "fruits": 0.10,
            "grains": 0.50,
            "proteins": 0.05,
            "vegetables": 0.50,
            "sugars": 0.50,
        },
        "tracking": {
            "fruits": True,
            "grains": True,
            "proteins": True,
            "vegetables": True,
            "sugars": True,
        },
        "effectSettings": {
            "balanced": False,
            "sugarRush": False,
        },
        "penaltySettings": {
            "singleLowNutrition": True,
            "multipleLowNutrition": True,
        },
        "targetDietValue": 0.80,
        "lowPenaltyEnabled": True,
        "nutritionPenaltyValue": 0.15,
    }
    comp_factory = CompFactoryStub()
    matched_results = Diet.applyEffects("player", data, comp_factory)
    assert_equal(
        comp_factory.effect.calls,
        [("weakness", 6, 0, True), ("slowness", 6, 0, True)],
        "two low nutrition groups apply weakness and slowness",
    )
    message = Diet.buildLowPenaltyEffectMessage(data, matched_results)
    assert_equal(message, "营养不足，请及时补充水果、蛋白质。", "message only names low nutrition groups")

    disease_results = Diet.applyEffects("player", data, comp_factory, diseaseActive=True)
    assert_equal(disease_results, [], "active disease suppresses ordinary low penalties")
    assert_equal(Diet.buildLowPenaltyEffectMessage(data, disease_results), "", "suppressed penalties send no duplicate reminder")


def test_tip_message_aggregation():
    state = TipMessage.createPlayerState()
    TipMessage.queueMessage(
        state,
        100,
        tip_message_config.dietFoodGainKey,
        "§a补充了水果。",
        tip_message_config.priorityNormal,
    )
    TipMessage.queueMessage(
        state,
        109,
        tip_message_config.dietFoodWarningKey,
        "§e谷物偏低。",
        tip_message_config.priorityWarning,
    )
    assert_equal(state["firstPendingTick"], 100, "later messages do not extend the fixed merge window")
    assert_equal(TipMessage.takeReadyMessage(state, 109), "", "fixed merge window waits ten ticks")
    assert_equal(
        TipMessage.takeReadyMessage(state, 110),
        "§e谷物偏低。\n§a补充了水果。",
        "one batch merges messages by priority instead of overwriting the first tip",
    )
    assert_equal(state["visibleUntilTick"], 160, "display lock protects the visible tip")

    TipMessage.queueMessage(
        state,
        111,
        tip_message_config.constipationProgressKey,
        "§a便秘缓解进度：1/12。",
        tip_message_config.priorityProgress,
    )
    TipMessage.queueMessage(
        state,
        112,
        tip_message_config.constipationProgressKey,
        "§a便秘缓解进度：2/12。",
        tip_message_config.priorityProgress,
    )
    assert_equal(len(state["pendingMessages"]), 1, "repeated semantic keys replace pending content")
    assert_equal(TipMessage.takeReadyMessage(state, 121), "", "pending batch cannot overwrite the visible tip")
    assert_equal(
        TipMessage.takeReadyMessage(state, 160),
        "§a便秘缓解进度：2/12。",
        "the latest repeated progress appears as soon as the display lock ends",
    )

    stale_progress_state = TipMessage.createPlayerState()
    TipMessage.queueMessage(
        stale_progress_state,
        0,
        tip_message_config.dietFoodGainKey,
        "§a补充了蔬菜。",
        tip_message_config.priorityNormal,
    )
    TipMessage.takeReadyMessage(stale_progress_state, tip_message_config.mergeWindowTick)
    TipMessage.queueMessage(
        stale_progress_state,
        11,
        tip_message_config.constipationProgressKey,
        "§a便秘缓解进度：11/12。",
        tip_message_config.priorityProgress,
    )
    TipMessage.removeMessage(stale_progress_state, tip_message_config.constipationProgressKey)
    TipMessage.queueMessage(
        stale_progress_state,
        12,
        tip_message_config.diseaseChangeKey,
        "§a便秘已经缓解。",
        tip_message_config.priorityImportant,
    )
    assert_equal(
        TipMessage.takeReadyMessage(stale_progress_state, 60),
        "§a便秘已经缓解。",
        "curing constipation cancels stale pending squat progress",
    )

    overflow_state = TipMessage.createPlayerState()
    overflow_messages = (
        ("low", "§7低优先级。", tip_message_config.priorityProgress),
        ("normal", "§a普通。", tip_message_config.priorityNormal),
        ("warning", "§e警告。", tip_message_config.priorityWarning),
        ("important", "§c重要。", tip_message_config.priorityImportant),
        ("normal_extra", "§b次要。", tip_message_config.priorityNormal),
    )
    for message_key, message, priority in overflow_messages:
        TipMessage.queueMessage(overflow_state, 0, message_key, message, priority)
    assert_equal(
        TipMessage.takeReadyMessage(overflow_state, tip_message_config.mergeWindowTick),
        "§c重要。\n§e警告。\n§a普通。\n§b次要。\n§7另有1条提示。",
        "overflow keeps four highest-priority messages and adds a compact summary",
    )


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
    python_paths.extend((behavior_root / "Diet_NullGr" / "ModSys" / "TipMessage").glob("*.py"))
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
        test_client_tips_contract,
        test_diet_tooltip_removal_contract,
        test_diet_initialization_persistence_and_death_boundary,
        test_disease_master_switch_state,
        test_new_player_protection,
        test_two_slots_and_half_progress_cap,
        test_blood_sugar_mutual_exclusion,
        test_constipation_squat_and_timeout_cure,
        test_recovery_transactions,
        test_resources_and_languages,
        test_hypoglycemia_custom_postprocess_resources,
        test_system_registration_and_ui_bindings,
        test_disease_ui_detail_binding_reads_precomputed_selection,
        test_disease_nutrition_outline_state,
        test_low_penalty_effect_message,
        test_tip_message_aggregation,
        test_modsdk_import_whitelist,
    ]
    for test in tests:
        test()
        print("PASS {}".format(test.__name__))
    print("Disease system regression test passed: {} groups".format(len(tests)))


if __name__ == "__main__":
    main()
