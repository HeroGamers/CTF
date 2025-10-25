@tool
extends Panel
signal changed()
var __XjVL : ConfigFile
var __H0aA : bool = false
@onready var __oTE5 : CheckBox = $ScrollContainer/VBoxContainer/InlineConstants/CheckBox
@onready var __tmS4 : CheckBox = $ScrollContainer/VBoxContainer/InlineEnums/CheckBox
@onready var __z9tJ : CheckBox = $ScrollContainer/VBoxContainer/ObfuscateExportVars/CheckBox
@onready var __UC6a : CheckBox = $ScrollContainer/VBoxContainer/ObfuscateSignals/CheckBox
@onready var __gPyy : LineEdit = $ScrollContainer/VBoxContainer/IDPrefix/LineEdit
@onready var __YOYe : LineEdit = $ScrollContainer/VBoxContainer/IDCharacterList/LineEdit
@onready var __mJe0 : SpinBox = $ScrollContainer/VBoxContainer/IDTargetLength/SpinBox
@onready var __o3dA : SpinBox = $ScrollContainer/VBoxContainer/GeneratorSeed/SpinBox
@onready var __Iw3L : CheckBox = $ScrollContainer/VBoxContainer/DynamicSeed/CheckBox
@onready var __RQvl : CheckBox = $ScrollContainer/VBoxContainer/StripComments/CheckBox
@onready var __U_QP : CheckBox = $ScrollContainer/VBoxContainer/StripEmptyLines/CheckBox
@onready var __hzM8 : CheckBox = $ScrollContainer/VBoxContainer/FeatureFilters/CheckBox
@onready var __G_R4 : LineEdit = $ScrollContainer/VBoxContainer/DebugScripts/LineEdit
@onready var __yu8j : LineEdit = $ScrollContainer/VBoxContainer/DebugResources/LineEdit
@onready var __FikY : CheckBox = $ScrollContainer/VBoxContainer/ObfuscateDebugOnly/CheckBox
func _ready() -> void:
	__4gOn()
func __rJtr(__LYSP : ConfigFile) -> void:
	self.__XjVL = __LYSP
func __4gOn() -> void:
	if !__XjVL:
		return
	__oTE5.button_pressed = __XjVL.get_value("obfuscator", "inline_consts", false)
	__tmS4.button_pressed = __XjVL.get_value("obfuscator", "inline_enums", false)
	__z9tJ.button_pressed = __XjVL.get_value("obfuscator", "export_vars", false)
	__UC6a.button_pressed = __XjVL.get_value("obfuscator", "signals", false)
	__gPyy.text = __XjVL.get_value("id", "prefix", "")
	__YOYe.text = __XjVL.get_value("id", "character_list", "")
	__mJe0.value = __XjVL.get_value("id", "target_length", 0)
	__o3dA.value = __XjVL.get_value("id", "seed", 0)
	__Iw3L.button_pressed = __XjVL.get_value("id", "dynamic_seed", false)
	__RQvl.button_pressed = __XjVL.get_value("post_process", "strip_comments", false)
	__U_QP.button_pressed = __XjVL.get_value("post_process", "strip_empty_lines", false)
	__hzM8.button_pressed = __XjVL.get_value("post_process", "feature_filters", false)
	__G_R4.text = __XjVL.get_value("debug", "debug_scripts", "")
	__yu8j.text = __XjVL.get_value("debug", "debug_resources", "")
	__FikY.button_pressed = __XjVL.get_value("debug", "obfuscate_debug_only", false)
func __5Fs7(__1weX : bool = false) -> void:
	if !__XjVL or (__H0aA and !__1weX):
		return
	__H0aA = true
	await get_tree().process_frame
	__XjVL.set_value("obfuscator", "inline_consts", __oTE5.button_pressed)
	__XjVL.set_value("obfuscator", "inline_enums", __tmS4.button_pressed)
	__XjVL.set_value("obfuscator", "export_vars", __z9tJ.button_pressed)
	__XjVL.set_value("obfuscator", "signals", __UC6a.button_pressed)
	__XjVL.set_value("id", "prefix", __gPyy.text)
	__XjVL.set_value("id", "character_list", __YOYe.text)
	__XjVL.set_value("id", "target_length", __mJe0.value)
	__XjVL.set_value("id", "seed", __o3dA.value)
	__XjVL.set_value("id", "dynamic_seed", __Iw3L.button_pressed)
	__XjVL.set_value("post_process", "strip_comments", __RQvl.button_pressed)
	__XjVL.set_value("post_process", "strip_empty_lines", __U_QP.button_pressed)
	__XjVL.set_value("post_process", "feature_filters", __hzM8.button_pressed)
	__XjVL.set_value("debug", "debug_scripts", __G_R4.text)
	__XjVL.set_value("debug", "debug_resources", __yu8j.text)
	__XjVL.set_value("debug", "obfuscate_debug_only", __FikY.button_pressed)
	changed.emit()
	__H0aA = false
func __ARiR(__rs4s : bool) -> void:
	__5Fs7()
func __kTUL(__vPC1 : String) -> void:
	__5Fs7()
func __mu0z(value : float) -> void:
	__5Fs7()
