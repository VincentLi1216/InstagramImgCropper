from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from tkinter import ttk
from tkinter import filedialog as fd
import random
R_size = [800, 1000]
R_ratio = R_size[0]/R_size[1]
LR_x = [10,810]
LR_y = [10,1010]
RR_x = [100,200]
RR_y = [0,100]
RR3_x = [0, 0]
RR3_y = [0, 0]
R_num = 2


def do_zoom(event):
    global img, R_size
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    factor = 1.001 ** event.delta
    R_size = [int(R_size[0]*factor), int(R_size[0]*factor/R_ratio)]
    update_R_coord()




root = tk.Tk()
root.title('my window')

width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
file_path = "芹壁_李善得.jpg"
cv_img = cv2.imread(file_path)
img = Image.open(file_path)
def get_img_size(img, ratio=0.9):
    win_ratio = width/height
    img_ratio = img.size[0]/img.size[1]

    if win_ratio*img_ratio>0:
        img_height = height
        img_width = int(img.size[0]*height/img.size[1])
    else:
        img_width = width
        img_height = int(img.size[1]*width/img.size[1])
    return (int(img_width*ratio), int(img_height*ratio))
img_width, img_height = get_img_size(img)
def update_R_coord():
    global RR_x, RR_y, RR3_x, RR3_y
    LR_x[1] = LR_x[0]+R_size[0]
    LR_y[1] = LR_y[0]+R_size[1]
    RR_y = LR_y
    RR_x[0] = LR_x[1]
    RR_x[1] = RR_x[0] +R_size[0]


    try:
        canvas.delete(ALL)
    except:
        except_vari = None

    canvas.create_image(0, 0, anchor=tk.NW, image=img2)
    left_rec = canvas.create_rectangle(LR_x[0], LR_y[0], LR_x[1], LR_y[1], width=1, outline="red")
    right_rec = canvas.create_rectangle(RR_x[0], RR_y[0], RR_x[1], RR_y[1], width=1, outline="red")
    canvas.create_line(LR_x[0], LR_y[0] + int(R_size[1]/2), RR_x[1], LR_y[0] + int(R_size[1]/2), fill="gray", dash=(10, 2))
    canvas.create_line(LR_x[0]+int(R_size[0]/2), LR_y[0], LR_x[0]+int(R_size[0]/2), LR_y[1], fill="gray", dash=(10, 2))
    canvas.create_line(RR_x[0] + int(R_size[0] / 2), LR_y[0], RR_x[0] + int(R_size[0] / 2), LR_y[1], fill="gray",dash=(10, 2))

    if R_num == 3:
        RR3_y = LR_y
        RR3_x = [RR_x[1], RR_x[1]+R_size[0]]
        canvas.create_rectangle(RR3_x[0], RR3_y[0], RR3_x[1], RR3_y[1], width=1, outline="red")
        canvas.create_line(RR3_x[0] + int(R_size[0] / 2), LR_y[0], RR3_x[0] + int(R_size[0] / 2), LR_y[1], fill="gray", dash=(10, 2))
        canvas.create_line(RR3_x[0], LR_y[0] + int(R_size[1] / 2), RR3_x[1], LR_y[0] + int(R_size[1] / 2), fill="gray", dash=(10, 2))

def move_R(event):

    global LR_x, LR_y
    LR_x[0] = event.x
    LR_y[0] = event.y
    if event.x <= 0+3:
        LR_x[0] = 0+3
    if event.y <= 0+3:
        LR_y[0] = 0+3
    if event.x >= img_width - R_size[0]*R_num-1:
        LR_x[0] = img_width - R_size[0]*R_num -1
    if event.y >= img_height - R_size[1]-1:
        LR_y[0] = img_height - R_size[1] -1



    # print(LR_x, LR_y)
    update_R_coord()
