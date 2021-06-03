import sys


LL_GRAMMAR = {
    ("S", "a"): ("A", "B"),
    ("S", "b"): ("B", "A"),
    ("A", "b"): ("C"),
    ("A", "a"): (""),
    ("B", "c"): ("c", "S", "b", "c"),
    ("B", ""): (""),
    ("C", ""): ("A", "A")
}


class LLParser:
    def __init__(self):
        self.input_string = []

        self.processed_non_terminal_symbols = []

        self.start_non_terminal_symbol = "S"

        self.curr_string = [self.start_non_terminal_symbol]

        self.string_conforms = None

        self.grammar = LL_GRAMMAR


    def _write_processed_non_terminal_symbols_to_stdout(self):
        output_line = "{}\n".format("".join(self.processed_non_terminal_symbols))
        
        sys.stdout.write(output_line)

        if self.string_conforms:
            sys.stdout.write("DA\n")

        else:
            sys.stdout.write("NE\n")


    def _check_string_conforms(self):
        if self.curr_string == self.input_string:
            self.string_conforms = True

        else:
            self.string_conforms = False


    def _process_rule_without_terminal_symbol(self, curr_position):
        self.processed_non_terminal_symbols.append(self.curr_string[curr_position])

        curr_symbol = self.curr_string[curr_position]

        self.curr_string[curr_position] = ""

        rule_output = list(self.grammar[(curr_symbol, "")])

        self.curr_string = self.curr_string[:curr_position + 1] + rule_output + self.curr_string[curr_position + 1:]

        self.curr_string.remove("")


    def _process_rule_with_terminal_symbol(self, curr_position):
        self.processed_non_terminal_symbols.append(self.curr_string[curr_position])

        curr_symbol = self.curr_string[curr_position]
    
        self.curr_string[curr_position] = self.input_string[curr_position]

        rule_output = list(self.grammar[(curr_symbol, self.input_string[curr_position])])

        self.curr_string = self.curr_string[:curr_position + 1] + rule_output + self.curr_string[curr_position + 1:]


    def _process_after_end_of_string(self, curr_position):
        if (self.curr_string[curr_position], "") in self.grammar:
            self._process_rule_without_terminal_symbol(curr_position)

            return True

        self.processed_non_terminal_symbols.append(self.curr_string[curr_position])
            
        return False


    def _process_before_end_of_string(self, curr_position):
        if (self.curr_string[curr_position], self.input_string[curr_position]) in self.grammar:
            self._process_rule_with_terminal_symbol(curr_position)

            return True

        if (self.curr_string[curr_position], "") in self.grammar:
            self._process_rule_without_terminal_symbol(curr_position)

            return True

        
        self.processed_non_terminal_symbols.append(self.curr_string[curr_position])
            
        return False


    def _check_early_fail(self):
        terminal_symbol_count = 0

        for symbol in self.curr_string:
            if symbol.islower():
                terminal_symbol_count += 1
            else:
                break

        if self.curr_string[:terminal_symbol_count] != self.input_string[:terminal_symbol_count]:
            return False
        
        return True


    def _read_input_string_from_stdin(self):
        input_line = sys.stdin.readline().strip()

        self.input_string = list(input_line)


    def simulate(self):
        self._read_input_string_from_stdin()

        curr_position = 0

        while curr_position < len(self.curr_string):

            if not self._check_early_fail():
                break
  
            if self.curr_string[curr_position].isupper() and curr_position < len(self.input_string):
                processed_successfully = self._process_before_end_of_string(curr_position)
                
                if processed_successfully:
                    curr_position = 0
                    continue

                else:
                    break

            if self.curr_string[curr_position].isupper() and curr_position >= len(self.input_string):
                processed_successfully = self._process_after_end_of_string(curr_position)
                
                if processed_successfully:
                    curr_position = 0
                    continue

                else:
                    break

            curr_position += 1

        self._check_string_conforms()

        self._write_processed_non_terminal_symbols_to_stdout()


def main():
    ll_parser = LLParser()
    ll_parser.simulate()
    return


if __name__ == "__main__":
    main()
