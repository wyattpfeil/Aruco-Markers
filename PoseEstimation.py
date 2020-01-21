import numpy as np
import time
import cv2
import cv2.aruco as aruco
import pickle

aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)

# Creating a theoretical board we'll use to calculate marker positions
board = aruco.GridBoard_create(
    markersX=5,
    markersY=7,
    markerLength=0.04,
    markerSeparation=0.01,
    dictionary=aruco_dict)

mtx = None
dist = None

with open('callibrationData.pickle', 'rb') as handle:
    callibrationData = pickle.load(handle)
    dist = callibrationData["dist"]
    mtx = callibrationData["mtx"]
    
# while(cam.isOpened()):
#     # Capturing each frame of our video stream
#     ret, QueryImg = cam.read()
#     if ret == True:
#         # grayscale image
#         gray = cv2.cvtColor(QueryImg, cv2.COLOR_BGR2GRAY)
#         parameters = aruco.DetectorParameters_create()
    
#         # Detect Aruco markers
#         corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
#         # Make sure markers were detected before continuing
#         if ids is not None and corners is not None and len(ids) > 0 and len(corners) > 0 and len(corners) == len(ids):
#             # The next if makes sure we see all matrixes in our gridboard
#             if len(ids) == len(board.ids):
#                 # Calibrate the camera now using cv2 method
#                 ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
#                         objectPoints=board.objPoints,
#                         imagePoints=corners,
#                         imageSize=gray.shape, #[::-1], # may instead want to use gray.size
#                         cameraMatrix=None,
#                         distCoeffs=None)

#                 # # Calibrate camera now using Aruco method
#                 # ret, cameraMatrix, distCoeffs, _, _ = aruco.calibrateCameraAruco(
#                 #     corners=corners,
#                 #     ids=ids,
#                 #     counter=35,
#                 #     board=board,
#                 #     imageSize=gray.shape[::-1],
#                 #     cameraMatrix=None,
#                 #     distCoeffs=None)

#                 # Print matrix and distortion coefficient to the console
#                 break
# print("Callibrated!")
# print(dist)
# print("")
# print(mtx)
# callibrationData = {"dist": dist, "mtx": mtx}
#with open('callibrationData.pickle', 'wb') as handle:
    #pickle.dump(callibrationData, handle, protocol=pickle.HIGHEST_PROTOCOL)


cap = cv2.VideoCapture(4)

time.sleep(5)
while (True):
    ret, frame = cap.read()

    # operations on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(ids != None):

        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        #(rvec-tvec).any() # get rid of that nasty numpy value array error

        for i in range(0, ids.size):
            # draw axis for the aruco markers
            aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners)


        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0])+', '

        cv2.putText(frame, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)


    else:
        # code to show 'No Ids' when no markers are found
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    # display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()