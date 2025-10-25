extends RefCounted
const __2ayH := preload("script_data.gd")
const __tQfG := preload("symbol_table.gd")
var __2cVH : Object
var path : String
var __Rlpa : String
var ___4Yj : bool = false
var code : String
var __lxkl : Array[__oGqV]
var __obaI : PackedStringArray
var __5_qo : __tQfG
var __eCSF : Dictionary
var __x44c : Dictionary
var __eCNA : int = -1
var __1BiI : Dictionary
func _init(seed : int, __V1N9 : Dictionary) -> void:
	__5_qo = __tQfG.new(seed, true)
	self.__x44c = __V1N9
func reload(__kugK : Dictionary) -> void:
	var __tDEF : __2ayH = __kugK.get(__Rlpa)
	while __tDEF:
		for member in __tDEF.__eCSF:
			__eCSF[member] = __tDEF.__eCSF[member]
		__tDEF = __kugK.get(__tDEF.__Rlpa)
	for name in __eCSF.keys(): 
		var __wnC3 : PackedStringArray = name.split(".")
		var __drxj : PackedStringArray = __eCSF[name].name.split(".")
		var __vPAM : String
		for i in __wnC3.size():
			if __x44c.has(__wnC3[i]):
				__vPAM += ("." if __vPAM else "") + __x44c[__wnC3[i]]
			elif __wnC3.size() == __drxj.size():
				__vPAM += ("." if __vPAM else "") + __drxj[i]
			else:
				__vPAM = __eCSF[name].name
				break
		__eCSF[name].name = __vPAM
func __gZdO() -> __oGqV:
	__lxkl.append(__oGqV.new())
	return __lxkl.back()
func get_line_count() -> int:
	return __lxkl.size()
func __PFto() -> __oGqV:
	__eCNA += 1
	if __eCNA < __lxkl.size():
		return __lxkl[__eCNA]
	return null
func __hZNc(__o1h3 : int, __TBA5 : int) -> Array[__2yH7]:
	var __gVcL : Array[__2yH7]
	var __wVHj : String
	var __zxi8 : bool = false
	var __Oyjm : int = __o1h3
	var __faEc : int = __TBA5
	var __koNS : int = -1
	for i in range(__o1h3, __lxkl.size()):
		var __S170 : __oGqV = __lxkl[i]
		while __TBA5 < __S170.__VESq.size():
			var __ATno : String = __S170.__VESq[__TBA5]
			if __ATno == '"' or __ATno == "'":
				__zxi8 = true
			if __ATno == "(":
				__koNS += 1
				if __koNS > 0:
					__wVHj += __ATno
			elif __ATno == ")":
				__koNS -= 1
				if __koNS > 0:
					__wVHj += __ATno
				else:
					__gVcL.append(__2yH7.new(__wVHj, __Oyjm, __faEc, i, __TBA5, __zxi8))
					return __gVcL
			elif __ATno == ",":
				if __koNS == 0:
					__gVcL.append(__2yH7.new(__wVHj, __Oyjm, __faEc, i, __TBA5, __zxi8))
					__wVHj = ""
					__zxi8 = false
					__Oyjm = i
					__faEc = __TBA5
			else:
				__wVHj += __ATno
			__TBA5 += 1
		__TBA5 = 0
	return __gVcL
func ___XNG(__Qxse : String, __7Vps : __tQfG.__LGoC) -> __tQfG.__LGoC:
	__eCSF[__Qxse] = __7Vps
	return __7Vps
func __FzbM(__nOBW : String) -> __tQfG.__LGoC:
	return __eCSF.get(__nOBW)
func __wdWb(__PJdm : String, __wOsW : String, __5R9T : String, type : String = "", __0963 : String = "") -> String:
	var __1sS6 : __tQfG.__LGoC = __5_qo.__H1Dg(__wOsW + "." + __PJdm + "." + __5R9T)
	if __1sS6:
		return __1sS6.name
	if __x44c.has(__PJdm) or (!__0963 and !__5_qo.__TZWU):
		__0963 = __PJdm
	__5_qo.__maN2(__wOsW + "." + __PJdm + "." + __5R9T, __0963, type)
	__1sS6 = __5_qo.__H1Dg(__wOsW + "." + __PJdm + "." + __5R9T)
	var __rivd : Dictionary = __1BiI.get(__wOsW + "." + __PJdm, {})
	__1BiI[__wOsW + "." + __PJdm] = __rivd
	__rivd[__5R9T] = __1sS6
	return __1sS6.name
func __R8g3(name : String, __O1u7 : String, __IIiu : String) -> __tQfG.__LGoC:
	var __Alnp : Dictionary = __1BiI.get(__O1u7 + "." + name, {})
	for target_scope_id : String in __Alnp:
		if !target_scope_id or __IIiu.begins_with(target_scope_id):
			return __Alnp[target_scope_id]
	return null
func __vWRH(__pMwv : int, __4qZQ : int, __yKrZ : int) -> Array[int]:
	var __Kg8b : Array[int] = [__pMwv, __4qZQ]
	for i in __yKrZ:
		__4qZQ += 1
		while __4qZQ >= __lxkl[__pMwv].__VESq.size():
			if __pMwv >= __lxkl.size():
				return __Kg8b
			__4qZQ = 0
			__pMwv += 1
	return [__pMwv, __4qZQ]
func __9fTB(__oLF4 : int, __vN9C : int) -> String:
	return __lxkl[__oLF4].__VESq[__vN9C]
func __oV8l(__UPBy : int, __5WVF : int, new : String) -> void:
	__lxkl[__UPBy].__VESq[__5WVF] = new
class __oGqV:
	var skip : bool
	var text : String
	var __VESq : PackedStringArray
	var __EZ3e : PackedStringArray
	var __RBVo : String
	var __1y_o : String
	var __Xf1Y : int
	var __U7YO : bool
	var __QffC : bool
class __2yH7:
	var __MXIT : String
	var __QdlP : int
	var __xlRt : int
	var __A7WG : int
	var __FzQo : int
	var __RKzp : bool
	func _init(__jgwm : String, __lAlW : int, __Eol5 : int, __HHkD : int, __NrEI : int, __fUvp : bool) -> void:
		self.__MXIT = __jgwm
		self.__QdlP = __lAlW
		self.__xlRt = __Eol5
		self.__A7WG = __HHkD
		self.__FzQo = __NrEI
		self.__RKzp = __fUvp
