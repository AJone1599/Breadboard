import pygame
from pygame.locals import *

pygame.font.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Breadboard holes
class Hole(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Hole,self).__init__()
        self.color = (0,0,0)
        self.radius = 10   
        self.width = 10 
        self.x = x
        self.y = y   
        self.pos = (x,y)
        self.select = False
        self.pressed = False
        self.wireConnecting = False
    def update(self):
        self.area = pygame.draw.circle(screen,self.color,self.pos,self.radius,self.width)
        if self.select == True:
            self.color = (0,255,0)
        else:
            self.color = (0,0,0)

holeRadius = 10
holeWidth = 10
listOfHoles = []
rectx = 25
recty = 25
rectWidth = 600
rectHeight = 600
distanceBetweenHoles = 50    

#Create list of coordinates for the holes to be drawn
def drawHoles():
    y = distanceBetweenHoles+recty
    yEnd = rectHeight-distanceBetweenHoles
    xEnd = rectWidth-distanceBetweenHoles
    #While loop gets coordinate of rows
    while y <= yEnd+recty:
        #Goes to first column
        x = distanceBetweenHoles+rectx
        #While loop gets coordinate for column
        while x <= xEnd+rectx:
            xValue = x + holeRadius/2
            yValue = y + holeRadius/2
            listOfHoles.append([xValue,yValue])
            #Next column
            x = x + distanceBetweenHoles
        #Next row
        y = y + distanceBetweenHoles
    #Draws holes from the list of coordinates
    for x, idk in enumerate(listOfHoles):
        holes.add(Hole(listOfHoles[x][0],listOfHoles[x][1]))

    return listOfHoles
holes = pygame.sprite.Group()
drawHoles()

class Component(pygame.sprite.Sprite):
    def __init__(self,points,color):
        super(Component,self).__init__()
        self.surface = screen
        self.color = color
        self.points = points
    def update(self):
        pygame.draw.polygon(screen,self.color,self.points)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
components = pygame.sprite.Group()

addComponents = False
componentPoints = ()

def createComponents(color):
    global addComponents
    global componentPoints

    #Loops through each hole to see if it is pressed
    for index, hole in enumerate(holes):
        if hole.area.collidepoint(pygame.mouse.get_pos()):
            #If button is pressed
            if event.type == MOUSEBUTTONDOWN:
                if not hole.pressed:
                    point = (hole.x,hole.y)
                    #Activate hole and add it to coordinates for component
                    if addComponents == False and hole.select == False:
                        hole.select = True
                        componentPoints = componentPoints + (point,)
                    #Activate hole and add it to coordinates for component
                    elif addComponents == True and hole.select == False:
                        hole.select = True
                        componentPoints = (point,)
                    #Create component when a selected hole is pressed and deselect all holes
                    elif addComponents == False and hole.select == True:
                        components.add(Component(componentPoints,color))
                        for hole2 in holes:
                            hole2.select = False
                        componentPoints = ()
                    else:
                        components.add(Component(componentPoints,color))
                        for hole2 in holes:
                            hole2.select = False
                        componentPoints = ()
                    hole.pressed = True
            else:
                hole.pressed = False

class Wire(pygame.sprite.Sprite):
    def __init__(self,x1,y1,x2,y2,color):
        super(Wire,self).__init__()
        self.surface = screen
        self.color = color
        self.width = 10
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def update(self):
        self.line = pygame.draw.line(self.surface, self.color, (self.x1, self.y1), (self.x2, self.y2), self.width)
    
