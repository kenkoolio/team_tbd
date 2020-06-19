# Noah says:
# this file is currently a stub to be integrated once we know the structure of our program.
# the Current functionality is to take a video file path, and spit out slides and audio
# segments from that video file, with the intention that later we would send those
# audio segments to get transcribed prior to creating the document.
# still do to: probably overlap the audio to get better transcription.

import os  # for file handling
# this package will have to be installed to the environment to be included.
# to get this package into conda, run from terminal: conda install -c conda-forge moviepy
from moviepy.editor import *


# this is just a decimal version of the standard range function
# adapted from https://www.techbeamers.com/python-float-range/#:~:text=Python%20range%20can%20only%20generate,arguments%20are%20of%20integer%20type.
def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += step
        start = round(start, 2)


# this function does all the stuff listed at the top of this file.
# based on https://stackoverflow.com/questions/43148590/extract-images-using-opencv-and-python-or-moviepy
def spliceAndProcess(movie, movie_path, timeIncrementSeconds=60.0, outputDir='slides'):
    # ensure that slide directory exists and is empty
    # this is technically dangerous:
    #   In the finished product we may want to delete dir when we're done, and
    #   bail if dir exists when entering function.
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
    else:
        fileList = [f for f in os.listdir(
            outputDir)]  # jacked from https://stackoverflow.com/questions/1995373/deleting-all-files-in-a-directory-with-python/1995397
        for f in fileList:
            os.remove(os.path.join(outputDir, f))

    # get video handler and calculate segment times
    clip = VideoFileClip(os.path.join(movie_path, movie))
    print("the duration is: ", clip.duration)
    times = list(float_range(0, clip.duration, timeIncrementSeconds))
    print("the clips are at: ", times)

    # spit out slides
    for t in times:
        slidePath = os.path.join(outputDir, '{}.png'.format(t))
        clip.save_frame(slidePath, t)

    # spit out video clips
    times.append(clip.duration)  # add the end time
    subClips = []
    # this needs to be done in two loops to avoid assertions from the sub clipping
    for i in range(0, len(times) - 1):
        startTime = times[i]
        endTime = times[i+1]
        subClips.append(clip.subclip(startTime, endTime))
    for i, segment in enumerate(subClips):
        segment.audio.write_audiofile(outputDir + "/clip_" + str(times[i]) + ".mp3")


# example function execution
#moviePath = 'testVid.mp4'  # path of the video to process
#outputPath = 'slides'  # temp dir to store the files
#timeIncrement = 60.0  # time per slide in seconds
#spliceAndProcess(moviePath, timeIncrement, outputPath)
