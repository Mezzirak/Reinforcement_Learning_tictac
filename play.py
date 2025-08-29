# RL_tictac_game/play.py

from RL_tictac_game.environment import TicTacToe
from RL_tictac_game.agent import QLearningAgent

def play_game(q_table_filename="q_table.pkl"):
    env = TicTacToe()
    agent = QLearningAgent()
    
    try:
        agent.load_q_table(q_table_filename)
    except FileNotFoundError:
        print(f"Error: Could not find Q-table file '{q_table_filename}'.")
        print("Please run train.py to train the agent and create the file.")
        return

    print("Let's play Tic-Tac-Toe! You are 'O'.")
    
    state = env.reset()
    done = False
    
    # Agent is player 1 ('X'), Human is player -1 ('O')
    agent_player = 1
    human_player = -1

    while not done:
        # Agent's turn
        valid_actions = env.get_valid_actions()
        # Use the greedy action method for playing (no exploration)
        action = agent.get_greedy_action(state, valid_actions)
        state, reward, done = env.step(action, agent_player)
        print("Agent (X) plays:")
        env.render()

        if done:
            if env.winner == agent_player:
                print("Agent wins!")
            elif env.winner is None:
                print("It's a draw!")
            break

        # Human's turn
        human_action = None
        while human_action is None:
            try:
                move = int(input(f"Enter your move {env.get_valid_actions()}: "))
                if move in env.get_valid_actions():
                    human_action = move
                else:
                    print("Invalid move. That spot is already taken or out of bounds.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 8.")
        
        state, reward, done = env.step(human_action, human_player)
        env.render()

        if done:
            if env.winner == human_player:
                print("Congratulations, you win!")
            elif env.winner is None:
                print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()