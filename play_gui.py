<<<<<<< HEAD
# play_gui.py

import pygame
import sys
from RL_tictac_game.environment import TicTacToe
from RL_tictac_game.agent import QLearningAgent

#Pygame Setup and Constants
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors (RGB)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

# Fonts
FONT = pygame.font.SysFont('Arial', 60, bold=True)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 70, bold=True)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Tic-Tac-Toe")

#Drawing Functions
def draw_lines():
    """Draws the grid lines for the Tic-Tac-Toe board."""
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures(board):
    """Draws the X's and O's on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1: # Player X
                # Draw two crossing lines for 'X'
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + SQUARE_SIZE - 50), 25)
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + SQUARE_SIZE - 50), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + 50), 25)
            elif board[row][col] == -1: # Player O
                # Draw a circle for 'O'
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, O_COLOR, center, SQUARE_SIZE // 2 - 50, 15)

def draw_game_over_text(message):
    """Displays the game over message on the screen."""
    text = GAME_OVER_FONT.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    # Add a semi-transparent background for better visibility
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128)) 
    screen.blit(overlay, (0,0))
    
    screen.blit(text, text_rect)

    # Add a 'Press R to Restart' message
    restart_text = FONT.render("Press R to Restart", True, GRAY)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

#Main Game Loop
def play_game_gui():
    # Load the trained agent
    agent = QLearningAgent()
    try:
        agent.load_q_table("q_table.pkl")
    except FileNotFoundError:
        print("Error: q_table.pkl not found. Please train the agent first.")
        return

    #Initialise game environment
    env = TicTacToe()
    agent_player = 1
    human_player = -1
    running = True

    while running:
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Handle mouse click for human player
            if event.type == pygame.MOUSEBUTTONDOWN and not env.done:
                mouseX = event.pos[0]  # x coordinate
                mouseY = event.pos[1]  # y coordinate

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)
                
                # Convert 2D board position to 1D action
                action = clicked_row * BOARD_COLS + clicked_col
                
                if action in env.get_valid_actions():
                    # Human makes a move
                    env.step(action, human_player)

                    # AI makes a move if the game is not over
                    if not env.done:
                        state = env._get_state()
                        valid_actions = env.get_valid_actions()
                        ai_action = agent.get_greedy_action(state, valid_actions)
                        env.step(ai_action, agent_player)

            # Handle key press for restarting the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and env.done:
                    env.reset()

        #Drawing the screen
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures(env.board)

        #Game Over Condition
        if env.done:
            message = ""
            if env.winner == agent_player:
                message = "AI Wins!"
            elif env.winner == human_player:
                message = "You Win!"
            else:
                message = "It's a Draw!"
            draw_game_over_text(message)

        # Update the display
        pygame.display.update()

if __name__ == "__main__":
    play_game_gui()
=======
# play_gui.py (FINAL CLEAN VERSION)
import pygame, sys
from RL_tictac_game.environment import TicTacToe
from RL_tictac_game.agent import QLearningAgent

pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 3
BG_COLOR=(28,170,156); LINE_COLOR=(23,145,135); X_COLOR=(84,84,84); O_COLOR=(242,235,211)
WHITE=(255,255,255); GRAY=(200,200,200)
FONT = pygame.font.SysFont('Arial', 60, bold=True)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 70, bold=True)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Unbeatable AI Tic-Tac-Toe")

def draw_board(board):
    screen.fill(BG_COLOR)
    pygame.draw.line(screen,LINE_COLOR,(0,SQUARE_SIZE),(WIDTH,SQUARE_SIZE),15)
    pygame.draw.line(screen,LINE_COLOR,(0,2*SQUARE_SIZE),(WIDTH,2*SQUARE_SIZE),15)
    pygame.draw.line(screen,LINE_COLOR,(SQUARE_SIZE,0),(SQUARE_SIZE,HEIGHT),15)
    pygame.draw.line(screen,LINE_COLOR,(2*SQUARE_SIZE,0),(2*SQUARE_SIZE,HEIGHT),15)
    for r in range(3):
        for c in range(3):
            if board[r,c] == 1:
                pygame.draw.line(screen,X_COLOR,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50),(c*SQUARE_SIZE+SQUARE_SIZE-50,r*SQUARE_SIZE+SQUARE_SIZE-50),25)
                pygame.draw.line(screen,X_COLOR,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+SQUARE_SIZE-50),(c*SQUARE_SIZE+SQUARE_SIZE-50,r*SQUARE_SIZE+50),25)
            elif board[r,c] == -1:
                pygame.draw.circle(screen,O_COLOR,(c*SQUARE_SIZE+SQUARE_SIZE//2,r*SQUARE_SIZE+SQUARE_SIZE//2),SQUARE_SIZE//2-50,15)

def draw_game_over(message):
    text=GAME_OVER_FONT.render(message,True,WHITE); rect=text.get_rect(center=(WIDTH//2,HEIGHT//2-50))
    overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); overlay.fill((0,0,0,128))
    screen.blit(overlay,(0,0)); screen.blit(text,rect)
    restart_text=FONT.render("Press R to Restart",True,GRAY); restart_rect=restart_text.get_rect(center=(WIDTH//2,HEIGHT//2+50))
    screen.blit(restart_text,restart_rect)

def main():
    agent = QLearningAgent(); env = TicTacToe()
    try: agent.load_q_table("q_table.pkl")
    except FileNotFoundError: print("q_table.pkl not found."); return
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not env.done:
                action = int(event.pos[1]//SQUARE_SIZE)*3 + int(event.pos[0]//SQUARE_SIZE)
                if action in env.get_valid_actions():
                    env.step(action, -1) # Human
                    if not env.done: env.step(agent.get_greedy_action(env._get_state(), env.get_valid_actions()), 1) # AI
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and env.done: env.reset()
        draw_board(env.board)
        if env.done: draw_game_over("AI Wins!" if env.winner==1 else "You Win!" if env.winner==-1 else "It's a Draw!")
        pygame.display.update()

if __name__ == "__main__":
    main()
>>>>>>> f950839 (small changes)
