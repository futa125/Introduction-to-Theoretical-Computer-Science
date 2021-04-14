import sys


class EpsillonNFA:
    def __init__(self):
        self.input_strings = []
        self.states = []
        self.alphabet = []
        self.accepting_states = []
        self.initial_state = None
        self.transition_functions = {}
        self.all_states = []

    def calc_epsillon_states(self, current_states):
        final_states = current_states[:]

        for state in current_states:
            key = (state, "$")
            if key in self.transition_functions:
                value = self.transition_functions[key]
                final_states.extend(value)

        if set(final_states) == set(current_states):
            if all(x == "#" for x in final_states):
                return ["#"]

            elif "#" in final_states:
                return sorted(list(dict.fromkeys([x for x in final_states if x != "#"])))

            else:
                return sorted(list(dict.fromkeys(final_states)))

        else:
            return self.calc_epsillon_states(sorted(list(dict.fromkeys(final_states))))

    def calc_normal_states(self, current_states, symbol):
        final_states = []

        for state in current_states:
            key = (state, symbol)
            if key in self.transition_functions:
                value = self.transition_functions[key]
                final_states.extend(value)

        if all(x == "#" for x in final_states):
            return ["#"]

        elif "#" in final_states:
            return sorted(list(dict.fromkeys([x for x in final_states if x != "#"])))

        else:
            return sorted(list(dict.fromkeys(final_states)))

    def calc_all_states(self):
        for string in self.input_strings:

            str_states = []

            eps_states = self.calc_epsillon_states([self.initial_state])
            str_states.append(eps_states)

            for symbol in string:
                norm_states = self.calc_normal_states(eps_states, symbol)
                eps_states = self.calc_epsillon_states(norm_states)
                str_states.append(eps_states)

            self.all_states.append(str_states)

    def load_stdin(self):
        line = sys.stdin.readline().strip()
        for input_string in line.split("|"):
            self.input_strings.append(input_string.split(","))

        line = sys.stdin.readline().strip()
        self.states.append(line.split(","))

        line = sys.stdin.readline().strip()
        self.alphabet.append(line.split(","))

        line = sys.stdin.readline().strip()
        self.accepting_states.append(line.split(","))

        line = sys.stdin.readline().strip()
        self.initial_state = line

        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            line = line.split("->")
            key = tuple(line[0].split(","))
            value = line[1].split(",")
            self.transition_functions[key] = value

    def save_stdout(self):
        for str_states in self.all_states:
            str_states = "|".join([",".join(x) for x in str_states])
            sys.stdout.write(str_states + "\n")


def main():
    nfa = EpsillonNFA()
    nfa.load_stdin()
    nfa.calc_all_states()
    nfa.save_stdout()


if __name__ == "__main__":
    main()
