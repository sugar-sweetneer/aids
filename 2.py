# Audio Analysis
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
audio_path = "audio.mp3"
audio, sample_rate = librosa.load(audio_path)
duration = librosa.get_duration(y=audio, sr=sample_rate)
print(f"Audio Duration: {duration:.2f} seconds")
print(f"Audio Sample Rate: {sample_rate} Hz")
num_samples = len(audio)
print(f"Number of Audio Samples: {num_samples}")
plt.figure(figsize=(12, 4))
librosa.display.waveshow(audio, sr=sample_rate)
plt.title("Audio Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.show()
plt.figure(figsize=(12, 6))
spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate)
librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max), sr=sample_rate, x_axis="time", y_axis="mel")
plt.colorbar(format="%+2.0f dB")
plt.title("Spectrogram")
plt.xlabel("Time (seconds)")
plt.ylabel("Mel Frequency")
plt.show()

# Image Analysis
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
image_path = "image.jpg"
image = Image.open(image_path)
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")
plt.show()
width, height = image.size
print(f"Image Dimensions: {width}x{height}")
image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
num_channels = image_cv.shape[2]
print(f"Number of Color Channels: {num_channels}")
colors = ("b", "g", "r")
plt.figure(figsize=(8, 4))
plt.title("Color Histograms")
for i, color in enumerate(colors):
  histogram = cv2.calcHist([image_cv], [i], None, [256], [0, 256])
  plt.plot(histogram, color=color)
  plt.xlim([0, 256])
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.show()

# Video Analysis
import pandas as panda
from google.colab.patches import cv2_imshow
import cv2
import time
from datetime import datetime
initialState = None
motionTrackList= [ None, None ]
motionTime = []
dataFrame = panda.DataFrame(columns = ["Initial", "Final"])
video = cv2.VideoCapture("video.mp4")
while True:
   check, cur_frame = video.read()
   var_motion = 0
   gray_image = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
   gray_frame = cv2.GaussianBlur(gray_image, (21, 21), 0)
   if initialState is None:
       initialState = gray_frame
       continue
   differ_frame = cv2.absdiff(initialState, gray_frame)
   thresh_frame = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)[1]
   thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
   cont,_ = cv2.findContours(thresh_frame.copy(),
                      cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   for cur in cont:
       if cv2.contourArea(cur) < 10000:
           continue
       var_motion = 1
       (cur_x, cur_y,cur_w, cur_h) = cv2.boundingRect(cur)
       cv2.rectangle(cur_frame, (cur_x, cur_y), (cur_x + cur_w, cur_y + cur_h), (0, 255, 0), 3)
   motionTrackList.append(var_motion)
   motionTrackList = motionTrackList[-2:]
   if motionTrackList[-1] == 1 and motionTrackList[-2] == 0:
       motionTime.append(datetime.now())
   if motionTrackList[-1] == 0 and motionTrackList[-2] == 1:
       motionTime.append(datetime.now())
   cv2_imshow(gray_frame)
   cv2_imshow(differ_frame)
   cv2_imshow(thresh_frame)
   cv2_imshow(cur_frame)
   wait_key = cv2.waitKey(1)
   if wait_key == ord('m'):
       if var_motion == 1:
           motionTime.append(datetime.now())
       break
for a in range(0, len(motionTime), 2):
   dataFrame = dataFrame.append({"Initial" : time[a], "Final" : motionTime[a + 1]}, ignore_index = True)
dataFrame.to_csv("EachMovement.csv")
video.release()
cv2.destroyAllWindows()