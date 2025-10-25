extends EditorExportPlugin
const __2ayH := preload("script_data.gd")
const __tQfG := preload("symbol_table.gd")
const __EGAL := preload("parser.gd")
var __XjVL : ConfigFile
var __Jndm : PackedStringArray
var __xy8o : bool
var __xjNI : bool
var __VFhV : String
var __KG73 : Dictionary
var __GwGx : Dictionary
var __hFn4 : Dictionary
var __eyvh : __tQfG
var __V4Rv : Dictionary
var __0ETJ : Dictionary
var __08u7 : Dictionary
var __YTf7 : Dictionary
var __MUJV : bool
var __byWh : bool
var __NAGG : bool
var __IHIq : bool
var __oUrD : String
var __hFwD : String
var __k1hG : int
var __RK_0 : int
var __OTDw : bool
var __60BK : bool
var __hFzk : bool
var __3w0u : bool
var __bnJE : PackedStringArray
var __fqm3 : PackedStringArray
var __cRWp : bool
func _get_name() -> String:
	return "gdmaim"
func _export_begin(__zNdd : PackedStringArray, __grBT : bool, path : String, flags : int) -> void:
	__Jndm = __zNdd
	__VFhV = path
	__xy8o = !__zNdd.has("no_gdmaim")
	if !__xy8o:
		return
	__MUJV = __XjVL.get_value("obfuscator", "inline_consts", false)
	__byWh = __XjVL.get_value("obfuscator", "inline_enums", false)
	__NAGG = __XjVL.get_value("obfuscator", "export_vars", false)
	__IHIq = __XjVL.get_value("obfuscator", "signals", false)
	__oUrD = __XjVL.get_value("id", "prefix", "")
	__hFwD = __XjVL.get_value("id", "character_list", "")
	__k1hG = __XjVL.get_value("id", "target_length", 0)
	__OTDw = __XjVL.get_value("id", "dynamic_seed", false)
	__RK_0 = __XjVL.get_value("id", "seed", 0) if !__OTDw else int(Time.get_unix_time_from_system())
	__60BK = __XjVL.get_value("post_process", "strip_comments", false)
	__hFzk = __XjVL.get_value("post_process", "strip_empty_lines", false)
	__3w0u = __XjVL.get_value("post_process", "feature_filters", false)
	__bnJE = __XjVL.get_value("debug", "debug_scripts", "").split(",", false)
	__fqm3 = __XjVL.get_value("debug", "debug_resources", "").split(",", false)
	__cRWp = __XjVL.get_value("debug", "obfuscate_debug_only", false)
	__xjNI = ProjectSettings.get_setting("editor/export/convert_text_resources_to_binary", false)
	if __xjNI:
		push_warning("GDMaim: the project setting 'editor/export/convert_text_resources_to_binary' is enabled, but will be ignored during export")
	__oXcO()
func _export_end() -> void:
	if !__xy8o:
		return
	var __eqEj : String
	for symbol in __eyvh.__5Ws3:
		__eqEj += __eyvh.__5Ws3[symbol].name + "=" + symbol + "\n"
	if __Uh6b(__VFhV.get_basename() + "_symbols.txt", __eqEj):
		print("GDMaim - a list of all identifiers and their generated names has been saved to '" + __VFhV.get_basename() + "_symbols.txt'")
	else:
		push_warning("GDMaim - failed to write symbol table to '" + __VFhV.get_basename() + "_symbols.txt'!")
func _export_file(path : String, type : String, __705n : PackedStringArray) -> void:
	if !__xy8o:
		return
	var __S7Eh : String = path.get_extension()
	if __S7Eh == "csv":
		skip() 
	elif __S7Eh == "ico":
		skip() 
		add_file(path, FileAccess.get_file_as_bytes(path), true) 
	elif __S7Eh == "tres" or __S7Eh == "tscn":
		if __NAGG or __S7Eh == "tscn":
			var data : String = __wqGl(path, FileAccess.get_file_as_string(path))
			add_file(path, data.to_utf8_buffer(), true)
	elif __S7Eh == "gd":
		var code : String = __U7Ll(path)
		add_file(path, code.to_utf8_buffer(), true)
func __oXcO() -> void:
	var __xNsA : PackedStringArray = __kJy4("res://", ".gd")
	__YTf7.clear()
	__GwGx.clear()
	__hFn4.clear()
	var __rldt : ConfigFile = ConfigFile.new()
	__rldt.load("res://project.godot")
	for ___4Yj : String in __rldt.get_section_keys("autoload"):
		__GwGx[__rldt.get_value("autoload", ___4Yj).replace("*", "")] = ___4Yj
	var __1xby : Script = preload("builtins.gd")
	for global in __1xby.__Ay4a:
		__hFn4[global] = global
	for variant in __1xby.__FPdI:
		if variant.has("class"):
			__hFn4[variant["class"]] = variant["class"]
		for signal_ in variant.get("signals", []):
			__hFn4[signal_] = signal_
		for var_ in variant.get("properties", []):
			__hFn4[var_] = var_
		for func_ in variant.get("methods", []):
			__hFn4[func_] = func_
	for class_ in ClassDB.get_class_list():
		for symbol in __t7V0(class_):
			__hFn4[symbol] = symbol
	__eyvh = __tQfG.new(hash(str(__RK_0)), true, __hFn4)
	__eyvh.__2cVH = self
	__0ETJ.clear()
	for path in __xNsA:
		__z5Bn(path)
	for symbol in __eyvh.__5Ws3:
		var __M8aX : PackedStringArray = symbol.split(".")
		var __b5Iz : PackedStringArray = __eyvh.__5Ws3[symbol].name.split(".")
		var __pJu2 : String
		for i in __M8aX.size():
			if __hFn4.has(__M8aX[i]):
				__pJu2 += ("." if __pJu2 else "") + __hFn4[__M8aX[i]]
			elif __M8aX.size() == __b5Iz.size():
				__pJu2 += ("." if __pJu2 else "") + __b5Iz[i]
			else:
				__pJu2 = __eyvh.__5Ws3[symbol].name
				break
		__eyvh.__5Ws3[symbol].name = __pJu2
	var __nwy0 : Dictionary
	for constant in __V4Rv:
		__3XXz(constant, __V4Rv, __nwy0)
