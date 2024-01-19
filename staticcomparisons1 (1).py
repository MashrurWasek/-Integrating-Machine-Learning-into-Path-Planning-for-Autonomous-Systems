# -*- coding: utf-8 -*-
"""StaticComparisons1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rBaNHB4n-f_FSHwpzwAeMcnUkTZuZlDv
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import random
import heapq


def heuristics(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristics(start, goal)}

    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        close_set.add(current)

        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristics(current, neighbor)

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [
                i[1] for i in oheap
            ]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristics(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return False


def monte_carlo_pathfinding(grid, start, goal, num_paths=1000):
    best_path = None
    best_score = float("inf")

    for _ in range(num_paths):
        path = generate_random_path(grid, start, goal)
        score = evaluate_path(grid, path)

        if score < best_score:
            best_path = path
            best_score = score

    return best_path


class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.05, discount_factor=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.q_table = np.zeros((state_size, action_size))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.action_size = action_size

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            chosen_action = random.randint(0, self.action_size - 1)
            print(f"\t\tRandom action chosen: {chosen_action}")
            return chosen_action
        best_action = np.argmax(self.q_table[state])
        print(f"\t\tBest action chosen: {best_action}")
        return best_action

    def learn(self, state, action, reward, next_state):
        predict = self.q_table[state, action]
        target = reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state, action] += self.lr * (target - predict)

    def update_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)



def take_action(grid, state_index, action, goal):
    grid_shape = grid.shape
    state = (state_index // grid_shape[1], state_index % grid_shape[1])

    action_effects = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    new_state = (state[0] + action_effects[action][0], state[1] + action_effects[action][1])

    if 0 <= new_state[0] < grid_shape[0] and 0 <= new_state[1] < grid_shape[1]:
        if grid[new_state] == 0:  # Valid move
            new_state_index = new_state[0] * grid_shape[1] + new_state[1]
            done = new_state == goal
            reward = 100 if done else -1
        else:  # Obstacle encountered
            print(f"\t\tObstacle encountered at {new_state}")
            new_state_index = state_index
            reward = -10
            done = False
    else:  # Out of bounds
        print(f"\t\tOut of bounds move attempted to {new_state}")
        new_state_index = state_index
        reward = -15
        done = False

    return new_state_index, reward, done


def run_q_learning(grid, start, goal, max_steps_per_episode=50):
    state_size = grid.size
    action_size = 4  # Up, Down, Left, Right
    agent = QLearningAgent(state_size, action_size)
    episodes = 500  # Number of episodes for training

    for _ in range(episodes):
        state = start[0] * grid.shape[1] + start[1]
        for step in range(max_steps_per_episode):
            action = agent.choose_action(state)
            next_state, reward, done = take_action(grid, state, action, goal)
            agent.learn(state, action, reward, next_state)
            state = next_state
            if done:
                break  # Exit loop if goal is reached
        agent.update_epsilon()  # Update epsilon after each episode

    # Find the path using the learned Q-table
    state = start[0] * grid.shape[1] + start[1]
    path = []
    while state != goal[0] * grid.shape[1] + goal[1]:
        action = np.argmax(agent.q_table[state])
        path.append(state)
        state, _, done = take_action(grid, state, action, goal)
        if done or len(path) > max_steps_per_episode:
            break  # Exit loop if goal is reached or max steps exceeded

    return path  # Ensure that a list is always returned




def generate_random_path(grid, start, goal):
    path = [start]
    current = start

    while current != goal:
        possible_moves = get_possible_moves(grid, current)
        if not possible_moves:
            break
        current = random.choice(possible_moves)
        path.append(current)

    return path


def evaluate_path(grid, path):
    score = 0
    for point in path:
        if grid[point[0]][point[1]] == 1:  # Hitting an obstacle
            score += 10
        else:
            score += 1  # A step taken
    return score


def get_possible_moves(grid, position):
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    possible_moves = []

    for i, j in moves:
        neighbor = position[0] + i, position[1] + j
        if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
            possible_moves.append(neighbor)

    return possible_moves


# Parameters
num_episodes = 100
grid_size = 10
start, goal = (0, 0), (grid_size - 1, grid_size - 1)

# Data collection lists
astar_path_lengths = []
astar_times = []
astar_scores = []

monte_carlo_path_lengths = []
monte_carlo_times = []
monte_carlo_scores = []


# Data collection lists for Q-learning
q_learning_path_lengths = []
q_learning_times = []
q_learning_scores = []

# Generate shared grid configurations
grids = []
for _ in range(num_episodes):
    num_obstacles = random.randint(1, 10)  # Random number of obstacles
    grid = np.zeros((grid_size, grid_size), dtype=int)
    for _ in range(num_obstacles):
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        if (x, y) != start and (x, y) != goal:
            grid[x][y] = 1
    grids.append(grid)

# Running both algorithms on each grid
for grid in grids:
    # A* Pathfinding
    start_time = time.time()
    astar_route = astar(grid, start, goal)
    astar_time = time.time() - start_time
    astar_path_length = len(astar_route) if astar_route else 0
    astar_score = max(0, 100 - astar_path_length - np.count_nonzero(grid))

    astar_path_lengths.append(astar_path_length)
    astar_times.append(astar_time)
    astar_scores.append(astar_score)

    # Monte Carlo Pathfinding
    start_time = time.time()
    monte_carlo_route = monte_carlo_pathfinding(grid, start, goal, num_paths=1000)
    monte_carlo_time = time.time() - start_time
    monte_carlo_path_length = len(monte_carlo_route) if monte_carlo_route else 0
    monte_carlo_score = max(0, 100 - monte_carlo_path_length - np.count_nonzero(grid))

    monte_carlo_path_lengths.append(monte_carlo_path_length)
    monte_carlo_times.append(monte_carlo_time)
    monte_carlo_scores.append(monte_carlo_score)

for grid in grids:
    start_time = time.time()
    q_learning_route = run_q_learning(grid, start, goal)
    q_learning_time = time.time() - start_time
    q_learning_path_length = len(q_learning_route)
    q_learning_score = max(0, 100 - q_learning_path_length - np.count_nonzero(grid))

    q_learning_path_lengths.append(q_learning_path_length)
    q_learning_times.append(q_learning_time)
    q_learning_scores.append(q_learning_score)

# Plotting the results
plt.figure(figsize=(15, 7))

# Path Lengths Comparison
plt.subplot(1, 3, 1)
plt.plot(astar_path_lengths, label="A* Path Length", color="blue")
plt.plot(monte_carlo_path_lengths, label="Monte Carlo Path Length", color="green")
plt.plot(q_learning_path_lengths, label="Q-Learning Path Length", color="red")
plt.xlabel("Episode")
plt.ylabel("Path Length")
plt.title("Path Lengths Comparison")
plt.legend()


# Computation Times Comparison
plt.subplot(1, 3, 2)
plt.plot(astar_times, label="A* Computation Time", color="blue")
plt.plot(monte_carlo_times, label="Monte Carlo Computation Time", color="green")
plt.plot(q_learning_times, label="Q-Learning Computation Time", color="red")
plt.xlabel("Episode")
plt.ylabel("Time (seconds)")
plt.title("Computation Times Comparison")
plt.legend()

# Scores Comparison
plt.subplot(1, 3, 3)
plt.plot(astar_scores, label="A* Score", color="blue")
plt.plot(monte_carlo_scores, label="Monte Carlo Score", color="green")
plt.plot(q_learning_scores, label="Q-Learning Score", color="red")
plt.xlabel("Episode")
plt.ylabel("Score")
plt.title("Scores Comparison")
plt.legend()

plt.tight_layout()
plt.show()
