import pyglet, math
import pyglet.window as pw
import os

window = pyglet.window.Window(720,720)
import quadtree


window.set_caption('Vizualização de curva implícita')
window.set_location(200,40)

path = os.path.join(os.path.dirname(__file__), 'images')
bg = pyglet.image.load(f'{path}/background.png')

tree = quadtree.QuadTree(boundary=quadtree.boundary.Boundary(104,104,512))
MODE = 1
drawDepth = 8

def equation1(x,y):
    return abs(x)+ abs(y) - 2
def equation2(x,y):
    return math.sin(x) - math.cos(y)
def equation3(x,y):
    return (x**2 + y**2 - 4)**3 - x**2 * y**3
def equation4(x,y):
    return x**7 -y**5 + x**2 * y**3 - (x*y)**2  
def equation5(x,y):
    return x**3 + y**2 - 6*x*y 
def equation6(x,y):
    a = -1
    b = 1.04
    return y**4-x**4 + a*y**2 + b*x**2
def equation7(x,y):
    a = 2
    return x**4-(a**2)*(x**2-y**2) 

equation = equation1

def resetQuadTree():
    global equation
    
    
@window.event
def on_key_press(symbol,modifiers):
    global MODE, equation
    
    # Aperte 1 para vizualizar os nós fronteira
    if symbol == pyglet.window.key._1 and MODE != 1:
        MODE = 1

    #Aperte 2 para vizualizar as áreas internas e externas
    elif symbol == pyglet.window.key._2 and MODE != 2:
        MODE = 2

    # Aperte 3 para vizualizar todos os níveis da QuadTree
    elif symbol ==pyglet.window.key._3 and MODE != 3:
        MODE = 3
       
        
@window.event
def on_draw():
    window.clear()
    bg.blit(0,0)
    
        
    #Alterna entre os modos de vizualização
    if MODE == 1:
        tree.showCurve(drawDepth)
    elif MODE == 2:
        tree.showIntExt(drawDepth)
    elif MODE == 3:
        tree.ShowQuadTree(drawDepth)
    quadtree.pic.draw()

    #Medidor da profundidade da árvore a ser desenhada
    pyglet.text.Label(
        f"|{drawDepth}/9|",
        font_name= 'Times New Roman',
        font_size= 50,
        x= 0, y = 660
    ).draw()
    pyglet.text.Label(
        f"Utilize o scroll do mouse\n para mudar o refinamento",
        font_name= 'Times New Roman',
        font_size= 18,
        width= 400,
        x= 130, y = 685,
        multiline= True,
    ).draw()
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    global equation, MODE
    #Clique nos botões da tela para alternar entre as equações
    if y<105 and quadtree.action:
        if x < 103 and equation != equation1:
            equation = equation1
        elif x < 205 and equation != equation2:
            equation = equation2
        elif x < 307 and equation != equation3:
            equation = equation3
        elif x < 409 and equation != equation4:
            equation = equation4
        elif x < 511 and equation != equation5:
            equation = equation5
        elif x < 613 and equation != equation6:
            equation = equation6
        elif x < 715 and equation != equation7:
            equation = equation7
        else:
            return
        quadtree.action = False
        quadtree.pic.visible=True
        #Deleta os filhos da árvore, assim removendo por completo restando apenas sua raiz
        # A medida que os filhos perdem referência, são elegíveis para serem removidos pelo Garbage Collector
        # E assim por diante até remover os nós folhas
        
        tree.northEast = None
        tree.northWest = None
        tree.southEast = None
        tree.southWest = None
        pyglet.clock.schedule_once(tree.plot,0.1,equation)
        
    #Clique nos botões acima para alternar entre os modos de vizualização
    if y >=616 and quadtree.action:
        if x >= 616 and MODE != 3:
            MODE = 3
        elif x >= 512 and MODE != 2:
            MODE = 2
        elif x >= 408 and MODE != 1:
            MODE = 1
            
            

@window.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):
    global drawDepth
    dy = drawDepth + int(scroll_y)
    if dy >= 0 and dy < 10 and quadtree.action:
        drawDepth = dy

pyglet.app.run()
