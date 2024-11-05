import pygame
import time 
from constant import *

class rock():
    def __init__(self, x, y, rock_weight):
        self.image = pygame.image.load('Source/Asset/images/rock.png')
        self.image  = pygame.transform.scale(self.image, (Unit_Dimention, Unit_Dimention))
        self.x = x
        self.y = y
        self.rock_weight = rock_weight
    def draw(self, display_surface):
        rock_rect = self.image.get_rect()
        rock_rect.center = (self.x, self.y)
        display_surface.blit(self.image,rock_rect)
        pygame.draw.circle(display_surface, White, (self.x, self.y), 15)
        font = pygame.font.Font(None,20)
        text_surface = font.render(self.rock_weight, True, Black)
        text_rect = text_surface.get_rect(center= (self.x, self.y))
        display_surface.blit(text_surface, text_rect)
        pygame.display.update()


        
class Maze:
    def __init__(self, input, display_surface) -> None:
        self.file = open(input).read().split('\n')
        self.list_rock = []
        self.list_brick = []
        self.list_gate = []
        self.Prince = []
        self.Start = Button_choose('Start', display_surface, Window_Width - 80, 60, 70, 20, Red)
        self.Pause = Button_choose('Pause', display_surface, Window_Width - 80, 100, 70, 20, Red)
        self.Restart = Button_choose('Restart', display_surface, Window_Width - 80, 140, 70, 20, Red)
        self.weight_rock = Button_choose('Weight rock: 0', display_surface, Window_Width -700, 30, 240, 40, Red)
        self.num_step = Button_choose('Number Step: 0', display_surface, Window_Width - 350, 30, 240, 40, Red)

         # Tải và điều chỉnh kích thước ảnh gạch
        brick = pygame.image.load('Source/Asset/images/brick.png')
        self.image_brick = pygame.transform.scale(brick, (Unit_Dimention, Unit_Dimention))
        
        image_prince = pygame.image.load('Source/Asset/images/prince.png')  
        self.image_prince = pygame.transform.scale(image_prince, (250,50))
        # Tải và điều chỉnh kích thước đá
        rock_image = pygame.image.load('Source/Asset/images/rock.png')
        self.rock_image = pygame.transform.scale(rock_image, (Unit_Dimention, Unit_Dimention))
        rock_weight = self.file[0].split(' ')
        num_rock = 0

        
        for i in range(len(self.file)):
            for j in range(len(self.file[i])):
                if self.file[i][j] == '#':
                    self.list_brick.append ([(j + (21 -len(self.file[1])) / 2) * Unit_Dimention, (i  + (12 - len(self.file)) / 2) * Unit_Dimention])
                if self.file[i][j] == '$':
                    rock_temp = ([(j + (21 -len(self.file[1])) / 2) * Unit_Dimention, (i  + (12 - len(self.file)) / 2) * Unit_Dimention, rock_weight[num_rock]])
                    self.list_rock.append(rock_temp)
                    num_rock += 1 
                if self.file[i][j] == '.':
                    self.list_gate.append([(j + (21 -len(self.file[1])) / 2) * Unit_Dimention , (i  + (12 - len(self.file)) / 2) * Unit_Dimention ])
                if self.file[i][j] == '@':
                    self.Prince.append([(j + (21 -len(self.file[1])) / 2) * Unit_Dimention , (i  + (12 - len(self.file)) / 2) * Unit_Dimention ])
                if self.file[i][j] == '+':
                    self.Prince.append([(j + (21 -len(self.file[1])) / 2) * Unit_Dimention , (i  + (12 - len(self.file)) / 2) * Unit_Dimention ])
                    self.list_gate.append([(j + (21 -len(self.file[1])) / 2) * Unit_Dimention , (i  + (12 - len(self.file)) / 2) * Unit_Dimention ])

    def draw(self, display_surface):
        pygame.draw.line(display_surface, Yellow, (Unit_Dimention*21, 0), (Unit_Dimention*21, Unit_Dimention*13), 5)
        for i in range(len(self.list_gate)):
            pygame.draw.circle(display_surface, Red, (self.list_gate[i][0], self.list_gate[i][1]), Unit_Dimention/2)
        self.Pause.draw_button()
        self.Start.draw_button()
        self.Restart.draw_button()
        self.num_step.draw_button()
        self.weight_rock.draw_button()
        prince_rect = self.image_prince.get_rect()
        prince_rect.center = (self.Prince[0][0],self.Prince[0][1])
        display_surface.blit(self.image_prince, prince_rect)

        for i in range(len(self.list_brick)):
            brick_rect = self.image_brick.get_rect()
            brick_rect.center = (self.list_brick[i][0], self.list_brick[i][1])
            display_surface.blit(self.image_brick, brick_rect)

        for i in range(len(self.list_rock)):
            rock_rect = self.rock_image.get_rect()
            rock_rect.center = (self.list_rock[i][0], self.list_rock[i][1])
            display_surface.blit(self.rock_image,rock_rect)
            pygame.draw.circle(display_surface, White, (self.list_rock[i][0], self.list_rock[i][1]), 15)
            font = pygame.font.Font(None,20)
            text_surface = font.render(self.list_rock[i][2], True, Black)
            text_rect = text_surface.get_rect(center= (self.list_rock[i][0], self.list_rock[i][1]))
            display_surface.blit(text_surface, text_rect)
            pygame.display.update()
       
        pygame.display.flip()
        pygame.display.update()
 
            


    def move(self, display_surface, route):
        bool_Restart = True
        
        while(bool_Restart):
            bool_Restart = False
            time_wait = 0.05
            Start(self.Start)
            weight_rock = 0
            num_step = 0

            for step in route:
                num_step += 1
                self.num_step.name = "Number step: " + str(num_step)
                if step == 'u':
                    time.sleep(time_wait*3)
                    for i in range(1,10):
                        
                        if  Pause(self.Pause,self.Restart):
                            return True

                        display_surface.fill(Grey)
                        self.Prince[0][1] -= 5
                        time.sleep(time_wait)
                        self.draw(display_surface)  
                elif step == 'U':
                    time.sleep(time_wait*3)
                    index = 0
                    for i in range(len(self.list_rock)):
                    #   print(self.list_rock[i][1], self.Prince[0][1],  self.list_rock[i][0], self.Prince[0][0])
                        if self.list_rock[i][1] == self.Prince[0][1] - 45 and self.list_rock[i][0] == self.Prince[0][0] :
                            index = i 
                    weight_rock += int(self.list_rock[index][2])
                    self.weight_rock.name = 'Weight rock: ' + str(weight_rock)
                    for i in range(1,10):
                        if  Pause(self.Pause,self.Restart):
                            return True
                        display_surface.fill(Grey)
                        self.Prince[0][1] -= 5
                        self.list_rock[index][1] -= 5
                        time.sleep(time_wait)
                        self.draw(display_surface)
                elif step == 'd':
                    time.sleep(time_wait*3)
                    for i in range(1,10):
                        if  Pause(self.Pause,self.Restart):
                            return True
                        display_surface.fill(Grey)
                        self.Prince[0][1] += 5
                        time.sleep(time_wait)
                        self.draw(display_surface)
                elif step == 'D':
                    time.sleep(time_wait*3)
                    index = 0
                    for i in range(len(self.list_rock)):
                        if self.list_rock[i][1] == self.Prince[0][1] + 45 and self.list_rock[i][0] == self.Prince[0][0] :
                            index = i 
                    weight_rock += int(self.list_rock[index][2])
                    self.weight_rock.name = 'Weight rock: ' + str(weight_rock)
                    for i in range(1,10):
                        if  Pause(self.Pause,self.Restart):
                            return True
                        display_surface.fill(Grey)
                        self.Prince[0][1] += 5
                        self.list_rock[index][1] += 5
                        time.sleep(time_wait)
                        self.draw(display_surface)
                elif step == 'l':
                    time.sleep(time_wait*3)
                    for i in range(1,10):
                        if  Pause(self.Pause, self.Restart):
                            return True
                        display_surface.fill(Grey)
                        self.Prince[0][0] -= 5
                        time.sleep(time_wait)
                        self.draw(display_surface)
                elif step == 'L':
                    time.sleep(time_wait*3)
                    index = 0
                    for i in range(len(self.list_rock)):
                        if self.list_rock[i][0] == self.Prince[0][0] - 45 and self.list_rock[i][1] == self.Prince[0][1]:
                            index = i 
                            break
                    weight_rock += int(self.list_rock[index][2])
                    self.weight_rock.name = 'Weight rock: ' + str(weight_rock)
                    for i in range(1,10):
                        if  Pause(self.Pause, self.Restart):
                            return True
                        self.Prince[0][0] -= 5
                        self.list_rock[index][0] -= 5
                        self.draw(display_surface)
                        time.sleep(time_wait)
                        display_surface.fill(Grey)
                elif step == 'r':
                    time.sleep(time_wait*3)
                    for i in range(1,10):
                        if  Pause(self.Pause, self.Restart):
                            return True
                        display_surface.fill(Grey)                 
                        self.Prince[0][0] += 5
                        time.sleep(time_wait)
                        self.draw(display_surface)
                elif step == 'R':
                    time.sleep(time_wait*3)
                    index = 0
                    for i in range(len(self.list_rock)):
                        if self.list_rock[i][0] == self.Prince[0][0] + 45 and self.list_rock[i][1] == self.Prince[0][1] :
                            index = i 
                    weight_rock += int(self.list_rock[index][2])
                    self.weight_rock.name = 'Weight rock: ' + str(weight_rock)
                    for i in range(1,10):
                        if  Pause(self.Pause,self.Restart):
                            return True
                        display_surface.fill(Grey)
                        self.Prince[0][0] += 5
                        self.list_rock[index][0] += 5
                        time.sleep(time_wait)
                        self.draw(display_surface)
            font = pygame.font.Font(None, 100)
            text_surface = font.render('FINISH ALGORITHM', True, Yellow)
            text_rect = text_surface.get_rect(center = (Window_Width/2, Window_Height/2) )
            display_surface.blit(text_surface, text_rect)
        return False
            
