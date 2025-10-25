extends Node2D
@onready var __8jUj: PackedScene = preload("res://scenes/bird.tscn")
@onready var __5jI8: PackedScene = preload("res://scenes/wall.tscn")
@onready var __NOBi: Node = $Control/VBoxContainer/HBoxContainer/Score
@onready var __l56P: Label = $Control/VBoxContainer/HBoxContainer2/flag
var __yLAh: String = ""
var __x9JD: RandomNumberGenerator = RandomNumberGenerator.new()
func _ready():
	var b: Node2D = __8jUj.instantiate()
	b.global_position = Vector2(70,300)
	add_child(b)
	randomize()
	__vNjm()
	__yLAh += "D"
	__yLAh += "R"
	__yLAh += "E"
	__yLAh += "A"
	__yLAh += "M"
	__yLAh += "{"
	__yLAh += "y"
	__yLAh += "0"
	__yLAh += "u"
	__yLAh += "r"
	__yLAh += "3"
	__yLAh += "_"
	__yLAh += "0"
	__yLAh += "n"
	__yLAh += "l"
	__yLAh += "y"
	__yLAh += "_"
	__yLAh += "c"
	__yLAh += "h"
	__yLAh += "3"
	__yLAh += "4"
	__yLAh += "t"
	__yLAh += "1"
	__yLAh += "n"
	__yLAh += "g"
	__yLAh += "_"
	__yLAh += "y"
	__yLAh += "0"
	__yLAh += "u"
	__yLAh += "r"
	__yLAh += "s"
	__yLAh += "3"
	__yLAh += "l"
	__yLAh += "f"
	__yLAh += "}"
func __vNjm():
	var w: Node2D = __5jI8.instantiate()
	w.global_position.x = 512+92
	w.global_position.y = 250 - (randi() % 500)
	add_child(w)
func __VKX5(__NfWf: Area2D) -> void:
	if __NfWf.is_in_group("wall"):
		__vNjm()
func _process(delta: float) -> void:
	__NOBi.text = str(Globals.__DspH())
	if Globals.__DspH() >= 1_000_000 and not Globals.__oVAw:
		__l56P.text = __yLAh
	elif Globals.__DspH() >= 1_000_000 and Globals.__oVAw:
		__l56P.text = "No flags for cheaters!"
	elif Globals.__DspH() < 1_000_000:
		__l56P.text = "Score too low!"
