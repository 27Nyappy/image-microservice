import io
from PIL import Image

def image_processing(asset_path, is_cropped, frames, w, h, start_y, start_x = 0, is_stacked = False):
	with Image.open(asset_path) as im:
		strip = im

		if not is_cropped:
			even_frames = frames % 2 == 0
			top_frames = 2 if is_stacked else frames
			y_2 = start_y + (1 * h)
			# crop based on image box coordinates, as per Pillow docs:
			# Rectangles are represented as 4-tuples, (x1, y1, x2, y2), with the upper left corner given first.
			strip = im.crop((start_x, start_y, start_x + (top_frames * w), y_2))

			if is_stacked:
				bottom_frames = frames - top_frames
				# if frames are stacked extract the bottom frames
				bottom_strip = im.crop((start_x, y_2, start_x + (bottom_frames * w), y_2 + h))
				merged_strip = Image.new(im.mode, ((top_frames + bottom_frames) * w, h))
				# merge the two stacked frames into a single row of frames
				merged_strip.paste(strip)
				merged_strip.paste(bottom_strip, (top_frames * w, 0))
				strip = merged_strip

		buffer = io.BytesIO() # setup buffer to hold WebP image
		strip.save(buffer, format="WEBP", lossless=True, quality=100, method=6)

		buffer.seek(0) # move to start of buffer

	return buffer

