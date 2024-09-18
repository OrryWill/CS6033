from collections import deque
import time
import heapq

# Road map data
road_map = {
    'arad': [('zerind', 75), ('sibiu', 140), ('timisoara', 118)],
    'zerind': [('arad', 75), ('oradea', 71)],
    'oradea': [('zerind', 71), ('sibiu', 151)],
    'sibiu': [('arad', 140), ('oradea', 151), ('fagaras', 99), ('rimnicu vilcea', 80)],
    'timisoara': [('arad', 118), ('lugoj', 111)],
    'lugoj': [('timisoara', 111), ('mehadia', 70)],
    'mehadia': [('lugoj', 70), ('drobeta', 75)],
    'drobeta': [('mehadia', 75), ('craiova', 120)],
    'craiova': [('drobeta', 75), ('rimnicu vilcea', 146), ('pitesti', 138)],
    'rimnicu vilcea': [('sibiu', 80), ('craiova', 146), ('pitesti', 97)],
    'fagaras': [('sibiu', 99), ('bucharest', 211)],
    'pitesti': [('rimnicu vilcea', 97), ('craiova', 138), ('bucharest', 101)],
    'bucharest': [('fagaras', 211), ('pitesti', 101), ('giurgiu', 90), ('urziceni', 85)],
    'giurgiu': [('bucharest', 90)],
    'urziceni': [('bucharest', 85), ('hirsova', 98), ('vaslui', 142)],
    'hirsova': [('urziceni', 98), ('eforie', 86)],
    'eforie': [('hirsova', 86)],
    'vaslui': [('urziceni', 142), ('iasi', 92)],
    'iasi': [('vaslui', 92), ('neamt', 87)],
    'neamt': [('iasi', 87)]
}

# SLD values
sld = {
    'arad': 366, 'zerind': 374, 'oradea': 380, 'sibiu': 253, 'timisoara': 329,
    'lugoj': 244, 'mehadia': 241, 'drobeta': 242, 'craiova': 160, 'rimnicu vilcea': 193,
    'fagaras': 178, 'pitesti': 98, 'bucharest': 0, 'giurgiu': 77, 'urziceni': 80,
    'hirsova': 151, 'eforie': 161, 'vaslui': 199, 'iasi': 226, 'neamt': 234
}

# BFS Algorithm
def bfs(road_map, start, goal):
    if start not in road_map or goal not in road_map:
        return None, 0, 0

    queue = deque([(start, [start], 0)]) 
    visited = set()
    cities_visited = 0

    while queue:
        city, path, cost = queue.popleft()
        
        if city in visited:
            continue

        cities_visited += 1
        visited.add(city)

        if city == goal:
            return path, cost, cities_visited  

        for neighbor, distance in road_map[city]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], cost + distance))

    return None, 0, cities_visited

# Greedy Algorithm
def greedy(road_map, start, goal, sld):
    return None

# DFS Algorithm
def dfs(graph, start, goal):
   return None

def a_star(road_map, start, goal, heuristic_func):
    # Priority queue: stores tuples of (f, current_city, path, g)
    priority_queue = [(heuristic_func(start, goal, road_map), start, [start], 0)]
    visited = {}  # Dictionary to keep track of the best cost to reach a node
    cities_visited = 0
    
    while priority_queue:
        f, current_city, path, g = heapq.heappop(priority_queue)
        
        if current_city == goal:
            return path, g, cities_visited  
        
        if current_city in visited and visited[current_city] <= g:
            continue
        
        visited[current_city] = g
        cities_visited += 1
        
        for neighbor, distance in road_map[current_city]:
            new_g = g + distance
            h = heuristic_func(neighbor, goal, road_map)
            f = new_g + h
            if neighbor not in visited or visited[neighbor] > new_g:
                heapq.heappush(priority_queue, (f, neighbor, path + [neighbor], new_g))
    


# Heuristic functions for A* algorithm
def heuristic_with_bucharest(start, goal, road_map):
    return sld.get(start, float('inf'))

