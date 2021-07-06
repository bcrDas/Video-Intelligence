# Video-Intelligence
A repo for video intelligence 

## Table of contents
* [General info](#general-info)
* [Prerequisites](#prerequisites)
* [Script_execution](#script_execution)
* [Contributing](#contributing)
* [License](#license)


## General info
#### `Folder details`:
* `youtube_data_collector` -> Collect data through YouTube data API(Experimental)
* `csv_to_xls_converter` -> GUI for Converting a csv file into a xls file for better visualization.
* `trend_analyzer` -> For analyzing the datasets containing trending videos(YouTube) and idntifying the patterns bwtween the trending videos(country-wise).
* `youtube_video_downloader` -> GUI for downloading a video from youtube.
* `audio_extraction` -> Extract the audio from a video.
* `video_analytics` -> Video analysis algorithms.


## Prerequisites
#### Dependencies :
Don't forget to install all the dependencies before executing the codes.

#### API Key :
In order to run the `youtube_data_collector` script, you will need a valid API key for the YouTube Data API. The instructions for doing so are [here](https://developers.google.com/youtube/registering_an_application).Once you have the key, put it inside the text file named `api_key.txt`.

#### Country Codes :
Also in order to run the `youtube_data_collector` script, you will need country codes for the countries from which you will going to collect the trending videos.A list of all existing country codes can be found [here](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes).Once you have the country codes you need, put it inside the text file named `country_codes.txt`(remember may be some of the country codes will not gonna work).

#### Datasets : 
* Download the Trending videos(Youtube) country-wise(For trend_analysis.py) - [Click here](https://drive.google.com/file/d/1BGTGiGpwlLlRTPLcQHyfJb8zYxDkJY--/view?usp=sharing)
   
* Download the object detection model(For 
frame_wise_analysis.py and
general_object_detection.py)  - [Click here](https://drive.google.com/file/d/10D5c9XbB2sr-yc-lCUDErFNavfBvnsOm/view?usp=sharing)
  
* Download the face detection model(For face_detection.py) - [Click here](https://drive.google.com/file/d/1nBm8N0rfxqJtYYFOUhYNy6PbzLpum0vj/view?usp=sharing)

* Download the face detection model(For face_mask_detection_system.py) - [Click here](  https://drive.google.com/drive/folders/1EucKhzv6kjhnuLiZ7pIkwCeGhWC_k5gT?usp=sharing)

* Download the mask detection model(For face_mask_detection_system.py) - [Click here](https://drive.google.com/file/d/1_yk-W8HdT9G6_JdhW2MWeD8N4a_p-LuE/view?usp=sharing)

  
 #### Databases : 
* When working with the `real-time attendance system(videobased_realtime_attendance_system.py)`,first you need to make sure that known person's faces were already present in the database because the system can only recognize known person's faces as generally we can tell the name of a person only if we saw and know them,same applies for this system.Also if you want to add new faces/want the system to recognize new faces, just put the images into the `inputs/attendance_system_image_database` folder. 


## Script_execution
#### 1. When working with youtube_data_collector(Experimental,format of data is not as intended) :

```bash
$ cd youtube_data_collector
$ python youtube_data_collector.py --API_key_path file_name.txt --country_code_path filename.txt 
--output_dir folder_name/
```


#### 2. When working with csv_to_xls_converter :

```bash
$ cd csv_to_xls_converter
$ python csv_xls.py --xls_file_name xls_filename
```


#### 3. When working with trend_analyzer :

```bash
$ cd trend_analyzer
$ python trend_analysis1.py --dataset filename.csv --json_file filename.json
```

#### 4. When working with youtube_video_downloader : 

```bash
$ cd youtube_video_downloader
$ python video_downloader.py
```

#### 5. When working with audio_extraction :

```bash
$ cd audio_extraction
$ python audio_extraction.py --video_file video_filename(with extension) 
--audio_file audio_filename(with extension)
```


#### 6. When working with video_analytics :

```bash
$ cd video_analytics
```
1. For running the object detection alogrithm(general_object_detection.py) -
```bash
$ python object_detection.py --object_detector ./models/model_name(with_extension) --input_path 
'inputs/file_name(with_extention)' --frames_per_second 20 --output_path 
'outputs/file_name(no_extension_needed)'
```
2. For running the object detection alogrithm along with object detection(frame_wise_analysis.py) -
```bash
$ python frame_wise_analysis.py --object_detector ./models/model_name(with_extension) --input_path 
'inputs/file_name(with_extention)' --frames_per_second 20 --output_path 
'outputs/file_name(no_extension_needed)'
```
3.1. For running the face detection alogrithm(face_detection.py) if video is already present(Not very accurate) -
```bash
$ python face_detection.py --model models/haarcascade_frontalface.xml
--video inputs/file_name(with extension) 
```
3.2. For running the face detection alogrithm(face_detection.py) if you want to use webcam(Not very accurate) -
```bash
$ python face_detection.py --model models/haarcascade_frontalface.xml
```

4. For running the real-time attendance system algorithm(videobased_realtime_attendance_system.py) -
```bash
$ python videobased_realtime_attendance_system.py --image_database_path 
inputs/images/attendance_system_image_database --attendance_logger_path
outputs/attendance_logger/Attendance.csv
```

5.1. For running the face mask detection algorithm using default location of models(face and mask detector) and default confidence threshold 
for mask detection(face_mask_detection_system.py) -
```bash
$ python face_mask_detection_system.py
```

5.2. For running the face mask detection algorithm using custom location of models(face and mask detector) and custom confidence threshold
for mask detection(face_mask_detection_system.py) -
```bash
$ python face_mask_detection_system.py --face face_detector_path --model mask_detector_model
--confidence confidence_score
```
  
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Always make sure to update the script execution command as well.

## License
N/A


