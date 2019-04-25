import pygame, sys
from random import randint

SCREENWIDTH = 500
SCREENHEIGHT = 400

BLOCK_HEIGHT = round(SCREENHEIGHT/10)
BLOCK_WIDTH = round(SCREENWIDTH/10)

GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
BLACK = (0, 0, 0, 0)
GREEN = (0, 200, 0)
DARKGREY = (150, 150, 150)
LIGHTGREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)

"""
    ===================================
                 class Tile
    ===================================
"""

class Tile:
    def __init__(self, x, y, contents):
        # print("in tile, contents are of type: {}".format(type(contents)))
        if not isinstance(contents, str):
            print("contents ({}) are NOT of type string. They are of type: {}".format(contents), type(contents))
            pygame.quit()
            sys.exit("Error in class Tile. Contents were not of type str.")
        self._x = x
        self._y = y
        self._contents = contents
        self.neighbors = []

    @property
    def contents(self):
        temp = []
        temp.append(self._x)
        temp.append(self._y)
        temp.append(self._contents)
        return temp

    @contents.setter
    def contents(self, value):
        # I've changed my mind, there is no reason x or y should ever be changed.
        # read/accessed, sure, but not changed.
        # if not isinstance(value, list):
        #     print("value ({}) is NOT of type list. It is of type: {}".format(value), type(value))
        #     pygame.quit()
        #     sys.exit("Error in class Tile in def contents (property setter). Contents were not of type list.")
        # if not isinstance(value[0], int):
        #     raise ValueError("Contents ({}) are not of type int. They are of type ({}).".format(value[0], type(value[0])))
        # if not isinstance(value[1], int):
        #     raise ValueError("Contents ({}) are not of type int. They are of type ({}).".format(value[1], type(value[1])))
        if not isinstance(value, str):
            raise ValueError("Contents ({}) are not of type str. They are of type ({}).".format(value, type(value)))
        # self._x = value[0]
        # self._y = value[1]
        self._contents = value

    def drop_neighbors(self):
        self.neighbors = []

    def has_neighbors(self):
        if len(self.neighbors) > 0:
            return True
        return False

    # def get_nothing_tile(self):
    #     new_tile = Tile(-1, -1, "nothing")
    #     new_tile.neighbors = []
    #     return new_tile

    def debug_print(self):
        print_string = "{}-{}-{}-[{}] || ".format(self._x, self._y, self._contents, len(self.neighbors))
        # print_string = "{}-{}-{} || ".format(self._x, self._y, self._contents)
        print(print_string)

    def return_string(self):
        # print("{}-{}-{}".format(self._x, self._y, self._contents))
        return "{}-{}-{}-[{}] || ".format(self._x, self._y, self._contents, len(self.neighbors))

"""
    ===================================
                 class Map
    ===================================
"""

