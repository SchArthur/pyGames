import pygame
import math
import fileLoader

class newMap():
    def __init__(self, file, height) -> None:
        content = fileLoader.loadFile(file)
        self.cells = self.loadMap(content)
        self.height = height
        self.createMiniMap()

    def loadMap(self, fileContent):
        cells = []
        for line in fileContent:
            row = line.strip().split(',')
            cells.append(row)
        return cells
    
    def createMiniMap(self, ):
        self.cell_size = self.height // len(self.cells)
        self.rect_list = []
        self.width = self.cell_size * len(self.cells[0])
        self.miniMap_surface = pygame.surface.Surface((self.width,self.height))
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                y = self.cell_size * row
                x = self.cell_size * col

                cell_rect = pygame.rect.Rect(x,y,self.cell_size,self.cell_size)
                if self.cells[row][col] == '1':
                    self.rect_list.append(cell_rect)

    def isWall(self, coords : pygame.Vector2) -> bool :
        isWall = False
        max_x = self.width//self.cell_size-1
        max_y = self.height//self.cell_size-1

        if coords.x < 1 or coords.x > max_x or coords.y < 1 or coords.y > max_y:
            isWall = True
        else:
            if not coords.x.is_integer():
                x = int(math.floor(coords.x))
                y_1 = int(coords.y)
                y_2 = y_1 - 1
                if self.cells[y_1][x] == '1' or self.cells[y_2][x] == '1':
                    isWall = True
            elif not coords.y.is_integer():
                y = int(math.floor(coords.y))
                x_1 = int(coords.x)
                x_2 = x_1 - 1
                if self.cells[y][x_1] == '1' or self.cells[y][x_2] == '1':
                    isWall = True

        return isWall

    def drawMiniMap(self) -> pygame.surface.Surface:
        self.miniMap_surface.fill('white')
        for elt in self.rect_list:
            pygame.draw.rect(self.miniMap_surface, 'black', elt)

        return self.miniMap_surface