def Pause(button, button_restart):
    paused = False  # Mặc định không tạm dừng
    
    for event in pygame.event.get():
        # Kiểm tra nếu người dùng nhấn nút đóng cửa sổ
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        
        # Kiểm tra sự kiện chuột nhấn
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Nếu nhấn chuột vào nút, kích hoạt trạng thái tạm dừng
            if button.rect.collidepoint(mouse_pos):
                paused = True  # Kích hoạt trạng thái tạm dừng
            elif button_restart.rect.collidepoint(mouse_pos):
                return True
    # Nếu tạm dừng, giữ chương trình trong trạng thái tạm dừng cho đến khi nhấn lại
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Kiểm tra sự kiện nhấn chuột trong khi đang tạm dừng
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Nếu nhấn chuột vào nút, tiếp tục chương trình
                if button.rect.collidepoint(mouse_pos):
                    paused = False  # Thay đổi trạng thái để tiếp tục
    return False
        # Cập nhật màn hình trong khi tạm dừng

def Start(button):
      
    paused = True         

    while(paused):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                        # Kiểm tra sự kiện chuột nhấn
                if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if button.rect.collidepoint(mouse_pos):
                            paused = not paused

def Restart (button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

                        # Kiểm tra sự kiện chuột nhấn
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_pos):
                return True
         
                  

