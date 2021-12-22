from ImageLibrary import ImageLibrary

def main():
    # เริ่มโปรแกรม
    print("program 61050273 imgage processing LAB start here... \n")
    print("=================Phase 1=================")
    img = ImageLibrary()

    img.read("img/FinalDIP64.bmp")
    img.adjustBrightness(-107)
    img.write("img/1_delete_brightness.bmp")

    img.read("img/1_delete_brightness.bmp")
    img.cannyEdgeDetector(100, 250)
    img.write("img/2_canny_edgedetect.bmp") #test

    img.read("img/2_canny_edgedetect.bmp")
    # perfect rotate = 315
    # better = 325
    # more better = 330 or -30 ,i guess ...
    img.rotateImage("img/2_canny_edgedetect.bmp","img/3_canny_edgedetect_rotated.bmp",330)
    img.read("img/3_canny_edgedetect_rotated.bmp")

    print("==============Set orignal image -> set crop coordinate จากรูป testroated========================")
    coorY1, coorY2, coorX1, coorX2 = img.coordinateNumpy()

    ## Important key rotate 328  = 420591 ,329 = 620591,  330 = 620531
    img.rotateImage("img/1_delete_brightness.bmp","img/4_delete_brightness_rotated.bmp",329)
    img.read("img/4_delete_brightness_rotated.bmp")

    img.imageCropCoordinate("img/5_delete_brightness_rotated_crop.bmp",coorY1, coorY2, coorX1, coorX2)

    print("=================Phase 2=================")
    print("=================Threshold Original Image and Crop by picked Coordinate=================")
    img.read("img/5_delete_brightness_rotated_crop.bmp")

    img.otsuThreshold()
    img.paddingBG()
    img.write("img/6_image_thresholded.bmp")

    img.read("img/6_image_thresholded.bmp")

    img.cannyEdgeDetector(100, 150)
    img.paddingBG2()
    img.write("img/7_image_thresholded_edge_detect.bmp")

    print("=================Phase 3=================")
    print("===========MAP COORDINATE OF DIGIT NUMBER===========") #ทำให้รูป thershold conform ไปตาม edge canny coordinate

    img.read("img/7_image_thresholded_edge_detect.bmp")
    coorY1, coorY2, coorX1, coorX2 = img.coordinateNumpy()
    img.imageCropCoordinate("img/8_group_of_number_canny.bmp", coorY1, coorY2, coorX1, coorX2)
    img.rotateImage("img/8_group_of_number_canny.bmp", "img/8_group_of_number_canny.bmp", 180)

    img.read("img/6_image_thresholded.bmp")
    img.imageCropCoordinate("img/9_group_of_number_thresholded.bmp", coorY1, coorY2, coorX1, coorX2)
    img.rotateImage("img/9_group_of_number_thresholded.bmp", "img/9_group_of_number_thresholded.bmp", 180)

    img.read("img/8_group_of_number_canny.bmp")
    coorY1, coorY2, coorX1, coorX2 = img.coordinateNumpy()
    img.imageCropCoordinate("img/8_group_of_number_canny.bmp", coorY1, coorY2, coorX1, coorX2)
    img.rotateImage("img/8_group_of_number_canny.bmp", "img/8_group_of_number_canny.bmp", 180)

    img.read("img/9_group_of_number_thresholded.bmp")
    img.imageCropCoordinate("img/9_group_of_number_thresholded.bmp", coorY1, coorY2, coorX1, coorX2)
    img.rotateImage("img/9_group_of_number_thresholded.bmp", "img/9_group_of_number_thresholded.bmp", 180)

    print("=================Phase 4=================")
    print("===========GET SINGLE NUMBER and Compare to Font Image===========")
    img.read("img/9_group_of_number_thresholded.bmp")
    img.cropToFiveSector()
    img.cropSingleCoordinateNumber()  # หา ROI ของ Single Number Thershold ที่ตัดมาแต่ละตัวแล้ว
    final_number_output = img.checkDigit()

    print("==================================Result==================================")

    print("The Number in Picture should Be = ",
          final_number_output[0], final_number_output[1], final_number_output[2],
          final_number_output[3], final_number_output[4], final_number_output[5])

    print("เลขจริงตามภาพ =  6 2 0 5 9 1")
    print("The end")
    print("นาย ภูผา ศิริโกมลสิงห์ 61050273")


if __name__ == '__main__':
    main()

