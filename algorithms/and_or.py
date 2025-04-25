from .helpers import get_neighbors

def and_or_search(start, goal, max_depth=50):
    expansions = 0

    def goal_test(state):
        return state == goal

    def results(state, action):
        return [action]

    def or_search(state, path, depth):
        nonlocal expansions
        if goal_test(state):
            return [state]
        if state in path or depth > max_depth:
            return None
        expansions += 1
        for neighbor in get_neighbors(state):
            if neighbor not in path:
                plan = and_search(results(state, neighbor), path + [state], depth + 1)
                if plan:
                    return [state] + plan
        return None

    def and_search(states, path, depth):
        full_plan = []
        for s in states:
            plan = or_search(s, path, depth)
            if plan is None:
                return None
            full_plan.extend(plan[1:] if full_plan else plan)
        return full_plan

    plan = or_search(start, [], 0)
    return (plan, expansions) if plan else (None, expansions)