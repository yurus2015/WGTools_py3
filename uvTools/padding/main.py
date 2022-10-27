import maya.cmds as cmds
from maya.mel import eval as meval
import os
import cv2
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WHITEFILE = os.path.join(CURRENT_DIR, "source.jpg")
TEMPDIR = cmds.internalVar(utd=True)


def progress_bar(count):
    gMainProgressBar = meval('$tmp = $gMainProgressBar')

    cmds.progressBar(gMainProgressBar,
                     edit=True,
                     beginProgress=True,
                     isInterruptable=True,
                     status='Example Calculation ...',
                     maxValue=count)

    return gMainProgressBar


def selected():
    meshes = cmds.filterExpand(sm=12, fp=1)
    if meshes:
        return meshes
    else:
        cmds.confirmDialog(title='Select meshes', message='Select poligonal mesh', button=['Yes'], defaultButton='Yes')
        return


def wrap_image(meshes, size=1024):
    snapshot = os.path.join(TEMPDIR, "snapshot.jpg")
    cmds.polyWarpImage(xResolution=size, yResolution=size, inputName=WHITEFILE, outputName=snapshot,
                       inputUvSetName='map1', outputUvSetName='map1', fileFormat='jpg', background=[0, 0, 0],
                       overwrite=1, noAlpha=1)

    return snapshot


def contours_edges(img, padding=8):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of Contours found 2 = " + str(len(contours)))
    cv2.drawContours(img, contours, -1, (0, 255, 0), 5)
    cv2.imshow('Canny Edges After Contouring', img)

    '''
    edged = cv2.Canny(gray, 100, 200)
    image, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of Contours found = " + str(len(contours)))
    '''

    # cv2.imshow('Canny Edges After Contouring', gray)
    # return
    '''
    #test
    del contours[::2]
    print("Number of Contours after del = " + str(len(contours)))
    #test
    '''
    # cv2.drawContours(img, contours, -1, (0, 255, 0), padding)
    # cv2.imshow('Contours', img)

    # for i in range(len(contours)):
    # 	cv2.drawContours(img, contours[i], -1, (0, 255, 0), 3)
    # 	cv2.imshow('WTF' + str(i), img)
    # cv2.imshow('gray', gray)
    # img_pad = cv2.bitwise_or(img, edged)
    # cv2.imshow('Contours', img_pad)
    cv2.imwrite(os.path.join(TEMPDIR, "padding.jpg"), img)

    '''
    #test
    del contours[::2]
    print("Number of Contours after del = " + str(len(contours)))
    #test
    '''
    return contours


def bounding_box(contour, padding=8):
    x, y, w, h = cv2.boundingRect(contour)
    real_padding = int(padding / 2)
    bb = [x - real_padding, y - real_padding, w + padding, h + padding]

    # img = np.ones((1024,1024,1),np.uint8)
    # cv2.drawContours(img, contour, -1, (0, 255, 0), 1)
    # cv2.imshow('wtf', img)
    # cv2.rectangle(img, (x-real_padding, y-real_padding), (x+w+real_padding, y+h+real_padding), (255,0,0), 1)
    # cv2.imshow("lalala", img)
    # cv2.imwrite("D://my.jpg",img)
    # print 'Bounding box ', bb
    return bb


def bounding_box_intersection(box_a, box_b):
    if (abs(box_a[0] - box_b[0]) * 2 < (box_a[2] + box_b[2])) and (
            abs(box_a[1] - box_b[1]) * 2 < (box_a[3] + box_b[3])):
        return True
    else:
        return False


# pass
# bool DoBoxesIntersect(Box a, Box b) {
#  return (abs(a.x - b.x) * 2 < (a.width + b.width)) &&
#         (abs(a.y - b.y) * 2 < (a.height + b.height));

def bounding_box_list(counturs, padding=8):
    bb_array = []
    for i in range(len(counturs)):
        bb = bounding_box(counturs[i], padding)
        bb_array.append(bb)

    intersection_array = []
    for i in range(len(bb_array)):
        add_list = []
        for j in range(i + 1, len(bb_array)):
            if bounding_box_intersection(bb_array[i], bb_array[j]):
                add_list.append(j)
        intersection_array.append(add_list)

    # print 'INTER', intersection_array
    return intersection_array


def intersection(counturs, size=1024, padding=8):
    intersection_list = bounding_box_list(counturs, padding)
    img_zero = np.ones((size, size, 1), np.uint8)
    progress_control = progress_bar(len(counturs))

    for i in range(len(counturs)):
        if cmds.progressBar(progress_control, query=True, isCancelled=True):
            break

        # adds
        if intersection_list[i]:
            img1 = np.zeros((size, size, 1), dtype="uint8")
            countur_1 = cv2.drawContours(img1, counturs[i], -1, 255, padding)
            for j in intersection_list[i]:
                img2 = np.zeros((size, size, 1), dtype="uint8")
                countur_2 = cv2.drawContours(img2, counturs[j], -1, 255, padding)
                intersection = np.bitwise_and(countur_1, countur_2)
                if cv2.countNonZero(intersection) != 0:
                    img_zero = cv2.bitwise_or(img_zero, intersection)

        # adds end

        '''
        box_a = bounding_box(counturs[i])

        img1 = np.zeros((size, size, 1), dtype = "uint8")
        countur_1 = cv2.drawContours(img1, counturs[i], -1, 255, padding)



        for j in range(i+1, len(counturs)):
            box_b = bounding_box(counturs[j])
            if bounding_box_intersection(box_a, box_b):
                #pass
                img2 = np.zeros((size, size, 1), dtype = "uint8")
                countur_2 = cv2.drawContours(img2, counturs[j], -1, 255, padding)
                # cv2.imshow("contour_" + str(i), countur_1)
                intersection = np.bitwise_and( countur_1, countur_2 )
                if cv2.countNonZero(intersection) != 0:
                    img_zero = cv2.bitwise_or(img_zero, intersection)

        '''

        cmds.progressBar(progress_control, edit=True, step=1)

    cmds.progressBar(progress_control, edit=True, endProgress=True)

    ret, mask = cv2.threshold(img_zero, 1, 255, cv2.THRESH_BINARY_INV)
    rgb_image = cv2.cvtColor(img_zero, cv2.COLOR_GRAY2RGB)
    rgb_image[mask == 0] = [255, 0, 255]
    cv2.imwrite(os.path.join(TEMPDIR, "intersection.jpg"), rgb_image)
    cv2.imshow("result ", rgb_image)


def opencv(image, size=1024, padding=8):
    img = cv2.imread(image)
    contours = contours_edges(img, padding)
    intersection(contours, size, padding)


def main(size=1024, padding=8):
    # selected
    # check it
    mesh = selected()

    # wrap image
    snapshot = wrap_image(mesh, size)

    # opencv
    opencv(snapshot, size, padding)

# open in render view
# meval('RenderViewWindow')
