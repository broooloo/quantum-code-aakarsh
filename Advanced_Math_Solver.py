"""Advanced Math Solver

A Python GUI application built using Tkinter and SymPy that can:

- Solve equations
- Factor expressions
- Expand expressions
- Differentiate functions
- Integrate functions
- Simplify expressions
- Evaluate mathematical expressions

Built with:
- Python
- Tkinter
- SymPy
"""
import tkinter as tk
from sympy import *
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

x = symbols('x')
a = symbols('a')
b = symbols('b')
y = symbols('y')
z = symbols('z')
p = symbols('p')
q = symbols('q')
r = symbols('r')

transformations = (
    standard_transformations +
    (implicit_multiplication_application,)
)

from sympy.parsing.sympy_parser import convert_xor
transformations = (
    standard_transformations
    + (
        implicit_multiplication_application,
        convert_xor
    )
)

def solve_math():
    try:
        user_input = entry.get().strip()

        lower = user_input.lower()

        # solve
        if lower.startswith("solve "):
            expr = user_input[6:]

            left, right = expr.split("=")

            equation = Eq(
                parse_expr(left, transformations = transformations),
                parse_expr(right, transformations = transformations)
            )

            result = solve(equation)

        # factor
        elif lower.startswith("factor "):
            expr = user_input[7:]

            result = factor(
                parse_expr(expr, transformations=transformations)
            )
            
        elif lower.startswith("expand "):
            expr = user_input[7:]

            result = expand(
                parse_expr(expr, transformations=transformations)
            )

        elif lower.startswith("integrate "):
            expr = user_input[10:]

            result = integrate(
                parse_expr(expr, transformations=transformations),
                x
            )

        elif lower.startswith("differentiate "):
            expr = user_input[14:]

            result = diff(
                parse_expr(expr, transformations=transformations),
                x
            )

        elif lower.startswith("simplify "):
            expr = user_input[9:]

            result = simplify(
                parse_expr(expr, transformations=transformations)
            )

        else:
            result = parse_expr(
                user_input,
                transformations=transformations
            )

            result = result.evalf()

        output.delete(1.0, tk.END)
        output.insert(tk.END, str(result))

    except Exception as e:
        output.delete(1.0, tk.END)
        output.insert(tk.END, f"Error: {e}")

window = tk.Tk()
window.title("Math Solver")
window.geometry("800x500")

title = tk.Label(
    window,
    text="Math Solver",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

entry = tk.Entry(
    window,
    width=60,
    font=("Consolas", 12)
)
entry.pack(pady=10)

solve_button = tk.Button(
    window,
    text="Solve",
    command=solve_math
)
solve_button.pack()

output = tk.Text(
    window,
    height=10,
    width=70,
    font=("Consolas", 11)
)

output.pack(pady=20)

window.mainloop()
