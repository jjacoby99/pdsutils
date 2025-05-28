from typing import List
def read_position_state(state_text: List) -> List[float]:
    state_values = []
    for line in state_text:
        if not ('<state>' in line or '</state>' in line or line == '\n'):
            state_values.append(float(line))            

    if not len(state_values) == 12:
        raise ValueError(f"Provided state file did not contain 12 items. It may be controlled via ABA.\n{state_text}")

    return state_values[-6:]
