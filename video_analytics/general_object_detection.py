### python object_detection.py --object_detector ./models/model_name(with_extension) --input_path 'inputs/file_name(with_extention)' --frames_per_second 20 --output_path 'outputs/file_name(no_extension_needed)'

#############################################################################################################################

from imageai.Detection import VideoObjectDetection
import argparse
import tensorflow as tf
tf.compat.v1.Session()

#############################################################################################################################

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_path", required=True)
ap.add_argument("-d", "--object_detector", required=True)
ap.add_argument("-fp", "--frames_per_second", required=True)
ap.add_argument("-o", "--output_path", required=True)
args = vars(ap.parse_args())

#############################################################################################################################

# Loading and applying the object detection model.
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(args["object_detector"])
detector.loadModel()

video_path = detector.detectObjectsFromVideo(input_file_path=args["input_path"],
                            output_file_path=args["output_path"]
                            , frames_per_second= int(args["frames_per_second"]), log_progress=True)

#############################################################################################################################