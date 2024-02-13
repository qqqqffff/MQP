import numpy as np
import cv2
import os

for dirname, dirnames, filenames in os.walk('MQP-Apollo-Rowe-2023-11-25-3d/videos'):
    for file in filenames:
        if not file.__contains__('.mp4'):
            continue

        cap = cv2.VideoCapture('MQP-Apollo-Rowe-2023-11-25-3d/videos/' + file)
        cnt = 0

        w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)


        x, y, h, w = 700, 350, 450, 500
        if file.__contains__('side'):
            x, y, h, w = 540, 380, 210, 195

        # output
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('MQP-Apollo-Rowe-2023-11-25-3d/cropped-videos/cropped-' + file, fourcc, fps, (w, h))


        # Now we start
        while cap.isOpened():
            ret, frame = cap.read()

            # Counting frames
            cnt += 1

            # Avoid problems when video finish
            if ret == True:
                # Croping the frame
                crop_frame = frame[y:y+h, x:x+w]

                # Percentage
                xx = cnt * 100 / frames
                print(int(xx), '%')

                # Saving from the desired frames
                #if 15 <= cnt <= 90:
                #    out.write(crop_frame)

                # I see the answer now. Here you save all the video
                out.write(crop_frame)

                # Just to see the video in real time
                cv2.imshow('frame', frame)
                cv2.imshow('croped', crop_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

