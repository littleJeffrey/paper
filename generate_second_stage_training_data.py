import csv
import math
import numpy as np
import argparse
import os

original = []
FRAME_WIDTH = 1920
NORMAL_LENGTH = 100
KEYPOINTS = [0, 5, 6, 7, 8, 9, 10, 11, 1, 2, 3, 4]

def get_distance(A, B):
    distance = math.pow((A[0] - B[0]), 2) + math.pow((A[1] - B[1]), 2)
    distance = math.sqrt(distance)
    return distance

def get_angle(first, second, angle):
    x1 = second[0] - first[0]
    y1 = second[1] - first[1]

    if angle == 0:
        x2 = 1
        y2 = 0
    elif angle == 90:
        x2 = 0
        y2 = 1
    elif angle == 180:
        x2 = -1
        y2 = 0
    elif angle == 270:
        x2 = 0
        y2 = -1
    dot = x1*x2+y1*y2
    det = x1*y2-y1*x2
    theta = np.arctan2(det, dot)
    theta = theta if theta>0 else 2*np.pi+theta
    theta = theta*180/np.pi
    if theta == 360: theta = 0.0

    return theta

if __name__ == '__main__':
    for names in os.listdir("before_transformed"):
        with open('./before_transformed/' + names, newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                lis = []
                for i in range(len(row)-1):
                    temp = eval(row[i])
                    lis.append(temp)
                lis.append(row[-1])
                original.append(lis)

    after = []
    for person in original:
        temp = []
        if person[5][0] == 0 or person[7][0] == 0: continue
        if get_distance(person[5], person[7]) == 0: continue
        scale = NORMAL_LENGTH / get_distance(person[5], person[7])

        #關鍵點位資訊(調過大小的)
        # temp.append(person[5][0])
        # temp.append(person[5][1])
        for i in KEYPOINTS:
            if i != 5:
                if person[i][0] == 0:
                    temp.append(-1)
                    temp.append(-1)
                else:
                    temp.append((person[i][0] - person[5][0]) * scale)
                    temp.append((person[i][1] - person[5][1]) * scale)

        #加入"左中右"和label
        if person[5][0] < (FRAME_WIDTH / 3): temp.append('left')
        elif person[5][0] > (FRAME_WIDTH / 3 * 2): temp.append('right')
        else: temp.append('middle')
        temp.append(person[-1])
        
        after.append(temp)


    with open('after_transform_1to15_second_stage.csv', 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)

        for i in after:
            writer.writerow(i)