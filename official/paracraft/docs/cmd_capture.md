<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/capture`**

**quick ref:**
> /capture [none|image|video|sound|text|objectdetection] [-width 400] [-height 300] [-duration 5] [-file temp/capture.png] [-event eventName]

**description:**

```
capture image with computer's camera. we will use webview to capture the image.
ESC key to close the camera window, click the camera window to take image. 
@return file|filename: if start with "temp/" we will save to temp folder, otherwise we will save to world folder.
@return callback function(filename, bSucceed). 
/capture image -width 400 -height 300 -file temp/camera.jpg
/capture sound -file temp/capture.wav
-- Chinese audio to text for 5 seconds at most
/capture text -duration 5
-- English audio to text
/capture text -language en -duration 3
/capture objectdetection start|stop
/capture pose start|stop
-- when user clicked, an event is fired with msg:{filename}
/capture video -event OnVideoCaptured
-- close camera capture window
/capture video stop
```

<!-- END_AUTOGEN-->