class Button_choose:
        def __init__(self,name,display_surface,x, y,width, height, color):
            self.name = name
            self.display_surface = display_surface
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        def draw_button(self):
           
            pygame.draw.rect(self.display_surface, self.color,self.rect )
            font = pygame.font.Font(None, 30)
            text_surface = font.render(self.name, True, Yellow)
            text_rect = text_surface.get_rect(center = (self.x + self.width/2,self.y + self.height/2))
            self.display_surface.blit(text_surface, text_rect)
 


class home:
    def __init__(self):
        pass
    def draw(self, display_surface):
        image_home = pygame.image.load('Source/Asset/images/home.png')
        image_home = pygame.transform.scale(image_home, (Window_Width, Window_Height))
        home_rect = image_home.get_rect()
        home_rect.topleft = (0, 0)
        display_surface.blit(image_home, home_rect)

        font = pygame.font.Font(None,45)
        text_surface = font.render('VISUALIZE SEARCH OLGORITHMS', True, Red)
        text_rect = text_surface.get_rect(center=(300,100))
        display_surface.blit(text_surface, text_rect)

        button_BFS = Button_choose('Breath First Search',display_surface,100,200,220,30,Red)
        button_DFS = Button_choose('Deep First Search',display_surface,100,270,220,30,Red)
        button_UCS = Button_choose('Uniform Cost Search',display_surface,100,340,220,30,Red)
        button_AS  = Button_choose('A* Search',display_surface,100,410,220,30,Red)


        button_AS.draw_button()
        button_BFS.draw_button()
        button_DFS.draw_button()
        button_UCS.draw_button()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if button_BFS.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                return int(1)
            else:
                button_BFS.color = Pretty_Red
                button_BFS.draw_button()
                return 0
        elif button_DFS.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                return int(2)
            else:
                button_DFS.color = Pretty_Red
                button_DFS.draw_button()
                return 0
        elif button_UCS.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                return int(3)
            else:
                button_UCS.color = Pretty_Red
                button_UCS.draw_button()
                return 0
        elif button_AS.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                return int(4)
            else:
                button_AS.color = Pretty_Red
                button_AS.draw_button()
                return 0
        else:
            return 0

 
class home_search:
    def __init__(self,display_surface):
        pass
    def draw(self, display_surface):
        image_home_search = pygame.image.load('Source/Asset/images/home_input.png')
        image_home_search = pygame.transform.scale(image_home_search, (Window_Width, Window_Height))
        home_search_rect = image_home_search.get_rect()
        home_search_rect.topleft = (0,0)
        display_surface.blit(image_home_search, home_search_rect)

        font = pygame.font.Font(None, 40)
        text_surface = font.render('CHOOSE INPUT', True, Red)
        text_rect = text_surface.get_rect(center = (400, 50) )
        display_surface.blit(text_surface, text_rect)


        list_button = []
        for i in range(2):
            for j in range(5):
                button_temp = Button_choose('Input '+ str((i * 5) + j + 1 ), display_surface, 400 + i* 300, j * 70 + 100, 200,50, Red)
                button_temp.draw_button()
                list_button.append(button_temp)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for i in range(10):
            if list_button[i].rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    return int(i+1)
                else:
                    list_button[i].color = Blue
                    list_button[i].draw_button()  
                    return 0  
            
        return 0
class prince:
    def __init__(self):
      pass
    def draw(self, display_surface, x, y):
        prince_rect = self.image.get_rect()
        prince_rect.center = (x, y)
        display_surface.blit(self.image, prince_rect)

           


        

        

        