func __3XXz(constant : String, __wuqH : Dictionary, ___nrb : Dictionary):
	if ___nrb.has(constant):
		return ___nrb[constant]
	var path : String = constant.substr(0, constant.rfind("."))
	var __C4zc : String = __wuqH[constant].name
	var __sYph : PackedStringArray = __zHuL(__C4zc, "+-*/(),")
	var __CAGV : PackedStringArray
	var __f18g : Array
	if __C4zc.contains(constant):
		___nrb[constant] = __C4zc
		return ___nrb[constant]
	for token in __sYph:
		var __o9GU : String = token
		if token and !token.contains(".") and !"01234567890".contains(token[0]):
			token = path + "." + token
		if __wuqH.has(token):
			__CAGV.append(__o9GU)
			__f18g.append(__3XXz(token, __wuqH, ___nrb))
	var __tBFs := Expression.new()
	__tBFs.parse(__C4zc, __CAGV)
	var __1H0x = __tBFs.execute(__f18g, null, false, true)
	if __tBFs.has_execute_failed():
		___nrb[constant] = __C4zc
		return __C4zc
	var __gQ1D : __tQfG.__LGoC = __wuqH[constant]
	match __gQ1D.type:
		"bool": __gQ1D.name = str(bool(__1H0x))
		"Color": __gQ1D.name = "Color" + str(Color(__1H0x))
		"float": __gQ1D.name = str(__1H0x) if str(__1H0x).contains(".") else str(__1H0x) + ".0"
		"int": __gQ1D.name = str(int(__1H0x))
		"NodePath": __gQ1D.name = 'NodePath("' + str(NodePath(__1H0x)) + '")'
		"Vector2": __gQ1D.name = "Vector2" + str(Vector2(__1H0x))
		"Vector2i": __gQ1D.name = "Vector2i" + str(Vector2i(__1H0x))
		"Vector3": __gQ1D.name = "Vector3" + str(Vector3(__1H0x))
		"Vector3i": __gQ1D.name = "Vector3i" + str(Vector3i(__1H0x))
		"Vector4": __gQ1D.name = "Vector4" + str(Vector4(__1H0x))
		"Vector4i": __gQ1D.name = "Vector4i" + str(Vector4i(__1H0x))
		_: pass
	__gQ1D.get_meta("member").name = __gQ1D.name
	___nrb[constant] = __1H0x
	return __1H0x
func __t7V0(__I0AY : String) -> PackedStringArray:
	var __gCap : PackedStringArray
	__gCap.append(__I0AY)
	for signal_ in ClassDB.class_get_signal_list(__I0AY, true):
		__gCap.append(signal_.name)
	for const_ in ClassDB.class_get_integer_constant_list(__I0AY, true):
		__gCap.append(const_)
	for var_ in ClassDB.class_get_property_list(__I0AY, true):
		const __ivhI : PackedInt32Array = [64]
		if !__ivhI.has(var_.usage):
			__gCap.append(var_.name)
	for func_ in ClassDB.class_get_method_list(__I0AY, true):
		__gCap.append(func_.name)
	return __gCap
