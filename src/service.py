import json
from flask import Flask, abort, send_file, request
from src.image_processing import image_processing

app = Flask(__name__)

ALLOWED_APPS = ["WildWags", "FireSTORM"]
ALLOWED_RESOURCES = ["cat1", "cat2", "dog1", "dog2", "effects"]

@app.route("/<app_id>/characters/<resource_name>/<action>", methods=["GET"])
def get_character_actions(app_id, resource_name, action):
	if app_id not in ALLOWED_APPS:
		abort(401)
	if resource_name not in ALLOWED_RESOURCES:
		abort(404)

	data_path = f"data/{app_id}/characters/{resource_name}.json"
	with open(data_path) as file:
		data = json.load(file)

		action_data = data["actions"][action]
		src = action_data["source"]
		is_cropped = data["isCropped"]
		frames = action_data["frames"]
		w = data["frameDimensions"]["w"]
		h = data["frameDimensions"]["h"]
		start_y = action_data["startY"]
		if "startX" in action_data:
			start_x = action_data["startX"]
		else:
			start_x = 0


		buffer = image_processing(src, is_cropped, frames, w, h, start_y, start_x)

		return send_file(buffer, mimetype="image/webp")


@app.route("/<app_id>/effects/<effect>", methods=["GET"])
def get_effect(app_id, effect):
    if app_id not in ALLOWED_APPS:
        abort(401)

    data_path = f"data/{app_id}/effects/{effect}.json"
    try:
        with open(data_path) as file:
         	data = json.load(file)
    except FileNotFoundError:
        abort(400)
    src = data["source"]
    frames = data["frames"]
    is_stacked = data["isStacked"]
    w=data["frameDimensions"]["w"]
    h=data["frameDimensions"]["h"]
    is_cropped = data["isCropped"]
    start_y = data["startY"]
    if "startX" in data:
        start_x = data["startX"]
    else:
        start_x = 0

    buffer = image_processing(src, is_cropped, frames, w, h, start_y, start_x, is_stacked=is_stacked)
    return send_file(buffer, mimetype="image/webp")


@app.route("/<app_id>/icons/<icon_name>", methods=["GET"])
def get_icon(app_id, icon_name):
    if app_id not in ALLOWED_APPS:
        abort(401)

    data_path = f"data/{app_id}/icons/{icon_name}.json"
    try:
        with open(data_path) as file:
        	data = json.load(file)
    except FileNotFoundError:
        abort(404)

    src = data["source"]
    w = data["frameDimensions"]["w"]
    h = data["frameDimensions"]["h"]
    is_cropped = data["isCropped"]
    start_y = data["startY"]
    if "startX" in data:
        start_x = data["startX"]
    else:
        start_x = 0

    buffer = image_processing(src, is_cropped, w, h, start_y, start_x)
    return send_file(buffer, mimetype="image/webp")


def main():
	port = 8000
	print("\nImage Service started in port", port, "\n")
	app.run(debug=True, port=port)

if __name__ == "__main__":
	main()