# ข้อสอบปลายภาควิชา Image Processing ปี 64 โดย ภูผา ศิริโกมลสิงห์ 61050273
# === อธิบายการคิดและ การทำงานของโปรแกรม ===
#
# Flow การคิดก่อนทำของผม
# 1 ปรับรูปให้สีเท่ากันทั้งหมด เพื่อให้ง่านในการทำ threshold >> 2 ทำ Threshold 3 >> 4 หาขอบรูปเพื่อ crop
# 5 rotate รูปให้ตรง >> 6 crop ตัวเลขทั้งหมด >> 7 canny edge หา contour ของตัวอักษรทั้งหก >> 8 loop check
#
# Flow เมื่อทำงานจริง
# 1 ปรับแสงจากรูปออกให้หมด >> 2 หา canny edge >> 3 หา coordinate มุม จากข้อ2 >> 4 นำ coordinate มา crop ในรูปจริง
# 5 ทำ threshold >> 6 ทำ canny edge แล้วหา coordinate มา crop รูปที่ threshold >> 7 ตัดเลขออกมาที่ละตัว >>
# 8 loop หาว่าเป็นเลขอะไร โดยเทียบกับ font จริง
#
# === อธิบายการทำงานของโปรแกรมแบบละเอียด ===
#
# โปรแกรมทำงานทั้งหมด 4 phase ดังนี้่
# phase 1 = Clean รูป และ crop by picked coordinate (output รูป 1,2,3,4,5 )
# phase 2 = threshold รูป ให้เหลือแค่เลข ที่เด่นออกมา   (output รูป 6,7)
# phase 3 = หา coordinate แล้ว crop ให้เหลือแค่กลุ่มตัวเลข  (output รูป 8,9, digit_easy_crop)
# phase 4 = หาตัวเลขแต่ละตัวว่าตรงกับเลขไหนของชุด font มากที่สุด (output result (เลขที่โปรแกรมหาได้)
#
# อธิบายแต่ละ phase แบบละเอียด
# phase 1 = Clean รูป และ crop by picked coordinate
# 1.1 import ไฟล์ตั้งต้น (FinalDIP64.bmp)
# 1.2 adjust brightness ลงเพื่อลบแสงสะท้อนบนโต๊ะ (output รูป 1)
# 1.3 หา canny edge (output รูป 2)
# 1.4 rotate รูปโดยใช้ค่ามุม 325-330 Degree เพื่อทำให้รูปตรง (output รูป 3)
# 1.5 เก็บ coordinate x1,x2,y1,y2 (จุดแรกที่เป็นสีขาว และ จุดสุดท้ายที่เป็นสีขาว)
# 1.6 rotate รูปที่ 1 เป็นมุม 330 Degree (output รูป 4)
# 1.7 crop รูปที่ 1 จาก coordinate ที่หาได้จากข้อ 1.5 (output รูป 5)
# ======================================================================
#
# phase 2 = threshold รูป ให้เหลือแค่เลข ที่เด่นออกมา
# 2.1 threshold รูปที่ 5 จะได้ภาพที่เห็นแต่เลขเป็นสีดำ (output รูป 6)
# 2.2 ทำ canny edge จากรูปที่ 6 เตรียมจะเก็บ coordinate (output รูป 7)
# ======================================================================
#
# phase 3 = หา coordinate แล้ว crop ให้เหลือแค่กลุ่มตัวเลข
# 3.1 ทำการ pick coordinate โดยวิธีการเป็นดังนี้
# ผมเก็บแค่ 2 coordinate จากจริง ๆ ถ้าจะหามุมให้ชัดเจนจะต้องการถึง 4 มุม coordinate
# แต่ผมไม่ต้องการใช้ algo ที่ค่อนข้างจะหายากจึงทำการเก็บเหมือนเดิม 2 จุดคือ จุดแรกที่เจอสีขาว และจุดท้ายที่เจอสีขาว
# แต่จะทำ 2 รอบ หรือก็คือ ผมจะกลับหัวรูปเพื่อ หา coordinate มุมที่ผมไม่ได้ pick มา
#
# 3.2 รูปที่จะทำการหา coordinate คือภาพ ที่ทำ canny edge และจะ crop รูป threshold ไปตาม coordinate ของรูป canny ด้วย
# มันจะทำงานและ crop พร้อมกันแบบนี้ 2 รอบ ( crop รอบที่หัวตรงปกติ กับ crop รอบที่กลับหัว) จากนั้นกลับตั้งคืนเหมือนเดิม (output รูป 8,9)
# 3.3 เราต้องการเลข 6 ตัวเลข แล้วเราได้แถบตัวเลขตรง ๆ มาแล้วก็ทำการหารเพื่อ split ตัวเลขแต่ละตัวลงไป save ที่ digit_easy_crop (output digit_easy_crop)
# ======================================================================
#
# phase 4 = หาตัวเลขแต่ละตัวว่าตรงกับเลขไหนของชุด font มากที่สุด
# 4.1 import รูป font ทั้ง 10 ตัวอักษรที่จะนำมาเทียบกับชุดเลขที่เราหามาได้
#
# โดยมีวิธีการดังนี้คือ Loop ทุก 6 ตัวอักษร ไป check ทุกรูปของ font ว่าได้คะแนนจาก font ที่เท่าไรมากสุด
# นั่นคือถ้าตรงกันจะได้คะแนน +1 ถ้าไม่ตรงได้ -1
# จากนั้นก็ไป sort หาว่า index ตัวไหนได้คะแนนมากที่สุดหรือก็คือรูปนั้นตรงกับ font เลขอะไรมากที่สุด
# print result ออกมาผลลัพธ์คือ 6 2 0 5 9 1 ตรงกับเลขในกระดาษ
# ======================================================================
#
# ู Directory ในการ start program
# -----main.py
# -----ImageLibrary.py (AKA image manager)
# -------|
# -------img
# -----------FinalDIP64.bmp