func __z5Bn(path : String) -> void:
	if __8x5w(path):
		print("\n---------- ", "PARSE SCRIPT ", path, " ----------\n")
	var __vOik : Script = load(path)
	var source_code : String = __vOik.source_code
	var __gMOU : Dictionary
	for method in __vOik.get_script_method_list():
		__gMOU[method.name] = method
	var __k3vc : Dictionary
	for signal_ in __vOik.get_script_signal_list():
		__k3vc[signal_.name] = signal_
	__eyvh.__TZWU = true
	var __qxbG : bool = __GwGx.has(path)
	var __Blaq : String = __GwGx.get(path, path.get_file().replace(".", "_"))
	var __aR49 : String = __Blaq + "."
	var __Gop4 : Array[int]
	var __xkEg : int = 0
	var ___KZR : Array
	var __OU3p : Array = ___KZR
	var __LKZ6 : Array[int]
	var __KlZk : String = ""
	var __OotC : bool = false
	var __aLtN : bool = false
	var __YlQ6 : PackedStringArray = source_code.split("\n")
	var __bMcP : __2ayH = __2ayH.new(hash(path + str(__RK_0)), __hFn4)
	__bMcP.__2cVH = self
	__bMcP.__5_qo.__2cVH = self
	__bMcP.path = path
	__bMcP.__Rlpa = __vOik.get_base_script().resource_path if __vOik.get_base_script() else ""
	__bMcP.___4Yj = __qxbG
	__bMcP.code = source_code
	__bMcP.__obaI = __YlQ6
	__0ETJ[path] = __bMcP
	const __mx4O : Dictionary = {
		NONE = 0,
		VAR = 1,
		FUNC = 2,
		CLASS = 3,
		CLASS_NAME = 4,
		SIGNAL = 5,
		ENUM = 6,
		ENUM_VALUES = 7,
		ENUM_VALUE_ASSIGNMENT = 8,
		CONST = 9,
		PARAMS = 10,
		PARAMS_HINT = 11,
		STRING = 12,
	}
	const __E5dp : Dictionary = {
		"var": __mx4O.VAR,
		"func": __mx4O.FUNC,
		"class": __mx4O.CLASS,
		"class_name": __mx4O.CLASS_NAME,
		"signal": __mx4O.SIGNAL,
		"enum": __mx4O.ENUM,
		"const": __mx4O.CONST,
		"'": __mx4O.STRING,
		"\"": __mx4O.STRING,
	}
	var __FUAJ : int = __mx4O.NONE
	var __Kbrz : String
	var __U01n : int = 0
	var __T2S3 : String
	var __U1AV : String
	var __pCTt : int
	var __LCk9 : int = -1
	var __E9SI : PackedStringArray
	var __tR_v : Dictionary
	var __a_C_ : Dictionary
	for line in __YlQ6:
		var __Mx2H := __EGAL.new(line)
		var __f9jX : int = __Mx2H.__MzuD()
		var __8zpr : PackedStringArray = __Mx2H.__jN2c()
		var __HJ12 : PackedStringArray = __Mx2H.__sh6w
		var __Pn_e : int = __bMcP.get_line_count()
		if line.begins_with("##OBFUSCATE ") and __8zpr.size() >= 4:
			if __8zpr[3] == "true":
				__eyvh.__TZWU = true
			elif __8zpr[3] == "false":
				__eyvh.__TZWU = false
			__bMcP.__5_qo.__TZWU = __eyvh.__TZWU
			if __8x5w(path):
				prints(__Pn_e+1, "##OBFUSCATE", __eyvh.__TZWU)
		elif line.begins_with("##OBFUSCATE_STRING_PARAMETERS"):
			__E9SI = line.trim_prefix("##OBFUSCATE_STRING_PARAMETERS").replace(" ", "").split(",", false)
			if __8x5w(path):
				prints(__Pn_e+1, "##OBFUSCATE_STRING_PARAMETERS", __E9SI)
		if __8zpr and __8zpr[0] != "#":
			var __nKyv : bool = false
			for __kgfK in range(__Gop4.size() -1, -1, -1):
				if __f9jX <= __Gop4[__kgfK]:
					__Gop4.remove_at(__kgfK)
					__nKyv = true
			if __nKyv:
				__Blaq = __JTG0(__Blaq, __Gop4.size() + 1)
				__OotC = false
			if __xkEg != __f9jX:
				__aLtN = __aLtN and __f9jX > 0
				if __f9jX > __xkEg:
					for x in __f9jX - __xkEg:
						__LKZ6.append(__OU3p.size())
						__OU3p.append([])
						__OU3p = __OU3p.back()
				else:
					for x in __xkEg - __f9jX:
						__LKZ6.pop_back()
				__KlZk = ""
				__OU3p = ___KZR
				for __kgfK in __LKZ6.size():
					__OU3p = __OU3p[__LKZ6[__kgfK]]
					__KlZk += str(__LKZ6[__kgfK]) + ("-" if __kgfK+1 < __LKZ6.size() else "")
				__xkEg = __f9jX
		var __kgfK : int = 0
		while __kgfK < __8zpr.size():
			var __ZbTD : String = __8zpr[__kgfK]
			if __ZbTD.begins_with("#") and !__Kbrz:
				break
			match __FUAJ:
				__mx4O.NONE:
					if __E5dp.has(__ZbTD):
						__FUAJ = __E5dp[__ZbTD]
						if __FUAJ == __mx4O.STRING:
							__Kbrz = __ZbTD
				__mx4O.STRING:
					if __ZbTD == "\\":
						__kgfK += 1
					elif __ZbTD == __Kbrz:
						__FUAJ = __mx4O.NONE
						__Kbrz = ""
				__mx4O.VAR:
					if line.begins_with("@export") and !__NAGG:
						__eyvh.__9nrY(__ZbTD)
						if __8x5w(path):
							print(__Pn_e+1, " SKIP EXPORT VAR ", __ZbTD) 
					else:
						var type : String = __nZQ4(__kgfK, __8zpr)
						if __OotC:
							__bMcP.__wdWb(__ZbTD, __Blaq, __KlZk, type)
						else:
							var __9q1A : __tQfG.__LGoC = __eyvh.__maN2(__ZbTD, "", "")
							if __9q1A.name and (__qxbG or __8zpr[0] == "static"):
								__eyvh.__maN2(__Blaq + "." + __ZbTD, __Blaq + "." + __9q1A.name, type)
							if !__aLtN:
								__bMcP.___XNG(__ZbTD, __tQfG.__LGoC.new(__9q1A.name if __9q1A.name else __ZbTD, type))
						if __8x5w(path):
							print(__Pn_e+1, " VAR " if !__OotC else " LOCAL VAR ",  __Blaq, ".", __ZbTD, " : ", type)
					__FUAJ = __mx4O.NONE
				__mx4O.FUNC:
					if __kgfK == 1 or (__kgfK == 2 and __8zpr[0] == "static"):
						var __iwHF : __tQfG.__LGoC = __eyvh.__maN2(__ZbTD)
						if __iwHF.name and (__qxbG or __8zpr[0] == "static"):
							__eyvh.__maN2(__Blaq + "." + __ZbTD, __Blaq + "." + __iwHF.name).__M9VX = __iwHF.__M9VX
						if !__OotC and !__aLtN:
							__bMcP.___XNG(__ZbTD, __iwHF if __iwHF else __tQfG.__LGoC.new(__ZbTD))
						__tR_v = __iwHF.__M9VX
						__Blaq += "." + __ZbTD
						__Gop4.append(__f9jX)
						__OotC = true
						if __8x5w(path):
							print(__Pn_e+1, " FUNC ", __Blaq)
						__FUAJ = __mx4O.PARAMS
					else:
						__FUAJ = __mx4O.NONE
				__mx4O.CLASS:
					var __mgGz : __tQfG.__LGoC = __eyvh.__maN2(__ZbTD)
					if __mgGz.name:
						__eyvh.__maN2(__Blaq + "." + __ZbTD, __Blaq + "." + __mgGz.name)
					if !__OotC and !__aLtN:
						__bMcP.___XNG(__ZbTD, __mgGz if __mgGz else __tQfG.__LGoC.new(__ZbTD))
					__Blaq += "." + __ZbTD
					__Gop4.append(__f9jX)
					__aLtN = true
					if __8x5w(path):
						print(__Pn_e+1, " CLASS ", __Blaq)
					__FUAJ = __mx4O.NONE
				__mx4O.CLASS_NAME:
					__Blaq = __ZbTD
					__aR49 = __ZbTD + "."
					__FUAJ = __mx4O.NONE
				__mx4O.SIGNAL:
					if !__IHIq:
						__FUAJ = __mx4O.NONE
					else:
						var __ooiq : __tQfG.__LGoC = __eyvh.__maN2(__ZbTD)
						if __ooiq.name and __qxbG:
							__eyvh.__maN2(__Blaq + "." + __ZbTD, __Blaq + "." + __ooiq.name)
						if !__OotC and !__aLtN:
							__bMcP.___XNG(__ZbTD, __ooiq if __ooiq else __tQfG.__LGoC.new(__ZbTD))
						__tR_v = __ooiq.__M9VX
						__Blaq += "." + __ZbTD
						__Gop4.append(__f9jX)
						__OotC = true
						if __8x5w(path):
							print(__Pn_e+1, " SIGNAL ", __Blaq)
						__FUAJ = __mx4O.NONE
						for j in range(__kgfK + 1, __8zpr.size()):
							if __8zpr[j] == "#":
								break
							elif __8zpr[j] == "(":
								__FUAJ = __mx4O.PARAMS
								break
				__mx4O.ENUM:
					var __lpcG : __tQfG.__LGoC = __eyvh.__maN2(__ZbTD)
					__eyvh.__maN2(__Blaq + "." + __ZbTD, __Blaq + "." + __lpcG.name if !__byWh or !__eyvh.__TZWU else "int")
					if !__OotC and !__aLtN:
						__bMcP.___XNG(__ZbTD, __lpcG if !__byWh or !__eyvh.__TZWU else __tQfG.__LGoC.new("int"))
					__pCTt = -1
					__T2S3 = __Blaq + "." + (__lpcG.name if __lpcG else __ZbTD)
					var __IBFS : int = __Blaq.find(".")
					if __IBFS != -1:
						__U1AV = __Blaq.substr(__IBFS + 1) + "." + __lpcG.name
					else:
						__U1AV = __lpcG.name
					__Blaq += "." + __ZbTD
					__Gop4.append(__f9jX)
					__OotC = true
					if __8x5w(path):
						print(__Pn_e+1, " ENUM ", __Blaq, " -> ", __T2S3)
					__FUAJ = __mx4O.ENUM_VALUES
				__mx4O.ENUM_VALUES:
					if __ZbTD == "}":
						__FUAJ = __mx4O.NONE
					elif __ZbTD == "=":
						__FUAJ = __mx4O.ENUM_VALUE_ASSIGNMENT
					elif __ZbTD != "{" and __ZbTD != ",":
						__pCTt += 1
						if __kgfK + 2 < __8zpr.size() and __8zpr[__kgfK + 1] == "=":
							__pCTt = int(__8zpr[__kgfK + 2])
						var name : String = __bMcP.__wdWb(__ZbTD, __Blaq, __KlZk, "", str(__pCTt) if __byWh and __eyvh.__TZWU else "")
						if name:
							__eyvh.__maN2(__Blaq + "." + __ZbTD, str(__pCTt) if __byWh and __eyvh.__TZWU and __eyvh.__TZWU else __T2S3 + "." + name)
							__eyvh.__maN2(___gEx(__Blaq) + "." + __ZbTD, str(__pCTt) if __byWh and __eyvh.__TZWU else ___gEx(__T2S3) + "." + name)
							if !__aLtN:
								__bMcP.___XNG(
									__Blaq.trim_prefix(__aR49) + "." + __ZbTD,
									__tQfG.__LGoC.new(str(__pCTt) if __byWh else __T2S3.trim_prefix(__aR49) + "." + name))
							if __8x5w(path):
								print(__Pn_e+1, " ENUM VALUE ", __Blaq + "." + __ZbTD, " -> ", __T2S3 + "." + name)
				__mx4O.ENUM_VALUE_ASSIGNMENT:
					if __ZbTD == "}":
						__FUAJ = __mx4O.NONE
					elif __ZbTD == ",":
						__FUAJ = __mx4O.ENUM_VALUES
				__mx4O.CONST:
					var type : String = __nZQ4(__kgfK, __8zpr)
					const __4wXq : Array[String] = ["bool", "Color", "float", "int", "NodePath", "Vector2", "Vector2i", "Vector3", "Vector3i", "Vector4", "Vector4i"]
					var value : String
					if __MUJV and __kgfK + 4 < __8zpr.size() and __8zpr[__kgfK + 3] == "=" and __4wXq.has(type):
						__a_C_[__Pn_e] = true
						for s in range(__kgfK + 4, __8zpr.size()):
							if __8zpr[s] == "#":
								break
							value += __8zpr[s]
						if __kgfK + 5 < __8zpr.size() and __8zpr[__kgfK + 5] == "(" and !__8zpr.has(")") and (__8zpr.find("#") == -1 or __8zpr.find(")") < __8zpr.find("#")):
							var depth : int = 0
							for l in range(__Pn_e + 1, __YlQ6.size()):
								__a_C_[l] = true
								var __RFlg := __EGAL.new(__YlQ6[l])
								var __0cbV : PackedStringArray = __RFlg.__jN2c()
								for line_token in __0cbV:
									if line_token == "(":
										depth += 1
									elif line_token == ")":
										depth -= 1
									elif line_token == "#":
										break
									value += line_token
								if depth < 0:
									break
					if __OotC:
						__bMcP.__wdWb(__ZbTD, __Blaq, __KlZk, type, value)
					else:
						var ___jvl : __tQfG.__LGoC = __eyvh.__maN2(__ZbTD, value, "")
						__V4Rv[__Blaq + "." + __ZbTD] = __eyvh.__maN2(__Blaq + "." + __ZbTD, value if value else __Blaq + "." + ___jvl.name, type)
						if !__OotC and !__aLtN:
							__V4Rv[__Blaq + "." + __ZbTD].set_meta("member",
								__bMcP.___XNG(__ZbTD, __tQfG.__LGoC.new(value if value else (___jvl.name if ___jvl else __ZbTD), type)))
					if __8x5w(path):
						print(__Pn_e+1, " CONST ", __Blaq + "." + __ZbTD, " : ", type)
					__FUAJ = __mx4O.NONE
				__mx4O.PARAMS:
					if __ZbTD == ")":
						__LCk9 = -1
						__E9SI = PackedStringArray()
						__FUAJ = __mx4O.NONE
					elif __ZbTD == ":" or __ZbTD == "=":
						__FUAJ = __mx4O.PARAMS_HINT
						__U01n = 0
					elif __ZbTD != "(" and __ZbTD != "," and __ZbTD != "\\":
						var type : String = __nZQ4(__kgfK, __8zpr)
						var name : String = __bMcP.__wdWb(__ZbTD, __Blaq, "", type)
						__LCk9 += 1
						if __E9SI.has(__ZbTD):
							__tR_v[__LCk9] = __ZbTD
							if __8x5w(path):
								prints(__Pn_e+1, "SET STRING PARAM", __ZbTD, __LCk9)
						if __8x5w(path):
							print(__Pn_e+1, " PARAM ", __Blaq + "." + __ZbTD, " : ", type)
				__mx4O.PARAMS_HINT:
					if __ZbTD == ")":
						__U01n -= 1
						if __U01n < 0:
							__LCk9 = -1
							__E9SI = PackedStringArray()
							__FUAJ = __mx4O.NONE
					elif __ZbTD == "(":
						__U01n += 1
					elif __ZbTD == "," and __U01n <= 0:
						__FUAJ = __mx4O.PARAMS
				_:
					__FUAJ = __mx4O.NONE
			__kgfK += 1
		var __CZmz : __2ayH.__oGqV = __bMcP.__gZdO()
		__CZmz.skip = __a_C_.get(__Pn_e, false)
		__CZmz.text = line
		__CZmz.__VESq = __8zpr
		__CZmz.__EZ3e = __HJ12
		__CZmz.__RBVo = __Blaq
		__CZmz.__1y_o = __KlZk
		__CZmz.__Xf1Y = __f9jX
		__CZmz.__U7YO = __OotC
		__CZmz.__QffC = __aLtN
