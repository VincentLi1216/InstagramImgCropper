import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk, ImageChops
import os


class PhotoApp:

    def __init__(self):
        # Make window
        self.mainwindow = tk.Tk()

        # Centers Window To Screen
        self.screenwidth = self.mainwindow.winfo_screenwidth()
        self.screenheight = self.mainwindow.winfo_screenheight()
        self.place_width = str(int(self.screenwidth / 2 - 400))
        self.place_height = str(int(self.screenheight / 2 - 329))
        self.mainwindow.geometry("+" + self.place_width + "+" + self.place_height)

        # Initial Window Setup
        self.mainwindow.title("Photo Viewer")
        self.mainwindow.iconbitmap("unitato.ico")
        self.mainwindow.resizable(width=False, height=False)

        # Variable Declaration
        self.avariable = 1
        self.photoindex = 0
        self.currentphoto = ""
        self.photofactor = 0
        self.currentphotopath = ""
        self.currentphotoready = ""
        self.folderpath = ""
        self.lastfolderpath = ""
        self.photopath = ""
        self.photolist = []
        self.listspot = 0
        self.cwd = "C:/Users/Aaron/Pictures"
        self.rememberme = False
        self.displayatx = 0
        self.displayaty = 0
        self.mouseup = True
        self.currentrotation = 0
        self.thecolor = self.colorcheck()
        self.zoomlevel = 0

        # Widget Layout
        self.setup()

        # Key Bindings
        self.mainwindow.bind("<Up>", self.moveup)

        # Initiates Main Loop
        self.mainwindow.mainloop()

    def setup(self):
        print("Setup Begin")
        b_border = 10

        self.frame1 = tk.Frame(self.mainwindow)
        self.frame1.pack(side=tk.TOP)

        self.frame2 = tk.Frame(self.mainwindow)
        self.frame2.pack(side=tk.TOP)

        self.leftframe = tk.Frame(self.frame1, height=600, width=100,
                                  bd=5, relief=tk.GROOVE)
        self.leftframe.pack(side=tk.LEFT)
        self.leftframe.pack_propagate(0)

        self.rotaterightbutton = tk.Button(self.leftframe, text="Rotate ->",
                                           font=("Arial", 12), command=self.rotateright)
        self.rotaterightbutton.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.rotateleftbutton = tk.Button(self.leftframe, text="<- Rotate",
                                          font=("Arial", 12), command=self.rotateleft)
        self.rotateleftbutton.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.photoframe = tk.Frame(self.frame1, width=600, height=600)
        self.photoframe.pack(side=tk.LEFT)
        self.photoframe.pack_propagate(0)

        self.rightframe = tk.Frame(self.frame1, height=600, width=100,
                                   bd=5, relief=tk.GROOVE)
        self.rightframe.pack(side=tk.LEFT)
        self.rightframe.pack_propagate(0)

        self.wipbutton = tk.Button(self.rightframe, text="WIP",
                                   font=("Arial", 14), command=self.whatwip)
        self.wipbutton.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.leftbutton = tk.Button(self.rightframe, text="[Left]",
                                    font=("Arial", 14), command=self.moveleft)
        self.leftbutton.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.rightbutton = tk.Button(self.rightframe, text="[Right]",
                                     font=("Arial", 14), command=self.moveright)
        self.rightbutton.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.upbutton = tk.Button(self.rightframe, text="[Up]",
                                  font=("Arial", 14))  # , command=self.moveup)
        self.upbutton.pack(side=tk.TOP, pady=10, fill=tk.X)
        self.upbutton.bind("<ButtonPress-1>", self.moveup)

        self.downbutton = tk.Button(self.rightframe, text="[Down]",
                                    font=("Arial", 14), command=self.movedown)
        self.downbutton.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.photodisplay = tk.Label(self.photoframe, text="No Photo To Display",
                                     font=("Arial", 14))
        self.photodisplay.place(x=self.zoomsizing_frame()[2],
                                y=self.zoomsizing_frame()[3],
                                width=1000, height=1000)

        self.bottomframe = tk.Frame(self.frame2, width=600, height=100, bd=5,
                                    relief=tk.GROOVE)
        self.bottomframe.pack(side=tk.TOP)
        self.photoframe.pack_propagate(0)

        self.previousbutton = tk.Button(self.bottomframe, text="Previous",
                                        font=("Arial", 14), width=10,
                                        command=self.previous)
        self.previousbutton.pack(side=tk.LEFT, anchor=tk.W,
                                 padx=b_border)

        self.zoomout = tk.Button(self.bottomframe, text="(-)",
                                 font=("Arial", 18), command=self.zoomout)
        self.zoomout.pack(side=tk.LEFT, padx=b_border)

        self.folderbutton = tk.Button(self.bottomframe, text="Folder Select",
                                      font=("Arial", 14), width=15, command=self.folderselect)
        self.folderbutton.pack(side=tk.LEFT, padx=b_border)

        self.zoomin = tk.Button(self.bottomframe, text="(+)",
                                font=("Arial", 18), command=self.zoomin)
        self.zoomin.pack(side=tk.LEFT, padx=b_border)

        self.nextbutton = tk.Button(self.bottomframe, text="Next", font=(
            "Arial", 14), width=10, command=self.next)
        self.nextbutton.pack(side=tk.LEFT, padx=b_border)

        print("Setup End")

    def colorcheck(self):
        color16 = self.mainwindow.winfo_rgb("systembuttonface")
        color8List = []

        for value in color16:
            newvalue = value / 256
            newvalue = int(newvalue)
            color8List.append(newvalue)
            print(value, newvalue, "\n", color8List)

        rgbtuple = tuple(color8List)
        return (rgbtuple)

    def zoomsizing_photo(self):
        resolution = [600, 600]
        if self.zoomlevel == 0:
            resolution = [600, 600]
        elif self.zoomlevel == 1:
            resolution = [1200, 1200]
        elif self.zoomlevel == -1:
            resolution = [300, 300]
        else:
            resolution = [600, 600]
        return resolution

    def zoomsizing_frame(self):
        resandplace = [1000, 1000, -200, -200]
        if self.zoomlevel == 0:
            resolution = [1000, 1000, -200, -200]
        elif self.zoomlevel == 1:
            resolution = [2000, 2000, -700, -700]
        elif self.zoomlevel == -1:
            resolution = [500, 500, 50, 50]
        else:
            resolution = [1000, 1000, -200, -200]
        return resolution

    def zoomin(self):
        self.zoomlevel = self.zoomlevel + 1
        self.reloadphoto()
        print(self.zoomlevel)

    def zoomout(self):
        self.zoomlevel = self.zoomlevel - 1
        self.reloadphoto()
        print(self.zoomlevel)

    def next(self):
        print("Next Begin")
        self.displayatx = 0
        self.displayaty = 0
        self.zoomlevel = 0
        self.currentrotation = 0
        if self.currentphoto != None:
            self.currentphoto.close()
            self.currentphoto = None
        if self.photoindex < len(self.photolist) - 1:
            self.photoindex = self.photoindex + 1
        else:
            self.photoindex = 0

        self.reloadphoto()

        print("Next End")

    def previous(self):
        print("Previous Begin")
        self.displayatx = 0
        self.displayaty = 0
        self.zoomlevel = 0
        self.currentrotation = 0
        if self.currentphoto != None:
            self.currentphoto.close()
            self.currentphoto = None
        if self.photoindex == 0:
            self.photoindex = len(self.photolist) - 1
        else:
            self.photoindex = self.photoindex - 1

        self.reloadphoto()
        print("Previous End")

    def folderselect(self):
        print("Folder Select Begin")
        self.folderpath = filedialog.askdirectory(parent=self.mainwindow,
                                                  initialdir=self.cwd,
                                                  title="Choose A Folder To View Photos In.")
        if self.folderpath != "":
            self.lastfolderpath = self.folderpath
            self.rememberme = False
        else:
            self.lastfolderpath = self.lastfolderpath
            self.folderpath = self.lastfolderpath
            self.rememberme = True

        print(self.folderpath)
        if self.folderpath != "" and self.rememberme == False:
            print("Mark 1")
            self.photolist = []
            self.photoindex = 0
            self.displayatx = 0
            self.displayaty = 0
            self.currentphotoready = None
            self.cwd = self.folderpath
            for name in os.listdir(self.folderpath):
                if name.lower().endswith(".jpg") or name.lower().endswith(".png") or name.lower().endswith(
                        "tiff") or name.lower().endswith(".gif"):
                    self.photolist.append(name)
            # print(self.photolist)

            if self.photolist != []:
                self.reloadphoto()
            else:
                self.photodisplay["image"] = ""
                self.photodisplay["text"] = "No photos in this folder."
                print(self.photodisplay["text"], self.photodisplay["image"])

        else:
            self.folderpath = self.lastfolderpath
            if self.photolist != []:
                self.reloadphoto()
            else:
                self.photodisplay["image"] = ""
                self.photodisplay["text"] = "No photos in this folder."
                print(self.photodisplay["text"], self.photodisplay["image"])

        print("Folder Select End")

    def loadphoto(self):
        print("Load Photo Begin")
        print(self.photoindex)
        self.photodisplay["image"] = ""
        self.currentphotoready = ""
        name = self.photolist[self.photoindex]
        if name.lower().endswith(".gif"):
            self.gifplayback()
        else:
            if self.folderpath != "":
                self.currentphotopath = self.folderpath + "/" + str(self.photolist[self.photoindex])
                self.currentphoto = Image.open(self.currentphotopath)

        print("Load Photo End")

    def reloadphoto(self):
        self.loadphoto()
        self.photoscale()
        self.photorotate()
        self.displayphoto()

    def displayphoto(self):
        print("Display Photo Begin")
        self.photodisplay.place(width=self.zoomsizing_frame()[0], height=self.zoomsizing_frame()[1],
                                x=self.zoomsizing_frame()[2] + self.displayatx,
                                y=self.zoomsizing_frame()[3] + self.displayaty)
        self.currentphotoready = ImageTk.PhotoImage(self.currentphoto)
        self.photodisplay.config(image=self.currentphotoready)
        print("Display Photo End")

    def photoscale(self):
        print("Photo Scale Begin")
        print(self.currentphoto.width, self.currentphoto.height)
        if self.currentphoto.width > self.currentphoto.height:
            self.photofactor = self.currentphoto.width / self.zoomsizing_photo()[0]
        else:
            self.photofactor = self.currentphoto.height / self.zoomsizing_photo()[1]

        # self.currentphoto = self.currentphoto.resize((int(self.currentphoto.width / self.photofactor),
        # int(self.currentphoto.height / self.photofactor)), resample=0)

        self.currentphoto.thumbnail((int(self.currentphoto.width / self.photofactor),
                                     int(self.currentphoto.height / self.photofactor)), Image.ANTIALIAS)

        print(self.currentphoto.width, self.currentphoto.height)
        print("Photo Scale End")

    def photorotate(self):
        self.currentphoto = self.currentphoto.rotate(self.currentrotation, expand=True,
                                                     fillcolor=self.thecolor)

    def gifplayback(self):
        if self.currentphoto != "":
            self.currentphoto.close()
        self.photodisplay["image"] = ""
        self.photodisplay["text"] = "Gif playback is not yet implemented. \n Please come back later.\n =)"

    def whatwip(self):
        if self.currentphoto != "":
            self.currentphoto.close()
        self.photodisplay["image"] = ""
        self.photodisplay["text"] = ("""Gif playback \n \n Image rotation \n \n Slideshow mode \n \n Image Too Large Error (or ignore)
                                   \n Zoom In \n \n Zoom Out \n \n Move Image With Mouse
                                   \n Hold Down Mouse For Move""")

    def moveleft(self):
        print("moveleft")
        if self.currentphoto != "":
            self.displayatx = self.displayatx + 10
            self.reloadphoto()

    def moveright(self):
        print("moveright")
        if self.currentphoto != "":
            self.displayatx = self.displayatx - 10
            self.reloadphoto()

    def moveup(self, key):
        print("moveup")
        if self.currentphoto != "":
            self.displayaty = self.displayaty + 10
            self.reloadphoto()

    def movedown(self):
        print("movedown")
        if self.currentphoto != "":
            self.displayaty = self.displayaty - 10
            self.reloadphoto()

    def rotateleft(self):
        print("Rotate left")
        if self.currentphoto != "":
            self.currentrotation = self.currentrotation + 10
            self.reloadphoto()

    def rotateright(self):
        print("Rotate right")
        if self.currentphoto != "":
            self.currentrotation = self.currentrotation - 10
            self.reloadphoto()


def main():
    program = PhotoApp()


if __name__ == "__main__":
    main()