from dataclasses import dataclass
import io
import os
import unittest
from PIL import Image
from src.image_processing import image_processing

@dataclass
class Sprite:
	path: str
	is_cropped: bool
	frames: int
	w: int
	h: int
	start_y: int

class TestImageProcessing(unittest.TestCase):
	def setUp(self):
		# "eat-left": {
		# 	"source": "tests/test-assets/EATING.png",
		# 	"startY": 32,
		# 	"frames": 4,
		# 	"defaultFps": 12
		# }
		self.dog_eat_left = Sprite(
			path="tests/test-assets/EATING.png",
			is_cropped=False,
			frames=4,
			w=32,
			h=32,
			start_y=32
		)
		# "happy": {
		# 	"source": "tests/test-assets/happy.png",
		# 	"startY": 0,
		# 	"frames": 3,
		# 	"defaultFps": 12
		# }
		self.icon_happy = Sprite(
			path="tests/test-assets/happy.png",
			is_cropped=True,
			frames=3,
			w=32,
			h=32,
			start_y=0
		)
		# "freeze": {
		# 	"source": "tests/test-assets/freezeEffect.png",
		# 	"startY": 0,
		# 	"frames": 3,
		# 	defaultFPS: 12
		# }
		self.freeze_effect = Sprite(
			path="tests/test-assets/freezeEffect.png",
			is_cropped=False,
			frames=3,
			w=67,
			h=67,
			start_y=0
		)

	def test_sprite_crop(self):
		sprite = self.dog_eat_left
		res = image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y)
		res_img = Image.open(res)

		self.assertEqual(res_img.size[0], 128, "Width does not match full frames width")
		self.assertEqual(res_img.size[1], 32, "Height does not match sprite height")

		res_img.close()

	def test_sprite_crop_stacked(self):
		sprite = self.freeze_effect
		res = image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y, 0, True)
		res_img = Image.open(res)

		self.assertEqual(res_img.size[0], 201, "Width does not match full frames width")
		self.assertEqual(res_img.size[1], 67, "Height does not match sprite height")
		res_img.show()
		res_img.close()

	def test_sprite_no_crop(self):
		sprite = self.icon_happy
		res = image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y)
		res_img = Image.open(res)

		self.assertEqual(res_img.size[0], 96, "Width does not match full frames width")
		self.assertEqual(res_img.size[1], 32, "Height does not match sprite height")

		res_img.close()

	def test_asset_format_conversion(self):
		sprite = self.icon_happy
		res = image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y)
		res_img = Image.open(res)

		self.assertEqual(res_img.format, "WEBP", "Format does not match WEBP")

		res_img.close()

	def test_original_img_not_modified(self):
		sprite = self.dog_eat_left
		image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y)
		og_img = Image.open(sprite.path)

		self.assertEqual(og_img.size[0], 128, "Width does not match original width")
		self.assertEqual(og_img.size[1], 128, "Height does not match original height")
		self.assertEqual(og_img.format, "PNG", "Format does not match original PNG format")

		og_img.close()

	def test_sprite_size_reduction(self):
		sprite = self.dog_eat_left
		og_size = os.stat(sprite.path).st_size
		res = image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y)
		res_size = res.getbuffer().nbytes

		size_reduction = ((og_size - res_size) / og_size) * 100

		self.assertLess(res_size, og_size, "Image processing resulted in a larger file")
		self.assertGreaterEqual(size_reduction, 20, "Reduction does not meet requirements")

	def test_sprite_icon_size_reduction(self):
		sprite = self.icon_happy
		og_size = os.stat(sprite.path).st_size
		res = image_processing(sprite.path, sprite.is_cropped, sprite.frames, sprite.w, sprite.h, sprite.start_y)
		res_size = res.getbuffer().nbytes

		size_reduction = ((og_size - res_size) / og_size) * 100

		self.assertLess(res_size, og_size, "Image processing resulted in a larger file")
		self.assertGreaterEqual(size_reduction, 20, "Reduction does not meet requirements")
