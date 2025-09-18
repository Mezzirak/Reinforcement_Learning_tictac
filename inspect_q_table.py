# inspect_q_table.py

import pickle

def inspect_q_table(filename="q_table.pkl"):
    try:
        with open(filename, 'rb') as f:
            q_table = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return

    print(f"--- Q-Table Inspection ---")
    print(f"File: '{filename}'")
    
    num_states = len(q_table)
    print(f"Total number of states learned: {num_states}")

    if num_states == 0:
        print("The Q-table is EMPTY. The agent has not learned anything.")
        return

    # Print a few sample states and their Q-values
    print("\n--- Sample States ---")
    count = 0
    for state, values in q_table.items():
        # Check if there are any non-zero values for this state
        if any(v != 0 for v in values):
            print(f"State: {state}")
            # Format values to 3 decimal places for readability
            formatted_values = [f"{v:.3f}" for v in values]
            print(f"  Q-Values: {formatted_values}\n")
            count += 1
        if count >= 5: # Print up to 5 non-zero samples
            break
            
    if count == 0:
        print("The Q-table contains states, but ALL Q-values are still ZERO.")
        print("This means the update logic is failing.")

if __name__ == "__main__":
    inspect_q_table()