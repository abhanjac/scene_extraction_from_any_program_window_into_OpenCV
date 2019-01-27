# -*- coding: utf-8 -*-

import numpy as np, copy, os, time, sys

import cv2, ctypes, tkinter as ttk
from PIL import ImageGrab

#==============================================================================

class videoRecorder( object ):
    '''
    Records the video from the video capture object given as input.
    '''
    def __init__( self, videoCaptureObject=None, fps=0 ):
        # If no fps is specified then set the fps from the input object.
        self.fps = videoCaptureObject.get( cv2.CAP_PROP_FPS ) if fps==0 else fps      
        self.fourcc = cv2.VideoWriter_fourcc( 'M','P','E','G' )
        self.recordStatus = False   # Indicates if recording is occuring or not.
        # This flag when True, indicates that the recording command is given.
    
#------------------------------------------------------------------------------

    def record( self, filePath, name, frame, recordFrame, overwrite=0 ):   
        # recordFrame is the command to start or stop recording.
        if recordFrame == ord('r') and self.recordStatus == False: 
            # Initialize writer and start recording when r is pressed.
            
            self.recordStatus = True
            # Since this flag is True from now onwards, so even if the r is 
            # pressed again, this if will not be executed and then the writer 
            # will not be reinintialized.
            
            nameOfFile = time.strftime('%Y_%m_%d_%H_%M_%S_') + name + '.avi' if \
                overwrite == 0 else name + '.avi' 
            # If overwrite is 0, video files will be created with time stamp so 
            # that they do not overwrite any previously saved files.
            
            nameOfFile = os.path.join( filePath, nameOfFile )
            
            row, col = frame.shape[0], frame.shape[1]
            self.writer = cv2.VideoWriter( nameOfFile, self.fourcc, self.fps, \
                (col, row) )
            #print( self.writer.isOpened() )
            self.writer.write( frame )  # Writing the frame.
            print( '\nVideo Recording Started...' )
            
        elif recordFrame == ord('s') and self.recordStatus == True:
            # Stop recording on pressing s (if writer was initialized before).
            self.writer.release()
            self.recordStatus = False
            print( '\nStopped Recording Video...' )
            
        elif self.recordStatus == True:
            # recordframe flag is True means that writer is already initialized.
            self.writer.write( frame )  # Writing the frame.
        
        else:
            pass
        
        return self.recordStatus

#==============================================================================

# The target window name should be a global variable, which is updated as per
# the choice provided by the user from the menu (created later).
targetWinName = None

# This is the index of the target window which is updated inside the showChoice
# callback function. This is initialized to -1.
targetWinIdx = -1

#==============================================================================

# Create some callback function to find out the list of opened program windows. 
EnumWindows = ctypes.windll.user32.EnumWindows
# https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/

# Used to create a callback function.
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), \
                                     ctypes.POINTER(ctypes.c_int))
# Gives window name text.
GetWindowText = ctypes.windll.user32.GetWindowTextW

# Gives window name length.
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW

# Checks if window is visible.
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

IsIconic = ctypes.windll.user32.IsIconic    # Checks if window is minimized.
OpenIcon = ctypes.windll.user32.OpenIcon    # Maximizes a window.

# Gets the rectangle of the window.
GetWindowRect = ctypes.windll.user32.GetWindowRect

# Sets the window to the foreground.
SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow

# https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-getwindowrect
# https://docs.python.org/3/library/ctypes.html
# https://programtalk.com/python-examples/ctypes.windll.user32.GetWindowRect/
# https://stackoverflow.com/questions/49268120/why-cannot-imagegrab-grab-capture-the-whole-screen

# File "C:\ProgramData\Anaconda3\lib\site-packages\PIL\Image.py", line 2539, in _decompression_bomb_check
#   (pixels, 2 * MAX_IMAGE_PIXELS))

#==============================================================================

def foreachWindow( hwnd, lParam ):
    '''
    This function is used to create a callback function. It is used to return 
    the handle for the window whose name matches the targetWinName (which is 
    a global variable).
    '''
    if IsWindowVisible( hwnd ):
        length = GetWindowTextLength( hwnd )
        buff = ctypes.create_unicode_buffer( length + 1 )
        GetWindowText( hwnd, buff, length + 1 )
        #print( buff.value )
        
        if buff.value == targetWinName:    # buff.value is the window name.
            titles.append( buff.value )
            hwndList.append( hwnd )
            
            if IsIconic( hwnd ):
                # If window is minimized then maximize it.
                OpenIcon( hwnd )
                print( '\nWARNING: Minimizing the window is not permitted. ' \
                       'Stop this code and then minimize the window.\n' )
            
            # The rect object should be send in by reference.
            rect = ctypes.wintypes.RECT()
            GetWindowRect( hwnd, ctypes.byref( rect ) )
            windowRect.append( [ rect.left, rect.top, rect.right, rect.bottom ] )
            
    return True
    