def crop_btn_press():
    DR = img_width / cv_img.shape[1]  # display ratio
    final1 = cv_img[int((LR_y[0] - 3) / DR): int((LR_y[0] - 3) / DR) + int(R_size[1] / DR),
             int((LR_x[0] - 3) / DR): int((LR_x[0] - 3) / DR) + int(R_size[0] / DR)]
    cv2.imshow("final1", final1)
    print(int((LR_y[0] - 3) / DR), int((LR_y[0] - 3) / DR) + int(R_size[1] / DR), int((LR_x[0] - 3) / DR),
          int((LR_x[0] - 3) / DR) + int(R_size[0] / DR))
    cv2.imwrite("finals/final1.jpg", final1)

    final2 = cv_img[int((RR_y[0] - 3) / DR): int((RR_y[0] - 3) / DR) + int(R_size[1] / DR),
             int((RR_x[0] - 3) / DR) + 1: int((RR_x[0] - 3) / DR) + int(R_size[0] / DR)]
    cv2.imshow("final2", final2)
    print(int((RR_y[0] - 3) / DR), int((RR_y[0] - 3) / DR) + int(R_size[1] / DR), int((RR_x[0] - 3) / DR) + 1,
          int((RR_x[0] - 3) / DR) + int(R_size[0] / DR))
    cv2.imwrite("finals/final2.jpg", final2)

    if R_num == 3:
        final3 = cv_img[int((RR3_y[0] - 3) / DR): int((RR3_y[0] - 3) / DR) + int(R_size[1] / DR),
                 int((RR3_x[0] - 3) / DR) + 1: int((RR3_x[0] - 3) / DR) + int(R_size[0] / DR)]
        cv2.imshow("final3", final3)
        print(int((RR_y[0] - 3) / DR), int((RR_y[0] - 3) / DR) + int(R_size[1] / DR), int((RR_x[0] - 3) / DR) + 1,
              int((RR_x[0] - 3) / DR) + int(R_size[0] / DR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("finals/final3.jpg", final3)

def callbackFunc(event):
    global R_num
    if combo.get() == "2x1":
        R_num = 2
    if combo.get() == "3x1":
        R_num = 3
    # print(R_num)

def open_file():
    global cv_img, img, img2
    # file type
    filetypes = (
       ('Image Files', '*.jpg *.png'),
       ('All files', '*.*')
    )
    # show the open file dialog
    file = fd.askopenfile(filetypes=filetypes)
    print(file.name)
    cv_img = cv2.imread(file.name)
    img = Image.open(file.name)
    img = img.resize(get_img_size(img, 0.9))

    img2 = ImageTk.PhotoImage(img)
    canvas.create_image(10, 10, anchor=tk.NW, image=img2)
    canvas.imgref = img2
    # img = cv2.imread(file.name)
# def show_frame():
#     cv2image = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
#     cv2image = cv2.resize(cv2image, (int(cv2image.shape[1] * 720 / cv2image.shape[0]), 720))
#     img = Image.fromarray(cv2image)
#     # Convert image to PhotoImage
#     imgtk = ImageTk.PhotoImage(image=img)

def exit():
   root.destroy()

img = img.resize(get_img_size(img, 0.9))

img2 = ImageTk.PhotoImage(img)
#img2 = tk.PhotoImage(file='lena.gif')

canvas = tk.Canvas(root, width=width, height=height)

canvas.create_image(10,10, anchor=tk.NW, image=img2)
update_R_coord()
left_rec = canvas.create_rectangle(LR_x[0], LR_y[0], LR_x[1], LR_y[1], width=1, outline="red")
right_rec = canvas.create_rectangle(RR_x[0], RR_y[0], RR_x[1], RR_y[1], width=1, outline="red")


canvas.bind("<MouseWheel>", do_zoom)
canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
canvas.bind("<B1-Motion>", lambda event:move_R(event))
canvas.pack(padx=20, pady=20)

crop_btn = tk.Button(root, text="Open File", command=open_file)
crop_btn.place(x=20+img_width+20, y=20)

combo = ttk.Combobox(root, values=["2x1", "3x1"], width=8)
combo.place(x=20+img_width+20, y=70)
combo.current(0)
combo.bind("<<ComboboxSelected>>", callbackFunc)

crop_btn = tk.Button(root, text="crop", command=crop_btn_press)
crop_btn.place(x=20+img_width+20, y=115)

#init exit_bttn_lbl
exit_bttn_lbl = Button(root, text="Exit The App", command=exit)
exit_bttn_lbl.place(x=20+img_width+20, y=160 )


root.mainloop()