def heuristic_with_common_neighbor(start, goal, road_map):
    neighbors_start = {neighbor for neighbor, _ in road_map[start]}
    neighbors_goal = {neighbor for neighbor, _ in road_map[goal]}
    common_neighbors = neighbors_start.intersection(neighbors_goal)
    
    if common_neighbors:
        common_city = next(iter(common_neighbors))
        return sld.get(start, float('inf')) + sld.get(common_city, float('inf'))
    
    if neighbors_start:
        closest_city = next(iter(neighbors_start))
        return sld.get(start, float('inf')) + sld.get(closest_city, float('inf'))
    
    return sld.get(start, float('inf'))




#GRAPHICAL USER INTERFACE FOR TERMINAL

def main_menu():
    while True:
        print("\n")
        print("\033[1;33mWelcome to the Romanian Road Map Search!\033[0m\n")

        start_city = input("\033[1;36mEnter start city (case insensitive): \033[0m").lower()
        destination_city = input("\033[1;36mEnter destination city (case insensitive): \033[0m").lower()

        if start_city not in road_map:
            print(f"\033[1;31mError: {start_city} is not in the road map.\033[0m")
            continue
        elif destination_city not in road_map:
            print(f"\033[1;31mError: {destination_city} is not in the road map.\033[0m")
            continue

        print("\033[1;36m\nSelect an algorithm:\033[0m")
        print("1. BFS")
        print("2. DFS")
        print("3. A*")
        print("4. Greedy")
        print("5. Exit")
        choice = input("\033[1;36mEnter the number of the algorithm you want to use: \033[0m")

        if choice == '1':
            algorithm_name = "BFS"
            algorithm_func = run_bfs
        elif choice == '2':
            algorithm_name = "DFS"
            algorithm_func = run_dfs
        elif choice == '3':
            print("\033[1;36mSelect a heuristic for A*:\033[0m")
            print("1. Heuristic with Bucharest")
            print("2. Heuristic with Common Neighbor")
            heuristic_choice = input("\033[1;36mEnter the number of the heuristic you want to use: \033[0m")

            if heuristic_choice == '1':
                heuristic_func = heuristic_with_bucharest
                heuristic_name = "Heuristic with Bucharest"
            elif heuristic_choice == '2':
                heuristic_func = heuristic_with_common_neighbor
                heuristic_name = "Heuristic with Common Neighbor"
            else:
                print("\033[1;31mInvalid choice. Defaulting to Heuristic with Bucharest.\033[0m")
                heuristic_func = heuristic_with_bucharest
                heuristic_name = "Heuristic with Bucharest"

            algorithm_name = "A*"
            algorithm_func = lambda start, goal: run_a_star(start, goal, heuristic_func)
        
        elif choice == '4':
            algorithm_name = "Greedy"
            algorithm_func = run_greedy
        elif choice == '5':
            print("\033[1;33mExiting...\033[0m")
            break
        else:
            print("\033[1;31mInvalid choice. Please enter a number between 1 and 5.\033[0m")
            continue

        start_time = time.time()
        if algorithm_name == "DFS":
            result, total_cost, cities_visited, all_paths = algorithm_func(start_city, destination_city)
            print(f"\033[1;32mDFS - Shortest path: {result}\033[0m")
            print(f"\033[1;32mDFS - Total cost: {total_cost}\033[0m")
            print(f"\033[1;32mDFS - Number of cities visited: {cities_visited}\033[0m")
        else:
            result, total_cost, cities_visited = algorithm_func(start_city, destination_city)
            print(f"\033[1;32m{algorithm_name} - Shortest path: {result}\033[0m")
            print(f"\033[1;32m{algorithm_name} - Total cost (distance): {total_cost} km\033[0m")
            print(f"\033[1;32m{algorithm_name} - Number of cities visited: {cities_visited}\033[0m")

        end_time = time.time()
        print(f"\033[1;32m{algorithm_name} - Execution time: {end_time - start_time:.6f} seconds\033[0m")


def run_bfs(start, goal):
    return bfs(road_map, start, goal)

def run_dfs(start, goal):
    return dfs(road_map, start, goal)

def run_a_star(start, goal, heuristic_func):
    return a_star(road_map, start, goal, heuristic_func)

def run_greedy(start, goal):
    return greedy(road_map, start, goal, sld)

if __name__ == "__main__":
    main_menu()
