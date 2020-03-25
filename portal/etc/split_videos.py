import os, argparse
import cv2 # gotta install on pis


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='video filename')
args = parser.parse_args()

#TODO: check file format is legal
vid = cv2.VideoCapture(args.file)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
ratio = float(height)/width
print("width", width)
print("height", height)
print("video ratio:", ratio)
# one side of portal is 6x3

size_x = 1280
size_y = 720

border_x = 250
border_y = 150

total_x = 8930.0
total_y = 2360.0
target_ratio =  total_x/total_y

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

os.makedirs("./grid_video", exist_ok=True) 
#tvs are indexed by reading sequences
#w:h:x:y out.mp4
cmd_template = 'ffmpeg -i {} -vf "crop={}:{}' \
				.format(args.file, frame_width, frame_height) \
				 + ':{}:{}" grid_video/{}.mp4'
for x_indx in range(6):
	for y_indx in range(3):
		x = x_indx * (frame_width + border_width)
		y = y_indx * (frame_height + border_height)
		command = cmd_template.format(x, y, 3*x_indx + y_indx)
		os.system(command)