func __U7Ll(path : String) -> String:
	if __8x5w(path):
		print("\n---------- ", "OBFUSCATE SCRIPT ", path, " ----------\n")
	elif __cRWp:
		return __0ETJ[path].code
	var __ggWu : PackedStringArray
	var __2ZXT : bool = true
	var __G9P2 : __2ayH = __0ETJ[path]
	__G9P2.reload(__0ETJ)
	var __S5uV : __2ayH.__oGqV = __G9P2.__PFto()
	while __S5uV:
		var __2AkQ : String
		if __S5uV.text.begins_with("##OBFUSCATE ") and __S5uV.__VESq.size() >= 4:
			if __S5uV.__VESq[3] == "true":
				__2ZXT = true
			elif __S5uV.__VESq[3] == "false":
				__2ZXT = false
			__ggWu.append(__S5uV.text)
			__S5uV = __G9P2.__PFto()
			if __8x5w(path):
				prints(__G9P2.__eCNA-1, "##OBFUSCATE", __2ZXT)
			continue
		var __4EEH : int = 0
		while __4EEH < __S5uV.__VESq.size():
			var __OmLR : String = __S5uV.__VESq[__4EEH]
			var __vYKH : String = __OmLR
			var __BKvT : __tQfG.__LGoC
			if __S5uV.skip:
				break
			if __byWh and __OmLR == "enum" and __2ZXT:
				while __S5uV and !__S5uV.text.contains("}"):
					__2AkQ += "\n"
					__S5uV = __G9P2.__PFto()
				__2AkQ += "\n"
				__S5uV = __G9P2.__PFto() 
				__4EEH = 0
				continue
			__2AkQ += __S5uV.__EZ3e[__4EEH]
			if __OmLR == "#":
				__2AkQ += __OmLR
				__4EEH += 1
				while __4EEH < __S5uV.__VESq.size():
					__2AkQ += __S5uV.__EZ3e[__4EEH]
					__2AkQ += __S5uV.__VESq[__4EEH]
					__4EEH += 1
				break
			if __vYKH == "'" or __vYKH == '"':
				var str : String
				var __OwPi : String = __vYKH
				__2AkQ += __OmLR
				__4EEH += 1
				while __4EEH < __S5uV.__VESq.size():
					str += __S5uV.__EZ3e[__4EEH] + __S5uV.__VESq[__4EEH]
					if __S5uV.__VESq[__4EEH] == "\\":
						__4EEH += 1
						if __4EEH < __S5uV.__VESq.size():
							str += __S5uV.__EZ3e[__4EEH] + __S5uV.__VESq[__4EEH]
					elif __S5uV.__VESq[__4EEH] == __OwPi:
						break
					__4EEH += 1
				__4EEH += 1
				if __S5uV.text.ends_with("##OBFUSCATE_STRINGS") and str.length() >= 2:
					__BKvT = __eyvh.__H1Dg(str.trim_suffix(__OwPi))
					if __BKvT:
						__2AkQ += __BKvT.name + __OwPi
						if __8x5w(path):
							print(__G9P2.__eCNA+1, " FOUND STRING SYMBOL >", str.trim_suffix(__OwPi), "< = ", __BKvT.name)
						continue
					else:
						var __faRf : __tQfG.__LGoC = __eyvh.__maN2(str.trim_suffix(__OwPi))
						if __faRf:
							__2AkQ += __faRf.name + __OwPi
							if __8x5w(path):
								print(__G9P2.__eCNA+1, " CREATED STRING SYMBOL >", str.trim_suffix(__OwPi), "< = ", __faRf.name)
							continue
				__2AkQ += str
				continue
			if __OmLR.begins_with("$"):
				var __s4lK : String = __OmLR
				__4EEH += 1
				while __4EEH < __S5uV.__VESq.size():
					var __LVne : String = __S5uV.__VESq[__4EEH]
					__s4lK += __S5uV.__EZ3e[__4EEH] + __LVne
					if "()[].,<=>+".contains(__LVne):
						break
					__4EEH += 1
				__4EEH += 1
				__2AkQ += __s4lK
				if __8x5w(path):
					prints(__G9P2.__eCNA+1, "SKIPPING NODE PATH", ">" + __s4lK + "<")
				continue
			if !__2ZXT and ["class", "class_name", "signal", "enum", "const", "var", "func"].has(__OmLR):
				__2AkQ += __OmLR
				if __4EEH + 1 < __S5uV.__VESq.size():
					__2AkQ += __S5uV.__EZ3e[__4EEH + 1] + __S5uV.__VESq[__4EEH + 1]
				__4EEH += 2
				if __8x5w(path):
					print(__G9P2.__eCNA+1, " SKIPPING " + __OmLR.to_upper() + " DECLARATION")
				continue
			if __S5uV.__U7YO and (__4EEH == 0 or __S5uV.__VESq[__4EEH-1] != "."):
				__BKvT = __G9P2.__R8g3(__OmLR, __S5uV.__RBVo, __S5uV.__1y_o)
				if __BKvT and __8x5w(path):
					print(__G9P2.__eCNA+1, " FOUND LOCAL SYMBOL >", __S5uV.__RBVo + "." + __OmLR + "." + __S5uV.__1y_o, "< = ", __BKvT.name)
			if !__BKvT:
				var __Mqby : bool = __4EEH == 0 or __S5uV.__VESq[__4EEH-1] != "."
				var segments : PackedStringArray = [__OmLR]
				while __4EEH + 2 < __S5uV.__VESq.size() and __S5uV.__VESq[__4EEH + 1] == ".":
					segments.append("." + __S5uV.__VESq[__4EEH + 2])
					__OmLR += segments[-1]
					__4EEH += 2
				while segments.size() > 0:
					if __Mqby:
						__BKvT = __G9P2.__FzbM(__OmLR)
						if __BKvT:
							if __8x5w(path):
								print(__G9P2.__eCNA+1, " FOUND MEMBER SYMBOL >", __OmLR, "< = ", __BKvT.name, " : ", __BKvT.type)
							break
					if !__BKvT:
						__BKvT = __eyvh.__H1Dg(__OmLR)
						if __BKvT:
							if __8x5w(path):
								print(__G9P2.__eCNA+1, " FOUND SYMBOL >", __OmLR, "< = ", __BKvT.name)
							break
					segments.resize(segments.size() - 1)
					__OmLR = ""
					for segment in segments:
						__OmLR += segment
					if segments.size() > 0:
						__4EEH -= 2
			__2AkQ += __BKvT.name if __BKvT else __vYKH
			if __BKvT and __BKvT.__M9VX and __S5uV.__VESq[0] != "func":
				var __QEQ9 : Array[__2ayH.__2yH7] = __G9P2.__hZNc(__G9P2.__eCNA, __4EEH+1)
				for param_idx in __QEQ9.size():
					var __772P : __2ayH.__2yH7 = __QEQ9[param_idx]
					if !__BKvT.__M9VX.has(param_idx) or !__772P.__RKzp:
						continue
					var __1dTW : Array[int] = __G9P2.__vWRH(__772P.__QdlP, __772P.__xlRt, 2)
					var __J_H5 : String = __G9P2.__9fTB(__1dTW[0], __1dTW[1])
					var __qqJF : __tQfG.__LGoC = __eyvh.__maN2(__J_H5)
					__G9P2.__oV8l(__1dTW[0], __1dTW[1], __qqJF.name)
					if __8x5w(path):
						prints(__G9P2.__eCNA+1, "FOUND STRING PARAM", __772P.__MXIT, str(__772P.__QdlP+1) + ":" + str(__772P.__xlRt), "-", str(__772P.__A7WG+1) + ":" + str(__772P.__FzQo), " = ", "")
			if __BKvT and __BKvT.type and __BKvT.type == "Dictionary":
				while __4EEH + 2 < __S5uV.__VESq.size() and __S5uV.__VESq[__4EEH + 1] == ".":
					__2AkQ += __S5uV.__VESq[__4EEH + 1] + __S5uV.__VESq[__4EEH + 2]
					__4EEH += 2
			__4EEH += 1
		if __S5uV.__EZ3e.size() > __S5uV.__VESq.size():
			__2AkQ += __S5uV.__EZ3e[-1]
		__ggWu.append(__2AkQ)
		__S5uV = __G9P2.__PFto()
	if __3w0u:
		__ggWu = __HmMa(path, __G861(__ggWu)).split("\n")
	if __60BK:
		for i in range(__ggWu.size() - 1, -1, -1):
			var __QXbm : String = __ggWu[i]
			if __QXbm.contains("#"):
				var __KEV7 : String
				var ___g95 : int = 0
				while ___g95 < __QXbm.length():
					var __WreZ : String = __QXbm[___g95]
					if __WreZ == "'" or __WreZ == '"':
						if !__KEV7:
							__KEV7 = __WreZ
						elif __KEV7 == __WreZ:
							__KEV7 = ""
					elif __WreZ == "#" and !__KEV7:
						if ___g95 > 0:
							__ggWu[i] = __QXbm.substr(0, ___g95)
							break
						else:
							if __hFzk:
								__ggWu.remove_at(i)
							else:
								__ggWu[i] = "# ..."
							break
					___g95 += 1
	if __hFzk:
		for i in range(__ggWu.size() - 1, -1, -1):
			var __MyFm : String = __ggWu[i]
			if __MyFm.replace(" ", "").replace("\n", "").replace("\t", "").length() == 0:
				__ggWu.remove_at(i)
				continue
	var code : String
	for line in __ggWu:
		code += line + "\n"
	code = code.strip_edges(false, true) + "\n"
	if __8x5w(path):
		print("")
		__9V0F(code)
	return code
