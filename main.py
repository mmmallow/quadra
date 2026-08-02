import pygame

SCREEN_WIDTH = 2160
SCREEN_HEIGHT = 1215

TILE_SIZE = 72
TILE_COLOR = (160, 120, 80)
BG_COLOR = (55, 57, 58)
BOARD_COLOR = (168, 157, 149)
BOARD_SIZE = 1080
board_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
board_y = (SCREEN_HEIGHT - BOARD_SIZE) // 2

def draw_board(screen):
    pygame.draw.rect(screen, BOARD_COLOR, (board_x, board_y, BOARD_SIZE, BOARD_SIZE))

    # Draw outline
    pygame.draw.rect(screen, (0,0,0), (board_x, board_y, BOARD_SIZE+3, BOARD_SIZE+3), 3)

    # Draw vertical lines
    for i in range(0, 15):
        vert_x_pos = board_x + i*TILE_SIZE
        hor_y_pos = board_y + i*TILE_SIZE
        # Draw vertical lines
        pygame.draw.line(screen, (0,0,0), (vert_x_pos, board_y), (vert_x_pos, board_y+BOARD_SIZE),2)

        #Draw horizontal lines
        pygame.draw.line(screen, (0,0,0), (board_x, hor_y_pos), (board_x+BOARD_SIZE, hor_y_pos), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Resize Event Handler')

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw content that adapts to window size
        screen.fill(BG_COLOR)
        
        # Draw a rectangle that scales with window size
        draw_board(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
