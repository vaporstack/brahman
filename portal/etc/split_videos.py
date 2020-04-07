import os, sys
import cv2 # only local computer need this
from portal import get_portal_ip_list


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

	output_path = truncated_output

	if sys.version_info[0] < 3:
		if not os.path.exists(output_path):
			os.makedirs(output_path)
	else:
		os.makedirs(output_path, exist_ok=True)

	# tvs are indexed by top-left-is-0 coordinate
	# w:h:x:y out.mp4

	cmd_template = 'ffmpeg -i {} -vf "crop={}:{}' \
					.format('"' + path + '"', frame_width, frame_height) \
					 + ':{}:{}" {}'

	fnames = []
	for x_indx in range(6):
		for y_indx in range(3):
			x = x_indx * (frame_width + border_width)
			y = y_indx * (frame_height + border_height)
			idx = 3 * x_indx + y_indx
			# should we have our index correspond with our hostname? no, that's confusing since
			# the hostnames already make no sense in regards to the physical map
			filename = "./%s/%d.%s" % (truncated_output, idx, output_ext)
			fnames.append(filename)
			command = cmd_template.format(x, y, filename)
			print(command)
			os.system(command)
	return fnames, truncated_output


def send_videos(fnames, directory):

	cmd_template = "scp {} {}" # scp ./gen/dir/index pi_index_ip/dir/left or right 
	naming_mode = ["movie1", "movie2"]

	# want a mapping of: monitor index -> ip address + left or right
	for idx in range(18):
		portal = "portal%02d" % (1+int(idx/2))
		leftright = idx % 2

		if leftright == 0:
			os.system('ssh %s "mkdir -p ~/%s"' % (portal, directory))
		cmd = "scp %s %s:~/%s/%s" % (fnames[idx], portal, directory, naming_mode[leftright])
		print(cmd)
		os.system(cmd)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		path = sys.argv[1]
	else:
		path = "./gen/test/test.MP4"
		#path = "/Users/vs/personal/sync/projects/brahman/portal/media/portal-movies/Orcas following my boat....underwater view!-tau8up04Igo.mp4"
	
	fnames, directory = split_video(path)
	send_videos(fnames, directory)


