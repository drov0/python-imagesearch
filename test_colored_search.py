import cv2
import numpy as np


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

def f(base, template):
    base = np.array(base)
    template = np.array(template)

    res = cv2.matchTemplate(cv2.cvtColor(base, cv2.COLOR_BGR2GRAY), cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    b_channels = [base[:, :, i] for i in range(3)]
    t_channels = [template[:, :, i] for i in range(3)]

    chis = []

    for b, t in zip(b_channels, t_channels):
        t = np.reshape(t, (-1))

        n_classes = 10
        dx = 255 / n_classes
        
        t_bins = [t[(k * dx <= t) & ((k+1) * dx > t)].shape[0] for k in range(n_classes)]
        t_bins[n_classes - 1] += t[t == 255].shape[0]

        b_zone = b[max_loc[1]: max_loc[1] + template.shape[1], max_loc[0]: max_loc[0] + template.shape[0]]
        b = np.reshape(b_zone, (-1))

        b_bins = [b[(k * dx <= b) & ((k+1) * dx > b)].shape[0] for k in range(n_classes)]
        b_bins[n_classes - 1] += b[b == 255].shape[0]

        chi = chi_2(b_bins, t_bins)
        chis.append(chi)

    print(chis)
    if chis[0] < 20 and chis[1] < 20 and chis[2] < 20 and max_val > 0.8:
        print(max_loc)
    else:
        print("colored_search doesn't find anything")


rl = cv2.imread('images/rl.png')
gl = cv2.imread('images/gl.png')
yl = cv2.imread('images/yl.png')
red = cv2.imread('images/red.png')
green = cv2.imread('images/green.png')
yellow = cv2.imread('images/yellow.png')

print("red -> rl")
f(red, rl)
res = cv2.matchTemplate(cv2.cvtColor(red, cv2.COLOR_BGR2GRAY), cv2.cvtColor(rl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("red -> gl")
f(red, gl)
res = cv2.matchTemplate(cv2.cvtColor(red, cv2.COLOR_BGR2GRAY), cv2.cvtColor(gl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("red -> yl")
f(red, yl)
res = cv2.matchTemplate(cv2.cvtColor(red, cv2.COLOR_BGR2GRAY), cv2.cvtColor(yl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("green -> rl")
f(green, rl)
res = cv2.matchTemplate(cv2.cvtColor(green, cv2.COLOR_BGR2GRAY), cv2.cvtColor(rl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("green -> gl")
f(green, gl)
res = cv2.matchTemplate(cv2.cvtColor(green, cv2.COLOR_BGR2GRAY), cv2.cvtColor(gl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("green -> yl")
f(green, yl)
res = cv2.matchTemplate(cv2.cvtColor(green, cv2.COLOR_BGR2GRAY), cv2.cvtColor(yl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("yellow -> rl")
f(yellow, rl)
res = cv2.matchTemplate(cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY), cv2.cvtColor(rl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("yellow -> gl")
f(yellow, gl)
res = cv2.matchTemplate(cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY), cv2.cvtColor(gl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)

print("yellow -> yl")
f(yellow, yl)
res = cv2.matchTemplate(cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY), cv2.cvtColor(yl, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if max_val < 0.8:
    print("matchTemplate doesn't find anything")
else:
    print(max_loc)


