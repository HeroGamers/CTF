extends Node
var __26t3: int = 0
var __ohCj: int = 0
var __oVAw: bool = false
var __Enph: bool = false
func _process(delta: float) -> void:
	if __ohCj != __26t3:
		if __ohCj == __26t3 -123 and __Enph:
			__ohCj = __26t3
			__Enph = false
		else:
			__oVAw = true
	if __26t3 % 123 != 0:
		__oVAw = true
	if __ohCj % 123 != 0:
		__oVAw = true
func add_point():
	__26t3 += 123
	__Enph = true
func __DspH() -> int:
	return __26t3 / 123
