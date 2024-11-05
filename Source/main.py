import pygame
import time
from constant import *
from object import Maze, home, home_search
import BFS, DFS, UCS, A_start

pygame.init()
display_surface = pygame.display.set_mode((Window_Width, Window_Height))
pygame.display.set_caption("SEARCH")    

Home = home()
Home_search = home_search(display_surface)
running = True


val_home = 1
val_search = 0
val_maze = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if val_home == 1:
        display_surface.fill(Grey)
        val_search = Home.draw(display_surface)
        if 1 <= val_search <= 4:
            val_home = 0
            
    if 1 <= val_search <= 4:
        display_surface.fill(Grey)
        val_maze = Home_search.draw(display_surface)
        if 1 <= val_maze <= 10:
            val_al = val_search
            val_search = 0

        if val_maze == -1:
            val_home = 1
    
    if 1 <= val_maze <= 10:
        restart  = True
        while (restart):
            restart = False            
            display_surface.fill(Grey)


            
            filename= 'Source/input-0' +str(val_maze)+'.txt'
            maze = Maze(filename, display_surface)
            search_move = 1
            maze.draw(display_surface) 



            #BFS
            if val_al == 1:
                
                
                BFS.main(filename,'Source/output-0' + str(val_maze)+ '.txt')
                with open('Source/output-0' + str(val_maze)+ '.txt', "r+") as file:
                    # Đọc nội dung file
                    content = file.read().split('\n')
                    num_BFS = 0 
                    path = ''             
                    for i in range(len(content)):
                        if content[i] =='BFS':
                            pos = i
                            num_BFS += 1
                            path = content[i+2]
                        if num_BFS == 2:
                            content_new = content[0:i]
                            file.seek(0)
                            file.truncate()
                            for item in content_new:
                                file.write(item+'\n')
                            break
                       
            #DFS
            elif val_al == 2:
                DFS.main(filename,'Source/output-0' + str(val_maze)+ '.txt')
                with open('Source/output-0' + str(val_maze)+ '.txt', "r+") as file:
                    # Đọc nội dung file
                    content = file.read().split('\n')
                    print(content)   
                    num_BFS = 0 
                    path = ''             
                    for i in range(len(content)):
                        if content[i] =='DFS':
                            pos = i
                            num_BFS += 1
                            path = content[i+2]
                        if num_BFS == 2:
                            content_new = content[0:i]
                            file.seek(0)
                            file.truncate()
                            print(content_new)
                            for item in content_new:
                                file.write(item+'\n')
                            break
            elif val_al == 3:
                UCS.solve_ucs(filename, 'Source/output-0' + str(val_maze)+ '.txt')
                with open('Source/output-0' + str(val_maze)+ '.txt', "r+") as file:
                    # Đọc nội dung file
                    content = file.read().split('\n')
                    print(content)   
                    num_BFS = 0 
                    path = ''             
                    for i in range(len(content)):
                        if content[i] =='UCS':
                            pos = i
                            num_BFS += 1
                            path = content[i+2]
                        if num_BFS == 2:
                            content_new = content[0:i]
                            file.seek(0)
                            file.truncate()
                            print(content_new)
                            for item in content_new:
                                file.write(item+'\n')
                            break
                #A*
            elif val_al == 4:
                A_start.solve_as(filename, 'Source/output-0' + str(val_maze)+ '.txt')
                with open('Source/output-0' + str(val_maze)+ '.txt', "r+") as file:
                    # Đọc nội dung file
                    content = file.read().split('\n')
                    print(content)   
                    num_BFS = 0 
                    path = ''             
                    for i in range(len(content)):
                        if content[i] =='A*':
                            pos = i
                            num_BFS += 1
                            path = content[i+2]
                        if num_BFS == 2:
                            content_new = content[0:i]
                            file.seek(0)
                            file.truncate()
                            print(content_new)
                            for item in content_new:
                                file.write(item+'\n')
                            break
            restart = maze.move(display_surface, path)

            
            pygame.display.update()
            time.sleep(2)
        val_maze = 0
        val_home = 1
    
  
    
        
    
    pygame.display.update()
    # Cập nhật màn hình
   

# Thoát Pygame
pygame.quit()
