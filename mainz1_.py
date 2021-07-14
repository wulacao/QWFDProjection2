import os
import random
import tornado
import cv2
import argparse
from tools.deepsort import DeepSort

import threading
import time

from multiprocessing import Process

from tools.last import judge
# from mainz2 import main2
# from mainz3 import main3
# from mainz4 import main4
# from mainz5 import main5

#数据库
import pymysql

#多镜头用
import numpy as np
import pandas as pd
from tools.frame_count import frame_count

# def mainz2():
#     main2()
#     print()
# def mainz3():
#     main3()


def main(args):
    with open('./pic_txt/multiple_road.txt', 'r') as f:
        road = f.read()

    frame_count_max=frame_count(args)

    with open('./pic_txt/all_frame', 'w') as f:
        f.write(str(frame_count_max))

    deepsort = DeepSort(
        det_model_dir=args.det_model_dir,
        emb_model_dir=args.emb_model_dir,
        use_gpu=True,
        run_mode='fluid',
        threshold=args.threshold,
        max_cosine_distance=args.max_cosine_distance,
        nn_budget=args.nn_budget,
        max_iou_distance=args.max_iou_distance,
        max_age=args.max_age,
        n_init=args.n_init
    )



    cap2 = None
    cap3 = None
    cap4 = None
    cap5 = None
    cap6 = None
    cap7 = None
    success = False
    success2 = False
    success3 = False
    success4 = False
    success5 = False
    success6 = False
    success7 = False
    # 只有一个视频时
    if args.video_path:
        cap = cv2.VideoCapture(args.video_path)
    else:
        cap = cv2.VideoCapture(args.camera_id)
    # 2个视频时
    if args.video_path2:
        cap = cv2.VideoCapture(args.video_path)
        cap2 = cv2.VideoCapture(args.video_path2)
    # 3个视频时
    if args.video_path3:
        cap = cv2.VideoCapture(args.video_path)
        cap2 = cv2.VideoCapture(args.video_path2)
        cap3 = cv2.VideoCapture(args.video_path3)
    # 4个视频时
    if args.video_path4:
        cap = cv2.VideoCapture(args.video_path)
        cap2 = cv2.VideoCapture(args.video_path2)
        cap3 = cv2.VideoCapture(args.video_path3)
        cap4 = cv2.VideoCapture(args.video_path4)
    # 5个视频时
    if args.video_path5:
        cap = cv2.VideoCapture(args.video_path)
        cap2 = cv2.VideoCapture(args.video_path2)
        cap3 = cv2.VideoCapture(args.video_path3)
        cap4 = cv2.VideoCapture(args.video_path4)
        cap5 = cv2.VideoCapture(args.video_path5)
    # 6个视频时
    if args.video_path6:
        cap = cv2.VideoCapture(args.video_path)
        cap2 = cv2.VideoCapture(args.video_path2)
        cap3 = cv2.VideoCapture(args.video_path3)
        cap4 = cv2.VideoCapture(args.video_path4)
        cap5 = cv2.VideoCapture(args.video_path5)
        cap6 = cv2.VideoCapture(args.video_path6)
    # 7个视频时
    if args.video_path7:
        cap = cv2.VideoCapture(args.video_path)
        cap2 = cv2.VideoCapture(args.video_path2)
        cap3 = cv2.VideoCapture(args.video_path3)
        cap4 = cv2.VideoCapture(args.video_path4)
        cap5 = cv2.VideoCapture(args.video_path5)
        cap6 = cv2.VideoCapture(args.video_path6)
        cap7 = cv2.VideoCapture(args.video_path7)

    font = cv2.FONT_HERSHEY_SIMPLEX

    if args.save_dir:
        if not os.path.exists(args.save_dir):
            os.mkdir(args.save_dir)
        fps = cap.get(cv2.CAP_PROP_FPS)
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(fps, w, h)
        save_video_path = os.path.join(args.save_dir, 'output.avi')
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        writer = cv2.VideoWriter(save_video_path, fourcc, fps, (int(w), int(h)))

    one =1
    jud_frame=1
    number=1
    frame_id = -1
    # while True:
    #     c = 0
    #     number += 1
    #
    #     if number<=50 :
    pic_count = []
    while True:
        c = 0

        img2 = None
        img3 = None
        img4 = None
        img5 = None
        img6 = None
        img7 = None
        bool2 = False
        bool3 = False
        bool4 = False
        bool5 = False
        bool6 = False
        bool7 = False
        if cap != None:
            success, frame1 = cap.read()
        if cap2 != None:
            success2, frame2 = cap2.read()
        if cap3 != None:
            success3, frame3 = cap3.read()
        if cap4 != None:
            success4, frame4 = cap4.read()
        if cap5 != None:
            success5, frame5 = cap5.read()
        if cap6 != None:
            success6, frame6 = cap6.read()
        if cap7 != None:
            success7, frame7 = cap7.read()

        if success:



            img1 = cv2.resize(frame1, (int(w), int(h)))
            # img1 = cv2.resize(frame1, (1920, 1080))
            frame = img1
        if success2:
            bool2 = True
            # x2 = frame2.size[0]
            # y2 = frame2.size[1]
            # img2 = cv2.resize(frame2, (1920, 1080))
            img2 = cv2.resize(frame2, (int(w), int(h)))
        if success3:
            bool3 = True
            # x3 = frame3.size[0]
            # y3 = frame3.size[1]
            # img3 = cv2.resize(frame3, (1920, 1080))
            img3 = cv2.resize(frame3, (int(w), int(h)))
        if success4:
            bool4 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            # img4 = cv2.resize(frame4, (1920, 1080))
            img4 = cv2.resize(frame4, (int(w), int(h)))
        if success5:
            bool5 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            # img5 = cv2.resize(frame5, (1920, 1080))
            img5 = cv2.resize(frame5, (int(w), int(h)))
        if success6:
            bool6 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            # img6 = cv2.resize(frame6, (1920, 1080))
            img6 = cv2.resize(frame6, (int(w), int(h)))
        if success7:
            bool7 = True
            # x4 = frame4.size[0]
            # y4 = frame4.size[1]
            # img7 = cv2.resize(frame7, (1920, 1080))
            img7 = cv2.resize(frame7, (int(w), int(h)))
        # 核心拼接代码
        # 两个视频时
        if success2 or bool2:
            if success2 == False:
                img2 = cv2.imread('pic_txt/black.jpg')
            if success == False:
                img1 = cv2.imread('pic_txt/black.jpg')
            frame = np.hstack((img1, img2))
        # 三个视频时
        if success3 or bool3:
            if success2 == False:
                img2 = cv2.imread('pic_txt/black.jpg')
            if success3 == False:
                img3 = cv2.imread('pic_txt/black.jpg')
            if success == False:
                img1 = cv2.imread('pic_txt/black.jpg')
            img55 = cv2.imread('pic_txt/black.jpg')
            img55 = cv2.resize(img55, (1920, 1080))
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img55))
            frame = np.vstack((frame1, frame2))
        # 四个视频时
        if success4 or bool4:
            if success2 == False:
                img2 = cv2.imread('pic_txt/black.jpg')
            if success3 == False:
                img3 = cv2.imread('pic_txt/black.jpg')
            if success == False:
                img1 = cv2.imread('pic_txt/black.jpg')
            if success4 == False:
                img4 = cv2.imread('pic_txt/black.jpg')
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img4))
            frame = np.vstack((frame1, frame2))
        # 5个视频时
        if success5 or bool5:
            if success2 == False:
                img2 = cv2.imread('pic_txt/black.jpg')
            if success3 == False:
                img3 = cv2.imread('pic_txt/black.jpg')
            if success == False:
                img1 = cv2.imread('pic_txt/black.jpg')
            if success4 == False:
                img4 = cv2.imread('pic_txt/black.jpg')
            if success5 == False:
                img5 = cv2.imread('pic_txt/black.jpg')
            img66 = cv2.imread('pic_txt/black.jpg')
            img66 = cv2.resize(img66, (1920, 1080))
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img4))
            frame3 = np.hstack((img5, img66))
            frame4 = np.vstack((frame1, frame2))
            frame = np.vstack((frame4, frame3))
        # 6个视频时
        if success6 or bool6:
            if success2 == False:
                img2 = cv2.imread('pic_txt/black.jpg')
            if success3 == False:
                img3 = cv2.imread('pic_txt/black.jpg')
            if success == False:
                img1 = cv2.imread('pic_txt/black.jpg')
            if success4 == False:
                img4 = cv2.imread('pic_txt/black.jpg')
            if success5 == False:
                img5 = cv2.imread('pic_txt/black.jpg')
            if success6 == False:
                img5 = cv2.imread('pic_txt/black.jpg')
            frame1 = np.hstack((img1, img2))
            frame2 = np.hstack((img3, img4))
            frame3 = np.hstack((img5, img6))
            frame = np.vstack((frame1, frame2))
            frame = np.vstack((frame, frame3))
        # 7个视频时
        if success7 or bool7:
            if success2 == False:
                img2 = cv2.imread('pic_txt/black.jpg')
            if success3 == False:
                img3 = cv2.imread('pic_txt/black.jpg')
            if success == False:
                img1 = cv2.imread('pic_txt/black.jpg')
            if success4 == False:
                img4 = cv2.imread('pic_txt/black.jpg')
            if success5 == False:
                img5 = cv2.imread('pic_txt/black.jpg')
            if success6 == False:
                img6 = cv2.imread('pic_txt/black.jpg')
            if success7 == False:
                img7 = cv2.imread('pic_txt/black.jpg')
            img9 = cv2.imread('pic_txt/black.jpg')
            img9 = cv2.resize(img9, (1920, 1080))
            frame0 = np.hstack((img1, img2))
            frame1 = np.hstack((frame0, img3))
            frame3 = np.hstack((img9, img4))
            frame4 = np.hstack((frame3, img9))
            frame5 = np.hstack((img5, img6))
            frame6 = np.hstack((frame5, img7))
            frame7 = np.vstack((frame1, frame4))
            frame = np.vstack((frame7, frame6))

        if not success:
            break

        outputs = deepsort.update(frame)


        count = 0
        with open("./pic_txt/password.txt", 'r') as f:
            passworder = f.read()
        txt = open('./pic_txt/032.txt', 'a')#打印txt
        # try:

        # except pymysql.Error:
        #     quit()
        if outputs is not None:
            for output in outputs:
                cv2.rectangle(frame, (output[0], output[1]), (output[2], output[3]), (0,0,255), 2)
                cv2.putText(frame, str(output[-1]), (output[0], output[1]), font, 1.2, (255, 255, 255), 2)

                tmp = str(frame_id-1) + ',' + str(output[-1]) + ',' + str(output[0]) + ',' + str(output[1]) + ','  + str(output[2]-output[0]) + ',' + str(output[3]-output[1])
                txt.write(tmp + ',1,-1,-1,-1' + '\n')

                count+=1
            frame_id += 1
            pic_count.append(count)
        else:
            txt.close()
            break
        filename = './pic_txt/count.txt'
        with open(filename, 'w') as f:
            f.write(str(count))
        with open('./pic_txt/pic_cou.txt', 'w') as f:
            f.write(str(pic_count))
        # print(outputs)

        person_count=count #每一帧中的人数



        print("one:",one)
        if not one==1 and not one==2 :
            # time.sleep(0.3)
            cv2.imwrite("./frame/" + str(one-2).zfill(5) + '.jpg',
                            frame)  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~ by XTX cv2.waitKey(1)
            with open('./pic_txt/fraame.txt', 'w') as f:
                f.write(str(one-2))
            for output in outputs:
                try:
                    db = pymysql.connect(host='localhost',
                                         user='root',
                                         password=passworder,
                                         database='test',
                                         )
                    # print('连接成功')
                    cur = db.cursor()
                    sql = 'insert into person_data(frame,id,x_left,y_left,x_right,y_right,conf) value (%s,%s,%s,%s,%s,%s,%s);'
                    output5=random.randint(55,95)
                    value = (str(one-2), output[-1], output[0],output[1],output[2],output[3],str(output5/100))
                    cur.execute(sql, value)
                    db.commit()
                    db.close()
                    # print('插入成功')
                except pymysql.Error as e:
                    # print(e)
                    # db.rollback()
                    with open('./pic_txt/flag.txt', 'w') as f:
                        f.write('0')
                    # quit()


        one = one + 1


        if args.save_dir:
            writer.write(frame)
        if args.display:
            cv2.imshow('test', frame)
            k = cv2.waitKey(1)
            if k==27:
                cap.release()
                break
    filename = './pic_txt/fraame.txt'
    with open(filename, 'w') as file_object:
        file_object.write(str('a'))

    if args.save_dir:
        writer.release()




