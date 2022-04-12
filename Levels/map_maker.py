import pygame
import json
import os
import sys
import tkinter as tk
from functools import partial
from pygame.locals import *
import logging

logging.basicConfig(level=logging.DEBUG, filename="errorlog.txt", format="%(asctime)s : %(levelname)s : %(message)s")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (200, 30, 30)
GREEN = (0, 255, 0)

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000

objKey = {"x":"o", "o":"e", "e":"x"}

def main():
    window = tk.Tk()
    button1 = tk.Button(window, text="Pick Map", command=partial(option, window))
    button2 = tk.Button(window, text="Quit", command=end)
    button1.pack()
    button2.pack()
    window.mainloop()

def end():
    sys.exit()

def option(window):
    window.destroy()
    window = tk.Tk()
    with open(os.path.join("Levels", "meta.json"), "r") as metaMap:
        metaMap = json.loads(metaMap.read())
        k = 0
        c = 0
        for i in metaMap["levels"]:
            k += 1
            c = 0
            for j in i:
                c += 1
                frame = tk.Frame(
                    master=window,
                    relief=tk.RAISED,
                    borderwidth=1
                    )
                frame.grid(row=k, column=c, padx=5, pady=5)
                if j[0] != "x":
                    Button = tk.Button(master=frame, text=f"{str(j)}", command=partial(edit, j, window))
                else:
                    Button = tk.Button(master=frame, text=f"", command=partial(create, j, "null", window))
                Button.pack()
                if k == 1 and j[0] != "x":
                    frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=0, column=c, padx=5, pady=5)
                    Button = tk.Button(master=frame, text="up", command=partial(create, j, "up", window))
                    Button.pack()
                if c == 1 and j[0] != "x":
                    frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=k, column=0, padx=5, pady=5)
                    Button = tk.Button(master=frame, text="left", command=partial(create, j, "left", window))
                    Button.pack()
                if i == metaMap["levels"][len(metaMap["levels"])-1] and j[0] != "x":
                    frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=k+1, column=c, padx=5, pady=5)
                    Button = tk.Button(master=frame, text="down", command=partial(create, j, "down", window))
                    Button.pack()
                if j == i[len(i)-1] and j[0] != "x":
                    frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=k, column=c+1, padx=5, pady=5)
                    Button = tk.Button(master=frame, text="right", command=partial(create, j, "right", window))
                    Button.pack()
    window.mainloop()

def create(edge, direction, window):
    arr = []
    for i in range(10):
        arr.append([])
        for j in range(10):
            arr[i].append("o")
    data = {"Level":arr}

    if direction == "null":
        print("got here")
        Map = edge[1:]
        with open(os.path.join("Levels", f"level {Map}.json"), "w") as file:
            json.dump(data, file)
        with open(os.path.join("Levels", "meta.json"), "r") as file:
            current = json.load(file)
        levels = current["levels"]
        for i in range(len(levels)):
            for j in range(len(levels[i])):
                if Map == levels[i][j][1:]:
                    levels[i][j] = Map
                    print(Map)
        with open(os.path.join("Levels", "meta.json"), "w") as file:
            Level = {"levels":levels}
            json.dump(Level, file)


    else:
        info = edge.split(" ")

        if direction == "left":
            Map = (f"{int(info[0])-1} {info[1]}")
            with open(os.path.join("Levels", f"level {Map}.json"), "w") as file:
                json.dump(data, file)
            with open(os.path.join("Levels", "meta.json"), "r") as file:
                current = json.load("file")
            levels = current["levels"]
            coords = int(levels[0][0].split(" ")[1])
            for i in levels:
                if f"{int(info[0])-1} {coords}" == Map:
                    i.insert(0, f"{Map}")
                else:
                    i.insert(0, f"x{int(info[0])-1} {coords}")
                coords += 1
            with open(os.path.join("Levels", "meta.json"), "w") as file:
                Level = {"levels":levels}
                json.dump(Level, file)

        elif direction == "right":
            Map = (f"{int(info[0])+1} {info[1]}")
            with open(os.path.join("Levels", f"level {Map}.json"), "w") as file:
                json.dump(data, file)
            with open(os.path.join("Levels", "meta.json"), "r") as file:
                current = json.load(file)
            levels = current["levels"]
            coords = int(levels[0][0].split(" ")[1])
            for i in levels:
                if f"{int(info[0])+1} {coords}" == Map:
                    i.append(f"{Map}")
                else:
                    i.append(f"x{int(info[0])+1} {coords}")
                coords += 1
            with open(os.path.join("Levels", "meta.json"), "w") as file:
                Level = {"levels":levels}
                json.dump(Level, file)

        elif direction == "down":
            Map = (f"{info[0]} {int(info[1])+1}")
            with open(os.path.join("Levels", f"level {Map}.json", "w")) as file:
                json.dump(data, file)
            with open(os.path.join("Levels", "meta.json"), "r") as file:
                current = json.load(file)
            levels = current["levels"]
            arr = []
            coords = levels[0][0]
            if coords[0] == "x":
                coords = coords[1:]
            coords = int(coords.split(" ")[0])
            for i in range(len(levels[0])):
                if coords == int(info[0]):
                    arr.append(f"{Map}")
                else:
                    arr.append(f"x{coords} {int(info[1])+1}")
                coords += 1
            levels.append(arr)
            with open(os.path.join("Levels", "meta.json"), "w") as file:
                Level = {"levels":levels}
                json.dump(Level, file)

        elif direction == "up":
            Map = (f"{info[0]} {int(info[1])-1}")
            with open(os.path.join("Levels", f"level {Map}.json"), "w") as file:
                json.dump(data, file)
            with open(os.path.join("Levels", "meta.json"), "r") as file:
                current = json.load(file)
            levels = current["levels"]
            arr = []
            coords = levels[0][0]
            if coords[0] == "x":
                coords = coords[1:]
            coords = int(coords.split(" ")[0])
            for i in range(len(levels[0])):
                if coords == int(info[0]):
                    arr.append(f"{Map}")
                    print("got here")
                else:
                    arr.append(f"x{coords} {int(info[1])-1}")
                coords += 1
            levels.insert(0, arr)
            with open(os.path.join("Levels", "meta.json"), "w") as file:
                Level = {"levels":levels}
                json.dump(Level, file)


    edit(Map, window)

