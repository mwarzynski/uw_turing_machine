#!/usr/bin/python
import sys
from enum import Enum
from dataclasses import dataclass
from typing import NewType


Letter = NewType('Letter', str)
State = NewType('State', str)
Direction = NewType('Direction', str)

BLANK: Letter = "0"
STATE_INIT: State = "start"
STATE_ACCEPT: State = "accept"
STATE_REJECT: State = "reject"
DIRECTION_LEFT: Direction = "L"
DIRECTION_RIGHT: Direction = "R"
DIRECTION_STAY: Direction = "S"


@dataclass
class Transition:
    state_current: State
    letter_current: Letter
    state_target: State
    letter_to_write: Letter
    direction: Direction

@dataclass
class Move:
    letter_to_write: Letter
    direction: Direction
    state_target: State


class TransitionAlreadyExists(Exception):
    pass

class TransitionAlreadyExists(Exception):
    pass


class Definition:
    
    def __init__(self, transitions: [Transition]):
        self._parse_transitions(transitions)

    def _parse_transitions(self, transitions: [Transition]):
        self._definition: {State: {Letter: [(Letter, Direction, State)]}} = {}
        for t in transitions:
            if t.state_current not in self._definition:
                self._definition[t.state_current] = {}
            if t.letter_current not in self._definition[t.state_current]:
                self._definition[t.state_current][t.letter_current] = []
            self._definition[t.state_current][t.letter_current].append(Move(t.letter_to_write, t.direction, t.state_target))

    def evaluate_move(self, state: State, letter_current: Letter) -> Move:
        try:
            return self._definition[state][letter_current]
        except KeyError:
            return None


class Machine:

    def __init__(self, definition: Definition):
        self._definition = definition

    def run(self, steps: int, tape_str: str) -> str:
        tape = list(tape_str)
        head = 0
        state = STATE_INIT
        step_i = 0

        while step_i < steps:
            letter = BLANK
            if len(tape) > head:
                letter = tape[head]

            moves = self._definition.evaluate_move(state, letter)
            if moves is None or len(moves) == 0:
                state = STATE_REJECT
                break
            move = moves[0]
            
            state = move.state_target

            if head >= len(tape):
                tape = tape + [" "]
            
            tape[head] = move.letter_to_write
            
            if move.direction == DIRECTION_LEFT:
                if head > 0:
                    head -= 1
            elif move.direction == DIRECTION_RIGHT:
                head += 1
            else: # move.direction == DIRECTION_STAY:
                pass

            if state in [STATE_REJECT, STATE_ACCEPT]:
                break

            step_i += 1

        if state == STATE_ACCEPT:
            return "YES"
        return "NO"


def parse_transitions(filepath: str) -> [Transition]:
    transitions: [Transition] = []
    try:
        with open(filepath, "r") as f:
            for line in f.readlines():
                transitions.append(Transition(*line.replace("\n", "").split(" ")))
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    return transitions
 

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Example: ./interpreter.py <path_to_turing_machine> <steps>")
        sys.exit(0)

    transitions = parse_transitions(sys.argv[1])
    definition = Definition(transitions)
    steps = int(sys.argv[2])
    tape = input("")

    machine = Machine(definition)
    result = machine.run(steps, tape)
    print(result)