func __wqGl(path : String, __vXi4 : String) -> String:
	if __EnEG(path):
		print("\n---------- OBFUSCATE RESOURCE ", path, " ----------\n")
	elif __cRWp:
		return __vXi4
	var data : String = ""
	var __FPo9 : PackedStringArray = __vXi4.split("\n")
	var __O_HL : int = 0
	while __O_HL < __FPo9.size():
		var __s68a : String = __FPo9[__O_HL]
		if __s68a.begins_with("\""):
			data += __s68a + "\n"
			__O_HL += 1
			continue
		if __s68a.begins_with('[connection signal="') or __s68a.begins_with('[node name="'):
			var node_paths : bool = false
			var __X0bB : PackedStringArray = __s68a.split(" ", false)
			for token in __X0bB:
				if token.begins_with('signal="') or token.begins_with('method="') or token.begins_with('node_paths=PackedStringArray("') or node_paths:
					node_paths = (token.begins_with("node_paths") or node_paths) and token[-1] == ","
					var start : int = token.find('"')
					var end : int = token.find('"', start + 1)
					if end == -1:
						continue
					var name : String = token.substr(start + 1, end - (start + 1))
					var __UA9l : __tQfG.__LGoC = __eyvh.__H1Dg(name)
					if __UA9l:
						__s68a = __H_I9(__s68a, name, __UA9l.name)
						if __EnEG(path):
							print(__O_HL+1, " FOUND SYMBOL >", name, "< = ", __UA9l.name)
		data += __s68a + "\n"
		__O_HL += 1
		if __NAGG and (__s68a.begins_with("[node") or __s68a.begins_with("[sub_resource") or __s68a.begins_with("[resource")):
			var __QB0R : String
			var __EhvJ : bool = __s68a.contains("instance=") or __s68a.contains('type="Animation"')
			var __Q3gg : int = __O_HL
			while __Q3gg < __FPo9.size(): 
				if __FPo9[__Q3gg].begins_with("["):
					break
				__QB0R += __FPo9[__Q3gg] + "\n"
				var __0zGU : PackedStringArray = __FPo9[__Q3gg].split(" = ", false, 1)
				if __0zGU.size() == 2 and __0zGU[0] == "script":
					__EhvJ = true
					if __EnEG(path):
						prints(__O_HL+1, "FOUND SCRIPT", __s68a, __0zGU[1])
				__Q3gg += 1
			if !__EhvJ:
				data += __QB0R
				__O_HL = __Q3gg
			else:
				__Q3gg = mini(__Q3gg, __FPo9.size())
				while __O_HL < __Q3gg:
					__s68a = __FPo9[__O_HL]
					var __HThh : PackedStringArray = __s68a.split(" = ", false, 1)
					if __HThh.size() == 2:
						if __HThh[1].begins_with("NodePath(") and __HThh[1].contains(":"):
							var __aFop := __EGAL.new(__HThh[1])
							var __qXfI : String = __aFop.__Uocx()
							var properties : PackedStringArray = __qXfI.split(":", false)
							var __Zr_Y : String = properties[0]
							for property in properties.slice(1):
								var __XikW : __tQfG.__LGoC = __eyvh.__H1Dg(property)
								__Zr_Y += ":" + (__XikW.name if __XikW else property)
							__HThh[1] = 'NodePath("' + __Zr_Y + '")'
							__s68a = __HThh[0] + " = " + __HThh[1]
							if __EnEG(path) and __qXfI != __Zr_Y:
								print(__O_HL+1, " FOUND NODE PATH >", __qXfI, "< = ", __Zr_Y)
						var __mqiG : __tQfG.__LGoC = __eyvh.__H1Dg(__HThh[0])
						if __mqiG:
							__s68a = __mqiG.name + " = " + __HThh[1]
							if __EnEG(path):
								print(__O_HL+1, " FOUND EXPORT VAR >", __HThh[0], "< = ", __mqiG.name)
					elif __s68a.begins_with('"method":'):
						var __bdCi := __EGAL.new(__s68a.trim_prefix('"method":'))
						var __gjjD : String = __bdCi.__Uocx()
						var __KVUn : __tQfG.__LGoC = __eyvh.__H1Dg(__gjjD)
						if __KVUn:
							__s68a = '"method": &"' + __KVUn.name + '"'
							if __EnEG(path):
								print(__O_HL+1, " FOUND METHOD >", __gjjD, "< = ", __KVUn.name)
					data += __s68a + "\n"
					__O_HL += 1
	data = data.strip_edges(false, true) + "\n"
	if __EnEG(path):
		print("")
		__9V0F(data)
	return data
