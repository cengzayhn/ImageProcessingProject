from abc import ABC
import cv2
import tkinter
import numpy as np
from PIL import Image, ImageTk

width = 480
height = 480
delay = 250


class Frame_Grab(ABC):
    def __init__(self, value):
        self.value = value

    def Get_Frame(self):
        _, Frame = self.value.read()
        frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)

        return(frame)

class Sliders_Data(ABC):
    def __init__(self):
        pass

    def Set_Slider_Data(self, variable):
        self.__sliders_data = variable

    def Get_Slider_Data(self):
        return self.__sliders_data

class Region1(Frame_Grab, Sliders_Data):
    def __init__(self, value):
        Frame_Grab.__init__(self, value)
        Sliders_Data.__init__(self)
        self.pix_no = 0

    def Pixel_Calculation(self):
        img = self.Get_Frame()
        image = img[:, : width // 3]

        slider_data = self.Get_Slider_Data()
        low = (slider_data[0], slider_data[2], slider_data[4])
        up = (slider_data[1], slider_data[3], slider_data[5])

        remastered = np.array(cv2.inRange(image, low, up))
        uniques, count = np.unique(remastered, return_counts=True)
        self.pixelNo = count[np.where(uniques == 255)]

        if len(self.pixelNo) == 0:
            self.pixelNo = 0
        else:
            self.pixelNo = self.pixelNo[0]

        return self.pixelNo

class Region2(Frame_Grab, Sliders_Data):
    def __init__(self, cap):
        Frame_Grab.__init__(self, cap)
        Sliders_Data.__init__(self)
        self.PixelNO = 0

    def Pixel_Calculation(self):
        image = self.Get_Frame()
        image = image[:, width // 3 : 2 * width // 3]
        slider_data = self.Get_Slider_Data()
        lower = (slider_data[0], slider_data[2], slider_data[4])
        upper = (slider_data[1], slider_data[3], slider_data[5])
        filtered = np.array(cv2.inRange(image, lower, upper))
        uniques, count = np.unique(filtered, return_counts=True)
        self.PixelNO = count[np.where(uniques == 255)]

        if len(self.PixelNO) == 0:
            self.PixelNO = 0
        else:
            self.PixelNO = self.PixelNO[0]
        return(self.PixelNO)

class Region3(Frame_Grab, Sliders_Data):
    def __init__(self, value):
        Frame_Grab.__init__(self, value)
        Sliders_Data.__init__(self)
        self.PixelNO = 0

    def Pixel_Calculation(self):
        img = self.Get_Frame()
        img = img[:, 2 * width // 3 :]
        slider_data = self.Get_Slider_Data()
        low = (slider_data[0], slider_data[2], slider_data[4])
        upper = (slider_data[1], slider_data[3], slider_data[5])
        remastered = np.array(cv2.inRange(img, low, upper))
        uniques, count = np.unique(remastered, return_counts=True)
        self.PixelNO = count[np.where(uniques == 255)]

        if len(self.PixelNO) == 0:
            self.PixelNO = 0
        else:
            self.PixelNO = self.PixelNO[0]

        return self.PixelNO

class Filter(Frame_Grab, Sliders_Data):
    def __init__(self, value):
        Frame_Grab.__init__(self, value)
        Sliders_Data.__init__(self)

    def Filter_Implement(self):
        _, image = cv2.threshold(
            self.Get_Frame(), int(self.Get_Slider_Data()[6]), 255, cv2.THRESH_TRUNC
        )

        return image

class GUI:
    def __init__(self, ancestor):
        self.ancestor = ancestor
        ancestor.title("Term Project")

        self.apply_threshold = False

        cap = cv2.VideoCapture(0)

        self.r1 = Region1(cap)
        self.r2 = Region2(cap)
        self.r3 = Region3(cap)
        self.filter = Filter(cap)

        self.image_area = tkinter.Label(self.ancestor, width=width, height=height)
        self.image_area.grid(column=1, columnspan=10, row=1, rowspan=9)

        self.apply_threshold_button = tkinter.Button(
            self.ancestor,
            text="Apply\nThreshold",
            width=30,
            command=self.apply_threshold_func,
            background="red",
        )
        self.apply_threshold_button.grid(column=11, columnspan=2, row=7, rowspan=3)

        self.calculate_region_1 = tkinter.Button(
            self.ancestor,
            text="Calculate for\nRegion 1",
            width=30,
            command=lambda: self.calculate_region(self.r1),
            background="cyan",
        )
        self.calculate_region_1.grid(column=11, columnspan=2, row=10, rowspan=3)

        self.calculate_region_2 = tkinter.Button(
            self.ancestor,
            text="Calculate for\nRegion 2",
            width=30,
            command=lambda: self.calculate_region(self.r2),
            background="cyan",
        )
        self.calculate_region_2.grid(column=11, columnspan=2, row=13, rowspan=3)

        self.calculate_region_3 = tkinter.Button(
            self.ancestor,
            text="Calculate for\nRegion 3",
            width=30,
            command=lambda: self.calculate_region(self.r3),
            background="cyan",
        )
        self.calculate_region_3.grid(column=11, columnspan=2, row=16, rowspan=3)

        self.LH_slider = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="LH",
            length=450,
        )
        self.UH_slider = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="UH",
            length=450,
        )
        self.UH_slider.set(255)
        self.LS_slider = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="LS",
            length=450,
        )
        self.US_slider = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="US",
            length=450,
        )
        self.US_slider.set(255)
        self.LV_slider = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="LV",
            length=450,
        )
        self.UV_slider = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="UV",
            length=450,
        )
        self.UV_slider.set(255)
        self.threshold = tkinter.Scale(
            self.ancestor,
            from_=0,
            to=255,
            orient=tkinter.HORIZONTAL,
            label="Threshold",
            length=450,
        )

        self.LH_slider.grid(column=1, columnspan=10, row=10, rowspan=1)
        self.UH_slider.grid(column=1, columnspan=10, row=11, rowspan=1)
        self.LS_slider.grid(column=1, columnspan=10, row=12, rowspan=1)
        self.US_slider.grid(column=1, columnspan=10, row=13, rowspan=1)
        self.LV_slider.grid(column=1, columnspan=10, row=14, rowspan=1)
        self.UV_slider.grid(column=1, columnspan=10, row=15, rowspan=1)
        self.threshold.grid(column=1, columnspan=10, row=16, rowspan=1)

        self.loop()

    def loop(self):
        if self.apply_threshold:
            self.update_slider_data(self.filter)
            image = self.filter.Filter_Implement()
        else:
            self.update_slider_data(self.r1)
            image = self.r1.Get_Frame()

        image = ImageTk.PhotoImage(
            image=Image.fromarray(image).resize((width, height), Image.ANTIALIAS)
        )

        self.image_area["image"] = image
        self.image_area.image = image

        self.ancestor.after(delay, self.loop)

    def calculate_region(self, reg):
        self.update_slider_data(reg)
        pixel_no = reg.Pixel_Calculation()

        top = tkinter.Toplevel(self.ancestor)
        top.geometry("200x100")
        top.title("Pixel Calculation Result")
        tkinter.Label(
            top, text="Pixel No: {}".format(pixel_no), font=("Arial", 20)
        ).pack()

    def apply_threshold_func(self):
        self.apply_threshold = not self.apply_threshold

    def update_slider_data(self, val):
        slider_values = [
            self.LH_slider.get(),
            self.UH_slider.get(),
            self.LS_slider.get(),
            self.US_slider.get(),
            self.LV_slider.get(),
            self.UV_slider.get(),
            self.threshold.get(),
        ]

        val.Set_Slider_Data(slider_values)


root = tkinter.Tk()
gui = GUI(root)
root.mainloop()
