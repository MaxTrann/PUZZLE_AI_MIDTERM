import random

def q_learning(start_state, goal_state, episodes=10000, alpha=0.1, gamma=0.95, epsilon=0.3, max_steps=5000):
    def get_valid_actions(state):
        zero = state.index(0)
        r, c = divmod(zero, 3)
        actions = []
        if r > 0: actions.append("up")
        if r < 2: actions.append("down")
        if c > 0: actions.append("left")
        if c < 2: actions.append("right")
        return actions

    def take_action(state, action):
        zero = state.index(0)
        r, c = divmod(zero, 3)
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dr, dc = moves[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            idx2 = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[idx2] = new_state[idx2], new_state[zero]
            return tuple(new_state)
        return state

    # Khởi tạo bảng Q
    Q = dict()

    for ep in range(episodes):
        # Bắt đầu một episode
        state = start_state

        for step in range(max_steps):
            #Tác nhân thực hiện hành động
            actions = get_valid_actions(state)
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                q_vals = [Q.get((state, a), 0) for a in actions]
                action = actions[q_vals.index(max(q_vals))]

            # Xác định phần thưởng
            next_state = take_action(state, action)
            reward = 100 if next_state == goal_state else -1

            # Chuyển sang trạng thái mới (done)

            # Q-value được cập nhật
            max_q_next = max([Q.get((next_state, a), 0) for a in get_valid_actions(next_state)], default=0)
            td_target = reward + gamma * max_q_next
            td_error = td_target - Q.get((state, action), 0)
            Q[(state, action)] = Q.get((state, action), 0) + alpha * td_error

            # Episode kết thúc nếu đạt mục tiêu
            if next_state == goal_state:
                break

            # Cập nhật trạng thái
            state = next_state

    # Duyệt theo chính sách tốt nhất từ start → goal để dựng path
    path = [start_state]
    current = start_state
    for _ in range(100):
        if current == goal_state:
            break
        valid_actions = get_valid_actions(current)
        q_vals = [Q.get((current, a), -float("inf")) for a in valid_actions]
        best_action = valid_actions[q_vals.index(max(q_vals))]
        current = take_action(current, best_action)
        path.append(current)

    return path, len(Q)
