import pgzrun
import math
import re
import time
from random import randint
item = Actor('laser1')
itemdbuff =Actor('laser1.1')
item1 = Actor('item1.1')
item2 = Actor('item1.2')
item3 = Actor('item1.3')
item4 = Actor('item1.4')
player = Actor("player", (400, 550))
boss = Actor("boss")
#item1 = Actor("item1")
gameStatus = 0
highScore = []
time=0
goitem = False
goitem2 = False
goitem3 =False
goitem4 =False
goitem5 =False
goitem6 =False
def draw():  
    global updateBoss ,boss ,time ,item1,goitem3,item2,goitem4,item3,goitem5,item4,goitem6,gameStatus
    screen.blit('background', (0, 0)) 
    if gameStatus == 0:  
        drawCentreText(
            "DUMNBO HUNTER\n\n\nType your name then\npress Enter to start")
        screen.draw.text(player.name, center=(400, 500), owidth=0.5, ocolor=(
            139,69,19), color=(255,127,36), fontsize=50)
    if gameStatus == 1: 
        player.image = player.images[math.floor(player.status/6)]
        player.draw()
    if goitem == True:
        item.draw()
    if goitem2 == True:
        itemdbuff.draw()
    if goitem3 == True:
        item1.draw()
    if goitem4 == True:
        item2.draw()
    if goitem5 == True:
        item3.draw()
    if goitem6 == True:
        item4.draw()
        screen.draw.text(str(score), topright=(780, 10), owidth=0.5, ocolor=(
            139,69,19), color=(255,127,36), fontsize=60)
        if player.status >= 30:
            if player.lives > 0:
                drawCentreText("YOU TAKE A DAMAGE!\nPress Enter to re-spawn")
            else:  
                drawCentreText("GAME OVER!\nPress Enter to restart")
    if gameStatus == 2:
        drawHighScore()


def drawCentreText(t):
    screen.draw.text(t, center=(400, 300), owidth=0.5, ocolor=(
        	255,165,0), color=(	139,69,0), fontsize=50,)


def update():  
    global moveCounter, player, gameStatus, lasers, level, boss,aliens,updateBoss,score,laser1,item,goitem,item2,goitem4,item3,goitem5,item4,goitem6
    if gameStatus == 0:
        if keyboard.RETURN and player.name != "":
            gameStatus = 1
    if gameStatus == 1:
        if player.status < 30 :
            checkKeys()
            spawn()
            spawnitem2()
            if player.status > 0:
                player.status += 1
                if player.status == 30:
                    player.lives -= 1
        else:
            if keyboard.RETURN:
                if player.lives > 0:
                    player.status = 0
                else:
                    readHighScore()
                    gameStatus = 2
                    writeHighScore()
    if gameStatus == 2:
        if keyboard.ESCAPE:
            init()
            gameStatus = 0
    

def on_key_down(key):
    global player
    if gameStatus == 0 and key.name != "RETURN":
        if len(key.name) == 1:
            player.name += key.name
        else:
            if key.name == "BACKSPACE":
                player.name = player.name[:-1]


def readHighScore():
    global highScore, score, player
    highScore = []
    try:
        hsFile = open("highscores.txt", "r")
        for line in hsFile:
            highScore.append(line.rstrip())
    except:
        pass
    highScore.append(str(score) + " " + player.name)
    highScore.sort(key=natural_key, reverse=True)


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def writeHighScore():
    global highScore
    hsFile = open("highscores.txt", "w")
    for line in highScore:
        hsFile.write(line + "\n")


def drawHighScore():
    global highScore
    y = 0
    screen.draw.text("TOP SCORES", midtop=(400, 30), owidth=0.5, ocolor=(
        255, 255, 255), color=(0, 64, 255), fontsize=60)
    for line in highScore:
        if y < 400:
            screen.draw.text(line, midtop=(400, 100+y), owidth=0.5,
                             ocolor=(0, 0, 255), color=(255, 255, 0), fontsize=50)
            y += 50
    screen.draw.text("Press Escape to play again", center=(
        400, 550), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)


def drawLives():
    for l in range(player.lives):
        screen.blit("life", (10+(l*32), 10))


def drawAliens():
    for a in range(len(aliens)):
        aliens[a].draw()



def drawLasers():
    for l in range(len(lasers)):
        lasers[l].draw()


