import cv2
import numpy as np
import pyautogui
import random
import time
import platform
import subprocess
import os
import mss

is_retina = False
if platform.system() == "Darwin":
    is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell=True) == 0

'''

grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)

input : a tuple containing the 4 coordinates of the region to capture

output : a PIL image of the area selected.

'''


def region_grabber(region):
    if is_retina: region = [n * 2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

    region = x1, y1, width, height
    with mss.mss() as sct:
        return sct.grab(region)

'''

Searchs for an image within an area

input :

image : path to the image file (see opencv imread for supported types)
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

'''


def imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        if is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
        # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    if template is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


'''

click on the center of an image with a bit of random.
eg, if an image is 100*100 with an offset of 5 it may click at 52,50 the first time and then 55,53 etc
Usefull to avoid anti-bot monitoring while staying precise.

this function doesn't search for the image, it's only ment for easy clicking on the images.

input :

image : path to the image file (see opencv imread for supported types)
pos : array containing the position of the top left corner of the image [x,y]
action : button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
time : time taken for the mouse to move from where it was to the new position
'''


def click_image(image, pos, action, timestamp, offset=5):
    img = cv2.imread(image)
    if img is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset),
                     timestamp)
    pyautogui.click(button=action)


'''
Searchs for an image on the screen

input :

image : path to the image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

'''


def imagesearch(image, precision=0.8):
    with mss.mss() as sct:
        im = sct.grab(sct.monitors[0])
        if is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
        # im.save('testarea.png') useful for debugging purposes, this will save the captured region as "testarea.png"
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        if template is None:
            raise FileNotFoundError('Image file not found: {}'.format(image))
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc


'''
Searchs for an image on screen continuously until it's found.

input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element if found as an array [x,y]

'''


def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos


'''
Searchs for an image on screen continuously until it's found or max number of samples reached.

input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
maxSamples: maximum number of samples before function times out.
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element if found as an array [x,y]

'''


def imagesearch_numLoop(image, timesample, maxSamples, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


'''
Searchs for an image on a region of the screen continuously until it's found.

input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element as an array [x,y]

'''


def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    pos = imagesearcharea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    return pos


'''
Searchs for an image on a region of the screen continuously until it's found or max number of samples reached.

input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
maxSamples: maximum number of samples before function times out.
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element as an array [x,y]
'''


def imagesearch_region_numLoop(image, timesample, maxSamples, x1, y1, x2, y2, precision=0.8):
    pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    count = 0
    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos



'''
Searches for an image on the screen and counts the number of occurrences.

input :
image : path to the target image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.9

returns :
the number of times a given image appears on the screen.
optionally an output image with all the occurances boxed with a red outline.

'''


def imagesearch_count(image, precision=0.95):
    with mss.mss() as sct:
        im = sct.grab(sct.monitors[0])
        if is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        if template is None:
            raise FileNotFoundError('Image file not found: {}'.format(image))
        template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        count = 0
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            count = count + 1
        return count


'''
Get all screens on the provided folder and search them on screen.

input :
path : path of the folder with the images to be searched on screen
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
A dictionary where the key is the path to image file and the value is the position where was found.
'''


def imagesearch_from_folder(path, precision):
    print(path)
    imagesPos = {}
    path = path if path[-1] == '/' or '\\' else path+'/'
    valid_images = [".jpg", ".gif", ".png", ".jpeg"]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1].lower() in valid_images]
    for file in files:
        pos = imagesearch(path+file, precision)
        imagesPos[path+file] = pos
    return imagesPos


def r(num, rand):
    return num + rand * random.random()

'''
Wrapper around imagesearch and click_image

# TODO: optimize so that we only read the file once.

input :
image : path to the image file (see opencv imread for supported types)
action : button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
delay : time taken for the mouse to move from where it was to the new position
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
'''

def imagesearch_click(image, action, delay, offset=5, precision=0.8):
    pos = imagesearch(image, precision)
    img = cv2.imread(image)
    if img is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset),
                     delay)
    pyautogui.click(button=action)



def chi_2(l1, l2):
    """
    sort of chi squared test to check if the two color distributions are compatible
    """ 
    s = sum(l2) # number of pixels in template
    l1 = [x / s * 100 for x in l1] # scaling the bins of the histograms
    l2 = [x / s * 100 for x in l2] # scaling the bins of the histograms

    chi = 0
    for i in range(len(l2)):
        if l2[i] != 0:
            chi += (l1[i] - l2[i])**2 / l2[i]
        else:
            chi += l1[i]**2

    return chi / len(l2)

"""
Returns the coordinates of the given image but only if the colors match

input :
image : path to the image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
"""
def colored_search(image, precision=0.8):
    with mss.mss() as sct:
        im = sct.grab(sct.monitors[0])
        if is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
        # im.save('testarea.png')
        base = np.array(im)
        template = cv2.imread(image)
        if template is None:
            raise FileNotFoundError(f'Image file not found: {image}')
        template = np.array(template)

        res = cv2.matchTemplate(cv2.cvtColor(base, cv2.COLOR_BGR2GRAY), cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        b_channels = [base[:, :, i] for i in range(3)]
        t_channels = [template[:, :, i] for i in range(3)]

        chis = [] # list with chi squared tests results
        for b, t in zip(b_channels, t_channels): # for each channel, check if the color distributions are compatible
            #b = np.reshape(b, (-1))
            t = np.reshape(t, (-1))

            n_classes = 10 # I chose 10 because of the rule of thumb with histograms (which is to use ~~ Total_number_of_observations bins,
                           # in fact the function chi_2 scales the bins as if there were 100 pixels)
            dx = 255 / n_classes # width of the bins

            t_bins = [t[(k * dx <= t) & ((k+1) * dx > t)].shape[0] for k in range(n_classes)]
            t_bins[n_classes - 1] += t[t == 255].shape[0] # every bin contains the number of pixels that have a value between k*dx and (k+1)*dx, k=0,1,...,9

            b_zone = b[max_loc[1]: max_loc[1] + template.shape[1], max_loc[0]: max_loc[0] + template.shape[0]] # portion of the screen located by cv2.matchTemplate
            b = np.reshape(b_zone, (-1))
            b_bins = [b[(k * dx <= b) & ((k+1) * dx > b)].shape[0] for k in range(n_classes)]
            b_bins[n_classes - 1] += b[b == 255].shape[0]

            chi = chi_2(b_bins, t_bins)
            chis.append(chi)
        
        if chis[0] < 5 and chis[1] < 5 and chis[2] < 5 and max_val > 0.8: # 5 is maybe a high threshold for a chi squared, but when the colors are different
                                                                          # it's easy to reach hundreds or more.
                                                                          # Anyway this value needs more testing to be tuned 
            return(max_loc)
        else:
            return [-1, -1]