#===============================================================================

def listOfWindowNames( hwnd, lParam ):
    '''
    This function is used to create a callback function. This gives a list of 
    visible windows.
    '''
    if IsWindowVisible( hwnd ):
        length = GetWindowTextLength( hwnd )
        buff = ctypes.create_unicode_buffer( length + 1 )
        GetWindowText( hwnd, buff, length + 1 )
        #print( buff.value )
        
        if buff.value != '':    # Some program names are just ''. Skip those.
            winNameList.append( buff.value )
            winHwndList.append( hwnd )

    return True

#==============================================================================

def showChoice():
    '''
    This is the callback function that is used by the radiobuttons. This 
    returns the value of the variable v which indicates the choice which the 
    user has indicated using the buttons.
    '''
    global targetWinIdx    # This is declared as a global variable.
    global targetWinName   # This is declared as a global variable.
    targetWinIdx = v.get()  # Storing the index of the selected window.
    
#------------------------------------------------------------------------------

    #print( targetWinIdx )
    if targetWinIdx != -1:
        # Only if proper choice is provided (i.e. when the choice is some number 
        # other than the defalut -1), the targetWinName and targetWinHwnd 
        # variables are updated.
        targetWinName = winNameList[ targetWinIdx ]
        targetWinHwnd = winHwndList[ targetWinIdx ]
    
        if IsIconic( targetWinHwnd ):
            # If window is minimized then maximize it.
            OpenIcon( targetWinHwnd )
            print( '\nWARNING: Minimizing the window is not permitted. ' \
                   'Stop this code and then minimize the window.\n' )
        
        # When the button corresponding to a window is pressed, the window is 
        # brought to the foreground. This way the user can know which window is 
        # being currently chosen.
        SetForegroundWindow( targetWinHwnd )    # Bring target window to foreground.

#==============================================================================

if __name__ == '__main__':

    # The idea is that, the mass spectrometer program that shows the image of 
    # the reaction spots on the slide, should be located first and then the 
    # part of the window that shows the image of the reaction spot should be
    # extracted and displayed in a seperate window.
    # Then image processing should be applied to this display to find the 
    # location of the reaction spot.

    # Create display window.
    key = ord('`')

    # Defining the video recorders.
    vidRec = videoRecorder( fps=30 )
    vidRecPath = './'

    # A flag that indicates whether the target window exists or not.
    targetWinExists = False
    # A flag that indicates whether the display window is created or not.
    displayWinCreated = False
    displayWinName = 'Display'
    
#------------------------------------------------------------------------------

    # Before the extraction of the display begins, a window will pop up which
    # will show what are the current open displayed windows in the system.
    # This will be a menu window.
    
    # Finding the list of visible windows and their handles.
    winNameList, winHwndList = [], []
    
    EnumWindows( EnumWindowsProc( listOfWindowNames ), 0 )
    # print( winNameList )
    nWin = len( winNameList )
    
    # Finding the max length of all the window names.
    maxLengthOfText = 0
    for i in winNameList:
        lengthOfText = len(i)
        maxLengthOfText = lengthOfText if lengthOfText > maxLengthOfText \
                                       else maxLengthOfText
    # print( maxLengthOfText )

#------------------------------------------------------------------------------

    root = ttk.Tk()
    root.title( 'List Of Programs' )    # Title of the menu.
    
    # The overall text displayed will fixed.
    displayTextLen = 75

    # The height of this menu window will be proportional to the number of 
    # program names that is to be displayed.
    # Height is decided as per nWind and the multiplier is decided by trial.
    # Width is decided as per the displayTextLen times a fraction (which is 
    # decided by trial and error).

    menuW, menuH = int( displayTextLen * 8.25 ), nWin * 33 + 66
    root.geometry( f'{menuW}x{menuH}' )      # Size of the menu window.
    root.resizable( height=False, width=False )     # Resizing not allowed.
    
#------------------------------------------------------------------------------

    # Now taking each of the program name from the winNameList and displaying 
    # it in the menu window in a radiobutton.
    
    # This is the instruction label.
    instructionLabel1 = 'Select the program whose display window is to be extracted'
    label = ttk.Label( root, text=instructionLabel1, fg='blue', \
                       font=('Helvetica', 11, 'bold'), \
                       anchor='c', width=displayTextLen, \
                       padx=0, pady=5, wraplength=menuW*0.9 )
    label.pack()

    instructionLabel2 = '[NOTE: Close this window after selection to initiate extraction.]'
    label = ttk.Label( root, text=instructionLabel2, fg='red', \
                       font=('Helvetica', 9, 'bold'), \
                       anchor='c', width=displayTextLen, \
                       padx=0, pady=5, wraplength=menuW*0.9 )
    label.pack()