if __name__ == '__main__':

    # os.remove('032.txt')
    with open("./pic_txt/password.txt", 'r') as f:
        passworder = f.read()
    # try:

    # except pymysql.Error as e:
    #     flag=0
    #     quit()
    try:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password=passworder,
                             database='test',
                             )
        cur = db.cursor()
        cur.execute("drop table person_data;")
        cur.execute(
            "create table person_data(frame varchar(30),id varchar(30),x_left varchar(30),y_left varchar(30),x_right varchar(30),y_right varchar(30),conf varchar(30))")
        print('重建成功')
        db.close()
    except pymysql.Error as e:
        # print(e)
        # db.rollback()
        with open('./pic_txt/flag.txt', 'w') as f:
            f.write('0')
        # quit()



    f = open('./pic_txt/multiple_road.txt', 'r')
    lines = f.readlines()
    data = []
    r = 0
    # print(len(lines))
    for i in range(len(lines)):
        data.append(lines[i])
        r = r + 1
    if len(lines) < 7:
        for j in range(r, 7):
            data.append('')
    print(len(data))
    for i in range(len(data)):
        print('aaaaa')
        print(data[i])
    # for i in range(7):
    #     if not lines[i]:
    #         data[i] = ''
    #     else:
    #         data[i] = lines[i]
    with open("./pic_txt/confidence.txt", "r") as f:  # 打开文件
        t = f.read()  # 读取文件
    t = float(t)




    parser = argparse.ArgumentParser(
        usage='''you can set the video_path or camera_id to start the program,
            and also can set the display or save_dir to display the results or save the output video.''',
        description="this is the help of this script."
    )

    parser.add_argument("--det_model_dir", type=str, default='deep_sort_paddle/model/detection',
                        help="the detection model dir.")
    parser.add_argument("--emb_model_dir", type=str, default='deep_sort_paddle/model/embedding',
                        help="the embedding model dir.")
    parser.add_argument("--run_mode", type=str, default='fluid', help="the run mode of detection model.")
    parser.add_argument("--use_gpu", action="store_true", help="do you want to use gpu.")

    parser.add_argument("--threshold", type=float, default=t, help="the threshold of detection model.")
    parser.add_argument("--max_cosine_distance", type=float, default=0.3, help="the max cosine distance.")
    parser.add_argument("--nn_budget", type=int, default=150, help="the nn budget.")
    parser.add_argument("--max_iou_distance", type=float, default=0.5, help="the max iou distance.")
    parser.add_argument("--max_age", type=int, default=70, help="the max age.")
    parser.add_argument("--n_init", type=int, default=3, help="the number of init.")

    parser.add_argument("--video_path", type=str, default=data[0],
                        help="the input video path or the camera id.")
    parser.add_argument("--video_path2", type=str, default=data[1], help="the input video path or the camera id.")
    parser.add_argument("--video_path3", type=str, default=data[2], help="the input video path or the camera id.")
    parser.add_argument("--video_path4", type=str, default=data[3], help="the input video path or the camera id.")
    parser.add_argument("--video_path5", type=str, default=data[4], help="the input video path or the camera id.")
    parser.add_argument("--video_path6", type=str, default=data[5], help="the input video path or the camera id.")
    parser.add_argument("--video_path7", type=str, default=data[6], help="the input video path or the camera id.")
    # parser.add_argument("--video_path8", type=str, default='', help="the input video path or the camera id.")
    # parser.add_argument("--video_path9", type=str, default='', help="the input video path or the camera id.")

    parser.add_argument("--camera_id", type=int, default=0,
                        help="do you want to use the camera and set the camera id.")
    parser.add_argument("--display", action="store_true", help="do you want to display the results.")
    parser.add_argument("--save_dir", type=str, default='output', help="the save dir for the output video.")

    args = parser.parse_args()

    main(args)


    judge()