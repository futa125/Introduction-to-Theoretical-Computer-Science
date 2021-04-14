import sys


class DFA:
    def __init__(self):
        self.all_states = set()
        self.all_symbols = set()
        self.final_states = set()
        self.starting_state = None
        self.transition_functions = {}

        self.reachable_states = set()
        self.unreachable_states = set()

        self.nondistinguishable_states_list = []

    def calc_unreachable_states(self):
        self.reachable_states.add(self.starting_state)
        new_states = {self.starting_state}

        while True:
            tmp_set = set()
            for state in new_states:
                for symbol in self.all_symbols:
                    if (state, symbol) in self.transition_functions:
                        tmp_set.add(self.transition_functions[(state, symbol)])
            new_states = tmp_set.difference(self.reachable_states)
            self.reachable_states = self.reachable_states.union(new_states)

            if new_states == set():
                break

        self.unreachable_states = self.all_states.difference(self.reachable_states)

    def calc_nondistinguishable_states_list(self):
        P = [self.final_states, self.all_states.difference(self.final_states)]
        W = [self.final_states]

        while len(W) != 0:
            A = W[0]
            W.remove(A)
            
            for symbol in self.all_symbols:
                X = set()
                for k, v in self.transition_functions.items():
                    if k[1] == symbol and v in A:
                        X.add(k[0])

                for Y in P:
                    if X.intersection(Y) != set() and Y.difference(X) != set():
                        P.remove(Y)
                        P.append(X.intersection(Y))
                        P.append(Y.difference(X))
                        if Y in W:
                            W.remove(Y)
                            W.append(X.intersection(Y))
                            W.append(Y.difference(X))
                        else:
                            if len(X.intersection(Y)) <= len(Y.difference(X)):
                                W.append(X.intersection(Y))
                            else:
                                W.append(Y.difference(X))

        for set_of_states in P:
            if len(set_of_states) >= 2:
                self.nondistinguishable_states_list.append(set_of_states)

    def minimize(self):
        self.calc_unreachable_states()
        self.calc_nondistinguishable_states_list()

        states_to_be_removed = set(self.unreachable_states)
        states_to_be_replaced = {}
        
        for nondistinguishable_states in self.nondistinguishable_states_list:
            states_to_be_replaced[min(nondistinguishable_states)] = nondistinguishable_states.difference({min(nondistinguishable_states)})

        self.all_states = self.all_states.difference(states_to_be_removed)
        self.final_states = self.final_states.difference(states_to_be_removed)
        
        for key, value in list(self.transition_functions.items()):
            if key[0] in states_to_be_removed or value in states_to_be_removed:
                self.transition_functions.pop(key)
            
        for key, value in states_to_be_replaced.items():
            if self.all_states.intersection(value) != set():
                self.all_states = self.all_states.difference(value)
                self.all_states.add(key)
            if self.final_states.intersection(value) != set():
                self.final_states = self.final_states.difference(value)
                self.final_states.add(key)
            if self.starting_state in value:
                self.starting_state = key

            for func_key, func_value in list(self.transition_functions.items()):
                if func_key[0] in value and func_value in value:
                    self.transition_functions.pop(func_key)
                    self.transition_functions[(key, func_key[1])] = key
                elif func_key[0] in value:
                    self.transition_functions[(key, func_key[1])] = self.transition_functions.pop(func_key)
                elif func_value in value:
                    self.transition_functions[func_key] = key

    def read_from_stdin(self):
        self.all_states.update(sys.stdin.readline().rstrip().split(","))
        self.all_symbols.update(sys.stdin.readline().rstrip().split(","))
        self.final_states.update(sys.stdin.readline().rstrip().split(","))
        self.starting_state = sys.stdin.readline().rstrip()

        for line in sys.stdin:
            list_from_line = line.rstrip().split("->")
            self.transition_functions[tuple(list_from_line[0].split(","))] = list_from_line[1]

    def write_to_stdout(self):
        sys.stdout.write(",".join(sorted(list(self.all_states))) + "\n")
        sys.stdout.write(",".join(sorted(list(self.all_symbols))) + "\n")
        sys.stdout.write(",".join(sorted(list(self.final_states))) + "\n")
        sys.stdout.write(self.starting_state + "\n")

        for key, value in sorted(self.transition_functions.items()):
            sys.stdout.write(",".join(list(key)) + "->" + value + "\n")

def main():
    dfa = DFA()
    dfa.read_from_stdin()
    dfa.minimize()
    dfa.write_to_stdout()


if __name__ == "__main__":
    main()
