import random
import time
import pygame

SIZE = 40
pygame.display.set_caption("Snake Game")

class Apple:
    def __init__(self,screen):
        self.img = pygame.transform.scale(pygame.image.load("Apple.png"), (50,50))
        self.screen = screen
        self.x = SIZE*4
        self.y = SIZE*4

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(100, 800)
        self.y = random.randint(100, 500)

class Snake:
    def __init__(self, screen, length):
        self.length = length
        self.screen = screen
        self.SNAKE_BLOCK = pygame.transform.scale(pygame.image.load("Block.png"), (40,40))
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"
        self.speed = SIZE

    def increment(self):
        self.length += 1
        self.x.append(10000)
        self.y.append(10000)

    def draw(self):
        self.check_borders()
        for i in range(self.length):
            self.screen.blit(self.SNAKE_BLOCK, (self.x[i], self.y[i]))
        pygame.display.update()

    def check_borders(self):
        for i in range(0,self.length):
            if self.x[i] >= 900:
                self.x[i] = 10
            if self.x[i] <= 0:
                self.x[i] = 900
            if self.y[i] <= 0:
                self.y[i] = 590
            if self.y[i] >= 600:
                self.y[i] = 0



    def move_left(self):
        self.direction = "left"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]


        if self.direction == "up":
            self.y[0] -= self.speed
        elif self.direction == "down":
            self.y[0] += self.speed
        elif self.direction == "right":
            self.x[0] += self.speed
        elif self.direction == "left":
            self.x[0] -= self.speed
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.name = ""
        self.game_music()
        self.WIN = pygame.display.set_mode((900, 600))
        self.snake = Snake(self.WIN,2)
        self.apple = Apple(self.WIN)

    leaderBoard = pygame.Rect(250, 400, 300, 100)

    def collision(self,x1,x2,y1,y2,size):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def display_score(self):
        player_name =  pygame.font.SysFont("Ubuntu", 50, True)
        player_name_write = player_name.render("Name: " + str(self.name), 1, (255,255,255))
        score = pygame.font.SysFont("Ubuntu", 50, True)
        score_write = score.render("Score: " + str(self.snake.length),1,(255,255,255))
        self.WIN.blit(score_write,(650, 40))
        self.WIN.blit(player_name_write,(30,40))
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.WIN,2)
        self.apple = Apple(self.WIN)

    def show_leaderboard(self):
        run = True
        font = pygame.font.SysFont("Ubuntu", 60,1)
        font2 = pygame.font.SysFont("Ubuntu", 40,1)
        while run:
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                    pygame.quit()


            self.background()
            title = font.render("Top 10 Scores",1,(255,255,255))
            self.WIN.blit(title, (270,20))

            f = open("Scores.txt",'r')
            i = 0
            y = 120
            for x in f:
                if i >= 10:
                    break
                txt = font2.render(f"{i+1}.     {x[:-1]}",1,(255,255,255))
                self.WIN.blit(txt,(250,y))
                i += 1
                y += 50


            pygame.display.update()


    def game_over(self):
        self.background()
        font = pygame.font.SysFont("Arial", 40,1)
        l1 = font.render(f"Game Over! {self.name} got " + str(self.snake.length) + " points",1, (255, 255, 255))
        self.WIN.blit(l1, (100, 200))
        l2 = font.render("Press Enter to restart, Press esc to exit", 1, (255,255,255))
        self.WIN.blit(l2, (100, 250))
        pygame.draw.rect(self.WIN,(145,7,26),self.leaderBoard)
        font = pygame.font.SysFont("Arial",30,1,1)
        L_text = font.render("Leader Boards",1,(255,255,255))
        self.WIN.blit(L_text,(self.leaderBoard.x + 60, self.leaderBoard.y + 30))

        pygame.display.update()
        pygame.mixer.music.pause()
        f = open("Scores.txt",'at')
        f.write(f"{self.name}       Score: {self.snake.length}\n")
        f.close()

    def game_music(self):
        pygame.mixer.music.load("Back_Music.mp3")
        pygame.mixer.music.play(loops=-1)

    def background(self):
        img = pygame.transform.scale(pygame.image.load("Background.jpg"),(900,600))
        self.WIN.blit(img, (0,0))



    def start_game(self):
        run = True
        font = pygame.font.SysFont("Ubuntu",80,1)
        font2 = pygame.font.SysFont("Ubuntu",40,1)
        name_font = pygame.font.SysFont("Ubuntu",30)
        game_txt = font.render("SNAKE GAME",1,(42,14,226))
        name_txt = font2.render("Enter your name: ",1,(42,14,226))
        txt1 = font2.render("Press Enter to continue...",1,(42,14,226))
        name_box = pygame.Rect(150+name_txt.get_width()+10,270,300,40)
        active = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if name_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False


                if event.type == pygame.KEYDOWN:
                    if self.name != "":
                        if pygame.key.get_pressed()[pygame.K_RETURN]:
                            run = False
                    if active:
                        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                            self.name = self.name[:-1]
                        else:
                            self.name += event.unicode

            self.background()
            self.WIN.blit(game_txt, (200, 60))
            self.WIN.blit(name_txt,(150,260))
            self.WIN.blit(txt1,(230,410))

            if active:
                color = (42,14,226)
            else:
                color = (255,255,255)

            pygame.draw.rect(self.WIN,color,name_box,5)
            name = name_font.render(self.name,1,(42,14,226))
            self.WIN.blit(name, (name_box.x + 8, name_box.y))

            pygame.display.update()

        self.name = self.name[:-1]
        self.run_game()



    def run_game(self):
        run = True
        timer = pygame.time.Clock()
        pause = False
        self.snake.draw()
        self.apple.draw()
        while run:
            timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    run = False
                if not pause:
                    if pygame.key.get_pressed()[pygame.K_a]:
                        self.snake.move_left()
                    if pygame.key.get_pressed()[pygame.K_w]:
                        self.snake.move_up()
                    if pygame.key.get_pressed()[pygame.K_s]:
                        self.snake.move_down()
                    if pygame.key.get_pressed()[pygame.K_d]:
                        self.snake.move_right()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    pygame.mixer.music.unpause()
                    pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.leaderBoard.collidepoint(event.pos):
                        self.show_leaderboard()

            try:
                if not pause:
                    self.background()
                    self.snake.walk()
                    self.apple.draw()
                    self.display_score()

                    if self.collision(self.snake.x[0], self.apple.x, self.snake.y[0], self.apple.y, 50):
                        sound = pygame.mixer.Sound("EatingSound.wav")
                        pygame.mixer.Sound.play(sound)
                        self.apple.move()
                        self.snake.increment()

                    for i in range(3,self.snake.length):
                        if self.collision(self.snake.x[0],self.snake.x[i], self.snake.y[0], self.snake.y[i], 40):
                            sound = pygame.mixer.Sound("Explosion.wav")
                            pygame.mixer.Sound.play(sound)
                            raise "game over"

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.start_game()