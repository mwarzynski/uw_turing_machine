#!/usr/bin/python3
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
class Position:
    state: State
    letter: Letter

@dataclass
class Move:
    letter_to_write: Letter
    direction: Direction
    state_target: State


class MachineDefinition:

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

    def evaluate_moves(self, pos: Position) -> [Move]:
        try:
            return self._definition[pos.state][pos.letter]
        except KeyError:
            return None


class MachineState:

    def __init__(self, tape: [str], head: int, state: State):
        self._tape = tape
        self._head = head
        self._state = state

    def __hash__(self):
        return hash(("".join(self._tape), self._state, self._head))

    def copy(self):
        return MachineState(self._tape.copy(), self._head, self._state)

    def state(self) -> State:
        return self._state

    def position(self) -> Position:
        if self._head >= len(self._tape):
            return Position(self._state, BLANK)
        return Position(self._state, self._tape[self._head])

    def do_move(self, move: Move):
        # Update state to destination.
        self._state = move.state_target

        # Update letter in the Tape.
        if self._head >= len(self._tape):
            self._tape = self._tape + [BLANK]
        self._tape[self._head] = move.letter_to_write

        # Update head position.
        if move.direction == DIRECTION_LEFT:
            if self._head > 0:
                self._head -= 1
        elif move.direction == DIRECTION_RIGHT:
            self._head += 1
            if self._head >= len(self._tape):
                self._tape = self._tape + [BLANK]
        else: # move.direction == DIRECTION_STAY:
            pass


class Machine:

    _states_visited: set()

    def __init__(self, definition: MachineDefinition):
        self._definition = definition
        self._states_visited = set()

    def run(self, steps: int, tape_str: str) -> str:
        tape = list(tape_str)
        machines = [MachineState(tape, 0, STATE_INIT)]
        step_i = 0
        while step_i < steps:
            new_machines = []
            for machine in machines:
                pos = machine.position()
                moves = self._definition.evaluate_moves(pos)
                if moves is None or len(moves) == 0:
                    continue
                for move in moves:
                    new_machine = machine.copy()
                    new_machine.do_move(move)
                    if hash(new_machine) in self._states_visited:
                        continue
                    self._states_visited.add(hash(new_machine))
                    new_machines.append(new_machine)
            accepts = len([m for m in new_machines if m.state() == STATE_ACCEPT])
            rejects = len([m for m in new_machines if m.state() == STATE_REJECT])
            if accepts != 0 or rejects != 0:
                break
            machines = new_machines
            step_i += 1
            if len(machines) == 0:
                break
        if accepts > 0 and rejects == 0:
            return "YES"
        return "NO"


def parse_transitions(filepath: str) -> [Transition]:
    transitions: [Transition] = []
    try:
        with open(filepath, "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                if len(line.replace(" ", "")) == 0:
                    continue
                if len(line) >= 2 and line[:2] == "//":
                    continue
                transitions.append(Transition(*line.split(" ")))
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    return transitions


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Example: ./interpreter.py <path_to_turing_machine> <steps>")
        sys.exit(0)

    transitions = parse_transitions(sys.argv[1])
    definition = MachineDefinition(transitions)
    steps = int(sys.argv[2])
    tape = input("")

    machine = Machine(definition)
    result = machine.run(steps, tape)
    print(result)
