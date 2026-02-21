import io
from PIL import Image

def image_processing(asset_path, is_cropped, frames, w, h, start_y, start_x = 0):
	with Image.open(asset_path) as im:
		strip = im

		if not is_cropped:
			# crop based on image box coordinates, as per Pillow docs:
			# Rectangles are represented as 4-tuples, (x1, y1, x2, y2), with the upper left corner given first.
			strip = im.crop((start_x, start_y, start_x + (frames * w), start_y + (1 * h)))

		buffer = io.BytesIO() # setup buffer to hold WebP image
		strip.save(buffer, format="WEBP", lossless=True, quality=100, method=6)

		buffer.seek(0) # move to start of buffer

	return buffer

