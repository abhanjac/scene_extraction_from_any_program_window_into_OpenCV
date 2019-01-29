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

# Requirements: 
* This application is should be created to run of a **Windows 10** machine.
* The user can specify the name of any window that is currently running.
* If the window is not running, there should be a graceful exit.
* If window is minimized, then the code should automatically maximize the target window.
* There should be a functionality to record the displayed images as a video as well.

# Current Framework: 
* Opencv libraries, Windows 10, Python 3.6.3 (Anaconda), Spyder framework (optional).
* PIL and ctypes packages of Python.

# Overview of the Script:
This describes the overall process of how this [python script](codes/capture_window.py) make use of the ctype functions to capture the scene inside the target window.

At first a **Menu** window is created as a gui using **tkinter** package that lists all the visible opened window available. There are some windows detected whose name are just empty strings, these are ignored.
This gui serves as a menu. There is a **button** for each of the windows available. If one of these button is pressed then the corresponding window is maximized and brought to front.
After this if the menu is closed then this window name is updated in a variable called **targetWinName** indicating that this is the desired window whose display is to be extracted.

The **targetWinName** variable contains the name of the window that is to be captured.
The entire code runs in a while loop continuously unless the user closes the opencv display window (by pressing **ESC**) or closes the actual target program window. These are the only two cases by which the code stops.

In windows, all the program windows have a **window handle object** (which is like a pointer) associated with the window. This is not fixed for the program. If the same program is closed and reopened again, it may have a different handle the second time.
But if this handle object can be accessed, then there are lot of **ctype** functions that can be used to do a number of processing on features of the window itself and also with the content of the window.

The while loop of the code always keeps some lists, **titles**, **hwndList**, **windowRect**, to keep track of the title, the handle object and the coordinates of the box of the target window that is to be captured.

These lists are regularly updated using a separate internal thread, by a callback function (**foreach_window**).
This callback function is created using the **ctype** functions called **EnumWindows** and **EnumWindowsProc**. 
Some help forums describing these functions can be found in this [**link**](https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/).

The foreach_window function accesses all the opened and visible windows (using the ctype function **IsWindowVisible**) with their respective handles and checks if the name of the window matches the targetWinName or not.

If a match is found then the window is first maximized (using the ctype function **OpenIcon**) and then the rectangle which is bounding this window is extracted using **GetWindowRect** function.

These are all stored into the lists (mentioned earlier) and they are accessed by local variables inside the main function inside the while loop from these lists.

They are then displayed inside an opencv window as a numpy array. These images can also be recorded as the frames of a video.

Provision has been made such that the code will stop automatically if the target window is closed. And once the target window is found, the code using the ctype function **IsIconic** checks if the window is minimized or not and prevents the user from accidentally minimizing it.

# Results:
The following images are the snaps of the different stages when the code is run.

#### Open script using Spyder:
The code is run using **Spyder**. Before the code is run, there should be some program windows which are visible either is maximized or minimized form. 
In this snapshot, a **VLC** player, a **Chrome** window and a folder called **data_3** is visible in minimized form (These are shown by the **RED** arrows).

![](images/1_marked_resized.png)

#### Run the script:
Once the script is run, the **Menu** window opens. This has the buttons for each available visible window. There may be some windows listed which are not visible as they are run by the windows os in background.
Since the user has not selected any program yet, so all the buttons are in **Released** position right now.

![](images/2_resized.png)

#### Select a window:
Once a button is pressed, the corresponding window is maximized and is brought to the front. 
The button in the menu which is in **Pressed** condition (follow the **RED** arrow in the image), belongs to the selected window.
This image shows that the **VLC** player is selected.

![](images/lion_king_1_marked_resized.png)

#### A change in selection:
If the user selects a different window now by pressing a different button, then that corresponding window will now be in the foreground above the previously selected window.
In the following image, the **Chrome** window is selected (indicated by the **RED** arrow), so it comes to the foreground in front of the previously selected **VLC** player (shown by the **BLUE** arrow).

![](images/chrome_1_marked_resized.png)

In this image the **data_3** folder window is selected (indicated by the **RED** arrow), and so it comes to the foreground. 
The **VLC** and **Chrome** windows (indicated by the **BLUE** arrows) goes to the background.

![](images/folder_1_marked_resized.png)

#### Extracting the display:
Now again we select back the **VLC** player window (indicated by the **RED** arrow). 
And after that the **Menu** gui is closed (using the cross mark at the top right corner, indicated by the **BLUE** arrow).

![](images/lion_king_2_marked_resized.png)

Immediately, the display inside the selected **VLC** player window is captured and displayed by the opencv window called **Display** (this Display window is indicated by the **RED** arrow and rectangle). 
These scenes are extracted in real time. Every scene of the VLC player window is captured and displayed in real time in the opencv **Display** window.

![](images/lion_king_3_marked_resized.png)

#### Recording the images as a video:
If the key **'r'** is pressed on the keyboard, then the images which are displayed in this opencv window will be recorded as a video and the recording will stop on pressing the key **'s'**.
This video will be saved in the location specified in the variable **vidRecPath**. 
The video recording is done with the help of the class **videoRecorder**. 

However, there is a small catch here, once the recording has started, video frames will be of the same size as the size of the current captured image. 
The screen size of the actual captured window should not be changed, else the recording will stop, as the same video cannot have frames of different sizes. 
So if the frame size changes (which will happen as the captured image always adjusts to the size of the actual program window) the video will stop.


## Video:
* A video of the real time operation of this code is available in this [**video**](video)

* This video is also uploaded to YouTube at this [**link**](https://youtu.be/0WNfKg60dAc)

* The glimpse of the operation is of this code is also shown in the following gif.

![](images/display_extration_gif.gif)

# Comments:
This script has only the access to the pixel coordinates of the rectangle of the target window, and so it shows whatever is being displayed in the region of the screen inside that rectangle. But if another window is blocking this region or is in the foreground of the target window, then this code will start showing the part of this foreground window inside that rectangle.
It really depends on the user to take care of this.

The code runs in real time just like the original program. But if the size of the target window is too large, for example the entire screen is specified as the target window, then the process may run at a slower speed. But if the target window is specified, then the code only takes into account that part of the screen and hence the code runs faster.

Also, to have the opencv window display the same content within a window of the same size as the rectangle of the target window, some of the display settings need to be altered. 
These following steps specifies that:

* You have to disable the high dpi settings for this python application (spyder python in this case). 
* Go to the **installed directory of this application -> right click on the shortcut -> go to properties -> Compatibility -> Change high DPI settings -> Check the box for 'override high DPI scaling behavior' -> in the dropdown select 'application'**. (These settings are tested for windows 10).
* This is a help [link](https://stackoverflow.com/questions/49268120/why-cannot-imagegrab-grab-capture-the-whole-screen) for this.

This same feature can also be implemented in Ubuntu using the **pyscreenshot** and **Xlib** package. But the pyscreenshot package is not very fast in grabbing the screen content.

# Possible Spin-offs from this Code:
* This code can be modified to create a function which will take the name of the target window as an argument and record the display.
* Image processing can be applied to the extracted display (or to a specific region of the extracted display) as well.

# References:
Some good links and websites to find the ctype functions and their applications are given below:

* [**Link1**](https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-getwindowrect), [**Link2**](https://docs.python.org/3/library/ctypes.html), [**Link3**](https://programtalk.com/python-examples/ctypes.windll.user32.GetWindowRect/), [**Link4**](https://stackoverflow.com/questions/49268120/why-cannot-imagegrab-grab-capture-the-whole-screen)


