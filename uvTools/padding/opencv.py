import cv2
import numpy

def cv_threshold(img, thresh=128, maxval=255, type=cv2.THRESH_BINARY):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshed = cv2.threshold(img, thresh, maxval, type)[1]
    return threshed

def find_contours(img):
    kernel   = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed  = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours[-2]

def find_contours_2(img):
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)

    cv2.imshow('image2', img)
    #return contours

def mask_from_contours(ref_img, contours):
    mask = numpy.zeros(ref_img.shape, numpy.uint8)
    mask = cv2.drawContours(mask, contours, -1, (255,255,255), -1)
    return cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

def draw_contours(src_img, contours):
    canvas = cv2.drawContours(src_img.copy(), contours, -1, (0,255,0), 2)
    x, y, w, h = cv2.boundingRect(contours[-1])
    cv2.rectangle(canvas, (x,y), (x+w,y+h), (0,0,255), 2)
    return canvas

def dilate_mask(mask, kernel_size=10):
    kernel  = numpy.ones((kernel_size,kernel_size), numpy.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    return dilated

def main():
    img = cv2.imread('D://big.jpg', 1)
    orig_img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    orig_threshed = cv_threshold(orig_img, 30, 255, cv2.THRESH_BINARY_INV)
    orig_contours = find_contours(orig_threshed)
    orig_mask = mask_from_contours(orig_img, orig_contours)
    orig_output = draw_contours(orig_img, orig_contours)

    dilated_mask = dilate_mask(orig_mask, 4)
    dilated_contours = find_contours(dilated_mask)
    dilated_output   = draw_contours(orig_img, dilated_contours)

    smooth_mask_blurred   = cv2.GaussianBlur(dilated_mask, (21,21), 0)
    smooth_mask_threshed1 = cv_threshold(smooth_mask_blurred)

    smooth_mask_blurred   = cv2.GaussianBlur(smooth_mask_threshed1, (21,21), 0)
    smooth_mask_threshed2 = cv_threshold(smooth_mask_blurred)

    smooth_mask_contours = find_contours(smooth_mask_threshed2)
    smooth_mask_output   = draw_contours(orig_img, smooth_mask_contours)

    cv2.imshow("dilated_output", dilated_output)
    #cv2.imshow("smooth_mask_output", smooth_mask_output)

