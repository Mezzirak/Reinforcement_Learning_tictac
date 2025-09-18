# train.py (CLAUDE'S SUPERIOR TRAINING SCRIPT)
import numpy as np
import matplotlib.pyplot as plt
import random
from RL_tictac_game.environment import TicTacToe
from RL_tictac_game.agent import QLearningAgent

class RandomAgent:
    def get_action(self, state, valid_actions):
        return random.choice(valid_actions)

class HeuristicAgent:
    def get_action(self, state, valid_actions):
        board = np.array(state).reshape(3, 3)
        for action in valid_actions:
            if self._wins_with_move(board, action, -1): return action # Block opponent
        for action in valid_actions:
            if self._wins_with_move(board, action, 1): return action # Win
        if 4 in valid_actions: return 4
        corners = [a for a in [0, 2, 6, 8] if a in valid_actions]
        if corners: return random.choice(corners)
        return random.choice(valid_actions)
    def _wins_with_move(self, board, action, player):
        r, c = divmod(action, 3); board_copy = board.copy(); board_copy[r,c]=player
        for i in range(3):
            if all(board_copy[i,:]==player) or all(board_copy[:,i]==player): return True
        if board_copy[0,0]==board_copy[1,1]==board_copy[2,2]==player: return True
        if board_copy[0,2]==board_copy[1,1]==board_copy[2,0]==player: return True
        return False

def train_smart_agent(episodes=50000, q_table_filename="q_table.pkl"):
    env = TicTacToe()
    agent = QLearningAgent(alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.9999, min_epsilon=0.05)
    opponents = {'random': RandomAgent(), 'heuristic': HeuristicAgent()}
    phases = [
        {'episodes': int(episodes*0.4), 'opponent': 'random', 'name': 'Random Exploration'},
        {'episodes': int(episodes*0.6), 'opponent': 'heuristic', 'name': 'Strategic Learning'}
    ]
    episode_count = 0
    for phase in phases:
        print(f"\n=== Phase: {phase['name']} ===")
        stats = {'win': 0, 'loss': 0, 'draw': 0}
        for ep in range(phase['episodes']):
            episode_count += 1
            opponent = opponents[phase['opponent']]
            state = env.reset()
            done = False
            while not done:
                player_turn = env.get_current_player()
                if player_turn == 1: # Agent's turn
                    action = agent.get_action(state, env.get_valid_actions())
                    next_state, reward, done = env.step(action, 1)
                    agent.update(state, action, reward if done else 0.0, next_state, done)
                    state = next_state
                else: # Opponent's turn
                    action = opponent.get_action(state, env.get_valid_actions())
                    state, _, done = env.step(action, -1)
            if env.winner == 1: stats['win']+=1
            elif env.winner == -1: stats['loss']+=1
            else: stats['draw']+=1
            agent.decay_epsilon()
            if (ep+1) % 5000 == 0:
                total=sum(stats.values()); print(f"  Ep {ep+1}/{phase['episodes']}: W={stats['win']/total*100:.1f}% L={stats['loss']/total*100:.1f}% D={stats['draw']/total*100:.1f}% (Epsilon: {agent.epsilon:.3f})")
    print(f"\n🎉 Training completed! Q-table contains {len(agent.Q)} states.")
    agent.save_q_table(q_table_filename)

if __name__ == "__main__":
    train_smart_agent()