def edit(map, window):
    window.destroy()
    with open(os.path.join("Levels", f"level {map}.json"), "r") as file:
        arr = json.load(file)
        arr = arr["Level"]
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    cursor = [0, 0]

    doors = Doors(map)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[K_DOWN]:
                if cursor[1] < 9:
                    cursor[1] += 1
            elif pygame.key.get_pressed()[K_UP]:
                if cursor[1] > 0:
                    cursor[1] -= 1
            elif pygame.key.get_pressed()[K_LEFT]:
                if cursor[0] > 0:
                    cursor[0] -= 1
            elif pygame.key.get_pressed()[K_RIGHT]:
                if cursor[0] < 9:
                    cursor[0] += 1
            elif pygame.key.get_pressed()[K_SPACE]:
                arr[cursor[1]][cursor[0]] = objKey[arr[cursor[1]][cursor[0]]]
            elif pygame.key.get_pressed()[K_RETURN]:
                with open(os.path.join("Levels", f"level {map}.json"), "w") as file:
                    Level = {"Level":arr}
                    json.dump(Level, file)
                pygame.quit()
                main()
        
        DISPLAYSURF.fill(WHITE)



        for i in range(10):
            for j in range(10):
                if arr[j][i] == "x":
                    pygame.draw.rect(DISPLAYSURF, BLACK, (i*100, j*100, 100, 100))
                elif arr[j][i] == "e":
                    pygame.draw.rect(DISPLAYSURF, RED, (i*100+25, j*100+25, 50, 50))
        pygame.draw.rect(DISPLAYSURF, BLUE, (cursor[0]*100+45, cursor[1]*100+45, 10, 10))

        for i in doors:
            pygame.draw.line(DISPLAYSURF, i[0], i[1], i[2], 10)

        pygame.display.update()


def Doors(map):
    with open(os.path.join("Levels", "meta.json"), "r") as file:
        meta = json.load(file)
    levels = meta["levels"]
    coords = [None, None]
    for i in range(len(levels)):
        for j in range(len(levels[i])):
            if levels[i][j] == map:
                coords = [i, j]
    # Refers to the levels with the doors in them
    lines = []
    # Refers to the actual lines that will be drawn
    real_lines = []
    try:    
        if bool(levels[coords[0]-1][coords[1]]) == True and levels[coords[0]-1][coords[1]][0] != "x":
            lines.append(["up", coords[0]-1, coords[1]])
    except IndexError:
        pass
    try:
        if bool(levels[coords[0]+1][coords[1]]) == True and levels[coords[0]+1][coords[1]][0] != "x":
            lines.append(["down", coords[0]+1, coords[1]])
    except IndexError:
        pass    
    try:    
        if bool(levels[coords[0]][coords[1]-1]) == True and levels[coords[0]][coords[1]-1][0] != "x":
            lines.append(["left", coords[0], coords[1]-1])
    except IndexError:
        pass
    try:
        if bool(levels[coords[0]][coords[1]+1]) == True and levels[coords[0]][coords[1]+1][0] != "x":
            lines.append(["right", coords[0], coords[1]+1])
    except IndexError:
        pass
    for i in lines:
        with open(os.path.join("Levels", f"level {levels[i[1]][i[2]]}.json"), "r") as file:
            level = json.load(file)
        line = read(level["Level"], i[0])
        count = 0
        for item in line:
            start_pos, end_pos = readLine(i[0], count)
            if item == "x":
                colour = BLACK
            else:
                colour = GREEN
            real_lines.append([colour, start_pos, end_pos])
            count += 1
        level = None
    return real_lines

def readLine(direction, count):
    if direction == "up":
        start_pos = (count*100, 0)
        end_pos = ((count+1)*100, 0)
    elif direction == "down":
        start_pos = (count*100, SCREEN_HEIGHT)
        end_pos = ((count+1)*100, SCREEN_HEIGHT)
    elif direction == "left":
        start_pos = (0, count*100)
        end_pos = (0, (count+1)*100)
    elif direction == "right":
        start_pos = (SCREEN_WIDTH, count*100)
        end_pos = (SCREEN_WIDTH, (count+1)*100)
    return start_pos, end_pos

def read(level, direction):
    arr = []
    if direction == "right":
        for i in level:
            arr.append(i[0])
    elif direction == "left":
        for i in level:
            arr.append(i[-1])
    elif direction == "up":
        arr = level[-1]
    elif direction == "down":
        arr = level[0]
    return arr


if __name__ == "__main__":
    main()