func __HmMa(path : String, source_code : String) -> String:
	if source_code.find("##FEATURE") == -1:
		return source_code
	var __FG6_ : String = ""
	if source_code.contains("class_name"):
		var __h8XX : int = source_code.find("class_name")
		var __OYXF : String = source_code.substr(__h8XX, source_code.find("\n", __h8XX) - __h8XX)
		__OYXF = __OYXF.lstrip("class_name ")
		for c in __OYXF:
			if c == " " or c == "\t":
				break
			__FG6_ += c
	else:
		__FG6_ = path.get_file().rstrip(".gd")
	var __0m5c : PackedStringArray = source_code.split("\n")
	source_code = ""
	var __yTWo : int = 0
	while __yTWo < __0m5c.size():
		var __0N2M : String = __0m5c[__yTWo]
		__yTWo += 1
		source_code += __0N2M + "\n"
		if __0N2M.begins_with("##FEATURE_FUNC "):
			var __jNlw : String = __0N2M.lstrip("##FEATURE_FUNC ")
			if __Jndm.has(__jNlw):
				continue
			var __Z2IZ : String = __FG6_
			var __cdnh : String
			__0N2M = __0m5c[__yTWo]
			if !__0N2M.begins_with("func"):
				continue
			else:
				source_code += __0N2M + "\n"
				var __b0dM : PackedStringArray = __0N2M.split("(")
				if __b0dM:
					__Z2IZ += "." + __b0dM[0].lstrip("func").replace(" ", "")
				var __i4QM : PackedStringArray = __0N2M.split(")")
				if __i4QM:
					__cdnh = __i4QM[-1].replace(" ", "").replace("->", "").replace(":", "")
			__yTWo += 1
			var __0tBg : String = ""
			while __yTWo < __0m5c.size():
				__0N2M = __0m5c[__yTWo]
				if (__0N2M and __0N2M[0] != "\t" and __0N2M[0] != " " and __0N2M[0] != "#") or __0N2M.begins_with("##FEATURE") or __yTWo + 1 >= __0m5c.size():
					source_code += '\tprinterr("ERROR: illegal call to ' + "'" + __Z2IZ + "'!" + '")\n'
					if __cdnh == "bool":
						source_code += "\treturn false"
					elif __cdnh == "int":
						source_code += "\treturn 0"
					elif __cdnh == "float":
						source_code += "\treturn 0.0"
					elif __cdnh == "String":
						source_code += '\treturn ""'
					elif __cdnh == "Array":
						source_code += "\treturn []"
					elif __cdnh == "Array[int]":
						source_code += "\treturn []"
					elif __cdnh == "Array[float]":
						source_code += "\treturn []"
					elif __cdnh == "Dictionary":
						source_code += "\treturn {}"
					elif __cdnh == "void":
						source_code += "\tpass"
					else:
						source_code += "\treturn null"
					source_code += __0tBg
					break
				else:
					var __ttzB : String = __0N2M.replace("\t", "").replace(" ", "").replace("\n", "")
					if __ttzB and __ttzB[0] != "#":
						__0tBg = "\n"
					else:
						__0tBg += __0m5c[__yTWo] + "\n"
				__yTWo += 1
	return source_code
