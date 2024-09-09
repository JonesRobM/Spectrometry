import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
from wrapt_timeout_decorator import *

def measure(name='Spectrum'):
    cap = cv2.VideoCapture(1)

    roi_selected = False
    
    while(True):
        ret, frame = cap.read()
        
        k = cv2.waitKey(1)
        
        if k & 0xFF == ord('s') and roi_selected == True:
            shape = cropped.shape
            r_dist = []
            b_dist = []
            g_dist = []
            i_dist = []
            for i in range(shape[1]):
                r_val = np.mean(cropped[:, i][:, 0])
                g_val = np.mean(cropped[:, i][:, 1])
                b_val = np.mean(cropped[:, i][:, 2])
                i_val = (r_val + b_val + g_val) / 3

                r_dist.append(r_val)
                g_dist.append(g_val)
                b_dist.append(b_val)
                i_dist.append(i_val)
            
            fig,[ax1,ax2] = plt.subplots(nrows=2, ncols=1,sharex=True)
            fig.set_size_inches(10, 10)
            fig.subplots_adjust(hspace=0.0)
            ax1.imshow(frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])])
            
            ax2.plot(r_dist, color='r', label='red')
            ax2.plot(g_dist, color='g', label='green')
            ax2.plot(b_dist, color='b', label='blue')
            ax2.plot(i_dist, color='k', label='mean')
            ax2.legend(loc="upper left")
            asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
            asp /= np.abs(np.diff(ax1.get_xlim())[0] / np.diff(ax1.get_ylim())[0])
            ax2.set_aspect(asp)
            ax1.set_ylabel('Pixel', fontsize = 14)
            ax2.set_xlabel('Pixel', fontsize = 14)
            ax2.set_ylabel('Intensity', fontsize = 14)
            plt.savefig(name+'.png', dpi = 600, bbox_inches='tight')
            plt.show()
            
        elif k & 0xFF == ord('r'):
            r = cv2.selectROI(frame)
            roi_selected = True
            
        elif k & 0xFF == ord('q'):
            break
        
        else:
            if roi_selected:
                cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                cv2.imshow('roi', cropped)
            else:
                cv2.imshow('frame', frame)

    cap.release()
    cv2.destroyAllWindows()
    print("Timeout after 60 seconds.")
    