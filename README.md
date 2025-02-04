```markdown
# Python Code Optimizer

Welcome to the **Python Code Optimizer**! This powerful tool helps you automatically optimize your Python code using several advanced techniques. Whether you prefer an interactive mode or want to use command-line arguments, this optimizer makes it easy to generate a "FAST" version of your code that is optimized for performance.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Command-Line Mode](#command-line-mode)
- [Optimization Methods](#optimization-methods)
- [Algorithm Overview](#algorithm-overview)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Multiple Optimization Techniques**:  
  Optimize your code with one of the following methods:
  1. **Multiprocessing Support**: Adds support for multiprocessing by wrapping your code with a `__main__` block.
  2. **Translation to C/C++ (Symbolic)**: Inserts comments and guidance for translating your code into C/C++ (using tools like pybind11 or Cython).
  3. **Numba JIT Optimization**: Uses the AST module to decorate functions with `@njit` for Just-In-Time compilation.
  4. **Cython Preparation**: Adds the necessary Cython directives to prepare your code for compilation.
  5. **Caching with lru_cache**: Decorates functions with `@lru_cache` to improve performance via caching.
  6. **Vectorized Operations**: Encourages the use of NumPy for vectorized operations and better performance.

- **Interactive and Command-Line Modes**:  
  Run the optimizer interactively or pass parameters directly via the command line.

- **Instant Execution**:  
  Use the `--run` flag to automatically execute the optimized file after creation.

- **AST-Based Transformations**:  
  The optimizer leverages Python's Abstract Syntax Tree (AST) to safely insert decorators without breaking your code’s structure.

---

## Installation

1. **Python Version**: Ensure you have Python 3.9 or above.  
   If you're using an older version, install the `astunparse` package:
   ```bash
   pip install astunparse
   ```

2. **Download the Optimizer**:  
   Save the optimizer script (e.g., `FastPython.py`) to your local machine.

---

## Usage

### Interactive Mode

If you run the program without any command-line arguments, you'll be prompted to enter the file name and select an optimization method interactively.

```bash
python FastPython.py
```

**Steps:**

1. **Enter the Python file name** to optimize when prompted.
2. **Select the optimization method** from the displayed menu by entering a number (1–6).
3. The program will generate an optimized file with the suffix `_FAST` added to the original file name.

### Command-Line Mode

You can also run the optimizer using command-line arguments:

```bash
python FastPython.py <filename> [method] [--run]
```

- `<filename>`: Path to the Python file you want to optimize.
- `[method]`: *(Optional)* A number (1–6) indicating the optimization method.
- `[--run]`: *(Optional)* Automatically execute the optimized file after creation.

**Example:**

```bash
python FastPython.py myscript.py 3 --run
```

This command optimizes `myscript.py` using **Numba JIT optimization** (method 3) and runs the optimized version immediately.

---

## Optimization Methods

Below is a brief overview of the available optimization methods:

1. **Multiprocessing Support**:  
   - Inserts a sample `main()` function and a `__main__` block if missing.
   - Wraps the main process in a new multiprocessing process.

2. **Translation to C/C++ (Symbolic)**:  
   - Adds comments and hints for manually translating the code to a C/C++ version.
   - Useful for preparing your code for tools like Cython or pybind11.

3. **Numba JIT Optimization**:  
   - Ensures the necessary `njit` import is added.
   - Uses AST transformations to add `@njit` decorators to all functions for JIT compilation.

4. **Cython Preparation**:  
   - Inserts the Cython language level directive.
   - Provides guidance for converting the file to a `.pyx` extension for Cython compilation.

5. **Caching with lru_cache**:  
   - Adds the required `lru_cache` import.
   - Uses AST transformations to add `@lru_cache` decorators to all functions.

6. **Vectorized Operations (NumPy)**:  
   - Inserts the `numpy` import.
   - Adds recommendations to convert iterative loops into vectorized NumPy operations.

---

## Algorithm Overview

The optimizer works in the following steps:

1. **Input Parsing**:  
   - Uses `sys.argv` to determine whether to run in interactive or command-line mode.
   - Reads the Python file specified by the user.

2. **Optimization Method Selection**:  
   - If a method is provided via command-line, it is used.
   - Otherwise, the program displays a menu for the user to choose the optimization method.

3. **AST Transformation (When Applicable)**:  
   - For methods such as Numba and caching, the optimizer parses the source code into an AST.
   - A custom AST transformer (`DecoratorAdder`) traverses the tree to add the necessary decorators.
   - The modified AST is then unparsed back to source code using `ast.unparse` (or `astunparse`).

4. **Import Verification**:  
   - Ensures that necessary imports (e.g., `from numba import njit` or `from functools import lru_cache`) are present at the beginning of the file.

5. **File Generation and (Optional) Execution**:  
   - The optimized code is saved in a new file with `_FAST` appended to the original file name.
   - If the `--run` flag is specified, the new file is executed immediately using the Python interpreter.

---

## Examples

### Example 1: Interactive Mode

1. Run the optimizer without arguments:
   ```bash
   python FastPython.py
   ```
2. When prompted, enter:
   - File name: `example.py`
   - Optimization method: `3` (for Numba JIT)
3. The file `example_FAST.py` is generated and saved.

### Example 2: Command-Line Mode with Execution

Run the following command to optimize and immediately execute `example.py` using caching:
```bash
python FastPython.py example.py 5 --run
```

The optimizer creates `example_FAST.py` with caching enhancements and then runs it.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to fork the repository and submit a pull request with your improvements.

1. **Fork the Repository**
2. **Create a Feature Branch**
3. **Commit Your Changes**
4. **Submit a Pull Request**

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as per the terms of the license.

---

*Happy Optimizing!*
```

Coded By Mohammad Taha Gorji
```