class Map:
    def __init__(self, mapfile, game):
        self.world_map = self.read_file(mapfile)
        self.surface = game.surface

    def __len__(self):
        return len(self.world_map)

    def read_file(self, mapfile):
        temp = []
        with open(mapfile, 'r') as f:
            temp = f.readlines()
        temp = [l.strip() for l in temp]
        # Width is the number of items in a row (the number of columns)
        self.map_width = len(temp[0])
        # Height is the number of rows.
        self.map_height = len(temp)
        # Translate into tiles
        x = 0
        y = 0
        the_map=[]
        for string_row in temp:
            y = 0
            the_row = []
            for elem in string_row:
                a_tile = Tile(x, y, elem)
                the_row.append(a_tile)
                y += 1
            x += 1
            the_map.append(the_row)
        return the_map

    def get_tile(self, x, y):
        if x < 0 or x >= self.map_width:
            raise ValueError("index (x) is out of range: {}".format(x))
        if y < 0 or y >= self.map_height:
            raise ValueError("index (y) is out of range: {}".format(y))
        return self.world_map[x][y]

    def get_tile_contents(self, x, y):
        return self.world_map[x][y].contents

    def get_row_as_list(self, row_number):
        return_list=[]
        for row in range(self.map_height):
            if row == row_number:
                row_list = self.world_map[row_number]
                # print("row list: {}".format(row_list))
                for r in row_list:
                    return_list.append(r.contents)
                return return_list

    def examine_world(self):
        new_map = []
        for j, this_row in enumerate(self.world_map):
            new_row = []
            for i, this_tile in enumerate(this_row):
                mylist = []
                if this_tile.contents[2] == "x":
                    i = this_tile.contents[0]
                    j = this_tile.contents[1]
                    tile_above = self._get_tile_above(i, j)
                    tile_right = self._get_tile_right(i, j)
                    tile_below = self._get_tile_below(i, j)
                    tile_left = self._get_tile_left(i, j)

                    if tile_above.contents[2] == "x":
                        mylist.append(tile_above)
                    if tile_below.contents[2] == "x":
                        mylist.append((tile_below))
                    if tile_right.contents[2] == "x":
                        mylist.append(tile_right)
                    if tile_left.contents[2] == "x":
                        mylist.append(tile_left)

                new_tile = Tile(this_tile.contents[0], this_tile.contents[1], this_tile.contents[2])
                if len(mylist) > 0:
                    new_tile.neighbors = mylist
                mylist = []
                new_row.append(new_tile)
            new_map.append(new_row)

        self.world_map = new_map

    def get_neighbor_tiles(self, this_tile):
        i = this_tile._x
        j = this_tile._y
        tile_above = self._get_tile_above(i, j)
        tile_right = self._get_tile_right(i, j)
        tile_below = self._get_tile_below(i, j)
        tile_left = self._get_tile_left(i, j)
        mylist = []
        mylist.append(tile_above)
        mylist.append(tile_right)
        mylist.append(tile_below)
        mylist.append(tile_left)
        return mylist

    def delete_neighbor_tiles(self):
        for this_row in self.world_map:
            for this_tile in this_row:
                this_tile.drop_neighbors()

    def decide(self):
        print("------ decide (begin) ----------")
        self.debug_print()
        for this_row in self.world_map:
            for this_tile in this_row:
                if this_tile.has_neighbors() == False:
                    # turn on an adjacent tile
                    num_of_neighbors = 1
                    # We need to assign neighbors to this tile. We do
                    # this by putting an "x" in the contents of
                    # neighboring tiles.
                    self.assign_neighbors(this_tile, num_of_neighbors)
                else:
                    if len(this_tile.neighbors) == 4:
                        self.remove_all_neighbors(this_tile)
        # Before we leave, let's strip away all the neighbour tiles.
        self.delete_neighbor_tiles()
        self.debug_print()
        print("------ decide (end) ----------")

    def assign_neighbors(self, this_tile, num_of_neighbors):
        mylist = self.get_neighbor_tiles(this_tile)
        # print("mylist: {}".format(mylist))
        if num_of_neighbors == 1:
            myran = randint(0, 3)
            for arow in self.world_map:
                for atile in arow:
                    if atile._x == mylist[myran]._x:
                        if atile._y == mylist[myran]._y:
                            atile.contents = "x"

    def remove_all_neighbors(self, this_tile):
        mylist = self.get_neighbor_tiles(this_tile)
        for arow in self.world_map:
            for atile in arow:
                for this_tile in mylist:
                    if atile._x == this_tile._x:
                        if atile._y == this_tile._y:
                            atile.contents = "."

    def change_element(self, x, y, new_value):
        myrow = self.world_map[y]
        temp = 0
        newstring = ""
        for elem in myrow:
            if temp == x:
                newstring += new_value
            else:
                newstring += elem
            temp += 1
        self.world_map[y] = newstring

    def _fill_map_tile(self, x, y):
        print("in fill_map_tile: {}, {}".format(x, y))
        self.change_element(x, y, "x")

    def _empty_map_tile(selfs, x, y):
        self.change_element(x, y, ".")

    def debug_print(self):
        print("----------------- DEBUG PRINT Begin -----------------")
        temp = ""
        for row in self.world_map:
            # print("row: {}".format(row))
            for a_tile in row:
                temp += a_tile.return_string()
            print("{}".format(temp))
            temp = ""
        print("length: {}".format(len(self.world_map)))
        print("----------------- DEBUG PRINT End -----------------")

    def update_map(self, center_tile, direction):
        tempx = center_tile.x
        tempy = center_tile.y
        if direction == "above":
            tempy += -1
        if direction == "below":
            tempy += 1
        if direction == "right":
            tempx += 1
        if direction == "left":
            tempx += -1
        self._fill_map_tile(tempx, tempy)

    def player_coords(self):
        for i, row in enumerate(self.world_map):
            for j, column in enumerate(row):
                if column == "p":
                    return (j, i)
        return (-1, -1)

    def neighbours_full(self, x, y):
        bor = []
        if (x+1) >= 0:
            print("looking at {}, {}".format(x+1, y))
            print("contents of {},{}: {}".format(x+1, y, self.map[x+1][y]))
            if self.world_map[x+1][y]=="x":
                bor.append((x+1, y))
        if (x-1) >= 0:
            if self.world_map[x-1][y]=="x":
                bor.append((x-1, y))
        if (y+1) >= 0:
            if self.world_map[x][y+1] == "x":
                bor.append((x, y+1))
        if (y-1) >= 0:
            if self.world_map[x][y-1] == "x":
                bor.append((x, y-1))
        return bor

    def _get_tile_above(self, x, y):
        if y > 0:
            return self.get_tile(x, y-1)
        else:
            return Tile(-1, -1, "nothing")

    def _get_tile_below(self, x, y):
        if y < (self.map_height-1):
            return self.get_tile(x, y+1)
        else:
            return Tile(-1, -1, "nothing")

    def _get_tile_right(self, x, y):
        if x < (self.map_width-1):
            return self.get_tile(x+1, y)
        else:
            return Tile(-1, -1, "nothing")

    def _get_tile_left(self, x, y):
        if x > 0:
            return self.get_tile(x-1, y)
        else:
            return Tile(-1, -1, "nothing")

    # --------------------------------

    def _set_tile_above(self, x, y, new_contents):
        x += -1
        mylist = []
        mylist.append(x)
        mylist.append(y)
        mylist.append(new_contents)
        self.world_map[x][y].contents = mylist

    def _set_tile_below(self, x, y, new_contents):
        x += 1
        mylist = []
        mylist.append(x)
        mylist.append(y)
        mylist.append(new_contents)
        self.world_map[x][y].contents = mylist

    def _set_tile_right(self, x, y, new_contents):
        y += 1
        mylist = []
        mylist.append(x)
        mylist.append(y)
        mylist.append(new_contents)
        self.world_map[x][y].contents = mylist

    def _set_tile_left(self, x, y, new_contents):
        y += -1
        mylist = []
        mylist.append(x)
        mylist.append(y)
        mylist.append(new_contents)
        self.world_map[x][y].contents = mylist

    def change_tiles(self, mydict, target_tile):
        temp_tile = Tile()
        if mydict('above')==True:
            atile = self._get_above_tile(target_tile)
            self._fill_map_tile(atile.x, atile.y)
        if mydict('below')==True:
            atile = self._get_below_tile(target_tile)
            self._fill_map_tile(atile.x, atile.y)
        if mydict('right')==True:
            atile = self._get_right_tile(target_tile)
            self._fill_map_tile(atile.x, atile.y)
        if mydict('left')==True:
            atile = self._get_left_tile(target_tile)
            self._fill_map_tile(atile.x, atile.y)

    def draw(self):
        draw_tile = False
        tile_color = BLACK
        for row in range(self.map_height):
            row_list = self.get_row_as_list(row)
            # print("row in def draw: {}".format(row_list))
            for elem in row_list:
                if elem[2] == ".":
                    tile_color = GREEN
                    draw_tile = True
                if elem[2] == "x":
                    tile_color = BLUE
                    draw_tile = True
                if elem[2] == "p":
                    tile_color = GREEN
                    draw_tile = True
                if draw_tile == True:
                    myrect = pygame.Rect(elem[1] * BLOCK_WIDTH, elem[0] * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
                    pygame.draw.rect(self.surface, tile_color, myrect)
                draw_tile = False
        self.draw_grid()

    def draw_grid(self):
        line_height = SCREENHEIGHT / 10
        line_width = SCREENWIDTH / 10
        for i in range(10):
            new_height = round(i * line_height)
            new_width = round(i * line_width)
            pygame.draw.line(self.surface, BLACK, (0, new_height), (SCREENWIDTH, new_height), 2)
            pygame.draw.line(self.surface, BLACK, (new_width, 0), (new_width, SCREENHEIGHT), 2)
