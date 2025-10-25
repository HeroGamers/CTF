extends CharacterBody2D
var __k_eI: bool = false
func kill():
	Globals.__26t3 = 0
	get_tree().quit(0)
func __VRhI():
	Globals.add_point()
func __ApnX():
	__k_eI = true
func _physics_process(delta: float) -> void:
	if velocity.y < 300:
		velocity.y += 400 * delta
	if __k_eI:
		velocity.y = -250
		__k_eI = false
	move_and_slide()
	if self.global_position.y >= 732:
		kill()
func _unhandled_input(__Vmzd):
	if __Vmzd is InputEventKey:
		if __Vmzd.is_pressed() == true and __Vmzd.is_echo() == false:
			__ApnX()
