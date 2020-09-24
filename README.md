## ros_video_recorder

ROS service to remotely start/stop recording videos from any camera stream.
Includes `*.srv` definitions necessary to issue requests.

This package spawns a subprocess of the following form to save a video stream: 
``` bash
roslaunch video_recorder record_video.launch filename:=NAME camera_topic:=TOPIC
```
which itself is just a call to the [image_view video_recorder node](http://wiki.ros.org/image_view).

The subrocess is killed when you ask to stop recording.

## Building

 - Clone the repo into the `src` directory of your catkin workspace
 - Run `catkin_make` from the root of your catkin workspace
 
## Running
### Start the service
- Start the service using launch file: `roslaunch video_recorder video_recorder.launch`

### Start/Stop recording
Use a ROS service call to start and stop recording. Here are some example code snippets:
```python
import video_recorder.srv as vrec

def start_saving(out_filename):
    rospy.wait_for_service('video_recorder/record')

    # Start saving a video
    try:
        service = rospy.ServiceProxy('video_recorder/record', vrec.RecordTopics)
        response = service(out_filename)
        return response.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def stop_saving(out_filename):
    # Stop saving data
    try:
        service = rospy.ServiceProxy('video_recorder/stop_recording', vrec.StopRecording)
        response = service(out_filename)
        return response.success
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

```