func __JTG0(__0R3O : String, __CHHd : int) -> String:
	var __mZRh : String
	var __POjw : int = 0
	var __pZ7y : int = 0
	while __pZ7y < __0R3O.length():
		if __0R3O[__pZ7y] == ".":
			__POjw += 1
			if __POjw >= __CHHd:
				break
		__mZRh += __0R3O[__pZ7y]
		__pZ7y += 1
	return __mZRh
func ___gEx(__Bx3E : String) -> String:
	var __vAzu : int = __Bx3E.rfind(".")
	if __vAzu != -1 and __vAzu + 1 < __Bx3E.length():
		return __Bx3E.substr(__vAzu + 1)
	return __Bx3E
func __nZQ4(__1C30 : int, __tmwy : PackedStringArray) -> String:
	if __1C30 + 2 < __tmwy.size() and __tmwy[__1C30 + 1] == ":" and __tmwy[__1C30 + 2] != "=":
		return __tmwy[__1C30 + 2] 
	return ""
func __G861(__3pVK : PackedStringArray) -> String:
	var code : String
	for line in __3pVK:
		code += line + "\n"
	return code
func __zHuL(source : String, __GCSd : String) -> PackedStringArray:
	var __1npb := PackedStringArray()
	var __E1wc : int = 0
	var __4MLd : int = 0
	while __E1wc < source.length():
		for d in __GCSd:
			if source[__E1wc] == d:
				var split : String = source.substr(__4MLd, __E1wc - __4MLd)
				if split:
					__1npb.append(split)
				__4MLd = __E1wc + 1
				break
		__E1wc += 1
	if __4MLd < __E1wc:
		__1npb.append(source.substr(__4MLd, __E1wc - __4MLd))
	return __1npb
