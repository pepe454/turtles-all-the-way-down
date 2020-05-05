import pygame
from math import sqrt, sin, cos
from numpy import arctan

distance = lambda p1, p2: sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) # get distance b/t two points
bound = lambda x: 0 if x < 0 else min(255, x) # keep values within [0,255]

#adjust resolution here
aspect_ratio = 3840 / 2160
x = 1540
y = int(x / aspect_ratio)
size = [x, y]

# various configurations change the way image is displayed
# feel free to play around and see how the image changes
squares = 800 # number of squares drawn in the window
gradient = 1.4 # if shading, how drastic is the fade?
shade = True # creates fading effect on the colors as spiral moves outward
rotate = True # rotates colors
consistent = True # 
same_colors = True # use the same color for all sides of a each square in the spiral

#define colors here, could be in an enumerated class 
black = (0, 0, 0)
white = (255, 255, 255)
whitegray = (192, 192, 192)
red = (255, 0, 0)
mid_red = (192, 0, 0)
dark_red = (128, 0, 0)
maroon = (80, 0, 0)
green = (0, 255, 0)
dark_green = (0, 128, 0)
graygreen = (0, 128, 128)
mint = (51,153,102)
jade = (0, 250, 154)
blue = (0, 0, 255)
navy = (0, 102, 204)
dark_blue = (0, 0, 128)
pink = (255, 0, 255)
yellow = (255, 255, 0)
modest_yellow = (128, 128, 0)
cyan = (0, 255, 255)
orange = (255, 102, 0)
purple = (128, 0, 128)
mid_purple = (192, 0, 192)
colors = [mint, jade, blue, cyan]

#initialize the window
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Create a spiral drawing")
done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # If user clicked close
            done=True
    screen.fill((0, 0, 0))
    curr_length = 2
    factor = 1.1
    adder = 4
    
    #start of each line
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

    #every iteration draws a new square and updates the points
    for j in range(squares):
        curr_length += adder
        points = new_points
        new_points = [0, 0, 0, 0]
        if rotate and j % 40 == 0: # change colors every 10 squares
            old = colors
            colors = [old[3], old[0], old[1], old[2]] # shuffle colors to create rotating effect
            
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i+1)%4]
            diff_x = p1[0] - p2[0]
            diff_y = p1[1] - p2[1]
            
            angle = arctan(abs(diff_x)/abs(diff_y))
            new_diff_x = int(sin(angle) * curr_length)
            new_diff_y = int(cos(angle) * curr_length)
            new_x = p1[0] + new_diff_x if diff_x < 0 else p1[0] - new_diff_x     
            new_y = p1[1] + new_diff_y if diff_y < 0 else p1[1] - new_diff_y   
            
            p1_new = [new_x, new_y]
            new_points[(i+1)%4] = p1_new
            col = colors[i]
            if consistent:
                col = colors[j%4]
            if same_colors:
                col = colors[0]
            fact = j * gradient if shade else 1
            new_col = (bound(col[0] - fact), bound(col[1] - fact), bound(col[2] - fact))
            pygame.draw.line(screen, new_col, p1, p1_new)
    pygame.display.flip()
