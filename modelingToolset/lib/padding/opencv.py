import maya.cmds as cmds
from maya.mel import eval as meval
import os
import cv2
import numpy as np
import time

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
    cmds.polyWarpImage(xResolution=size * 2, yResolution=size * 2, inputName=WHITEFILE, outputName=snapshot,
                       inputUvSetName='map1', outputUvSetName='map1', fileFormat='jpg', background=[0, 0, 0],
                       overwrite=1, noAlpha=1)

    return snapshot


def main(size=1024, padding=8, padclr=(0, 255, 0), interclr=(255, 0, 255)):
    # selected
    # check it
    mesh = selected()

    # wrap image
    snapshot = wrap_image(mesh, size)

    # convert to BGR/revert list
    # shellclr = shellclr[::-1]
    padclr = padclr[::-1]
    interclr = interclr[::-1]

    # opencv
    OpenCV(snapshot, size, padding, padclr, interclr)
    # opencv(snapshot, size, padding, padclr, interclr)

    # if cmds.optionVar( q='padding_assign_texture' ):
    # 	create_material(mesh)
    cmds.select(mesh)


class OpenCV(object):

    def __init__(self, image, size, padding, padding_color, intersection_color):
        self.snapshot = image
        self.size = size
        self.padding = padding
        self.padding_color = padding_color
        self.intersection_color = intersection_color

        # read shapshot
        img = cv2.imread(self.snapshot)
        # warp image to 4096 for presize? need to resize to low (real) resolution
        self.snapshot = cv2.resize(img, (self.size, self.size))
        # convert snapshot to gray
        self.gray = cv2.cvtColor(self.snapshot, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join('D:/', "gray.jpg"), self.gray)
        _1, self.gray = cv2.threshold(self.gray, 2, 255, cv2.THRESH_BINARY)
        # cv2.imwrite(os.path.join('D:/', "contrast.jpg"), _file)
        # self.invert_gray = cv2.bitwise_not(self.gray)
        # cv2.imwrite(os.path.join('D:/', "i_gray.jpg"), self.invert_gray)
        if cv2.countNonZero(self.gray) == 0:
            print("Error")
            return

        # compute intersection
        self.compute()

    def merge_paddings(self, padding_image, intersection_image):
        img2gray = cv2.cvtColor(intersection_image, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(intersection_image[:, :, 0], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        padding_image[np.where(mask == 255)] = intersection_image[np.where(mask == 255)]
        cv2.imwrite(os.path.join(TEMPDIR, "padintr.jpg"), padding_image)

    def contours_hierarchy(self):
        ret, thresh_img = cv2.threshold(self.gray, 100, 255, cv2.THRESH_BINARY)
        image, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

        return contours, hierarchy[0]

    def split_contours(self, contours, hierarchy_array):
        external_contours = []
        internal_contours = []

        for i in range(len(contours)):
            if hierarchy_array[i][
                3] > -1:  # this contour is internal(has parent) (https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html)
                internal_contours.append(contours[i])
            else:
                external_contours.append(contours[i])

        return external_contours, internal_contours

    def subtract_contours(self, contours, subtract_img, color=255):
        img_zero = np.ones((self.size, self.size, 1), np.uint8)  # black image
        result = cv2.drawContours(img_zero, contours, -1, color, self.padding)
        result = cv2.subtract(result, subtract_img)
        return result

    def subtract_contours_rgb(self, contours):
        copy_img = self.snapshot.copy()
        cv2.drawContours(self.snapshot, contours, -1, self.padding_color, self.padding)
        img = cv2.subtract(self.snapshot, copy_img)
        cv2.imwrite(os.path.join(TEMPDIR, "padding.jpg"), img)
        return img

    def fill_internal_contours(self, internal_image):

        # cv2.imwrite(os.path.join('D:/', "i.jpg"), self.invert_gray)
        invert = cv2.bitwise_not(internal_image)
        cv2.imwrite(os.path.join('D:/', "i.jpg"), invert)
        th, im_th = cv2.threshold(invert, 220, 255, cv2.THRESH_BINARY_INV)
        im_floodfill = im_th.copy()

        # mask used to flood filling
        # notice the size needs to be 2 pixels than the image
        h, w = im_th.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0, 0), 255);

        # invert floodfilled image
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        # combine the two images to get the foreground.
        im_out = im_th | im_floodfill_inv

        return im_out

    def compute(self):
        combined_image = []
        self.e_contours = None
        self.i_contours = None

        contours, hierarchy_array = self.contours_hierarchy()
        external_contours, internal_contours = self.split_contours(contours, hierarchy_array)

        if external_contours:
            self.e_contours = self.subtract_contours(external_contours, self.gray)

            progress_control = progress_bar(len(external_contours))
            for cnt in external_contours:
                if cmds.progressBar(progress_control, query=True, isCancelled=True):
                    break
                img_zero = np.ones((self.size, self.size, 1), np.uint8)
                subtract_contour = cv2.drawContours(img_zero, [cnt], -1, 255, -1)

                outer_padding = self.subtract_contours([cnt], subtract_contour)
                # outer_padding = self.padding_contours(cnt)
                combined_image.append(outer_padding)

                cmds.progressBar(progress_control, edit=True, step=1)

            cmds.progressBar(progress_control, edit=True, endProgress=True)

        if internal_contours:
            self.i_contours = np.ones((self.size, self.size, 1), np.uint8)
            for cnt in internal_contours:
                img_zero = np.ones((self.size, self.size, 1), np.uint8)  # black image
                result = cv2.drawContours(img_zero, [cnt], -1, 255, self.padding)
                cv2.imwrite(os.path.join('D:/', "result.jpg"), result)
                fill = self.fill_internal_contours(result)
                cv2.imwrite(os.path.join('D:/', "fill.jpg"), fill)
                intersect = cv2.bitwise_and(result, fill)
                cv2.imwrite(os.path.join('D:/', "inter.jpg"), intersect)
                self.i_contours = cv2.bitwise_or(self.i_contours, intersect)
            # cv2.imwrite(os.path.join('D:/', "subtr.jpg"), self.i_contours)
            # cmds.error()

            # self.i_contours = self.subtract_contours(internal_contours, self.gray)
            # fill = self.fill_internal_contours(self.i_contours)
            # cv2.imwrite(os.path.join('D:/', "fill.jpg"), fill)
            # self.i_contours = cv2.bitwise_and(self.i_contours, fill)
            cv2.imwrite(os.path.join('D:/', "before.jpg"), self.i_contours)
            self.i_contours = cv2.subtract(self.i_contours, self.gray)
            cv2.imwrite(os.path.join('D:/', "after.jpg"), self.i_contours)

        padding_image = self.subtract_contours_rgb(contours)
        intersect_image = self.compare_contours(combined_image)
        self.merge_paddings(padding_image, intersect_image)

    def compare_contours(self, contours):
        img_zero = np.ones((self.size, self.size, 1), np.uint8)
        if contours:
            bb_list = self.bounding_box_list(contours)
            if not bb_list:
                return
            progress_control = progress_bar(len(contours))
            for i in range(len(contours)):
                if bb_list[i]:
                    if cmds.progressBar(progress_control, query=True, isCancelled=True):
                        break

                    for j in bb_list[i]:
                        intersection = np.bitwise_and(contours[i], contours[j])
                        if cv2.countNonZero(intersection) != 0:
                            img_zero = cv2.bitwise_or(img_zero, intersection)

                cmds.progressBar(progress_control, edit=True, step=1)
            cmds.progressBar(progress_control, edit=True, endProgress=True)

        if self.i_contours != None:
            intersection = np.bitwise_and(self.e_contours, self.i_contours)
            img_zero = cv2.bitwise_or(img_zero, intersection)

        # colorize
        ret, mask = cv2.threshold(img_zero, 1, 255, cv2.THRESH_BINARY_INV)
        rgb_image = cv2.cvtColor(img_zero, cv2.COLOR_GRAY2RGB)
        rgb_image[mask == 0] = self.intersection_color
        cv2.imwrite(os.path.join(TEMPDIR, "intersection.jpg"), rgb_image)

        return rgb_image

    def bounding_box_list(self, counturs):
        bb_array = []

        for i in range(len(counturs)):
            bb = self.bounding_box(counturs[i])
            bb_array.append(bb)

        intersection_array = []
        for i in range(len(bb_array)):
            add_list = []
            for j in range(i + 1, len(bb_array)):
                if self.bounding_box_intersection(bb_array[i], bb_array[j]):
                    add_list.append(j)
            intersection_array.append(add_list)

        counter = 0
        for shell in intersection_array:
            counter = counter + len(shell)
        print('real intersection count', counter)

        return intersection_array

    def bounding_box(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        real_padding = int(self.padding / 2)
        bb = [x - real_padding, y - real_padding, x + w + real_padding, y + h + real_padding]

        return bb

    def bounding_box_intersection(self, box_a, box_b):
        xA = max(box_a[0], box_b[0])
        yA = max(box_a[1], box_b[1])
        xB = min(box_a[2], box_b[2])
        yB = min(box_a[3], box_b[3])

        interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
        if interArea > 0:
            return True
        else:
            return False
