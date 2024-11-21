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
            

    def main_interpreter(self):
        self.lexemes_result.clear()
        
        for line in self.lines_list:
            self.lexical_analyzer(line)

        self.output_box1.config(state="normal")
        self.output_box1.delete(1.0, tk.END) 

        for lexeme, lexeme_type in self.lexemes_result:
            self.output_box1.insert(tk.END, f"{lexeme:<15} {lexeme_type}\n")

        self.output_box1.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = LOLCodeInterpreter(root)
    root.mainloop()
