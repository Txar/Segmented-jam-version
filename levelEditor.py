import pygame, sys, os, math

mouseRightKeyPressed, mouseLeftKeyPressed, scrollingRight, scrollingLeft, gameOver = False, False, False, False, False
LEFT = 1
RIGHT = 3
SCROLLDOWN = 4
SCROLLUP = 5
existingBlocksAmount = 3
selectedBlock = 0
useBlock = 0
save = False
selectedTool = 0 #0 is pencil, 1 is pipette

lastUsedLevelFile = open("gameData/levelEditor.pgd", "r")
lastUsedLevel = ""
lastUsedLevel = str(lastUsedLevelFile.readlines(1))
lastUsedLevel = lastUsedLevel.replace("['", "")
lastUsedLevel = lastUsedLevel.replace("']", "")
lastUsedLevelFile.close()
loadLastUsedFile = os.path.exists("levels/" + str(lastUsedLevelFile))
wholeLevel = []

width = 1280
height = 704
cellSprite = pygame.image.load("floor.png")
cellSprite.blit(pygame.image.load("player0.png"), ((0, 0)))
"""playerSprite = pygame.image.load("sprites/icon.png")
pushblockSprite = pygame.image.load("sprites/pushblock.png")
floorSprite = pygame.image.load("sprites/floorTile.png")
blockSprite = pygame.image.load("sprites/block.png")
holeSprite = pygame.image.load("sprites/hole.png")
sectorIcon = pygame.image.load("sprites/icon.png")
tileOutline = pygame.image.load("sprites/tileOutline.png")
horizontalRailsSprite = pygame.image.load("sprites/horizontalRails.png")"""
exitSprite = pygame.image.load("exitButton.png")
floorSprite = pygame.image.load("floor.png")
blockSprite = pygame.image.load("wall.png")
tileOutline = pygame.image.load("tileOutline.png")

def loadLevelFile(levelName = lastUsedLevel):
	global lastUsedLevel, wholeLevel
	wholeLevel = []
	for i in range(0, 22):
		wholeLevel.append([])
	if loadLastUsedFile:
		levelName = lastUsedLevel
	loadedLevel = open("levels/" + str(levelName))
	for rowsLoaded in range(0, 22):
		wholeLevel[rowsLoaded].append(loadedLevel.readlines(rowsLoaded + 1))
		wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("\\n", "")
		wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("[['", "")
		wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("']]", "")
		wholeLevel[rowsLoaded] = wholeLevel[rowsLoaded].split(" ")
	loadedLevel.close()

def drawLevel():
	global wholeLevel
	for rowsDrawn in range(0, 22):
		for columnsDrawn in range(0, 40):
			x = int(columnsDrawn) * 32
			y = int(rowsDrawn) * 32
			if wholeLevel[rowsDrawn][columnsDrawn] == "01":
				dis.blit(blockSprite, (int(x), int(y)), (0, 0, 32, 32))
			if wholeLevel[rowsDrawn][columnsDrawn] == "00":
				dis.blit(floorSprite, (int(x), int(y)))
			if wholeLevel[rowsDrawn][columnsDrawn] == "02":
				dis.blit(cellSprite, (int(x), int(y)))
			if wholeLevel[rowsDrawn][columnsDrawn] == "03":
				dis.blit(exitSprite, (int(x), int(y)))

def roundTo32(x, base = 32):
    return int(base * math.ceil(float(x) / base) - 32)

def checkTilesUnderMouse():
	global mousepos, useBlock
	if mousepos[1] < height and mousepos[1] > 0 and mousepos[0] > 0 and mousepos[0] < width:
		dis.blit(tileOutline, (roundTo32(mousepos[0]), roundTo32(mousepos[1])))
		x = int(roundTo32(mousepos[0]) / 32)
		y = int(roundTo32(mousepos[1]) / 32)
		if mouseRightKeyPressed:
			wholeLevel[y][x] = "00"
		if mouseLeftKeyPressed:
			wholeLevel[y][x] = useBlock


def changeSelectedBlock():
	global selectedBlock, scrollingLeft, scrollingRight, existingBlocksAmount, useBlock
	if scrollingRight and selectedBlock < existingBlocksAmount + 1:
		selectedBlock = selectedBlock + 1
	elif scrollingLeft and selectedBlock >= 0:
		selectedBlock = selectedBlock - 1
	if selectedBlock == 0:
		useBlock = "00"
	elif selectedBlock == 1:
		useBlock = "01"
	elif selectedBlock == 2:
		useBlock = "02"
	elif selectedBlock == 3:
		useBlock = "03"

def openLevelWindow():
	global saveQuestion
	pygame.draw.rect(dis , (220, 220, 220),(0 , 0, 224, 96))
	dis.blit(saveQuestion, (0, 0))

"""def drawUi():
	global useBlock
	pygame.draw.rect(dis, (220, 220, 220), (0, 576, 800, 640))
	if useBlock == "00":
		dis.blit(floorSprite, (32, 592))
	if useBlock == "01":
		dis.blit(blockSprite, (32, 592), (0, 0, 32, 32))
	if useBlock == "02":
		dis.blit(pushblockSprite, (32, 592))
	if useBlock == "03":
		dis.blit(playerSprite, (32, 592))
	if useBlock == "04":
		dis.blit(holeSprite, (32, 592))
	if useBlock == "06":
		dis.blit(horizontalRailsSprite, (32, 592))
	if useBlock == "05":
		dis.blit(exitSprite, (32, 592))
	if useBlock == "08":
		dis.blit(lampSprite, (32, 592))"""

def saveLevel(levelSaveName = lastUsedLevel):
	global lastUsedLevel, wholeLevel, saveLevelName, save
	customLevelsDone = 0
	while True:
		filename = "levels/customLevel" + str(customLevelsDone) + ".plv"
		if os.path.exists(filename) == False:
			print(customLevelsDone)
			break
		customLevelsDone = customLevelsDone + 1
	filename = "levels/customLevel" + str(customLevelsDone) + ".plv"
	f = open(filename, "w+")
	content = ""
	for i in wholeLevel:
		for j in i:
			content += j + " "
		content += "\n"
	f.write(content)
	f.close()
	save = False
	"""newLevelFile = open(filename, "w+")

	newLevelFile.writelines(wholeLevel)
	newLevelFile.close()"""

loadLevelFile()

pygame.init()
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Segmented - level editor")
clock = pygame.time.Clock()

while not gameOver:
	scrollingLeft, scrollingRight = False, False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				save = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == RIGHT:
				mouseRightKeyPressed = True
			if event.button == LEFT:
				mouseLeftKeyPressed = True
			if event.button == SCROLLDOWN:
				scrollingRight = True
			if event.button == SCROLLUP:
				scrollingLeft = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == RIGHT:
				mouseRightKeyPressed = False
			if event.button == LEFT:
				mouseLeftKeyPressed = False
				

	mousepos = pygame.mouse.get_pos()
	changeSelectedBlock()
	print(useBlock)
	dis.fill((0, 0, 0))
	drawLevel()
	checkTilesUnderMouse()
	if save:
		saveLevel()
#	openLevelWindow()
#	drawUi()
	pygame.display.update()
	clock.tick(30)

pygame.quit()
sys.exit()