import ast
import tkinter as tk
from tkinter import scrolledtext

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.loop_depth = 0
        self.max_depth = 0

    def visit_For(self, node):
        self.loop_depth += 1
        self.max_depth = max(self.max_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        self.max_depth = max(self.max_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.max_depth += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.generic_visit(node)

    def visit_If(self, node):
        self.generic_visit(node)

    def visit_Return(self, node):
        self.generic_visit(node)

def Time_Complexity(code):
    tree = ast.parse(code)
    visitor = ComplexityVisitor()
    visitor.visit(tree)

    max_depth = visitor.max_depth
    if max_depth == 0:
        return "O(1)"
    elif max_depth == 1:
        return "O(n)"
    elif max_depth == 2:
        return "O(n^2)"
    elif max_depth == 3:
        return "O(n^3)"
    else:
        return f"O(n^{max_depth})"

def Space_Complexity(code):
    tree = ast.parse(code)
    variable_names = set()

    # Traverse the AST nodes to look for Assign and AnnAssign (type-hinted assignments)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            variable_names.add(node.target.id)
    
    # Return the number of unique variable names as the space complexity
    # Since we want to return O(n) where n is the number of unique variables, we calculate it like this:
    return len(variable_names)

def calculate_complexity():
    code = code_input.get("1.0", tk.END).strip()  # Get code input
    if code:
        space_complexity = Space_Complexity(code)
        time_complexity = Time_Complexity(code)
        result_text.set(f"Space Complexity: O({space_complexity})\nTime Complexity: {time_complexity}")
    else:
        result_text.set("Please enter some code.")

# Create the main window
root = tk.Tk()
root.title("Time and Space Complexity Calculator")

# Create a label
label = tk.Label(root, text="Enter your Python code:")
label.pack(pady=10)

# Create a text box for code input
code_input = scrolledtext.ScrolledText(root, width=50, height=15)
code_input.pack(padx=10, pady=10)

# Create a button to calculate complexity
calculate_button = tk.Button(root, text="Calculate Complexity", command=calculate_complexity)
calculate_button.pack(pady=10)

# Create a label to show results
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

# Run the application
root.mainloop()
