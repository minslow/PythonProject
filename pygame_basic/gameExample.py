import pygame

pygame.init()  #초기화 (항상 무조건 해야함)

#화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height)) #실질적으로 화면을 설정하는 문단

#제목: 게임 이름
pygame.display.set_caption("The Title") 

#FPS
clock = pygame.time.Clock()

#배경 이미지 불러오기
background = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_basic\\background.png")

#캐릭터 이미지 불러오기
chara = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_basic\\chara.png")
chara_size = chara.get_rect().size #캐릭터 크기
chara_width = chara_size[0] 
chara_height = chara_size[1]
charaX = screen_width/2 - chara_width/2 #캐릭터 위치
charaY = screen_height - chara_height

#적 캐릭터 만들기
enemy = pygame.image.load("C:\\Users\\user\\Desktop\\PythonWorkspace\\pygame_basic\\enemy.png")
enemy_size = enemy.get_rect().size #적 크기
enemy_width = enemy_size[0] 
enemy_height = enemy_size[1]
enemyX = screen_width/2 - enemy_width/2 #적 위치
enemyY = screen_height/2 - enemy_height/2

#이동할 좌표
speed = 0.5
moveLX = 0
moveRX = 0
moveUY = 0
moveDY = 0

#폰트 정의
game_font = pygame.font.Font(None, 40) #어떤 폰트를, 어떤 크기로 할건지 결정

#게임 시간
total_time = 10

#시작 시간 정보
start_ticks = pygame.time.get_ticks()

#이벤트 루프
running = True
while running:
    dt = clock.tick(60) # 게임화면 초당 프레임 수
    for event in pygame.event.get(): #이벤트를 받는, 무조건 적어야 하는 부분
        if(event.type == pygame.QUIT):
            running = False

        if event.type == pygame.KEYDOWN: #키 눌림
            if event.key == pygame.K_LEFT:
                moveLX -= speed
            elif event.key == pygame.K_RIGHT:
                moveRX = speed
            elif event.key == pygame.K_UP:
                moveUY -= speed
            elif event.key == pygame.K_DOWN:
                moveDY = speed
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLX = 0
            elif event.key == pygame.K_RIGHT:
                moveRX = 0
            elif event.key == pygame.K_DOWN:
                moveDY = 0
            elif event.key == pygame.K_UP:
                moveUY = 0
        
    charaX += (moveRX + moveLX) * dt
    charaY += (moveUY + moveDY) * dt

    #맵 경계
    if charaX <= 0:
        charaX = 0
    elif charaX >= screen_width - chara_width:
        charaX = screen_width - chara_width

    if charaY <= 0:
        charaY = 0
    elif charaY >= screen_height - chara_height:
        charaY = screen_height - chara_height

    #충돌 처리    
    chara_rect = chara.get_rect()
    chara_rect.left = charaX
    chara_rect.top = charaY

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemyX
    enemy_rect.top = enemyY

    if chara_rect.colliderect(enemy_rect):#충돌 했다면
        print("충돌했어요")

    screen.blit(background, (0,0)) #배경 그리기
    screen.blit(chara, (charaX, charaY))
    screen.blit(enemy, (enemyX, enemyY))

    #경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks)/1000 #초 단위로 표시하기 위해서 1000 
    
    #타이머
    timer = game_font.render(str(int(total_time - elapsed_time)) , True, (255, 255, 255))
    screen.blit(timer, (10,10))

    if total_time - elapsed_time <=0:
        print("타임오버!")
        running = False

    pygame.display.update() #게임화면 다시 그리기

pygame.time.delay(2000)

pygame.quit()