connectWire = False
wireX1Y1 = []
def createWire(color):
    global connectWire
    global wireX1Y1
    for index, hole in enumerate(holes):
        if hole.area.collidepoint(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN:
                if not hole.pressed:
                    #Activate hole and the first coordinate
                    if connectWire == False:
                        hole.select = True
                        wireX1Y1 = [hole.x, hole.y]
                        connectWire = True
                    #Create wire and deselect all holes
                    elif connectWire == True:
                        for hole2 in holes:
                            hole2.select = False
                        wires.add(Wire(wireX1Y1[0], wireX1Y1[1], hole.x, hole.y,color))
                        connectWire = False

                    hole.pressed = True
            else:
                hole.pressed = False
wires = pygame.sprite.Group()

colorSelect = (255,0,0)
class ColorButton(pygame.sprite.Sprite):
    def __init__(self,color,x,y,width,height):
        super(ColorButton,self).__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.height = height
        self.width = width
    def update(self):
        self.rect = pygame.draw.rect(self.screen,self.color,pygame.Rect(self.x,self.y,self.width,self.height))
    
def createColorButtons(buttonsX ,buttonsY):
    #buttonsHeight = 100
    #buttonsWidth = 200
    height = 50
    width = 50
    columns = 4
    buttonsWidth = width*columns
    y = buttonsY
    x = buttonsX
    listOfColors = [(255,0,0), (0,255,0), (0,0,255), (0,255,255), (255,0,255), (255,255,0), (255,255,255),(100,100,100)]
    for color in listOfColors:
        colors.add(ColorButton(color,x,y,width,height))
        x = x + width
        if x >= buttonsX+buttonsWidth:
            x = buttonsX
            y = y + height
def selectColor():
    global colorSelect
    for button in colors:
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN:
                colorSelect = button.color
colors = pygame.sprite.Group()
createColorButtons(650,400)

class Resistor(pygame.sprite.Sprite):
    def __init__(self,x1,y1,value):
        super(Resistor,self).__init__()
        self.surface = screen
        self.value = value
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1 + distanceBetweenHoles*2
        self.y2 = y1 
        self.resistorColor = (196,164,132)
        self.rectY = self.y1-distanceBetweenHoles/4
        #function to calculate resistor values
    def update(self):
        #draw wire line
        self.line = pygame.draw.line(self.surface, (100,100,100), (self.x1, self.y1), (self.x2, self.y2), 10)
        rectangle = pygame.Rect(self.x1+distanceBetweenHoles/3, self.rectY,distanceBetweenHoles*1.333,distanceBetweenHoles/2)
        pygame.draw.rect(screen,self.resistorColor,rectangle)
        #draw lines for the values
        pygame.draw.line(self.surface, (255,255,255), (self.x1+distanceBetweenHoles/2, self.rectY), (self.x1+distanceBetweenHoles/2, self.rectY+distanceBetweenHoles/2), 5)
        
        pygame.draw.line(self.surface, (255,255,255), (self.x1+distanceBetweenHoles/1.2, self.rectY), (self.x1+distanceBetweenHoles/1.2, self.rectY+distanceBetweenHoles/2), 5)
        
        pygame.draw.line(self.surface, (255,255,255), (self.x1+distanceBetweenHoles*1.1, self.rectY), (self.x1+distanceBetweenHoles*1.1, self.rectY+distanceBetweenHoles/2), 5)

        pygame.draw.line(self.surface, (255,255,255), (self.x1+distanceBetweenHoles*1.45, self.rectY), (self.x1+distanceBetweenHoles*1.45, self.rectY+distanceBetweenHoles/2), 5)

resistorButtonRect = Rect(650,300-distanceBetweenHoles/4,distanceBetweenHoles*2,distanceBetweenHoles/2)
resistorButtonDrag = False
resistorButton = Resistor(650,300,50)
resistorButtonColor = (100,50,100)
resistorButtonX = -50
resistorButtonY = -50

resistors = pygame.sprite.Group()

class LED(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super(LED,self).__init__()
        self.surface = screen
        self.x = x
        self.y = y
        self.color = color
        self.pinColor = (100,100,100)
    def update(self):
        #draw wires
        pygame.draw.line(self.surface, self.pinColor, (self.x, self.y+distanceBetweenHoles), (self.x+distanceBetweenHoles/4,self.y+distanceBetweenHoles/2), 5)
        pygame.draw.line(self.surface, self.pinColor, (self.x+distanceBetweenHoles/4+distanceBetweenHoles/2,self.y+distanceBetweenHoles/2), (self.x+distanceBetweenHoles, self.y+distanceBetweenHoles), 5)
        #draw LED
        rectangle = pygame.Rect(self.x+distanceBetweenHoles/4,self.y,distanceBetweenHoles/2,distanceBetweenHoles/2)
        pygame.draw.rect(screen,self.color,rectangle)
        pygame.draw.circle(screen,self.color,(self.x+distanceBetweenHoles/4+distanceBetweenHoles/4,self.y),distanceBetweenHoles/4)

LEDButtonX = 775
LEDButtonY = 300
LEDButtonRect = Rect(775, 300-distanceBetweenHoles/4,distanceBetweenHoles, distanceBetweenHoles+distanceBetweenHoles/4)
LEDButtonDrag = False
LEDButtonColor = (100,50,100)
LEDXtemp = -50
LEDYtemp = -50

LEDs = pygame.sprite.Group()

menu = Rect(650, 50,200,500)

class WireModeButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(WireModeButton,self).__init__()
        self.surface = screen
        self.color = (0,255,0)
        self.pressed = False
        self.modeList = ['wire','component']
        self.mode = 'wire'
        self.x = x
        self.y = y

    def update(self,color):
        screen.blit(base_font.render(self.mode,True,(255,255,255)),(self.x,self.y-25))
        self.componenentRect = pygame.draw.rect(self.surface, color, pygame.Rect(self.x,self.y,50,50))
        self.wireRect = pygame.draw.rect(self.surface, color, pygame.Rect(self.x+100,self.y,25,50))

        #If component selected
        if self.componenentRect.collidepoint(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN:
                if not self.pressed:
                    self.mode = 'component'
                    self.pressed = True
            else:
                self.pressed = False
        #If wire selected
        if self.wireRect.collidepoint(pygame.mouse.get_pos()):
            if event.type == MOUSEBUTTONDOWN:
                if not self.pressed:
                    self.mode = 'wire'
                    self.pressed = True                    
            else:
                self.pressed = False

wireModeButton = WireModeButton(650,125)


class Label(pygame.sprite.Sprite):
    def __init__(self,x,y,text,color):
        super(Label,self).__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.color = color
    def update(self):
        text_surface = base_font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.x,self.y))

labels = pygame.sprite.Group()

user_text = "right click to edit"
base_font = pygame.font.Font(None, 32)
input_rect = pygame.Rect(650,200,50,50)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False
def createText():
    if active:
        color = color_active
    else:
        color = color_passive
          
    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(screen, color, input_rect)
  
    text_surface = base_font.render(user_text, True, (255, 255, 255))
      
    # render at position stated in arguments
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
      
    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width()+10)

