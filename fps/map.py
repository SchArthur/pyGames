import pygame
import fileLoader

class newMap():
    def __init__(self, file, height) -> None:
        content = fileLoader.loadFile(file)
        self.cells = self.loadMap(content)
        self.createMiniMap(height)

    def loadMap(self, fileContent):
        cells = []
        for line in fileContent:
            row = line.strip().split(',')
            cells.append(row)
        return cells
    
    def createMiniMap(self, height):
        self.cell_size = height // len(self.cells)
        self.rect_list = []
        width = self.cell_size * len(self.cells[0])
        self.miniMap_surface = pygame.surface.Surface((width,height))
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                y = self.cell_size * row
                x = self.cell_size * col

                cell_rect = pygame.rect.Rect(x,y,self.cell_size,self.cell_size)
                if self.cells[row][col] == '1':
                    self.rect_list.append(cell_rect)


    def drawMiniMap(self) -> pygame.surface.Surface:
        self.miniMap_surface.fill('white')
        for elt in self.rect_list:
            pygame.draw.rect(self.miniMap_surface, 'black', elt)

        return self.miniMap_surface