import numpy as np
import matplotlib.pyplot as plt
from RL_tictac_game.environment import TicTacToe
from RL_tictac_game.agent import QLearningAgent
import random
import os

def get_smarter_opponent_action(env, agent_player, opponent_player):
    """
    An even smarter opponent:
    1: If it can win in the next move, it takes the winning move
    2: If the agent can win in the next move, it blocks the agent
    3: It checks for and takes any move that creates a fork (a situation with two potential winning moves)
    4: Otherwise, it makes a random move
    """
    valid_actions = env.get_valid_actions()
    temp_env = TicTacToe()

    # 1: Check for a winning move for the opponent
    for action in valid_actions:
        temp_env.board = env.board.copy()
        temp_env.done = False  # Reset the done flag for the simulation
        _, _, done = temp_env.step(action, opponent_player)
        if done and temp_env.winner == opponent_player:
            return action

    # 2: Check to block the agent's winning move
    for action in valid_actions:
        temp_env.board = env.board.copy()
        temp_env.done = False  # Reset the done flag for the simulation
        _, _, done = temp_env.step(action, agent_player)
        if done and temp_env.winner == agent_player:
            return action

    # 3: Check for a move that creates a fork
    for action in valid_actions:
        temp_env.board = env.board.copy()
        temp_env.done = False  # Reset the done flag for the simulation
        temp_env.step(action, opponent_player)
        if not temp_env.done:
            winning_moves_count = 0
            # Check for winning moves in the next turn
            for future_action in temp_env.get_valid_actions():
                future_temp_env = TicTacToe()
                future_temp_env.board = temp_env.board.copy()
                _, _, future_done = future_temp_env.step(future_action, opponent_player)
                if future_done and future_temp_env.winner == opponent_player:
                    winning_moves_count += 1
            if winning_moves_count >= 2:
                return action

    # 4: Otherwise, choose a random move
    return random.choice(valid_actions)


def train(episodes=200000, q_table_filename="q_table.pkl"):
    env = TicTacToe()
    agent = QLearningAgent()
    rewards = []

    print("Starting training against a smarter opponent")

    for ep in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        agent_player = 1
        opponent_player = -1

        # Randomly let the opponent start 50% of the time
        if random.random() < 0.5:
            opponent_actions = env.get_valid_actions()
            if opponent_actions:
                opponent_action = get_smarter_opponent_action(env, agent_player, opponent_player)
                state, _, done = env.step(opponent_action, opponent_player)

        while not done:
            # Check for valid actions before agent's turn
            valid_actions = env.get_valid_actions()
            if not valid_actions:
                break
                
            action = agent.get_action(state, valid_actions)

            next_state, reward, done = env.step(action, agent_player)

            final_reward_for_agent = reward

            if not done:
                opponent_actions = env.get_valid_actions()
                if opponent_actions:
                    opponent_action = get_smarter_opponent_action(env, agent_player, opponent_player)
                    next_state, opponent_reward, done = env.step(opponent_action, opponent_player)

                    if done and opponent_reward == 1:
                        final_reward_for_agent = -1

            agent.update(state, action, final_reward_for_agent, next_state, done)
            state = next_state
            total_reward += final_reward_for_agent

        agent.decay_epsilon()
        rewards.append(total_reward)

        if (ep + 1) % 1000 == 0:
            avg_reward = np.mean(rewards[-1000:])
            print(f"Episode {ep + 1}/{episodes}, Avg Reward: {avg_reward:.3f}, Epsilon: {agent.epsilon:.3f}")

    print("Training finished")
    agent.save_q_table(q_table_filename)

    # Create the images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Generate and save the plot
    moving_avg_rewards = [np.mean(rewards[i-100:i]) for i in range(100, len(rewards))]
    plt.figure(figsize=(10, 6))
    plt.plot(moving_avg_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Moving Average Reward (100 episodes)")
    plt.title("Training Progress")
    plt.savefig('images/training_progress.png')
    plt.close()


if __name__ == "__main__":
    train()