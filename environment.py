import pygame
import numpy as np

pygame.init()

grid_w = 900
grid_h = 600
ncolumns = 4
nrows = 3
cell_w = grid_w/ncolumns
cell_h = grid_h/nrows

gameDisplay = pygame.display.set_mode((grid_w,grid_h))
pygame.display.set_caption('Grid world')
clock = pygame.time.Clock()

stopped = False

values = np.zeros((nrows+2,ncolumns+2))
actions = []
gamma = 1
r = -0.1

#create four different actions
for i in range(0,4):
    if i == 0:
        actions.append(np.array([[0,0.8,0],[0.1,0,0.1],[0,0,0]]))
    else:
        #each action is a 90 degree rotation of the previously defined action
        currentaction = actions[i-1]
        rotated = np.rot90(currentaction)
        actions.append(np.array(rotated))



def convolve(F, G, s=1):
    # F to be convoled with G with stride length s

    # dimensions of F and G.
    l, w = F.shape
    n = G.shape[1]

    sums = []
    o_dim1, o_dim2 = (0,0) # dimensions of resulting matrix
    for i in range(0, l - n + 1 , s):
        o_dim1 += 1
        for j in range(0, w - n + 1, s):
            if i==0:
                o_dim2 += 1

            Fsub = F[i:i + n, j:j + n]  # get subset of F
            mult = np.sum(np.multiply(Fsub, G))
            sums.append(mult)

    return np.array(sums).reshape((int(o_dim1), int(o_dim2)))


def value_iteration(values,gamma,r,max_iteration):
    values = values
    for i in range(0,max_iteration):
        exvalues = gamma * values + r
        maxvalues = convolve(exvalues, actions[0])
        for a in range(1, len(actions)):
            ivals = convolve(exvalues, actions[a])

            # only add the values associated with the action that provide the greatest values
            greater = ivals >= maxvalues
            maxvalues = ivals * greater + (greater == 0) * (maxvalues)

        padded_values = np.zeros((nrows + 2, ncolumns + 2))

        maxvalues[0, ncolumns-1] = 1
        maxvalues[1, ncolumns-1] = -1
        # re-pad the values array
        padded_values[1:nrows + 1, 1:ncolumns + 1] = maxvalues
        padded_values[0, 1:ncolumns + 1] = maxvalues[0, :]
        padded_values[nrows + 1, 1:ncolumns + 1] = maxvalues[nrows-1, :]
        padded_values[1:nrows + 1, 0] = maxvalues[:, 0]
        padded_values[1:nrows + 1, ncolumns + 1] = maxvalues[:, ncolumns-1]

        values = padded_values
        if i == max_iteration-1:
            values = maxvalues


    return values




state_values = value_iteration(values,gamma,r,10000)
print(state_values)


def draw(canvas):
    canvas.fill((255,255,255))

    count = 0
    for i in range(0, nrows):
        for j in range(0, ncolumns):

            pygame.draw.rect(canvas, (15,100,90), (j*cell_w, i*cell_h, cell_w, cell_h),2)
            count = count + 1



while not stopped:
    draw(gameDisplay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopped = True

    pygame.display.update()
    clock.tick(60)