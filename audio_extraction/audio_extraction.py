#Run -> python audio_extraction.py --video_file video_filename(with extension) --audio_file audio_filename(with extension, .wav is better for analysis)
from moviepy.editor import *
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-vf", "--video_file", required=True)
ap.add_argument("-af", "--audio_file", required=True)

args = vars(ap.parse_args())



audioclip = AudioFileClip(args["video_file"])
audioclip.write_audiofile(args["audio_file"])
