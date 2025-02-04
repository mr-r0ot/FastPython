#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CoDed By Mohammad Taha Gorji


A powerful Python code optimizer.

This program takes a Python file as input and applies one of several optimization
methods to generate a "FAST" version of the code. The available methods are:

1. Multiprocessing support
2. Translation to C/C++ (symbolic)
3. Numba JIT optimization (adding @njit via AST)
4. Cython preparation (adding Cython directives)
5. Caching (adding @lru_cache via AST)
6. Vectorized operations (adding numpy recommendations)

Usage:
    Interactive mode (if no command-line parameters are provided):
        $ python optimizer.py
        (you will be prompted for the file name and the optimization method)

    Command-line mode:
        $ python optimizer.py <filename> [method] [--run]

    - <filename>: path to the Python file to optimize.
    - [method]: (optional) a number from 1 to 6 representing the optimization method.
                If not provided, you will be prompted interactively.
    - [--run]: (optional) if provided, the optimized file will be executed immediately.

The optimized file will be saved with the name:
    <original_filename>_FAST.py
"""

import os
import sys
import re
import ast
import subprocess

# For Python versions < 3.9, try to import astunparse
try:
    ast_unparse = ast.unparse
except AttributeError:
    try:
        import astunparse
        ast_unparse = astunparse.unparse
    except ImportError:
        print("This program requires Python 3.9+ or the 'astunparse' package.")
        sys.exit(1)


def add_decorator_to_functions(code: str, decorator_name: str) -> str:
    """
    Add the specified decorator to all function definitions (if not already present)
    using the AST module.
    """
    try:
        tree = ast.parse(code)
    except Exception as e:
        print("Error parsing AST:", e)
        return code

    class DecoratorAdder(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            # Check if the decorator is already present.
            has_decorator = any(
                isinstance(dec, ast.Name) and dec.id == decorator_name
                for dec in node.decorator_list
            )
            if not has_decorator:
                new_decorator = ast.Name(id=decorator_name, ctx=ast.Load())
                node.decorator_list.insert(0, new_decorator)
            self.generic_visit(node)
            return node

    new_tree = DecoratorAdder().visit(tree)
    ast.fix_missing_locations(new_tree)
    try:
        optimized_code = ast_unparse(new_tree)
    except Exception as e:
        print("Error generating optimized code from AST:", e)
        return code
    return optimized_code


def ensure_import(code: str, import_line: str) -> str:
    """
    If the given import line is not already in the code, add it at the beginning.
    """
    if import_line not in code:
        code = import_line + "\n" + code
    return code


def optimize_multiprocessing(code: str) -> str:
    """
    Optimize by adding multiprocessing support.
    If a "if __name__ == '__main__'" block is missing, add a sample one that runs a
    main() function in a separate process.
    """
    optimized = "# [OPTIMIZATION: Multiprocessing]\n" + code
    if "if __name__" not in code:
        # Insert a sample main() and __main__ block.
        sample_main = (
            "def main():\n"
            "    # Main function of the program\n"
            "    pass\n\n"
            "if __name__ == '__main__':\n"
            "    import multiprocessing\n"
            "    p = multiprocessing.Process(target=main)\n"
            "    p.start()\n"
            "    p.join()\n\n"
        )
        optimized = sample_main + optimized
    else:
        optimized = "# Note: Please ensure that the multiprocessing block in __main__ is correct.\n" + optimized
    return optimized


def optimize_translation(code: str) -> str:
    """
    Add comments and instructions for translating the code to C/C++ (symbolic).
    """
    optimized = "# [OPTIMIZATION: Translated to a C/C++ version using pybind11]\n" + code
    optimized += (
        "\n# Note: For an actual translation, you need to manually configure tools such as Cython or pybind11.\n"
    )
    return optimized


def optimize_numba(code: str) -> str:
    """
    Optimize with Numba JIT by adding the @njit decorator to all functions.
    """
    code = ensure_import(code, "from numba import njit")
    optimized = add_decorator_to_functions(code, "njit")
    optimized = "# [OPTIMIZATION: Numba JIT applied]\n" + optimized
    return optimized


def optimize_cython(code: str) -> str:
    """
    Prepare the code for Cython compilation by adding the necessary directive.
    """
    optimized = "# [OPTIMIZATION: Prepared for Cython]\n# cython: language_level=3\n" + code
    optimized += (
        "\n# Note: To compile with Cython, change the file extension to .pyx and apply further configurations.\n"
    )
    return optimized


def optimize_cache(code: str) -> str:
    """
    Optimize by adding caching to functions using @lru_cache.
    """
    code = ensure_import(code, "from functools import lru_cache")
    optimized = add_decorator_to_functions(code, "lru_cache")
    optimized = "# [OPTIMIZATION: Caching with lru_cache applied]\n" + optimized
    return optimized


def optimize_vectorize(code: str) -> str:
    """
    Optimize by suggesting vectorized operations with NumPy.
    """
    optimized = "# [OPTIMIZATION: Vectorized operations with NumPy]\n"
    optimized = ensure_import(optimized, "import numpy as np")
    optimized += "\n" + code
    optimized += "\n# Note: It is recommended to convert loops into numpy operations for better performance.\n"
    return optimized


def display_menu() -> str:
    """
    Display the menu for selecting an optimization method and return the user's choice.
    """
    menu = (
        "Please select one of the following optimization methods:\n"
        "1 - Multiprocessing support\n"
        "2 - Translation to C/C++\n"
        "3 - Numba JIT optimization\n"
        "4 - Cython preparation\n"
        "5 - Caching with lru_cache\n"
        "6 - Vectorized operations (NumPy)\n"
        "Your choice (1-6): "
    )
    choice = input(menu).strip()
    return choice


def main():
    # Check command-line arguments using sys.argv
    args = sys.argv[1:]
    filename = None
    method_choice = None
    run_flag = False

    if not args:
        # Interactive mode
        filename = input("Enter the Python file name to optimize: ").strip()
        method_choice = display_menu()
    else:
        # Command-line mode
        # First argument is assumed to be the filename.
        filename = args[0]
        # Check if any argument equals "--run"
        if "--run" in args:
            run_flag = True
            args.remove("--run")
        # If a second argument is provided and is one of the methods, use it.
        if len(args) >= 2:
            method_choice = args[1]
        else:
            # If not provided, ask interactively.
            method_choice = display_menu()

    # Verify that the file exists.
    if not os.path.isfile(filename):
        print("Error: The specified file does not exist.")
        sys.exit(1)

    # Read the file contents.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print("Error reading file:", e)
        sys.exit(1)

    # Apply the selected optimization method.
    if method_choice == "1":
        optimized_code = optimize_multiprocessing(code)
    elif method_choice == "2":
        optimized_code = optimize_translation(code)
    elif method_choice == "3":
        optimized_code = optimize_numba(code)
    elif method_choice == "4":
        optimized_code = optimize_cython(code)
    elif method_choice == "5":
        optimized_code = optimize_cache(code)
    elif method_choice == "6":
        optimized_code = optimize_vectorize(code)
    else:
        print("Invalid selection!")
        sys.exit(1)

    # Determine the output file name: add _FAST before the file extension.
    base, ext = os.path.splitext(filename)
    new_filename = base + "_FAST" + ext

    try:
        with open(new_filename, "w", encoding="utf-8") as f:
            f.write(optimized_code)
        print("Optimized file saved as '{}'.".format(new_filename))
    except Exception as e:
        print("Error saving the optimized file:", e)
        sys.exit(1)

    # If the --run flag was provided, execute the optimized file.
    if run_flag:
        print("Executing the optimized file...")
        try:
            subprocess.run([sys.executable, new_filename], check=True)
        except subprocess.CalledProcessError as e:
            print("Error running the optimized file:", e)
            sys.exit(1)


if __name__ == "__main__":
    main()
