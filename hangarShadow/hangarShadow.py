import maya.cmds as cmds
import maya.mel as mel
import os, posixpath
import cv2
import numpy as np
import time

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class OpenCV(object):

    @classmethod
    def adjastment_levels(cls, img, input_black, input_white, gamma, output_black, output_white):
        inBlack = np.array([input_black, input_black, input_black], dtype=np.float32)
        inWhite = np.array([input_white, input_white, input_white], dtype=np.float32)
        inGamma = np.array([gamma, gamma, gamma], dtype=np.float32)
        outBlack = np.array([output_black, output_black, output_black], dtype=np.float32)
        outWhite = np.array([output_white, output_white, output_white], dtype=np.float32)

        img = np.clip((img - inBlack) / (inWhite - inBlack), 0, 255)
        img = (img ** (1 / inGamma)) * (outWhite - outBlack) + outBlack
        img = np.clip(img, 0, 255).astype(np.uint8)

        return img

    @classmethod
    def gaussian_blur(cls, img, value):
        result = cv2.GaussianBlur(img, (value, value), cv2.BORDER_DEFAULT)
        return result

    @classmethod
    def merge_opacity(cls, background, overlay, alpha=1.0):
        result = cv2.addWeighted(background, alpha, overlay, 1 - alpha, 0)
        return result

    @classmethod
    def resize(cls, img, width, height):
        dim = (width, height)
        # resize image
        result = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return result

    @classmethod
    def crop(cls, img, width, height):
        y = 0
        x = 128
        result = img[y:y + height, x:x + width]
        return result

    @classmethod
    def invert(cls, img):
        result = cv2.bitwise_not(img)
        return result

    @classmethod
    def add_alpha(cls, img):
        result = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        return result

    @classmethod
    def copy_channels(cls, img):
        img_zero = np.ones((512, 256, 1), np.uint8)  # black image
        b_channel, g_channel, r_channel, a_channel = cv2.split(img)
        a_channel = r_channel
        r_channel = img_zero
        g_channel = img_zero
        b_channel = img_zero
        result = cv2.merge((r_channel, g_channel, b_channel, a_channel))
        return result

    def main(cls, original, output):
        img = cv2.imread(original)
        copy_img = img.copy()

        copy_img = cls.adjastment_levels(copy_img, 0, 215, 1.0, 0, 255)
        copy_img = cls.gaussian_blur(copy_img, 5)

        img = cls.adjastment_levels(img, 0, 215, 1.0, 255, 255)

        img = cls.merge_opacity(img, copy_img, 0.2)
        img = cls.resize(img, 512, 512)
        img = cls.crop(img, 256, 512)
        img = cls.invert(img)
        img = cls.add_alpha(img)
        img = cls.copy_channels(img)
        cv2.imwrite(os.path.join(CURRENT_PATH, output), img)


class Utils(object):

    @classmethod
    def file_name(cls):
        file_name = cmds.file(query=True, sn=1, shn=True)
        name = os.path.splitext(file_name)[0]
        return name

    @classmethod
    def file_path(cls):
        file_name = cmds.file(query=True, loc=True)
        return os.path.dirname(file_name)

    @classmethod
    def load_turtle(cls):
        pluginStat = cmds.pluginInfo('Turtle.mll', query=True, l=True)
        if pluginStat == False:
            try:
                cmds.loadPlugin('Turtle.mll')
            except:
                print("There is no Turtle plugin in Maya")
                return

    @classmethod
    def current_unit(cls):
        cmds.currentUnit(linear="m")

    @classmethod
    def create_bake_plane(cls):
        if cmds.objExists('shadow_plane*'):
            cmds.delete('shadow_plane*')

        shadow_plane = cmds.polyPlane(w=1, h=1, sx=1, sy=1, n="shadow_plane")[0]
        shadow_plane_shape = cmds.listRelatives(shadow_plane, c=1, type="mesh")[0]
        cmds.xform(shadow_plane, ws=1, a=1, s=[18.636, 1, 18.636])
        cmds.setAttr(shadow_plane + ".translateY", -0.006)
        return shadow_plane, shadow_plane_shape

    @classmethod
    def turtle_ao(cls, plane):
        cmds.setAttr('defaultRenderGlobals.currentRenderer', 'turtle', type='string')
        shader_ocl = cmds.shadingNode("ilrOccSampler", asShader=1)
        cmds.setAttr(shader_ocl + ".minSamples", 64)
        cmds.setAttr(shader_ocl + ".enableAdaptiveSampling", 0)
        cmds.select(plane)
        cmds.hyperShade(assign=shader_ocl)

    @classmethod
    def turtle_options(cls):
        try:
            mel.eval('ilrDefaultNodes(0);')
            mel.eval('ilrDefaultNodes(1);')
        except:
            mel.eval('ilrDefaultNodes();')

        render = "TurtleRenderOptions"
        cmds.setAttr(render + ".renderer", 1)
        cmds.setAttr(render + ".aaMinSampleRate", 0)
        cmds.setAttr("TurtleDefaultBakeLayer.renderType", 1)

    @classmethod
    def render_command(cls, plane, path):
        path = path.replace("\\", "/")
        command = 'ilrTextureBakeCmd  \
		-target ' + plane + ' \
		-selectionMode 0 \
		-camera "persp" \
		-normalDirection 0 \
		-bakeLayer TurtleDefaultBakeLayer \
		-width 1024 \
		-height 1024 \
		-saveToRenderView 0 \
		-saveToFile 1 \
		-directory "' + path + '" \
		-fileName "shadow.png" \
		-fileFormat 9 \
		-edgeDilation 3 \
		-bilinearFilter 0 \
		-merge 1 \
		-fullShading 1 \
		-useRenderView 1; '

        mel.eval(command)

    @classmethod
    def dds_convert(cls, img):
        tank_dir = cls.file_path()
        os.system(
            'start ' + CURRENT_PATH + '/nvdxt.exe -file ' + img + ' -outdir ' + tank_dir + ' -profile ' + CURRENT_PATH + '/profiles/hangar.dpf ')

    @classmethod
    def cleaning(cls, map_name):
        try:
            cmds.delete('shadow_plane*')
        except:
            pass
        try:
            cmds.delete('ilrOccSampler*')
        except:
            pass

        time.sleep(2)
        try:
            os.remove(os.path.join(CURRENT_PATH, 'shadow.png'))
        except OSError:
            pass
        try:
            os.remove(os.path.join(CURRENT_PATH, 'shadow.tif'))
        except OSError:
            pass
        try:
            os.remove(os.path.join(CURRENT_PATH, map_name))
        except OSError:
            pass


def main():
    tank_name = Utils.file_name()
    map_name = tank_name + '_HangarShadowMap.tif'

    Utils.load_turtle()
    Utils.current_unit()
    plane, plane_shape = Utils.create_bake_plane()
    Utils.turtle_ao(plane)
    Utils.turtle_options()
    Utils.render_command(plane_shape, CURRENT_PATH)

    opencv = OpenCV()
    img = os.path.join(CURRENT_PATH, 'shadow.png')
    opencv.main(img, map_name)
    img = os.path.join(CURRENT_PATH, map_name)

    Utils.dds_convert(img)
    Utils.cleaning(map_name)