dragText = False
textX = -50
textY = -50

running = True
while running:
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Edit text
            if input_rect.collidepoint(event.pos) and event.button == 3:
                active = True
            #Place text
            elif input_rect.collidepoint(event.pos) and event.button == 1:
                dragText = True
            #Place resistor
            elif resistorButtonRect.collidepoint(event.pos) and event.button == 1:
                resistorButtonDrag = True    
                resistorButtonColor = (0,100,100)
            #Place LED
            elif LEDButtonRect.collidepoint(event.pos) and event.button == 1:
                LEDButtonDrag = True    
                LEDButtonColor = (0,100,100)             
            #Cancel placing LED or Resistor
            else:
                active = False

                resistorButtonDrag = False
                resistorButtonColor = (100,50,100)

                LEDButtonDrag = False
                LEDButtonColor = (100,50,100)

        if event.type == pygame.MOUSEBUTTONUP:
            #Place text
            if event.button == 1 and dragText == True:
                dragText = False
                labels.add(Label(textX,textY,user_text,colorSelect))
                textX = -50
                textY = -50
            #Place resistor
            if event.button == 1 and resistorButtonDrag == True:
                resistorButtonDrag = False
                resistorButtonColor = (100,50,100)
                resistors.add(Resistor(resistorButtonX,resistorButtonY,69))
                resistorButtonX = -50
                resistorButtonY = -50
            #Place LED
            if event.button == 1 and LEDButtonDrag == True:
                LEDButtonDrag = False
                LEDButtonColor = (100,50,100)
                LEDs.add(LED(LEDXtemp,LEDYtemp,colorSelect))
                LEDXtemp = -50
                LEDYtemp = -50

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            #Coordinate for draging text, resistor, or LED
            if dragText == True:
                textX = mouse_x
                textY = mouse_y       
            if resistorButtonDrag == True:
                resistorButtonX = mouse_x
                resistorButtonY = mouse_y
            if LEDButtonDrag == True:
                LEDXtemp = mouse_x
                LEDYtemp = mouse_y             
        #Edit text
        if event.type == pygame.KEYDOWN and active == True:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]  
            else:
                user_text += event.unicode

        if event.type == QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))
    #draw white rectangle
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(rectx, recty, rectWidth, rectHeight))

    pygame.draw.rect(screen,(150,150,150),menu)

    #update everything
    holes.update()
    labels.update()
    resistors.update()
    colors.update()
    components.update()
    wires.update()
    LEDs.update()

    #Create text
    createText()
    screen.blit(base_font.render(user_text, True, (255, 0, 255)),(textX,textY))
    

    #Resistor Button
    pygame.draw.rect(screen, resistorButtonColor, resistorButtonRect)
    resistorButton.update()
    Resistor(resistorButtonX,resistorButtonY,69).update()

    #LED
    pygame.draw.rect(screen, LEDButtonColor, LEDButtonRect,)
    LED(LEDButtonX,LEDButtonY,colorSelect).update()
    LED(LEDXtemp,LEDYtemp,colorSelect).update()


    selectColor()
    
    #Button for wires and component
    wireModeButton.update(colorSelect)
    if wireModeButton.mode == 'wire':
        createWire(colorSelect)
    elif wireModeButton.mode == 'component':
        createComponents(colorSelect)
    pygame.display.flip()
