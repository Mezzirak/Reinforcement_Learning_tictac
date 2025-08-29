# RL_tictac_game/agent.py

import numpy as np
import random
import pickle

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.Q = {}  # Q-table
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def _ensure_state_in_q_table(self, state):
        """Ensure the state exists in the Q-table, initializing if necessary."""
        if state not in self.Q:
            self.Q[state] = np.zeros(9)

    def get_action(self, state, valid_actions):
        """Choose action using epsilon-greedy policy for training."""
        self._ensure_state_in_q_table(state)
        
        if not valid_actions:
            raise ValueError("get_action called with no valid actions.")

        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        else:
            return self.get_greedy_action(state, valid_actions)

    def get_greedy_action(self, state, valid_actions):
        """Choose the best action based on learned Q-values (for playing)."""
        self._ensure_state_in_q_table(state)

        if not valid_actions:
            raise ValueError("get_greedy_action called with no valid actions.")
        
        q_values = self.Q[state].copy()
        
        # Mask invalid actions by setting their Q-value to negative infinity
        invalid_actions = [i for i in range(9) if i not in valid_actions]
        q_values[invalid_actions] = -np.inf
        
        return int(np.argmax(q_values))

    def update(self, state, action, reward, next_state, done):
        """Update Q-table using Q-learning formula."""
        self._ensure_state_in_q_table(state)
        self._ensure_state_in_q_table(next_state)
            
        best_next_q = 0 if done else np.max(self.Q[next_state])
        
        # Q-learning formula
        self.Q[state][action] += self.alpha * (reward + self.gamma * best_next_q - self.Q[state][action])

    def decay_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save_q_table(self, filename):
        """
        Save the Q-table to a file using pickle.
        Note: Pickle is not secure against erroneous or maliciously constructed data.
        Only unpickle data you trust.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.Q, f)
        print(f"Q-table saved to {filename}")

    def load_q_table(self, filename):
        """Load the Q-table from a file."""
        with open(filename, 'rb') as f:
            self.Q = pickle.load(f)
        print(f"Q-table loaded from {filename}")