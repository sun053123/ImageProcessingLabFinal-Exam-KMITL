import math
import sys

from PIL import Image
import numpy as np

#
# class StructuringElement:
#     elements = None
#     width = 0
#     height = 0
#     origin = None
#     ignoreElements = None
#
#     def __init__(self, width=None, height=None, origin=None):
#         self.width = width
#
#         self.height = height
#         if (origin.real < 0 or origin.real >= width or origin.imag < 0 or origin.imag >= height):
#             self.origin = complex(0, 0)
#         else:
#             self.origin = origin
#         self.elements = np.zeros([width, height])
#         self.ignoreElements = []


class ImageLibrary:

    def __init__(self, width=None, height=None, bitDepth=None, img=None, data=None, origin=None, plot=None, font=None):
        self.width = width
        self.height = height
        self.bitDepth = bitDepth
        self.img = img
        self.data = data
        self.origin = origin
        self.plot = plot
        self.font = font

    def read(self, fileName):
        self.img = Image.open(fileName)
        self.data = np.array(self.img)
        self.original = np.copy(self.data)
        self.width = self.data.shape[0]
        self.height = self.data.shape[1]
        mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32,
                       "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
        bitDepth = mode_to_bpp[self.img.mode]

        print(
            "Image %s with %s x %s pixels (%s bits per pixel)  data has been read!" % (
                self.img.filename, self.width, self.height, bitDepth))

    def write(self, fileName):
        img = Image.fromarray(self.data)
        try:
            img.save(fileName)
        except:
            print("Write file error")
        else:
            print("Image %s has been written!" % (fileName))

    def write2(self, fileName):
        try:
            self.img.save(fileName)
        except:
            print("Write file error")
        else:
            print("Image %s has been written!" % (fileName))

    def imageCropCoordinate(self, fileName, y1, y2, x1, x2):
        self.restoreToOriginal()
        imgcrp = self.data[y1:y2, x1:x2]
        img = Image.fromarray(imgcrp)

        try:
            img.save(fileName)
        except:
            print("Write file error")
        else:
            print("Image %s has been written!" % (fileName))

    def rotateImage(self, fileNameIn, fileNameOut, degree):
        img = Image.open(fileNameIn)
        rotated = img.rotate(degree)

        try:
            rotated.save(fileNameOut)
        except:
            print("Write file error")
        else:
            print("Image %s has been written!" % (fileNameOut))

    def coordinateNumpy(self):
        self.data = self.data.transpose(2, 0, 1).reshape(-1, self.data.shape[1])
        pts = np.argwhere(self.data > 0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        print("ROI y1:y1,x2:x2 = ", y1, y2, x1, x2)
        # crop = self.data[y1:y2, x1:x2]
        return y1, y2, x1, x2

    def coordinateNumpyThes(self):
        self.data = self.data.transpose(2, 0, 1).reshape(-1, self.data.shape[1])
        pts = np.argwhere(self.data == 0)
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        print("ROI y1:y1,x2:x2 = ", y1, y2, x1, x2)
        # crop = self.data[y1:y2, x1:x2]
        return y1, y2, x1, x2

    def restoreToOriginal(self):
        self.data = np.copy(self.original)

    def rgb2gray(self):
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                graysclae = (self.data[x, y, 0] * 0.299) + (self.data[x, y, 1] * 0.587) + (self.data[x, y, 2] * 0.114)
                self.data[x, y] = graysclae

    def setWhite(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x, y, 0] > 0 and self.data[x, y, 1] > 0 and self.data[x, y, 2] > 0:
                    self.data[x, y, 0] = 255
                    self.data[x, y, 1] = 255
                    self.data[x, y, 2] = 255

    def convertToBlue(self):
        for y in range(self.height):
            for x in range(self.width):
                self.data[x, y, 0] = 0
                self.data[x, y, 1] = 0
                self.data[x, y, 1] = 0

    def dilation(self, se):
        self.rgb2gray()
        data_zeropaded = np.zeros([self.width + se.width * 2, self.height + se.height * 2, 3])
        data_zeropaded[se.width - 1:self.width + se.width - 1, se.height - 1:self.height + se.height - 1, :] = self.data
        for y in range(se.height - 1, se.height + self.height - 1):
            for x in range(se.width - 1, se.width + self.width - 1):
                subData = data_zeropaded[x - int(se.origin.real):x - int(se.origin.real) + se.width,
                          y - int(se.origin.imag):y - int(se.origin.imag) + se.height, 0:1]
                subData = subData.reshape(3, -1)

                for point in se.ignoreElements:
                    subData[int(point.real), int(point.imag)] = se.elements[int(point.real), int(point.imag)]
                max = np.amax(se.elements[se.elements > 0])
                subData = np.subtract(subData, np.flip(se.elements))
                if (0 <= x - int(se.origin.real) - 1 < self.width and 0 <= y - int(se.origin.imag) - 1 < self.height):
                    if (0 in subData):
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 0] = max
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 1] = max
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 2] = max
                    else:
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 0] = 0
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 1] = 0
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 2] = 0

    def erosion(self, se):
        self.rgb2gray()
        data_zeropaded = np.zeros([self.width + se.width * 2, self.height + se.height * 2, 3])
        data_zeropaded[se.width - 1:self.width + se.width - 1, se.height - 1:self.height + se.height - 1, :] = self.data
        for y in range(se.height - 1, se.height + self.height - 1):
            for x in range(se.width - 1, se.width + self.width - 1):
                subData = data_zeropaded[x - int(se.origin.real):x - int(se.origin.real) + se.width,
                          y - int(se.origin.imag):y - int(se.origin.imag) + se.height, 0:1]
                subData = subData.reshape(3, -1)

                for point in se.ignoreElements:
                    subData[int(point.real), int(point.imag)] = se.elements[int(point.real), int(point.imag)]
                min = np.amin(se.elements[se.elements > 0])

                if (0 <= x - int(se.origin.real) - 1 < self.width and 0 <= y - int(se.origin.imag) - 1 < self.height):
                    if (np.array_equal(subData, se.elements)):
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 0] = min
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 1] = min
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 2] = min
                    else:
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 0] = 0
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 1] = 0
                        self.data[x - int(se.origin.real) - 1, y - int(se.origin.imag) - 1, 2] = 0

    def boundaryExtraction(self, se):
        self.erosion(se)
        temp = self.data

        self.restoreToOriginal()
        self.rgb2gray()
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                boundex = (self.data[x, y, 0] - temp[x, y, 0]) + (self.data[x, y, 1] - temp[x, y, 1]) + (
                        self.data[x, y, 2] - temp[x, y, 2])
                self.data[x, y] = boundex

    def thresholding(self, threshold):
        self.rgb2gray()
        for y in range(self.height):
            for x in range(self.width):
                gray = self.data[x, y, 0]
                gray = 0 if gray < threshold else 255
                self.data[x, y, 0] = gray
                self.data[x, y, 1] = gray
                self.data[x, y, 2] = gray

    def otsuThreshold(self):
        self.rgb2gray()
        histogram = np.zeros(256)

        for y in range(self.height):
            for x in range(self.width):
                histogram[self.data[x, y, 0]] += 1

        histogramNorm = np.zeros(len(histogram))
        pixelNum = self.width * self.height

        for i in range(len(histogramNorm)):
            histogramNorm[i] = histogram[i] / pixelNum

        histogramCS = np.zeros(len(histogram))
        histogramMean = np.zeros(len(histogram))

        for i in range(len(histogramNorm)):
            if (i == 0):
                histogramCS[i] = histogramNorm[i]
                histogramMean[i] = 0
            else:
                histogramCS[i] = histogramCS[i - 1] + histogramNorm[i]
                histogramMean[i] = histogramMean[i - 1] + histogramNorm[i] * i

        globalMean = histogramMean[len(histogramMean) - 1]
        max = sys.float_info.min
        maxVariance = sys.float_info.min
        countMax = 0
        variance = 0

        for i in range(len(histogramCS)):
            if (histogramCS[i] < 1 and histogramCS[i] > 0):
                variance = ((globalMean * histogramCS[i] - histogramMean[i]) ** 2) / (
                        histogramCS[i] * (1 - histogramCS[i]))
            if (variance > maxVariance):
                maxVariance = variance
                max = i
                countMax = 1
            elif (variance == maxVariance):
                countMax = countMax + 1
                max = ((max * (countMax - 1)) + i) / countMax
        self.thresholding(round(max))

    def linearSpatialFilter(self, kernel, size):
        if (size % 2 == 0):
            print("Size Invalid: must be odd number!")
            return

        data_zeropaded = np.zeros([self.width + int(size / 2) * 2, self.height + int(size / 2) * 2, 3])
        data_zeropaded[int(size / 2):self.width + int(size / 2), int(size / 2):self.height + int(size / 2),
        :] = self.data

        for y in range(int(size / 2), int(size / 2) + self.height):
            for x in range(int(size / 2), int(size / 2) + self.width):
                subData = data_zeropaded[x - int(size / 2):x + int(size / 2) + 1,
                          y - int(size / 2):y + int(size / 2) + 1, :]

                sumRed = np.sum(np.multiply(subData[:, :, 0:1].flatten(), kernel))
                sumGreen = np.sum(np.multiply(subData[:, :, 1:2].flatten(), kernel))
                sumBlue = np.sum(np.multiply(subData[:, :, 2:3].flatten(), kernel))

                sumRed = 255 if sumRed > 255 else sumRed
                sumRed = 0 if sumRed < 0 else sumRed

                sumGreen = 255 if sumGreen > 255 else sumGreen
                sumGreen = 0 if sumGreen < 0 else sumGreen

                sumBlue = 255 if sumBlue > 255 else sumBlue
                sumBlue = 0 if sumBlue < 0 else sumBlue

                self.data[x - int(size / 2), y - int(size / 2), 0] = sumRed
                self.data[x - int(size / 2), y - int(size / 2), 1] = sumGreen
                self.data[x - int(size / 2), y - int(size / 2), 2] = sumBlue

    def cannyEdgeDetector(self, lower, upper):
        # Step 1 - Apply 5 x 5 Gaussian filter

        gaussian = [2.0 / 159.0, 4.0 / 159.0, 5.0 / 159.0, 4.0 / 159.0, 2.0 / 159.0,
                    4.0 / 159.0, 9.0 / 159.0, 12.0 / 159.0, 9.0 / 159.0, 4.0 / 159.0,
                    5.0 / 159.0, 12.0 / 159.0, 15.0 / 159.0, 12.0 / 159.0, 5.0 / 159.0,
                    4.0 / 159.0, 9.0 / 159.0, 12.0 / 159.0, 9.0 / 159.0, 4.0 / 159.0,
                    2.0 / 159.0, 4.0 / 159.0, 5.0 / 159.0, 4.0 / 159.0, 2.0 / 159.0]

        self.linearSpatialFilter(gaussian, 5)
        self.rgb2gray()

        # Step 2 - Find intensity gradient
        sobelX = [1, 0, -1,
                  2, 0, -2,
                  1, 0, -1]
        sobelY = [1, 2, 1,
                  0, 0, 0,
                  -1, -2, -1]

        magnitude = np.zeros([self.width, self.height])
        direction = np.zeros([self.width, self.height])

        data_zeropaded = np.zeros([self.width + 2, self.height + 2, 3])
        data_zeropaded[1:self.width + 1, 1:self.height + 1, :] = self.data

        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                gx = 0
                gy = 0

                subData = data_zeropaded[x - 1:x + 2, y - 1:y + 2, :]

                gx = np.sum(np.multiply(subData[:, :, 0:1].flatten(), sobelX))
                gy = np.sum(np.multiply(subData[:, :, 0:1].flatten(), sobelY))

                magnitude[x - 1, y - 1] = math.sqrt(gx * gx + gy * gy)
                direction[x - 1, y - 1] = math.atan2(gy, gx) * 180 / math.pi

        # Step 3 - Nonmaxima Suppression
        gn = np.zeros([self.width, self.height])
        print("Canny Edge Detect Working ...")
        for y in range(3, self.height - 3):
            for x in range(3, self.width - 3):
                targetX = 0
                targetY = 0

                # find closest direction
                if (direction[x - 1, y - 1] <= -157.5):
                    targetX = 1
                    targetY = 0
                elif (direction[x - 1, y - 1] <= -112.5):
                    targetX = 1
                    targetY = -1
                elif (direction[x - 1, y - 1] <= -67.5):
                    targetX = 0
                    targetY = 1
                elif (direction[x - 1, y - 1] <= -22.5):
                    targetX = 1
                    targetY = 1
                elif (direction[x - 1, y - 1] <= 22.5):
                    targetX = 1
                    targetY = 0
                elif (direction[x - 1, y - 1] <= 67.5):
                    targetX = 1
                    targetY = -1
                elif (direction[x - 1, y - 1] <= 112.5):
                    targetX = 0
                    targetY = 1
                elif (direction[x - 1, y - 1] <= 157.5):
                    targetX = 1
                    targetY = 1
                else:
                    targetX = 1
                    targetY = 0



                if (y + targetY >= 0 and y + targetY < self.height and x + targetX >= 0 and x + targetX < self.width and
                        magnitude[x - 1, y - 1] < magnitude[x + targetY - 1, y + targetX - 1]):
                    gn[x - 1, y - 1] = 0

                elif (
                        y - targetY >= 0 and y - targetY < self.height and x - targetX >= 0 and x - targetX < self.width and
                        magnitude[x - 1, y - 1] < magnitude[x - targetY - 1, y - targetX - 1]):
                    gn[x - 1, y - 1] = 0

                else:
                    gn[x - 1, y - 1] = magnitude[x - 1, y - 1]

                # set back first
                gn[x - 1, y - 1] = 255 if gn[x - 1, y - 1] > 255 else gn[x - 1, y - 1]
                gn[x - 1, y - 1] = 0 if gn[x - 1, y - 1] < 0 else gn[x - 1, y - 1]

                self.data[x - 1, y - 1, 0] = gn[x - 1, y - 1]
                self.data[x - 1, y - 1, 1] = gn[x - 1, y - 1]
                self.data[x - 1, y - 1, 2] = gn[x - 1, y - 1]

        # Step 4 - Hysteresis Thresholding

        # upper threshold checking with recursive
        for y in range(self.height):
            for x in range(self.width):
                if (self.data[x, y, 0] >= upper):
                    self.data[x, y, 0] = 255
                    self.data[x, y, 1] = 255
                    self.data[x, y, 2] = 255

                    self.hystConnect(x, y, lower)

        # clear unwanted values
        for y in range(self.height):
            for x in range(self.width):
                if (self.data[x, y, 0] != 255):
                    self.data[x, y, 0] = 0
                    self.data[x, y, 1] = 0
                    self.data[x, y, 2] = 0

    def hystConnect(self, x, y, threshold):
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if ((j < self.width) and (i < self.height) and (j >= 0) and (i >= 0) and (j != x) and (i != y)):
                    value = self.data[j, i, 0]
                    if (value != 255):
                        if (value >= threshold):
                            self.data[j, i, 0] = 255
                            self.data[j, i, 1] = 255
                            self.data[j, i, 2] = 255

                        else:
                            self.data[j, i, 0] = 0
                            self.data[j, i, 1] = 0
                            self.data[j, i, 2] = 0

    def adjustBrightness(self, brightness):
        for y in range(self.height):
            for x in range(self.width):
                r = self.data[x, y, 0]
                g = self.data[x, y, 1]
                b = self.data[x, y, 2]
                r = r + brightness
                r = 255 if r > 255 else r
                r = 0 if r < 0 else r
                g = g + brightness
                g = 255 if g > 255 else g
                g = 0 if g < 0 else g
                b = b + brightness
                b = 255 if b > 255 else b
                b = 0 if b < 0 else b
                self.data[x, y, 0] = r
                self.data[x, y, 1] = g
                self.data[x, y, 2] = b

    def paddingBG(self):
        for x in range(80):
            for y in range(self.height):
                self.data[x, y, 0] = 255
                self.data[x, y, 1] = 255
                self.data[x, y, 2] = 255
        for x in range(self.height):
            for y in range(35):
                self.data[x, y, 0] = 255
                self.data[x, y, 1] = 255
                self.data[x, y, 2] = 255
        for x in range(self.width):
            for y in range(self.height - 80, self.height):
                self.data[x, y, 0] = 255
                self.data[x, y, 1] = 255
                self.data[x, y, 2] = 255
        for x in range(self.width - 150, self.width):
            for y in range(self.height):
                self.data[x, y, 0] = 255
                self.data[x, y, 1] = 255
                self.data[x, y, 2] = 255

    def paddingBG2(self):
        for x in range(30):
            for y in range(self.height):
                self.data[x, y, 0] = 0
                self.data[x, y, 1] = 0
                self.data[x, y, 2] = 0
        for x in range(self.height):
            for y in range(35):
                self.data[x, y, 0] = 0
                self.data[x, y, 1] = 0
                self.data[x, y, 2] = 0
        for x in range(self.width):
            for y in range(self.height - 30, self.height):
                self.data[x, y, 0] = 0
                self.data[x, y, 1] = 0
                self.data[x, y, 2] = 0
        for x in range(self.width - 30, self.width):
            for y in range(self.height):
                self.data[x, y, 0] = 0
                self.data[x, y, 1] = 0
                self.data[x, y, 2] = 0

    def cropToFiveSector(self):
        # pic = 273 x 53 crop to 5 sect
        # 48 is cool
        i = 0
        hCrop = 48
        for i in range(6):
            left = 0 + hCrop * i
            top = 0
            right = hCrop + (hCrop * i)
            bottom = self.width

            img = Image.fromarray(self.data)
            cropped_single = img.crop((left, top, right, bottom))
            i += 1
            cropped_single.save(f'img/digit/digit_easy_crop/{i}_no.bmp')

        self.singleNumberPadding()

    def singleNumberPadding(self):
        self.read('img/digit/digit_easy_crop/6_no.bmp')
        for x in range(self.width):
            for y in range(self.height - 16, self.height):
                self.data[x, y, 0] = 255
                self.data[x, y, 1] = 255
                self.data[x, y, 2] = 255
        self.write('img/digit/digit_easy_crop/6_no.bmp')

    def cropSingleCoordinateNumber(self):
        for i in range(6):
            i += 1
            self.read(f'img/digit/digit_easy_crop/{i}_no.bmp')
            coorY1, coorY2, coorX1, coorX2 = self.coordinateNumpyThes()
            self.imageCropCoordinate(f'img/digit/digit_easy_crop/{i}_no.bmp', coorY1, coorY2, coorX1, coorX2)

    def checkDigit(self):
        all_point = []
        final_number_output = []

        for i in range(6):
            i += 1
            self.read(f'img/digit/digit_easy_crop/{i}_no.bmp')
            point_each_digit = self.checkingOriginalFont()

            all_point.append(point_each_digit)

            # numpy ops หา element ของ value และ index ในแต่ละ arr ที่มี value เยอะที่สุด หมายความว่า ตรงกับ font นั้นมากที่สุด
            maxElement = np.where(point_each_digit == np.amax(point_each_digit))
            final_number_output.append(maxElement[0])

            print("each ", i , "thes image point compare 0-9 font = ",point_each_digit)
        print('final point =', all_point)
        return final_number_output

    def checkingOriginalFont(self):
        point_each_digit=[]
        point_tmp = 0

        for i in range(10):
            font_img = Image.open(f'img/digit/digit_original_font/MICR2_{i}.bmp')

            font_resize = (self.height, self.width)
            font_img = font_img.resize((font_resize), Image.ANTIALIAS)

            font_data = np.array(font_img)
            font_dataW = font_data.shape[0]
            font_dataH = font_data.shape[1]

            print(font_dataW,font_dataH,self.width,self.height)

            for x in range(self.width):
                for y in range(self.height):
                    if self.data[x, y, 0] == font_data[x, y, 0]:
                        point_tmp += 1
                    else:
                        point_tmp -= 1
            point_each_digit.append(point_tmp)
            print("image piont of font" ,i," = " , point_each_digit)
            point_tmp = 0
            i += 1

        return point_each_digit

