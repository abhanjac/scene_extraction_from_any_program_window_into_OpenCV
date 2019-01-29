# Objective: 
The objective of this project is to be able to extract the scene or the content inside any active window of any program, into an opencv image or video. 

**A *Trailer* of Final Result:**

![](images/display_extration_gif.gif)

[**YouTube Link to Full Video**](https://youtu.be/0WNfKg60dAc)

---

In other words, anything that is shown inside the display window of a program, should be visible inside an opencv window as a numpy array.

The motivation of this project comes from various sources. Some of them are as follows: 

[**NOTE:** These also shows the potential application of the final code created at the end of this project.]

* There may also be some process running in a program window and we want to record the scene by scene changes of the process as shown in the window.
* Suppose the user is playing a computer game and wants to record the game like a movie as he plays it (some game software might have this option built in, but not all).
* Suppose the user wants to create a visual tutorial of some process or installation.
* There are often videos shown in the internet that are not available to record.
* Taking screenshot of only the display inside an opened window and not anything else visible in the neighboring region in the desktop.
* Suppose the user wants to do some kind of image processing on the scenes shown inside a program window.

These above aspects can be resolved if there is a code or a script such that the user will specify the name of the desired window (whose scene is to be extracted) and the code will display the scene as a numpy array in an 
opencv window.

