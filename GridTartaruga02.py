
# coding: utf-8

# <h1> Grid da tartaruga
# 

# In[1]:


import pygame
clock = pygame.time.Clock()


# In[2]:


class Coisa:
    
    def __init__(self,estado = None):
        self.estado = estado
        self.idNoTabuleiro = 0
        
    def __repr__(self):
        #representação do objeto na forma de string
        return '<{}>'.format(getattr(self, '__name__',self.__class__.__name__))
    
    def mostraEstado(self):
        return str(self.estado)
    
    def vivo(self):
        return hasattr(self, 'vivo') and self.vivo
    


# In[3]:


class Vertice:
    def __init__(self,rotulo):
        self.rotulo = rotulo
    def __eq__(self,outro):
        return outro == self.rotulo
    def __repr__(self):
        return self.rotulo
    def __hash__(self):
        return hash(self.rotulo)


# In[4]:


class Grafo:
  def __init__(self):
    self.numVerticesMaximo = 30
    self.numVertices = 0
    self.listaVertices = []
    self.matrizIncidencias =[]
    for i in range(self.numVerticesMaximo):
        linhaMatriz = []
        for j in range (self.numVerticesMaximo):
          linhaMatriz.append(0.0)
        self.matrizIncidencias.append(linhaMatriz)
 
  def adicionaVertice(self,rotulo):
    self.numVertices+=1
    self.listaVertices.append(Vertice(rotulo))
 
 
  def adcionaArco(self,inicio,fim,peso):
    i = self.localizaRotulo(inicio)
    j = self.localizaRotulo(fim)
    if i==-1 or j==-1: return
    self.matrizIncidencias[i][j]=peso
    self.matrizIncidencias[j][i]=peso
 
  def mostraVertice(self,vertice):
    print(self.matrizIncidencias[vertice].rotulo)
 
  def imprimeMatriz(self):
    print(" ",end = ',')
    for i in range(self.numVertices):
      print(self.listaVertices[i].rotulo,end=',')
    print()
    for i in range(self.numVertices):
      print(self.listaVertices[i].rotulo,end=',')
      for j in range(self.numVertices):
        print(self.matrizIncidencias[i][j],end=',')
      print()
 
  def localizaRotulo(self,ro):
    for i in range(self.numVertices):
      if  self.listaVertices[i].rotulo == ro:
        return i
    return -1
 
  def distancia(self,r1,r2):
    i= self.localizaRotulo("C3")
 
    n= self.localizaRotulo(r1)
    j= self.localizaRotulo(r2)
    if i==-1 or j==-1:return -1
    return self.matrizIncidencias[i][j]


# In[5]:


class Agente(Coisa):
    
    def __init__(self,estado = None, funcaoAgente = None):
        super().__init__(estado)
        if funcaoAgente == None:
            def funcaoAgente(*entradas):
                return "Ação Default"
        self.funcaoAgente = funcaoAgente
        self.historicoPercepcoes = []
        self.x = 2
        self.y = 3
        
    def percepcao(self):
        entrada = input("Entre com dados ")# percepções
        self.historicoPercepcoes.append(eval(entrada))
            
    def movimentacao(self,x,y):
        self.x = x
        self.y = y
        
    def saida(self):
        return self.funcaoAgente(self.historicoPercepcoes)


# In[6]:


class Tartaruga(Agente):
    def __init__(self,estadoInicial = None, funcaoAgente = None):
        super().__init__(estadoInicial,funcaoAgente)
        self.img = pygame.image.load('Tartaruga.png')
        self.idNoTabuleiro=3

        


# In[7]:


class bloco(Coisa):
    def __init__(self,estado = None,x = 0, y = 0):
        super().__init__(estado)
        self.img = pygame.Surface([128,128])
        self.img.fill((0,0,255))
        self.x = x
        self.y = y
        self.idNoTabuleiro =1
    
          
        
    


# In[8]:


class Minhoca(Coisa):
    def __init__(self,estado = None,x = 0, y = 0):
        super().__init__(estado)
        self.img = pygame.image.load('Minhoca.png')
        self.x = x
        self.y = y
        self.idNoTabuleiro=2


# In[9]:


class Ambiente:
    
    def __init__(self,estadoInicial = None, gr = None):
        self.estado = estadoInicial
        self.objetosNoAmbiente = []
        self.agentes = []
        self.dest = []
        self.tabuleiro = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
    def percepcao(self,agente):
        # Define as percepções do agente
        return None
    
    def adicionaAgente(self,agente):
        self.agentes.append(agente)
        self.tabuleiro[agente.y][agente.x]=agente.idNoTabuleiro
        
    def adicionaObjeto(self,obj):
        self.objetosNoAmbiente.append(obj)
        self.tabuleiro[obj.y][obj.x]=obj.idNoTabuleiro
        if obj.idNoTabuleiro == 1:
            for i in range(gr.numVertices):
                gr.adcionaArco(gr.listaVertices[obj.y*6+obj.x],gr.listaVertices[i],0.0)
        elif obj.idNoTabuleiro == 2:
            self.dest = gr.listaVertices[obj.y*6+obj.x]
        
        


