extends Node2D
var __vn4L: int = 100 + Globals.__DspH() * 10
func __F5oq(__4xjU: Node2D) -> void:
	if __4xjU.is_in_group("player"):
		__4xjU.kill()
func __EDpu(__lC7V: Node2D) -> void:
	if __lC7V.is_in_group("player"):
		__lC7V.__VRhI()
func _physics_process(delta: float) -> void:
	self.global_position.x -= __vn4L * delta
