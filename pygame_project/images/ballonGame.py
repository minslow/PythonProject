import pygame

pygame.init()

#화면 크기
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

#제목
pygame.display.set_caption("JJangBall")

#FPS
clock = pygame.time.Clock()

#이미지 불러오기
background = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\background.png")

stage = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\stage.png")
stageSize = stage.get_rect().size
stageHeight = stageSize[1]

chara = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\character.png")
charaSize = chara.get_rect().size
charaWidth = charaSize[0]
charaHeight = charaSize[1]
charaX = screenWidth/2 - charaWidth/2
charaY = screenHeight - charaHeight - stageHeight

weapon = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\weapon.png")
weaponSize = weapon.get_rect().size
weaponWidth = weaponSize[0]

ballImages = [
    pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\ball1.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\ball2.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\ball3.png"),
    pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_project\\images\\ball4.png")
]

ballSpeedY = [-18, -15, -12, -9]

balls = []

balls.append({
    "X" : screenWidth/2,
    "Y" : 50,
    "imgIndex" : 0,
    "toX": 3,
    "toY": -6,
    "initSpeedY" : ballSpeedY[0]
})

#사라질 무기와 공
removeW = -1
removeB = -1

#폰트
font = pygame.font.Font(None, 40)

gameResult = "게임 오버"

#캐릭터 움직임
charaMoveR = 0
charaMoveL = 0
speed = 0.5

#여러발 발사
weapons = []

weaponSpeed = 10

#시간
startTicks = pygame.time.get_ticks()
totalTime = 100

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                charaMoveL -= speed
            elif event.key == pygame.K_RIGHT:
                charaMoveR += speed
            elif event.key == pygame.K_SPACE and len(weapons) == 0: #무기발사
                weaponX = charaX + charaWidth/2 - weaponWidth/2
                weaponY = charaY 
                weapons.append([weaponX, weaponY])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                charaMoveL = 0
            elif event.key == pygame.K_RIGHT:
                charaMoveR = 0

    charaX += (charaMoveL + charaMoveR) * dt

    if charaX <= 0:
        charaX = 0
    elif charaX >= screenWidth-charaWidth:
        charaX = screenWidth-charaWidth

    #무기 위치
    weapons = [[w[0], w[1] - weaponSpeed] for w in weapons]

    #무기 천장에 충돌
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    #공 위치 정의
    for I, V in enumerate(balls):
        ballX = V["X"]
        ballY = V["Y"]
        ballImgIndex = V["imgIndex"]

        ballSize = ballImages[ballImgIndex].get_rect().size
        ballW = ballSize[0]
        ballH = ballSize[1]

        #벽에 튕김
        if ballX < 0 or ballX > screenWidth- ballW:
            V["toX"] = V["toX"] * -1

        if ballY  > screenHeight-stageHeight - ballH:
            V["toY"] = V["initSpeedY"]
        else:
            V["toY"] += 0.5
        
        V["X"] += V["toX"]
        V["Y"] += V["toY"]

    #공과 캐릭터 충돌
    charaRect = chara.get_rect()
    charaRect.left = charaX
    charaRect.top = charaY

    for ballIdx, ballVal in enumerate(balls):
        ballX = ballVal["X"]
        ballY = ballVal["Y"]
        ballImgIndex = ballVal["imgIndex"]

        ballRect = ballImages[ballImgIndex].get_rect()
        ballRect.left = ballX
        ballRect.top = ballY

        if charaRect.colliderect(ballRect):
            gameResult = "Game Over."
            running = False
            break

        #무기와 공 충돌
        for weaponIdx, weaponVal in enumerate(weapons):
            WX = weaponVal[0]
            WY = weaponVal[1]

            weaponRect = weapon.get_rect()
            weaponRect.left = WX
            weaponRect.top = WY

            if weaponRect.colliderect(ballRect):
                removeW = weaponIdx
                removeB = ballIdx

                if ballImgIndex < 3:
                    ballWidth = ballRect.size[0]
                    ballHeight = ballRect.size[1]

                    smallBallRect = ballImages[ballImgIndex + 1].get_rect()
                    smallBallW = smallBallRect.size[0]
                    smallBallH = smallBallRect.size[1]

                    #왼쪽으로 튕겨나가는 공
                    balls.append({
                        "X" : ballX + ballWidth/2  - smallBallW/2,
                        "Y" : ballY + ballHeight/2 -smallBallH/2,
                        "imgIndex" : ballImgIndex+1,
                        "toX": -3,
                        "toY": -6,
                        "initSpeedY" : ballSpeedY[ballImgIndex+1]})

                    #오른쪽으로 튕겨나가는 공
                    balls.append({
                        "X" : ballX + ballWidth/2 - smallBallW/2,
                        "Y" : ballY + ballHeight/2 -smallBallH/2,
                        "imgIndex" : ballImgIndex+1,
                        "toX": 3,
                        "toY": -6,
                        "initSpeedY" : ballSpeedY[ballImgIndex+1]})
                break
        else:
             continue
        break

    if removeB > -1:
        del balls[removeB]
        removeB = -1

    if removeW > -1:
        del weapons[removeW]
        removeW = -1

    if len(balls) == 0:
        gameResult = "Mission Complete!"
        running = False

    #화면에 그리기
    screen.blit(background, (0,0))
    
    for weaponX, weaponY in weapons:
        screen.blit(weapon, (weaponX, weaponY))

    for idx, val in enumerate(balls):
        ballX = val["X"]
        ballY = val["Y"]
        ballImgIndex = val["imgIndex"]
        screen.blit(ballImages[ballImgIndex], (ballX, ballY))

    screen.blit(stage, (0, screenHeight-stageHeight))
    screen.blit(chara, (charaX,charaY))

    #경과시간
    elapsedTime = (pygame.time.get_ticks() - startTicks)/1000

    #타이머
    timer = font.render(str((int(totalTime - elapsedTime))), True, (255,255,255))
    screen.blit(timer, (10,10))

    if totalTime - elapsedTime <= 0:
        gameResult = "Time Over."
        running = False

    pygame.display.update()

msg = font.render(gameResult, True, (0,0,0))
msgRect = msg.get_rect(center=(int(screenWidth/2), int(screenHeight/2)))
screen.blit(msg, msgRect)
pygame.display.update()

pygame.time.delay(2000)
pygame.quit()