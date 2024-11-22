import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from lexemes import lexemes_dict, identifier

class LOLCodeInterpreter:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter | Maiso & Paleracio")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.open_button = tk.Button(button_frame, text="Open File", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Save File", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(button_frame, text="Run", command=self.main_interpreter)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.text_box = tk.Text(main_frame, wrap="word", width=60, height=20)
        self.text_box.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.output_box1 = tk.Text(main_frame, wrap="word", state="disabled", width=30, height=10)
        self.output_box1.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.output_box2 = tk.Text(main_frame, wrap="word", state="disabled", width=30, height=10)
        self.output_box2.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.output_box3 = tk.Text(main_frame, wrap="word", state="disabled", width=60, height=10)
        self.output_box3.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.file_path = None
        self.lines_list = []
        self.lexemes_result = []

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('LOL Files', '*.lol')])
        if self.file_path:
            try:
                with open(self.file_path, "r") as file:
                    content = file.read()
                    lines = content.splitlines()
                    self.lines_list = [x.strip() for x in lines]
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        if self.file_path:
            try:
                content = self.text_box.get(1.0, tk.END)
                lines = content.splitlines()
                self.lines_list = [x.strip() for x in lines]
                with open(self.file_path, "w") as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            messagebox.showwarning("Warning", "No file opened to save.")

    def run_code(self):
        self.output_box1.config(state="normal")
        self.output_box2.config(state="normal")
        self.output_box3.config(state="normal")

        self.output_box1.delete(1.0, tk.END)
        self.output_box2.delete(1.0, tk.END)
        self.output_box3.delete(1.0, tk.END)

        self.output_box1.insert(tk.END, "Output 1")
        self.output_box2.insert(tk.END, "Output 2")
        self.output_box3.insert(tk.END, "Detailed Output or Logs")

        self.output_box1.config(state="disabled")
        self.output_box2.config(state="disabled")
        self.output_box3.config(state="disabled")

    def lexical_analyzer(self, line):
        terms = line.split()
        function_flag = 0
        loop_flag = 0
        while terms != []:
            
            curr_string = terms[0]
            other_terms = terms[1:]
            keyword_flag = 0
            while keyword_flag == 0:
                
                for regex, token_type in lexemes_dict.items():
                    if re.match(regex, curr_string):
                        keyword_flag = 1
                        terms = other_terms
                        print(curr_string, "\t", token_type)
                        self.lexemes_result.append([curr_string, token_type])
                        if token_type == "Function Declaration" or token_type == "Function Call":
                            function_flag = 1
                        elif token_type == "Loop Start":
                            loop_flag = 1
                        break
                if keyword_flag == 1:
                    break

                if other_terms != []:
                    curr_string += " " + other_terms[0]
                    other_terms = other_terms[1:]
                else:
                    curr_string = terms[0]
                    other_terms = terms[1:]
                    if re.match(identifier, curr_string):
                        print(curr_string, "\t", "Identifier")
                        if function_flag == 1:
                            self.lexemes_result.append([curr_string, "Function Identifier"])
                            function_flag = 0
                        elif loop_flag == 1:
                            self.lexemes_result.append([curr_string, "Loop Identifier"])
                            loop_flag = 0
                        else:
                            self.lexemes_result.append([curr_string, "Identifier"])
                        terms = other_terms
                        break

    def syntax_analyzer(self, lexemes):
        def expect(actual, expected_label):
            if actual != expected_label:
                raise SyntaxError(f"Syntax Error: Expected {expected_label}, but got {actual}.")

        def parse_program(lexemes):
            # Grammar: <program> ::= HAI <linebreak> <statement_list> KTHXBYE
            index = 0
            token, token_type = lexemes[index]
            expect(token_type, "Code Delimiter")  # Expect "HAI"
            if token != "HAI":
                raise SyntaxError("Program must start with 'HAI'.")

            index += 1
            token, token_type = lexemes[index]
            expect(token_type, "Linebreak")  # Expect linebreak
            index += 1

            index = parse_statement_list(lexemes, index)  # Parse statement list

            token, token_type = lexemes[index]
            expect(token_type, "Code Delimiter")  # Expect "KTHXBYE"
            if token != "KTHXBYE":
                raise SyntaxError("Program must end with 'KTHXBYE'.")

            index += 1
            return index

        def parse_statement_list(lexemes, index):
            # Grammar: <statement_list> ::= <statement> <linebreak> |
            #                                <statement> <linebreak> <statement_list>
            while index < len(lexemes):
                index = parse_statement(lexemes, index)

                token, token_type = lexemes[index]
                if token_type != "Linebreak":
                    break  # End of statements
                index += 1

            return index

        def parse_statement(lexemes, index):
            # Grammar: <statement> ::= <variable_declaration> | <print> | ... other statements
            token, token_type = lexemes[index]
            if token_type == "Variable Declaration":
                index = parse_variable_declaration(lexemes, index)
            elif token_type == "Output Keyword":
                index = parse_output(lexemes, index)
            elif token_type == "Input Keyword":
                index = parse_input(lexemes, index)
            else:
                raise SyntaxError(f"Unknown statement starting with {token} ({token_type}).")
            return index

        def parse_variable_declaration(lexemes, index):
            # Grammar: <variable_declaration> ::= I HAS A varident | I HAS A varident ITZ <expr>
            token, token_type = lexemes[index]
            expect(token_type, "Variable Declaration")  # Expect "I HAS A"
            index += 1

            token, token_type = lexemes[index]
            expect(token_type, "Identifier")  # Expect variable identifier
            index += 1

            if index < len(lexemes):
                token, token_type = lexemes[index]
                if token == "ITZ":
                    index += 1  # Move past "ITZ"
                    index = parse_expr(lexemes, index)

            return index

        def parse_output(lexemes, index):
            # Grammar: <print> ::= VISIBLE varident | VISIBLE <expr_list> | VISIBLE IT
            token, token_type = lexemes[index]
            expect(token_type, "Output Keyword")  # Expect "VISIBLE"
            index += 1

            token, token_type = lexemes[index]
            if token_type in {"Identifier", "Implicit Variable", "NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"}:
                index += 1  # Valid output
            elif token == "IT":
                index += 1
            else:
                index = parse_expr_list(lexemes, index)

            return index

        def parse_input(lexemes, index):
            # Grammar: <input> ::= GIMMEH varident
            token, token_type = lexemes[index]
            expect(token_type, "Input Keyword")  # Expect "GIMMEH"
            index += 1

            token, token_type = lexemes[index]
            expect(token_type, "Identifier")  # Expect variable identifier
            index += 1

            return index

        def parse_expr(lexemes, index):
            # Grammar: <expr> ::= <literal> | <operation>
            token, token_type = lexemes[index]
            if token_type in {"NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"}:
                index += 1  # Literal
            elif token_type in {"Arithmetic Operator", "Boolean Operator", "Comparison Operator", "Concatenation Operator"}:
                index = parse_operation(lexemes, index)
            else:
                raise SyntaxError(f"Expected expression, found {token} ({token_type}).")
            return index

        def parse_operation(lexemes, index):
            # Grammar: <operation> ::= <addition> | <subtraction> | ...
            token, token_type = lexemes[index]
            expect(token_type, "Arithmetic Operator")  # Example for arithmetic operations
            index += 1
            index = parse_expr_list(lexemes, index)
            return index

        def parse_expr_list(lexemes, index):
            # Grammar: <expr_list> ::= <expr> | <expr> AN <expr_list>
            index = parse_expr(lexemes, index)
            while index < len(lexemes):
                token, token_type = lexemes[index]
                if token != "AN":
                    break
                index += 1  # Skip "AN"
                index = parse_expr(lexemes, index)

            return index

        try:
            parse_program(lexemes)
            messagebox.showinfo("Syntax Analysis", "Syntax is valid!")
        except SyntaxError as e:
            messagebox.showerror("Syntax Error", str(e))




    def main_interpreter(self):
        self.lexemes_result.clear()
        
        for line in self.lines_list:
            self.lexical_analyzer(line)

        self.output_box1.config(state="normal")
        self.output_box1.delete(1.0, tk.END) 

        for lexeme, lexeme_type in self.lexemes_result:
            self.output_box1.insert(tk.END, f"{lexeme:<15} {lexeme_type}\n")

        self.output_box1.config(state="disabled")

        self.syntax_analyzer(self.lexemes_result)


if __name__ == "__main__":
    root = tk.Tk()
    app = LOLCodeInterpreter(root)
    root.mainloop()