def checkKeys():
    global player, score ,item
    if keyboard.left:
        if player.x > 40:
            player.x -= 5
    if keyboard.right:
        if player.x < 760:
            player.x += 5


def makeLaserActive():
    global player
    player.laserActive = 1



def updateLasers():
    global lasers, aliens
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += 2
            checkLaserHit(l)
            if lasers[l].y > 517:
                lasers[l].status = 1
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += 2
            checkLaserHit(l)
            if lasers[l].y > 517:
                lasers[l].status = 1

        if lasers[l].type == 1:
            lasers[l].y -= 5
            checkPlayerLaserHit(l)
            if lasers[l].y < 10:
                lasers[l].status = 1
    lasers = listCleanup(lasers)
    aliens = listCleanup(aliens)


def listCleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0:
            newList.append(l[i])
    return newList


def checkLaserHit(l):
    global player , level ,score 
    player.status = 1
    
    
  


def checkPlayerLaserHit(l):
    global score, boss
    for a in range(len(aliens)):
        if aliens[a].collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            aliens[a].status = 1
    if boss.active:
        if boss.collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            boss.active = 0
      
def init():
    global lasers, score, player, moveSequence, moveCounter, moveDelay, level, boss
   
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    lasers = []
    moveDelay = 30
    boss.active = False
    player.images = ["player", "explosion1", "explosion2",
                     "explosion3", "explosion4", "explosion5"]
    player.laserActive = 1
    player.lives = 1
    player.name = ""
    level = 1


def initAliens():
    global aliens, moveCounter, moveSequence
    aliens = []
    moveCounter = moveSequence = 0
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80, 100+(int(a/6)*64))))
        aliens[a].status = 0


def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y -
                                     self.height+30), (0, 0, 64, self.height))


def collideLaser(self, other):
    return (
        self.x-20 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )




def spawn():
    global item,goitem,score,item1,goitem3,item2,goitem4,item3,goitem5,item4,goitem6,gameStatus
    if goitem == True:
        item.y += 2
        item_collected = player.colliderect(item)
        if item.y >= 500:
            gameStatus== 2
        if item_collected:
            place_item()
            score += 500
            goitem = False
    else:
        if randint(0,1)== 0:
            goitem = True
            item.x = randint(40,760)
            item.y = 40
    if goitem3 == True:
        item1.y += 2
        item_collected = player.colliderect(item1)
        if item_collected:
            place_item()
            score += 200
            goitem3 = False
    else:
        if randint(0,20)== 0:
            goitem3 = True
            item1.x = randint(40,760)
            item1.y = 40
    if goitem4 == True:
        item2.y += 2
        item_collected = player.colliderect(item2)
        if item_collected:
            place_item()
            score += 100
            goitem4 = False
    else:
        if randint(0,25)== 0:
            goitem4 = True
            item2.x = randint(40,760)
            item2.y = 40
    if goitem5 == True:
        item3.y += 2
        item_collected = player.colliderect(item3)
        if item_collected:
            place_item()
            score += 500
            goitem5 = False
    else:
        if randint(0,30)== 0:
            goitem5 = True
            item3.x = randint(40,760)
            item3.y = 40
    if goitem6 == True:
        item4.y += 2
        item_collected = player.colliderect(item4)
        if item_collected:
            place_item()
            score += 1000
            goitem6 = False
    else:
        if randint(0,35)== 0:
            goitem6 = True
            item4.x = randint(40,760)
            item4.y = 40

def spawnitem2():
    global itemdbuff,goitem2,score,gameStatus
    if goitem2 == True:
        itemdbuff.y += 6
        item_collected = player.colliderect(itemdbuff)
        if item_collected:
            place_item2()
            gameStatus==2
            goitem2 = False
        if itemdbuff.y > 600:
            goitem2 = False
            gameStatus==2
    else:
        if randint(0,50)== 0:
            goitem2 = True
            itemdbuff.x = randint(40,760)
            itemdbuff.y = 40

def place_item():
    global item,a,power_up,count
    a = randint(1,2)
    item.x = randint(40,760)
    item.y = -550
    
  
def place_item2():
    global itemdbuff,a,power_up
    itemdbuff.x = randint(40,760)
    itemdbuff.y = -5000





init()
pgzrun.go()
