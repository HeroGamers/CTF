extends RefCounted
var __2cVH : Object
var __5Ws3 : Dictionary
var __TZWU : bool = true
var __LUvS : int
var __xjkd : Dictionary
var __HlsB : PackedStringArray
func _init(seed : int, __GFfx : bool = true, __cvq7 : Dictionary = {}) -> void:
	__LUvS = seed
	__TZWU = __GFfx
	__xjkd = __cvq7
func __maN2(name : String, __MP2B : String = "", type : String = "") -> __LGoC:
	const __6KCS : PackedStringArray = ["gd", "in", "for", "while", "if", "else", "pass", "break", "return", "res", "var", "func", "static", "const", "enum", "class", "signal", "await"]
	if __5Ws3.has(name):
		if !__TZWU:
			__9nrY(name)
		return __5Ws3[name]
	elif name.length() < 3 or __6KCS.has(name) or __xjkd.has(name):
		__9nrY(name)
		__MP2B = name
	elif !__TZWU and !__MP2B:
		if !name.contains("."):
			__9nrY(name)
		__MP2B = name
	var __RRqE := __LGoC.new(__dSDy(name) if !__MP2B else __MP2B, type)
	__5Ws3[name] = __RRqE
	return __RRqE
func __9nrY(name : String) -> void:
	__xjkd[name] = name
func __rUvs(name : String) -> bool:
	return __5Ws3.has(name)
func __H1Dg(name : String) -> __LGoC:
	return __5Ws3.get(name)
func __dSDy(name : String) -> String:
	var __YHKT := RandomNumberGenerator.new()
	__YHKT.seed = hash(name) + name.length() + __LUvS
	var __FDg5 : int = maxi(1, __2cVH.__k1hG)
	var id : String
	while !id or __HlsB.has(id):
		id = __2cVH.__oUrD
		for j in __FDg5:
			id += __2cVH.__hFwD[__YHKT.randi() % __2cVH.__hFwD.length()]
		__FDg5 += 1
	__HlsB.append(id)
	return id
class __LGoC:
	var name : String
	var type : String
	var __M9VX : Dictionary
	func _init(name : String = "", type : String = "") -> void:
		self.name = name
		self.type = type
