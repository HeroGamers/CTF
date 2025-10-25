@tool
extends EditorPlugin
var __XjVL := ConfigFile.new()
var __rzDl : EditorExportPlugin
var __ZIj_ : Control
func _enter_tree() -> void:
	name = "GDMaim"
	__XjVL.set_value("obfuscator", "inline_consts", true)
	__XjVL.set_value("obfuscator", "inline_enums", true)
	__XjVL.set_value("obfuscator", "export_vars", true)
	__XjVL.set_value("obfuscator", "signals", true)
	__XjVL.set_value("id", "prefix", "__")
	__XjVL.set_value("id", "character_list", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
	__XjVL.set_value("id", "target_length", 4)
	__XjVL.set_value("id", "seed", 0)
	__XjVL.set_value("id", "dynamic_seed", false)
	__XjVL.set_value("post_process", "strip_comments", true)
	__XjVL.set_value("post_process", "strip_empty_lines", true)
	__XjVL.set_value("post_process", "feature_filters", true)
	__XjVL.set_value("debug", "debug_scripts", "")
	__XjVL.set_value("debug", "debug_resources", "")
	__XjVL.set_value("debug", "obfuscate_debug_only", false)
	__Ij7I()
	__rzDl = preload("export_plugin.gd").new()
	__rzDl.__XjVL = __XjVL
	add_export_plugin(__rzDl)
	__ZIj_ = preload("ui/dock.tscn").instantiate()
	__ZIj_.__rJtr(__XjVL)
	__ZIj_.changed.connect(__KNmy)
	add_control_to_dock(DOCK_SLOT_LEFT_BR, __ZIj_)
func _exit_tree() -> void:
	remove_export_plugin(__rzDl)
	__ZIj_.__5Fs7(true)
	__ZIj_.queue_free()
func __8Q7t() -> String:
	return get_script().resource_path.get_base_dir()
func __Ij7I() -> void:
	__XjVL.load(__8Q7t() + "/export.cfg")
func __KNmy() -> void:
	if !DirAccess.dir_exists_absolute(__8Q7t()):
		DirAccess.make_dir_recursive_absolute(__8Q7t())
	__XjVL.save(__8Q7t() + "/export.cfg")