#------------------------------------------------------------------------------

    v = ttk.IntVar()     # This will indicate the choice supplied by the user.
    v.set(-1)    # Initializing the value of the variable to -1.
    # This will cause all the buttons to be deselected in the beginning.

    for idx, i in enumerate( winNameList ):
        # The text of the labels are wropped around if they are too long.
        lengthOfText = len( i )
        
        # Some programs may have very big names. So only the first and last 
        # part of the name is displayed in those cases.
        if lengthOfText > displayTextLen:
            textDisplayed = i[ : displayTextLen - 4 ] + ' ...'
        else:
            textDisplayed = i
        
        radiobutton = ttk.Radiobutton( root, text=textDisplayed, padx=0, \
                                       width=displayTextLen, indicatoron=0, \
                                       variable=v, command=showChoice, value=idx )
        radiobutton.pack( anchor='c' )
        # The indicatoron option = 0 will show the choices as buttons. If this
        # choice = 1, then they are shown as rounded circles.
        
    root.mainloop()

#------------------------------------------------------------------------------

    while key & 0xFF != 27:
        startTime = time.time()

        # These variables will hold the information about the desired window.
        titles, hwndList, windowRect = [], [], []

        # This runs in a seperate thread. Access the windows and find the 
        # rectangle region of the screen where this target window is located.
        EnumWindows( EnumWindowsProc( foreachWindow ), 0 )
        
#------------------------------------------------------------------------------
        
        if len( windowRect ) == 0:
            # If there are no window open which has the name same as targetWinName
            # and also there are no display window created as well, then break.
            print( f'\nERROR: No window found with the specified targetWinName, ' \
                   f'or no proper choice provided via the menu. Aborting.\n' )
            break

        elif len( windowRect ) > 0 and not displayWinCreated:
            # If the target window exists then create the display window if not 
            # created yet.
            cv2.namedWindow( displayWinName )
            cv2.moveWindow( displayWinName, 1000, 100 )
            displayWinCreated = True    # Update the flag.
        
        elif len( windowRect ) == 0 and displayWinCreated:
            # If the target window is not present (may be closed) but a 
            # display window is still present, then kill it and also break 
            # the loop.
            cv2.destroyWindow( displayWinName )
            displayWinCreated = False    # Update the flag.
            break
        
        else:
            # If the target window is found and also the display window is 
            # open, that means the code is running properly and so just check
            # for keypress.
            key = cv2.waitKey(1)    # Press ESC to stop the code.
            
#------------------------------------------------------------------------------
    
        # Top left and Bottom Right x and y coordinates of the targetWindow.
        tlx, tly, brx, bry = windowRect[0]
        #print( tlx, tly, brx, bry )
        
        # Grab frame with the included package. This is a PIL image object.
        # Grab and show the part of the screen. This way it is much faster.
        im = ImageGrab.grab( bbox=( tlx, tly, brx, bry ) )      # X1,Y1,X2,Y2.
        img = np.asanyarray( im )     # Convert to array.

        # You have to disable the high dpi settings for this application 
        # (spyder python in this case). Go to the installed directory of this 
        # application -> right click on the shortcut -> go to properties ->
        # Compatibility -> Change high DPI settings -> Check the box for 
        # 'override high DPI scaling behavior' -> in the dropdown select 
        # 'application'. (These settings are tested for windows 10).
        # https://stackoverflow.com/questions/49268120/why-cannot-imagegrab-grab-capture-the-whole-screen

        # Convert to BGR, since the inputed format is RGB (being a PIL image).
        img = cv2.cvtColor( img, cv2.COLOR_RGB2BGR )
        #cv2.rectangle( img, (20,40), (60,80), (0,255,0), 2 )
        cv2.imshow( displayWinName, img )

        # Press 'r' to record frames as a video.
        vidRec.record( filePath=vidRecPath, name='video', frame=img, \
                       recordFrame=(key & 0xFF) ) 

		# IMPORTANT: once the recording has started, video frames will be of 
        # the same size as the size of the current captured image. The screen 
        # size of the actual captured window should not be changed, else the 
        # recording will stop, as the same video cannot have frames of 
        # different sizes. So if the frame size changes (which will happen as
        # as the captured image always adjusts to the size of the actual 
        # window) the video will stop.

        #print( time.time() - startTime, 'sec' )
        
#------------------------------------------------------------------------------

    cv2.destroyAllWindows()
    

            
            