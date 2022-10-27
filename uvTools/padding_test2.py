import cv2
import numpy as np


def find_if_close(cnt1, cnt2):
    row1, row2 = cnt1.shape[0], cnt2.shape[0]
    for i in xrange(row1):
        for j in xrange(row2):
            dist = np.linalg.norm(cnt1[i] - cnt2[j])
            if abs(dist) < 10:
                return True
            elif i == row1 - 1 and j == row2 - 1:
                return False


def contours_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200)
    image, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of Contours found = " + str(len(contours)))
    cv2.imshow('Canny Edges After Contouring', edged)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    cv2.imshow('Contours', img)
    # test
    del contours[::2]
    print("Number of Contours after del = " + str(len(contours)))
    # test
    return contours


def dilate_mask(mask, kernel_size=10):
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print("Number of Contours found = " + str(len(contours)))
    cv2.imshow('Canny Edges After Contouring', mask)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Contours', image)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    return dilated


def intersection():
    square = np.zeros((300, 300), np.uint8)
    cv2.rectangle(square, (50, 50), (250, 250), 255, -1)
    ellipse = np.zeros((300, 300), np.uint8)
    cv2.ellipse(ellipse, (150, 150), (150, 150), 30, 0, 180, 255, -1)
    BitwiseAND = cv2.bitwise_and(square, ellipse)
    if cv2.countNonZero(BitwiseAND) == 0:
        print
        "non intersection"
    else:
        print
        "Intersected"
    cv2.imshow("AND", BitwiseAND)


def intersection2(counturs):
    img_zero = np.ones((1024, 1024, 1), np.uint8)

    for i in range(len(counturs)):
        for j in range(i + 1, len(counturs)):
            img1 = np.zeros((1024, 1024, 1), dtype="uint8")
            img2 = np.zeros((1024, 1024, 1), dtype="uint8")
            countur_1 = cv2.drawContours(img1, counturs[i], -1, 255, 8)
            # cv2.imshow("contour_" + str(i), countur_1)
            countur_2 = cv2.drawContours(img2, counturs[j], -1, 255, 8)
            intersection = np.bitwise_and(countur_1, countur_2)
            if cv2.countNonZero(intersection) != 0:
                # cv2.imshow("inter_" + str(i), intersection)
                img_zero = cv2.bitwise_or(img_zero, intersection)

    ret, mask = cv2.threshold(img_zero, 1, 255, cv2.THRESH_BINARY_INV)
    rgb_image = cv2.cvtColor(img_zero, cv2.COLOR_GRAY2RGB)
    rgb_image[mask == 0] = [255, 0, 255]

    cv2.imshow("result ", rgb_image)


def for_countur(img, contours):
    img_zero = np.ones((1024, 1024, 1), np.uint8)
    # img_zero = np.zeros( img.shape[0:2], np.uint8)
    for i, cnt1 in enumerate(contours):
        for x, cnt2 in enumerate(contours):
            if i != x:
                img1 = np.zeros((1024, 1024, 1), dtype="uint8")
                img2 = np.zeros((1024, 1024, 1), dtype="uint8")
                countur_1 = cv2.drawContours(img1, cnt1, -1, 255, 8)
                countur_2 = cv2.drawContours(img2, cnt2, -1, 255, 8)
                intersection = np.bitwise_and(countur_1, countur_2)
                if cv2.countNonZero(intersection) != 0:
                    # cv2.imshow("inter_" + str(i), intersection)
                    img_zero = cv2.bitwise_or(img_zero, intersection)

    cv2.imshow("result ", img_zero)


# return

# color = np.random.randint(0, 255, (3)).tolist()
# one_countur = cv2.drawContours(img, cnt1, -1, 255, 30)
# one_countur = cv2.drawContours(img_zero,cnt1,0,255,30)

# img2 = cv2.drawContours( blank.copy(), cnt1, 1, color, 8)
# blank = ( blank.copy() + img2) == 2

# img[img[:, :, 1:].all(axis=-1)] = 0
# one_countur[one_countur[:, :, 1:].all(axis=-1)] = 0

# intersection2 = (img_zero*127 + one_countur)
# intersection2 = np.bitwise_and( img_zero, one_countur )
# print 'Inter ', intersection2

# img_zero = cv2.addWeighted(img_zero, 0.5, one_countur, 0.5, 0)

# cv2.imshow("inter_" + str(i), intersection2)


# cv2.imshow("one_countur_" + str(i), one_countur)
# cv2.imshow("one_countur_final" , img_zero)
# cv2.imshow("one_countur_final___" , img)


def main():
    # img = cv2.imread('D://big.jpg')
    img = cv2.imread('D://test_w.jpg')

    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(gray,20,255,0)
    # image,contours,hier = cv2.findContours(thresh,cv2.RETR_EXTERNAL,1)

    # img[img[:, :, 1:].all(axis=-1)] = 0
    # img2[img2[:, :, 1:].all(axis=-1)] = 0

    # dst = cv2.addWeighted(img, 1, img2, 1, 0)
    # cv2.imshow("dst", dst)

    # edges = cv2.Canny(img,100,200)

    contours = contours_edges(img)

    # dil_edges = dilate_mask(edges, 1)
    # _, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # cv2.imshow("edges", edges)
    # cv2.imshow("edges", dil_edges)

    LENGTH = len(contours)
    print
    'Count counturs __: ', LENGTH
    # status = np.zeros((LENGTH,1))

    intersection2(contours)
    # for_countur(dil_edges, contours)
    # intersection()
    return

# for i,cnt1 in enumerate(contours):

# 	# one_countur = cv2.drawContours(img,cnt1,-1,(0,255,0),8)
# 	# cv2.imshow("one_countur", one_countur)


# 	x = i
# 	if i != LENGTH-1:
# 		for j,cnt2 in enumerate(contours[i+1:]):
# 			x = x+1
# 			dist = find_if_close(cnt1,cnt2)
# 			if dist == True:
# 				val = min(status[i],status[x])
# 				status[x] = status[i] = val
# 			else:
# 				if status[x]==status[i]:
# 					status[x] = i+1

# unified = []
# maximum = int(status.max())+1
# for i in xrange(maximum):
# 	pos = np.where(status==i)[0]
# 	if pos.size != 0:
# 		cont = np.vstack(contours[i] for i in pos)
# 		hull = cv2.convexHull(cont)
# 		unified.append(hull)

# unified_img = cv2.drawContours(img,unified,-1,(0,255,0),8)
# cv2.imshow("unified_img", unified_img)


# thresh_img = cv2.drawContours(thresh,unified,-1,255,-1, 20)
# cv2.imshow("thresh_img", thresh_img)
