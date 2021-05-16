import sys
from collections import deque


class PDA:
    def __init__(self):
        line = sys.stdin.readline().strip()
        self.input_strings = [input_string.split(",") for input_string in line.split("|")]

        line = sys.stdin.readline().strip()
        self.states = set(line.split(","))

        line = sys.stdin.readline().strip()
        self.input_alphabet = set(line.split(","))

        line = sys.stdin.readline().strip()
        self.stack_alphabet = set(line.split(","))

        line = sys.stdin.readline().strip()
        self.accepting_states = set(line.split(","))

        line = sys.stdin.readline().strip()
        self.start_state = line
    
        line = sys.stdin.readline().strip()
        self.start_stack_symbol = line

        self.transition_functions = {}

        while True:
            line = sys.stdin.readline().strip()

            if not line:
                break

            line = line.split("->")
            key = tuple(line[0].split(","))
            value = tuple(line[1].split(","))
            self.transition_functions[key] = value

    def __process_input_string(self, input_string):
        self.pda_stack = deque()
        self.pda_stack.append(self.start_stack_symbol)
        
        curr_state = self.start_state
        pda_output = "{}#{}".format(curr_state, ''.join(self.pda_stack)[::-1])
        i = 0


        while i < len(input_string):

            if len(self.pda_stack) > 0:
                stack_top = self.pda_stack.pop()
            else:
                pda_output += "|fail|0\n".format(curr_state)

                return pda_output
            

            transition_key = (curr_state, "$", stack_top)

            if transition_key in self.transition_functions:
                curr_state = self.transition_functions[transition_key][0]

                if self.transition_functions[transition_key][1] != "$":
                    self.pda_stack.extend(list(self.transition_functions[transition_key][1])[::-1])

                if len(self.pda_stack) > 0:
                    stack_contents = "".join(self.pda_stack)[::-1]
                else:
                    stack_contents = "$"
                pda_output += "|{}#{}".format(curr_state, stack_contents)

                continue

            
            transition_key = (curr_state, input_string[i], stack_top)

            if transition_key in self.transition_functions:
                curr_state = self.transition_functions[transition_key][0]

                if self.transition_functions[transition_key][1] != "$":
                    self.pda_stack.extend(list(self.transition_functions[transition_key][1])[::-1])

                if len(self.pda_stack) > 0:
                    stack_contents = "".join(self.pda_stack)[::-1]
                else:
                    stack_contents = "$"
                
                pda_output += "|{}#{}".format(curr_state, stack_contents)
               
                i += 1

                continue


            if i < len(input_string):
                pda_output += "|fail|0\n"

                return pda_output


        while True:
            
            if curr_state in self.accepting_states:
                pda_output += "|1\n"

                return pda_output

            if len(self.pda_stack) > 0:
                stack_top = self.pda_stack.pop()

            else:
                pda_output += "|fail|0\n".format(curr_state)

                return pda_output
            
            
            transition_key = (curr_state, "$", stack_top)

            if transition_key in self.transition_functions:
                curr_state = self.transition_functions[transition_key][0]

                if self.transition_functions[transition_key][1] != "$":
                    self.pda_stack.extend(list(self.transition_functions[transition_key][1])[::-1])

                if len(self.pda_stack) > 0:
                    stack_contents = "".join(self.pda_stack)[::-1]
                else:
                    stack_contents = "$"
                pda_output += "|{}#{}".format(curr_state, stack_contents)

            else:
                pda_output += "|0\n"

                return pda_output


    def run_simulation(self):

        for input_string in self.input_strings:
            sys.stdout.write(self.__process_input_string(input_string))


def main():
    pda = PDA()
    pda.run_simulation()


if __name__ == "__main__":
    main()
