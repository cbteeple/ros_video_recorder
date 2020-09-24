#!/usr/bin/env python

from video_recorder.srv import *
import rospy
import psutil
import shutil
import subprocess
import signal
from os.path import expanduser
import os
import time

pidDict = {}
recording = False
 
def recordTopics(req):
	global pidDict
	global recording
	global camera_topic

	if recording:
		pass

	command = "roslaunch video_recorder record_video.launch filename:=" + req.name + " camera_topic:=" + camera_topic
	print("Recording to file named %s."%(req.name))

	pidDict[req.name] = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True, cwd="/tmp/")
	#pidDict[req.name] = subprocess.Popen(command, shell=True, cwd="/tmp/",
	#											  stdin=None,
	#											  stdout=open(os.devnull, 'wb'),
	#											  stderr=open(os.devnull, 'wb'))

	recording = True

	time.sleep(2.0)
	print("waited 2 sec")

	return RecordVideoResponse(True)
 
def stopRecording(req, timeout = 2.0):
	global pidDict
	global recording

	if not recording:
		pass

	if req.name in pidDict:
		print("Stop recording to file named %s"%(req.name))
		p = pidDict[req.name]
		process = psutil.Process(p.pid)
		children = process.children(recursive=True)
		for subProcess in children:
			subProcess.send_signal(signal.SIGINT)
		psutil.wait_procs(children, timeout=timeout)
		p.wait()


	else:
		print("No current recording with name %s!"%req.name)

	recording = False
	return StopRecordingResponse(True)

 
def rosVideoRecorder():
	global camera_topic
	rospy.init_node('video_recorder_server')

	camera_topic = rospy.get_param(rospy.get_name()+'/camera_topic',False)

	recordServ = rospy.Service('record_video', RecordVideo, recordTopics)
	stopServ = rospy.Service('stop_recording', StopRecording, stopRecording)
	print("Ready to record topics")
	rospy.spin()

if __name__ == "__main__":
	rosVideoRecorder()
