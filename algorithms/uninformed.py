from .helpers import get_neighbors, is_solvable
from collections import deque
import heapq
import random

def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set([start])
    expansions = 0
    while queue:
        current_state, path = queue.popleft()
        expansions += 1
        if current_state == goal:
            return path, expansions
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                queue
    return None, expansions

def dfs(start, goal, depth_limit=50):
    def dfs_recursive(state, path, visited, depth, expansions):
        if depth > depth_limit:
            return None, expansions
        expansions += 1

        if state == goal:
            return path, expansions
        if state in visited:
            return None, expansions

        visited.add(state)
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                result, expansions = dfs_recursive(neighbor, path + [neighbor], visited, depth + 1, expansions)
                if result:
                    return result, expansions
        return None, expansions
    
    return dfs_recursive(start, [start], set(), 0, 0)

def ucs(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, [start]))  # (cost, state, path)
    visited = set()
    expansions = 0
    while pq:
        cost, current_state, path = heapq.heappop(pq)
        expansions += 1
        if current_state == goal:
            return path, expansions
        if current_state in visited:
            continue
        visited.add(current_state)
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + 1, neighbor, path + [neighbor]))
    return None, expansions

def iddfs(start, goal, max_depth=50):
    expansions = [0]
    def dls(current, limit, path, visited):
        expansions[0] += 1
        if current == goal:
            return path
        if limit == 0:
            return None
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dls(neighbor, limit - 1, path + [neighbor], visited)
                if result is not None:
                    return result
                visited.remove(neighbor)
        return None
    if start == goal:
        return [start], 0
    for depth in range(max_depth + 1):
        visited = set([start])
        result = dls(start, depth, [start], visited)
        if result is not None:
            return result, expansions[0]
    return [], expansions[0]

def backtracking_search(start, goal, max_depth = 50):
    expansions = [0]
    visited = set()
    def is_complete(state):
        return state == goal

    def is_consistent(state, path):
        return state not in path

    def recursive_backtracking(assignment, depth):
        expansions[0] += 1
        current = assignment[-1]
        if depth > max_depth:
            return None
        
        if is_complete(assignment[-1]):
            return assignment

        for neighbor in get_neighbors(assignment[-1]):
            if is_consistent(neighbor, assignment):
                visited.add(neighbor)
                assignment.append(neighbor)

                result = recursive_backtracking(assignment, depth + 1)
                if result:
                    return result
                
                assignment.pop()
                visited.remove(neighbor)
        return None
    
    visited.add(start)
    result = recursive_backtracking([start], 0)
    return (result, expansions[0])
