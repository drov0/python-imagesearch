from python_imagesearch.imagesearch import *

# Search for the github logo on the whole screen
# note that the search only works on your primary screen.

# This is intended to be used as examples to be copy pasted, do not run the whole file at once

pos = imagesearch("./github.png")
if pos[0] != -1:
    print("position : ", pos[0], pos[1])
    pyautogui.moveTo(pos[0], pos[1])
else:
    print("image not found")

# search for the github logo until found  :

pos = imagesearch_loop("./github.png", 0.5)

print("image found ", pos[0], pos[1])

# search for the logo on the 0,0,800,600 region
#  (a rectangle starting from the top left going 800 pixels to the right and down 600 pixels)

pos = imagesearcharea("./github.png", 0, 0, 800, 600)
if pos[0] != -1:
    print("position : ", pos[0], pos[1])
    pyautogui.moveTo(pos[0], pos[1])
else:
    print("image not found")

# the im parameter is useful if you plan on looking for several different images without the need for recapturing the screen
# the screen capture being one of the most time consuming function it's a good way to optimize

# non -optimized way :
time1 = time.clock()
for i in range(10):
    imagesearcharea("./github.png", 0, 0, 800, 600)
    imagesearcharea("./panda.png", 0, 0, 800, 600)
print(str(time.clock() - time1) + " seconds (non optimized)")

# optimized way :

time1 = time.clock()
im = region_grabber((0, 0, 800, 600))
for i in range(10):
    imagesearcharea("./github.png", 0, 0, 800, 600, 0.8, im)
    imagesearcharea("./panda.png", 0, 0, 800, 600, 0.8, im)
print(str(time.clock() - time1) + " seconds (optimized)")

# sample output :

# 1.6233619831305721 seconds (non optimized)
# 0.4075934110084374 seconds (optimized)


# click image is to be used after having found the image

pos = imagesearch("github.png")
if pos[0] != -1:
    click_image("github.png", pos, "right", 0.2, offset=5)
