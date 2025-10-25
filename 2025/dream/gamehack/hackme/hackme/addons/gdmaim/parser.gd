extends RefCounted
var code : String
var __HRoc : int = -1
var __EprW : String
var __sh6w : PackedStringArray
func _init(code : String) -> void:
	self.code = code
func __7ere() -> bool:
	return __HRoc >= code.length()
func reset() -> void:
	__HRoc = -1
func __C84V() -> String:
	__HRoc += 1
	if __HRoc < code.length():
		__EprW = code[__HRoc]
		return __EprW
	else:
		__EprW = ""
		return ""
func __1bzp(__WDRk : String) -> String:
	var __0tgX : String
	while __C84V():
		if __WDRk.find(__EprW) != -1:
			break
		__0tgX += __EprW
	return __0tgX
func __jN2c() -> PackedStringArray:
	var __7ugY : PackedStringArray
	reset()
	__sh6w.clear()
	var __IGvQ : String
	while !__7ere():
		var __rCRz : String = __1bzp(" ,\n\t(:.+-*/)[]{}'<=>|!#\"\\")
		if __rCRz:
			__7ugY.append(__rCRz)
			__sh6w.append(__IGvQ)
			__IGvQ = ""
		if __EprW:
			if __EprW != " " and __EprW != "\n" and __EprW != "\t":
				__7ugY.append(__EprW)
				__sh6w.append(__IGvQ)
				__IGvQ = ""
				if __EprW == "'" or __EprW == '"':
					var __d3wZ : String = __EprW
					var str : String
					while __C84V():
						if __EprW == __d3wZ:
							__7ugY.append(str)
							__sh6w.append("")
							__7ugY.append(__EprW)
							__sh6w.append("")
							break
						else:
							str += __EprW
							if __EprW == "\\":
								str += __C84V()
			else:
				__IGvQ += __EprW
	if __IGvQ:
		__sh6w.append(__IGvQ)
	return __7ugY
func __MzuD() -> int:
	var __fES0 : int
	reset()
	__C84V()
	while !__7ere():
		if __EprW == " " or __EprW == "\t":
			__fES0 += 1
		else:
			break
		__C84V()
	return __fES0
func __Uocx() -> String:
	while __C84V():
		if __EprW == "'" or __EprW == '"':
			var str : String
			var __DtIn : String = __EprW
			while __C84V():
				if __EprW == __DtIn:
					return str
				str += __EprW
				if __EprW == "\\":
					str += __C84V()
	return ""
