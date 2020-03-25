import os
import argparse
import sys
import cv2 # gotta install on pis


def sanitize_filename(data):
	illegals = "-!@#$$%^&*()-=_+[]{}. |;':,?/\\"
	output = data
	for i in illegals:
		output = output.replace(i, "_")
	while "__" in output:
		output = output.replace("__", "_")
	return output.lower()


def split_video(path=None):

	vid = cv2.VideoCapture(path)

	# configure output
	name = os.path.basename(path)
	trunk, ext = os.path.splitext(name)
	sanitized = sanitize_filename(trunk)
	truncated_output = sanitized[:32]

	height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
	width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
	ratio = float(height) / width
	print("width", width)
	print("height", height)
	print("video ratio:", ratio)
	# one side of portal is 6x3
	output_ext = "mp4"
	size_x = 1280
	size_y = 720

	border_x = 250
	border_y = 150

	total_x = 8930.0
	total_y = 2360.0
	target_ratio = total_x / total_y

	# get showable ara
	if ratio >= target_ratio:
		# too wide, crop side
		width = target_ratio * height
	else:
		# too tall, crop top
		height = width / target_ratio

	frame_width = size_x / total_x * width
	frame_height = size_y / total_y * height

	border_width = border_x / total_x * width
	border_height = border_y / total_y * height

	output_path = "./grid_video"

	if sys.version_info[0] < 3:
		if not os.path.exists(output_path):
			os.makedirs(output_path)
	else:
		os.makedirs(output_path, exist_ok=True)

	# tvs are indexed by reading sequences
	# w:h:x:y out.mp4

	cmd_template = 'ffmpeg -i {} -vf "crop={}:{}' \
					.format('"' + path + '"', frame_width, frame_height) \
					 + ':{}:{}" grid_video/{}'


	for x_indx in range(6):
		for y_indx in range(3):
			x = x_indx * (frame_width + border_width)
			y = y_indx * (frame_height + border_height)
			idx = 3 * x_indx + y_indx
			# should we have our index correspond with our hostname? no, that's confusing since
			# the hostnames already make no sense in regards to the physical map
			filename = "%s-%d.%s" % (truncated_output, idx, output_ext)
			command = cmd_template.format(x, y, filename)
			# print(command)
			os.system(command)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		path = sys.argv[1]
	else:
		path = "/Users/vs/personal/sync/projects/brahman/portal/media/portal-movies/Orcas following my boat....underwater view!-tau8up04Igo.mp4"
	split_video(path)

	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str, help='video filename')
	args = parser.parse_args()

	#TODO: check file format is legal
	if args.file:
		split_video(args.file)
	else:
		# test vid, worst possible filename woo
		path = "/Users/vs/personal/sync/projects/brahman/portal/media/portal-movies/Orcas following my boat....underwater view!-tau8up04Igo.mp4"
	"""