# In[10]:


class ReinoAnimal(Ambiente):
    def __init__(self,estadoInicial,gr):
        super().__init__(estadoInicial)
        pygame.init()
        self.tempo=0
        self.fim = False

    def executaAmbiente(self):
        self.lc=astar(gr,"C3",self.dest)
        print(self.lc)
        self.tela = pygame.display.set_mode((768,640),0,8)
        pygame.display.set_caption('Grid da Tartaruga')
        self.aux = 0                
        pygame.display.update()#AT elementos no display
        while not self.fim:
            self.aux +=1
            self.planoDeFundo()
            for i in range(len(self.objetosNoAmbiente)):
                self.tela.blit(self.objetosNoAmbiente[i].img,(self.objetosNoAmbiente[i].x*128, self.objetosNoAmbiente[i].y*128))
            self.tela.blit(self.agentes[0].img,(self.agentes[0].x*128, self.agentes[0].y*128))
            if self.aux== 100:
                self.aux=0
                if self.tempo< len(self.lc):
                    self.px,self.py = self.agentes[0].funcaoAgente(self.tempo,self.lc,gr.listaVertices)
                    self.agentes[0].movimentacao(self.px,self.py)
                self.tempo+=1
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.fim = True
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()
                    
    def exibeMIds(self):
        for i in range(5):
            for j in range(6):
                print(self.tabuleiro[i][j],end="")
            print(" ")
    def planoDeFundo(self):
        self.tela.fill((250,250,250))
        for x in range(0,768,128):
            pygame.draw.line(self.tela, (255,0,0), (x,0), (x,640))
        for y in range(0,640,128):
            pygame.draw.line(self.tela, (255,0,0), (0,y), (768,y))
            

        
        

  


# In[11]:


def criaGrafo(nohs):
  gr = Grafo()
  for n in nohs:
      gr.adicionaVertice(n)
  for j in range(4):
    n=6*j
    for i in range(5):
        gr.adcionaArco(gr.listaVertices[i+n],gr.listaVertices[i+n+1],1.0)
        gr.adcionaArco(gr.listaVertices[i+n],gr.listaVertices[i+n+6],1.0)
    gr.adcionaArco(gr.listaVertices[5+n],gr.listaVertices[11+n],1.0)
  for i in range(5):
    gr.adcionaArco(gr.listaVertices[24+i],gr.listaVertices[25+i],1.0)
  return gr


# In[12]:


def calculaCustosCaminhos(grafo,fronteira,meta):
  custos = []
  for i in fronteira:
      c = 0
      for j in range(1,len(i)):
        c+=grafo.distancia(i[j-1],i[j])
      else:
        c+=grafo.distancia(fronteira[-1],meta)
      custos.append(c)
  return custos


# In[13]:


def astar(grafo, inicio, meta):
  fronteira = [[inicio]]
  while fronteira:
    custos = calculaCustosCaminhos(grafo,fronteira,meta)
    indC = custos.index(min(custos))
    caminho=fronteira.pop(indC)
    v = caminho[-1]
    if v == meta:
        return caminho
    else:
        vi = grafo.localizaRotulo(v)
        
        for i, w in enumerate(grafo.matrizIncidencias[vi]):
          if w > 0:
            novoCaminho=list(caminho)
            novoElemento = grafo.listaVertices[i].rotulo
            novoCaminho.append(novoElemento)
            fronteira.append(novoCaminho)
  return "Sem"


# In[14]:


def deslocamendoParaExibi(t,lc,lv):
    if t< len(lc):
        for i in range(5):
            for j in range(6):
               if lc[t]==lv[6*i+j]:return j,i


# In[15]:


pontos =["A0","B0","C0","D0","E0","F0",         "A1","B1","C1","D1","E1","F1",         "A2","B2","C2","D2","E2","F2",         "A3","B3","C3","D3","E3","F3",         "A4","B4","C4","D4","E4","F4"]
gr = criaGrafo(pontos)
a = ReinoAnimal([],gr)
t = Tartaruga([],deslocamendoParaExibi)
a.adicionaAgente(t)
b1 = bloco(0,4,2)
b2 = bloco(0,4,3)
m = Minhoca(0,5,2)
a.adicionaObjeto(b1)
a.adicionaObjeto(b2)
a.adicionaObjeto(m)
a.executaAmbiente()

