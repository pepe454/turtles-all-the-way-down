import pygame
from math import sqrt, sin, cos
from numpy import arctan

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITEGRAY = (192, 192, 192)
RED = (255, 0, 0)
MIDRED = (192, 0, 0)
DARKRED = (128, 0, 0)
MAROON = (80, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 128, 0)
GREYGREEN = (0, 128, 128)
MINT = (51,153,102)
JADE = (0, 250, 154)
BLUE = (0, 0, 255)
NAVY = (0, 102, 204)
DARKBLUE = (0, 0, 128)
MIDBLUE = (0, 0, 192)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
MIDYELLOW = (192, 192, 0)
MODESTYELLOW = (128, 128, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 102, 0)
MIDORANGE = (192, 79, 0)
PURPLE = (128, 0, 128)
MIDPURPLE = (192, 0, 192)
sunset = [MIDORANGE, MIDRED, DARKRED, DARKBLUE]
ocean = [DARKGREEN, DARKBLUE, GREYGREEN, PURPLE]

#--------------CONFIGURATIONS----------------
# various configurations change the way image is displayed
# feel free to play around and see how the image changes
aspect_ratio = 3840 / 2160 # set this to the aspect ratio of your screen
x = 1540 # width of the window
y = int(x / aspect_ratio) # height of your screen
size = [x, y]
# MUST HAVE 4 COLORS - try out preset colorschemes or try out new ones
colors = sunset 
squares = 800 # number of squares drawn in the window
shade = True # creates fading effect on the colors as spiral moves outward
gradient = 1.05 # if shade, how drastic is the fade?
rotate = False # rotates colors around the spiral
same_colors = False # use the same color for all sides of a each square in the spiral
curr_length = 2 # starting side length of the first square in the spiral
adder = 4 # how big the side lengths grow linearly

#--------------HELPER FUNCTIONS---------------
distance = lambda p1, p2: sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) # get distance b/t two points
bound = lambda x: 0 if x < 0 else min(255, x) # keep color values within [0,255]

def next_point(p1, p2):
    diff_x = p1[0] - p2[0]
    diff_y = p1[1] - p2[1] 

    #calculate next point using triangle geometry
    angle = arctan(abs(diff_x) / abs(diff_y))
    new_diff_x = int(sin(angle) * curr_length)
    new_diff_y = int(cos(angle) * curr_length)
    new_x = p1[0] + new_diff_x if diff_x < 0 else p1[0] - new_diff_x     
    new_y = p1[1] + new_diff_y if diff_y < 0 else p1[1] - new_diff_y         
    return [new_x, new_y]

#--------------INITIALIZATION-----------------
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Create a spiral drawing")
done = False
clock = pygame.time.Clock()
screen.fill((0, 0, 0))

#-----------------ARTWORK---------------------
p1 = [x//2 - curr_length//2, y//2 - curr_length//2]
p2 = [x//2 + curr_length//2, y//2 - curr_length//2]
p3 = [x//2 + curr_length//2, y//2 + curr_length//2]
p4 = [x//2 - curr_length//2, y//2 + curr_length//2]
points = [p1, p2, p3, p4]

#end of each line
curr_length += adder
p12 = [p1[0] + curr_length, p1[1]]
p22 = [p2[0], p2[1] + curr_length]
p32 = [p3[0] - curr_length, p3[1]]
p42 = [p4[0], p4[1] - curr_length]
new_points = [p12, p22, p32, p42]

for p1, p2 in zip(points, new_points):
    pygame.draw.line(screen, colors[1], p1, p2)

# every iteration draws a new square and updates the points
for j in range(squares):
    curr_length += adder
    points = new_points
    new_points = [0, 0, 0, 0]
    if rotate and j % 40 == 0: # change colors every 10 squares
        old = colors
        colors = [old[3], old[0], old[1], old[2]] # shuffle colors to create rotating effect
        
    # every iteration calculates a new point and draws line from points[i] to new point
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i+1)%4]
        p1_new = next_point(p1,p2)
        
        new_points[(i+1)%4] = p1_new
        col = colors[0] if same_colors else colors[i]
        fact = j * gradient if shade else 1 # with shade set, colors naturally fade to black
        new_col = (bound(col[0] - fact), bound(col[1] - fact), bound(col[2] - fact))
        pygame.draw.line(screen, new_col, p1, p1_new)
pygame.display.flip()

#----------------EVENT LOOP-------------------
while not done:
    clock.tick(10)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # If user clicked close
            done = True
pygame.display.iconify()

filename = input("Enter filename with no extension or 0 to quit: ")
if filename != "0":
    pygame.image.save(screen, filename + ".jpeg") 