func __H_I9(str : String, replace : String, __EP4s : String) -> String:
	var __ECuX : int = str.find(replace)
	if __ECuX == -1:
		return str
	elif __ECuX == 0:
		return __EP4s + str.substr(__ECuX + replace.length())
	else:
		return str.substr(0, __ECuX) + __EP4s + str.substr(__ECuX + replace.length())
func __kJy4(path : String, __f_xv : String) -> PackedStringArray:
	var __VmAo : PackedStringArray
	var __zpIt : Array[String] = [path]
	while __zpIt:
		var __2_A5 : String = __zpIt.pop_front()
		for sub_dir in DirAccess.get_directories_at(__2_A5):
			if !sub_dir.begins_with("."):
				__zpIt.append(__2_A5.path_join(sub_dir))
		for file in DirAccess.get_files_at(__2_A5):
			if file.replace(".remap", "").ends_with(__f_xv):
				__VmAo.append(__2_A5.path_join(file))
	__VmAo.sort()
	return __VmAo
func __Uh6b(path : String, text : String) -> bool:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file:
		file.store_string(text)
		file.close()
		return true
	return false
func __D_M2() -> void:
	var __X0I3 : String = get_script().resource_path.get_base_dir() + "/cache"
	if !DirAccess.dir_exists_absolute(__X0I3):
		DirAccess.make_dir_recursive_absolute(__X0I3)
	__Uh6b(__X0I3 + "/.gdignore", "")
	__Uh6b(get_script().resource_path.get_base_dir() + "/.gitignore", "cache/")
func __bKGA(__W5I2 : String, __LCwn : String) -> PackedByteArray:
	return PackedByteArray() 
	var path : String = get_script().resource_path.get_base_dir() + "/cache/convert."
	var __2xJQ : String = "scn" if __W5I2 == "tscn" else "res"
	__Uh6b(path + __W5I2, __LCwn)
	var __BFsT : Resource = ResourceLoader.load(path + __W5I2, "", ResourceLoader.CACHE_MODE_IGNORE)
	if !__BFsT:
		return PackedByteArray()
	ResourceSaver.save(__BFsT, path + __2xJQ)
	return FileAccess.get_file_as_bytes(path + __2xJQ)
func __d4b7(path : String) -> String:
	var __KnXp : PackedByteArray
	var __Scvl : int = 0
	for i in 16: 
		var __H_cd : int = hash(__Scvl) % 256
		for j in int(ceil(path.length() / 4)):
			__H_cd = (__H_cd + path.unicode_at(__Scvl)) % 256
			__Scvl = posmod(__Scvl + 1, path.length())
		__KnXp.append(__H_cd)
	__KnXp[6] = (__KnXp[6] & 0x0f) | 0x40
	__KnXp[8] = (__KnXp[8] & 0x3f) | 0x80
	return "%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x" % (__KnXp as Array)
func __9V0F(source_code : String) -> void:
	var __rwjH : PackedStringArray = source_code.split("\n")
	for i in __rwjH.size():
		print(__bsEw(i+1, 7, "-"), "|", __rwjH[i])
func __bsEw(num : int, __17YU : int, char : String = " ") -> String:
	var str : String
	var __sHMS : int = num / 10
	var d : int = 1
	while __sHMS > 0:
		__sHMS /= 10
		d += 1
	for i in __17YU - d:
		str += char
	return str + str(num)
func __8x5w(path : String) -> bool:
	for debug_script in __bnJE:
		if path.contains(debug_script):
			return true
	return false
func __EnEG(path : String) -> bool:
	for res in __fqm3:
		if path.contains(res):
			return true
	return false
