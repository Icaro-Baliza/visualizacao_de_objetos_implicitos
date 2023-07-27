DOMAIN = 1
class Boundary:
    def __init__(self,x,y,w,depth=0):
        self.x = x
        self.y = y
        self.w = w #width
        self.signal = -1

    # Define o sinal daquele quadrante
    def sign(self, equation):
        x = (self.x - 360)/100 * DOMAIN
        y = (self.y - 360)/100 * DOMAIN
        w = self.w/100 * DOMAIN
        
        #Avalia a função em cada vértice do domínio e retorna assim que encontra valores opostos
        SW = 1 if equation(x,y) < 0 else 0 
        NW = 1 if equation(x,y+w) < 0 else 0
        if SW != NW:
            self.signal = -1
            return True
        SE = 1 if equation(x+w,y) < 0 else 0
        if SW != SE:
            self.signal = -1
            return True
        
        NE = 1 if equation(x+w,y+w) < 0 else 0
        if SW != NE:
            self.signal = -1
            return True
        
        self.signal = SW
        return False