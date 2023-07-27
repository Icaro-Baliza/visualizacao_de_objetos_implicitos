import pyglet
import boundary
import os
path = os.path.join(os.path.dirname(__file__), 'images')


#Tela de Carregamento
img = pyglet.image.load(f"{path}/working.png")
pic = pyglet.sprite.Sprite(img,104,124)
pic.visible=False
action = True

#Cores para vizualização dos níveis   
colors= ((0,0,0),(50, 225, 30),(255,120,255),(117,255,255),(255,255,119),(155,155,155),(0,0,0),(0,0,0),(0,0,0))

class QuadTree:
    def __init__(self, depth=0, boundary= boundary.Boundary(104,104,512)):
        self.depth = depth
        self.searchDepth = 2
        self.plotDepth = 9
        self.boundary = boundary

        # Quadrado a ser desenhado na tela
        self.square = pyglet.shapes.BorderedRectangle(
            self.boundary.x, self.boundary.y,
            self.boundary.w, self.boundary.w, 
            border=8 - depth+1, color=(255,255,255),
            border_color=colors[depth%7],
            )

        # Quadrantes representando cada nó da QuadTree
        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

    def __del__(self):
        return
    
    #Reliza a plotagem da QuadTree
    def plot(self,dt= None,eq = None):
        global action
        if self.depth < self.searchDepth:
            self.subdividePlot(eq)
            if self.depth == 0:
                pic.visible=False
                action = True
                return True
            return True
        
        if self.depth > self.plotDepth:
            return True
        
        if self.boundary.sign(eq):
            self.subdividePlot(eq)
            return True
    
    # Cria 4 nós filhos e 4 Quadrantes referentes ao subdomínio
    def subdividePlot(self,equation):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w // 2

        boundary_sw = boundary.Boundary( x, y, w, self.depth)
        boundary_nw = boundary.Boundary( x, y + w, w, self.depth)
        boundary_se = boundary.Boundary( x + w, y, w, self.depth)
        boundary_ne = boundary.Boundary( x + w, y + w, w, self.depth)

        self.northWest = QuadTree(self.depth+1, boundary_nw)
        self.northEast = QuadTree(self.depth+1, boundary_ne)
        self.southWest = QuadTree(self.depth+1, boundary_sw)
        self.southEast = QuadTree(self.depth+1, boundary_se)

        self.northWest.plot(eq=equation)
        self.northEast.plot(eq=equation)
        self.southWest.plot(eq=equation)
        self.southEast.plot(eq=equation)
        
    #Desenha os nós fronteiras
    def showCurve(self,drawDepth):
        if self.depth > drawDepth:
            return
        if self.depth >= drawDepth and self.boundary.signal == -1:
            self.square.color = self.square.border_color = (50, 225, 30)
            self.square.draw()

        if self.northWest != None:
            self.northWest.showCurve(drawDepth)
            self.northEast.showCurve(drawDepth)
            self.southWest.showCurve(drawDepth)
            self.southEast.showCurve(drawDepth)
            return

    #Desenha os níveis internos e externos
    def showIntExt(self,drawDepth):
        if self.depth > drawDepth:
            return
        if self.depth >= drawDepth:
            self.square.color = self.square.border_color = (0,0,255)
            self.square.draw()
        
        if self.northWest != None:
            self.northWest.showIntExt(drawDepth)
            self.northEast.showIntExt(drawDepth)
            self.southWest.showIntExt(drawDepth)
            self.southEast.showIntExt(drawDepth)
            return
        
        if self.boundary.signal == 1:
            self.square.color = self.square.border_color = (255,0,0)
        else:
            self.square.color = self.square.border_color = (0,0,255)
        
        if self.depth >= 8:
            self.border = -1
        
        
        self.square.draw()

    # Desenha a árvore em todos os seus níveis
    def ShowQuadTree(self, drawDepth):
        if self.depth <= drawDepth:
            if self.depth > 8:
                self.square.color = (100,100,100)
                self.square.border_color = (255,255,255)
            elif self.depth == 8:
                self.square.color = self.square.border_color = (0,0,0)
            else:
                self.square.color = (255,255,255)
                self.square.border_color = colors[self.depth]
            self.square.border = 1
            self.square.draw()
        else:
            return

        if self.northWest != None:
            self.northWest.ShowQuadTree(drawDepth)
            self.northEast.ShowQuadTree(drawDepth)
            self.southWest.ShowQuadTree(drawDepth)
            self.southEast.ShowQuadTree(drawDepth)
    
        

        
        
        