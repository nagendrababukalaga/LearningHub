import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.accounts.models import Profile
from apps.learning.models import LearningPath, Level, Topic, Resource, Bookmark
from apps.memory.models import PersonalLearningMemory, TopicNote, LearningDoubt, LearningMistake
from apps.progress.models import UserTopicProgress, DailyTask, UserDailyTask, PracticeProblem, UserPractice
from apps.bootcamp.models import Bootcamp, BootcampDay, UserBootcampProgress
from apps.guidance.models import MentorArticle, MentorTip
from apps.core.models import StudentStory


class Command(BaseCommand):
    help = 'Seeds the LearningHub database with complete Python curriculum, bootcamp, mentor guides, and demo user'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("[+] Starting LearningHub complete database seeding..."))

        # 1. Create Superuser and Demo Student
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@learninghub.dev',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Hub',
                'last_name': 'Admin'
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        demo_user, _ = User.objects.get_or_create(
            username='demo_student',
            defaults={
                'email': 'student@learninghub.dev',
                'first_name': 'Alex',
                'last_name': 'Chen'
            }
        )
        demo_user.set_password('password123')
        demo_user.save()

        # Update profile
        profile = demo_user.profile
        profile.full_name = "Alex Chen"
        profile.bio = "2nd-year CS student aiming for software engineering internships and building clean Python applications."
        profile.primary_goal = "internship"
        profile.experience_level = "rusty"
        profile.daily_goal_minutes = 60
        profile.current_streak = 5
        profile.longest_streak = 8
        profile.save()

        self.stdout.write(self.style.SUCCESS("[OK] Admin ('admin'/'admin123') & Demo Student ('demo_student'/'password123') ready."))

        # 2. Create Learning Path
        python_path, _ = LearningPath.objects.get_or_create(
            slug='python-mastery',
            defaults={
                'title': 'Python Programming Master Path',
                'tagline': 'Master modern Python from absolute zero to building real-world projects & software engineering readiness.',
                'description': 'A comprehensive, structured 7-level journey covering core fundamentals, algorithmic data structures, functional paradigms, object-oriented design, error handling, APIs, and practical software engineering practices.',
                'icon': 'terminal',
                'is_active': True,
                'order': 1
            }
        )

        # 3. Define Levels and Topics Data
        levels_data = [
            {
                'level_number': 1,
                'title': 'Fundamentals & Core Syntax',
                'tagline': 'Establish rock-solid programming foundations with Python core syntax and primitives.',
                'description': 'Understand how Python executes code, manage variables in memory, handle inputs and outputs, master arithmetic and logical operators, and avoid common type confusion bugs.',
                'topics': [
                    {
                        'title': 'Introduction to Python & Setup',
                        'difficulty': 'beginner',
                        'estimated_minutes': 25,
                        'objectives': "Understand Python's interpreted architecture and execution model.\nLearn how the Python interpreter and REPL work.\nDiscover PEP 8 code style guidelines and the Zen of Python (import this).\nRun your very first Python script successfully.",
                        'summary_content': """Python is a high-level, interpreted, dynamically-typed programming language created by Guido van Rossum. Unlike compiled languages like C++ where source code is converted to machine binary before execution, Python translates source code into intermediate bytecode (`.pyc`), which is executed line-by-line by the Python Virtual Machine (PVM).

### Why Python is Popular
- **Clean, readable syntax**: Eliminates curly braces in favor of whitespace indentation.
- **Batteries Included**: Vast standard library for everything from file I/O to networking and math.
- **Versatility**: Used for Web Development (Django/FastAPI), Data Science, Machine Learning, Automation, and Scripting.

### The Zen of Python
Type `import this` in any Python shell to view the core philosophy:
- *Beautiful is better than ugly.*
- *Explicit is better than implicit.*
- *Simple is better than complex.*
- *Readability counts.*""",
                        'code_snippet': """# Your first Python script with clean idiomatic style
import sys

def main():
    greeting = "Hello, LearningHub Student!"
    python_version = sys.version.split()[0]
    print(f"{greeting} Running on Python {python_version}")

if __name__ == "__main__":
    main()""",
                        'key_takeaways': "Python is interpreted and executes bytecode through the PVM.\nIndentation is part of Python syntax, not just formatting.\nPEP 8 is the standard Python style guide.\nAlways write readable and explicit code.",
                        'resources': [
                            ('Official Python Tutorial - Getting Started', 'doc', 'https://docs.python.org/3/tutorial/appetite.html', 'Python.org', '15 min read'),
                            ('Python for Beginners - Full Crash Course', 'video', 'https://www.youtube.com/watch?v=kqtD5dpn9C8', 'Programming with Mosh', '45 mins'),
                            ('The Zen of Python (PEP 20)', 'doc', 'https://peps.python.org/pep-0020/', 'Python.org', '5 min read')
                        ],
                        'practice': {
                            'title': 'Hello World & Interpreter Output',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a Python program that prints your name, your primary learning goal, and the result of calculating 365 * 24 (hours in a year).',
                            'starter_code': '# Write your Python script below:\n',
                            'solution_hint': 'Use print() statements and f-strings or arithmetic expressions inside print.',
                            'solution_code': 'name = "Alex"\ngoal = "Master Python"\nhours_in_year = 365 * 24\nprint(f"Student: {name}")\nprint(f"Goal: {goal}")\nprint(f"Hours in a year: {hours_in_year}")'
                        }
                    },
                    {
                        'title': 'Variables, Naming Rules & Constants',
                        'difficulty': 'beginner',
                        'estimated_minutes': 30,
                        'objectives': "Understand how Python variables are dynamic references to objects in memory.\nMaster Python naming conventions (snake_case vs PascalCase vs UPPER_CASE).\nUnderstand reserved keywords that cannot be used as identifiers.\nLearn how variable reassignment and garbage collection work conceptually.",
                        'summary_content': """In Python, variables are not typed boxes that hold values; they are **labeled tags (references)** attached to objects stored in heap memory.

### Variable Assignment
```python
x = 42
y = x  # y now points to the same integer object 42 in memory
```

### Naming Rules & PEP 8 Conventions
1. **Variables & Functions**: Use `snake_case` (e.g., `student_count`, `calculate_total`).
2. **Constants**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES = 5`, `DATABASE_URL = '...'`).
3. **Classes**: Use `PascalCase` (e.g., `UserProfile`, `LearningEngine`).
4. **Rules**:
   - Must begin with a letter (a-z, A-Z) or underscore (`_`).
   - Cannot begin with a number.
   - Cannot use Python reserved keywords (`if`, `for`, `class`, `def`, `return`, `is`, `in`, etc.).""",
                        'code_snippet': """# Python variables as references
user_name = "Alex"
login_attempts = 0
MAX_LOGIN_ATTEMPTS = 3  # Constant by convention
is_account_active = True

# Inspect memory identity with id()
a = [1, 2, 3]
b = a
print(f"Are a and b pointing to the same memory? {id(a) == id(b)}")  # True""",
                        'key_takeaways': "Variables are references/pointers to objects in memory.\nPython uses snake_case for variables and functions.\nConstants are written in ALL_CAPS by convention.\nDo not shadow built-in function names like list, str, id, max.",
                        'resources': [
                            ('Python Variables & Memory Models', 'article', 'https://realpython.com/python-variables/', 'Real Python', '12 min read'),
                            ('Variables and Data Types in Python', 'video', 'https://www.youtube.com/watch?v=T1b7r7lPwhs', 'Corey Schafer', '20 mins')
                        ],
                        'practice': {
                            'title': 'Variable Swap & Constants Assignment',
                            'difficulty': 'easy',
                            'prompt_description': 'Given two variables `a = 10` and `b = 20`, swap their values without using a temporary third variable using Pythonic tuple unpacking. Print the values before and after.',
                            'starter_code': 'a = 10\nb = 20\n# Swap a and b in one line using Pythonic syntax:\n',
                            'solution_hint': 'Python allows multi-variable assignment: a, b = b, a',
                            'solution_code': 'a = 10\nb = 20\nprint(f"Before: a={a}, b={b}")\na, b = b, a\nprint(f"After: a={a}, b={b}")'
                        }
                    },
                    {
                        'title': 'Core Data Types: int, float, str, bool, None',
                        'difficulty': 'beginner',
                        'estimated_minutes': 35,
                        'objectives': "Master Python's fundamental scalar primitive types: int, float, str, bool, and NoneType.\nUnderstand arbitrary-precision integers and floating-point precision caveats.\nMaster Boolean truthiness and falsy values in Python.\nLearn how and when to use NoneType for null values.",
                        'summary_content': """Python provides rich built-in scalar types:

1. **`int`**: Arbitrary-precision integers (can grow as large as memory permits without overflow).
2. **`float`**: IEEE 754 double-precision floating point numbers. Note: `0.1 + 0.2 != 0.3` due to binary fraction rounding! Use `math.isclose()` or `decimal.Decimal` for exact currency calculations.
3. **`str`**: Immutable sequence of Unicode characters.
4. **`bool`**: Subclass of integer (`True == 1`, `False == 0`).
5. **`NoneType` (`None`)**: Represents the absence of a value or a default return value.

### Truthy and Falsy in Python
The following evaluate to `False` in boolean contexts:
- `None`, `False`
- Numeric zeros: `0`, `0.0`, `0j`
- Empty sequences and collections: `""`, `[]`, `()`, `{}`, `set()`""",
                        'code_snippet': """# Inspecting types and checking truthiness
age = 21               # int
gpa = 3.85             # float
student_name = "Maya"  # str
enrolled = True        # bool
graduation_date = None # NoneType

print(type(age))       # <class 'int'>
print(isinstance(gpa, float))  # True

# Pythonic truthiness check:
cart_items = []
if not cart_items:
    print("Your cart is empty!")""",
                        'key_takeaways': "Python integers have infinite precision.\nFloats have binary precision limitations; use math.isclose() for float comparisons.\nStrings are immutable.\nEmpty containers and 0 are falsy; non-empty containers are truthy.",
                        'resources': [
                            ('Python Basic Data Types Guide', 'doc', 'https://docs.python.org/3/library/stdtypes.html', 'Python.org', '15 min read'),
                            ('Python Truth Value Testing & Boolean Operations', 'doc', 'https://docs.python.org/3/library/stdtypes.html#truth-value-testing', 'Python.org', '10 min read')
                        ],
                        'practice': {
                            'title': 'Type Identification & Truthiness Checker',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `inspect_value(val)` that prints the value, its data type name using `type(val).__name__`, and whether it evaluates to Truthy or Falsy.',
                            'starter_code': 'def inspect_value(val):\n    # Write logic here\n    pass\n',
                            'solution_hint': 'Use bool(val) to check truthiness and type(val).__name__ for readable type name.',
                            'solution_code': 'def inspect_value(val):\n    t_name = type(val).__name__\n    truthiness = "Truthy" if bool(val) else "Falsy"\n    print(f"Value: {repr(val)} | Type: {t_name} | Evaluation: {truthiness}")'
                        }
                    },
                    {
                        'title': 'Input and Output: print(), f-strings & input()',
                        'difficulty': 'beginner',
                        'estimated_minutes': 30,
                        'objectives': "Master standard input using `input()` and understand that it always returns a string.\nMaster `print()` parameters: `sep=`, `end=`, and `file=`.\nBecome fluent in Python 3.6+ formatted string literals (f-strings).\nFormat numbers with decimal places, padding, and thousand separators.",
                        'summary_content': """Outputting data and collecting user input are essential.

### Modern f-strings (Fastest & Most Readable)
```python
price = 49.995
item = "Python Book"
print(f"Item: {item:<15} Price: ${price:.2f}")
# Output: Item: Python Book     Price: $50.00
```

### Advanced `print()` parameters:
- `sep=`: Custom separator between arguments (default `' '`).
- `end=`: Custom string printed at the end (default `'\n'`).

### Reading User Input:
`input("Prompt: ")` halts execution until the user presses Enter and always returns a string. If you need numbers, convert explicitly: `int(input())` or `float(input())`.""",
                        'code_snippet': """# Formatting with f-strings
name = "Dev"
score = 94.5678
rank = 1

# Formatting numbers: 2 decimal places & padding
print(f"Rank #{rank:02d}: {name} - Score: {score:.2f}%")

# Separator and end arguments
print("Python", "Django", "SQLite", sep=" -> ", end=" [DONE]\n")""",
                        'key_takeaways': "f-strings are the preferred modern way to format strings in Python.\ninput() always produces a string; always cast to int() or float() when needed.\nUse :.2f for rounding floats in strings without modifying the underlying number.",
                        'resources': [
                            ('Python f-strings: An Indispensable Guide', 'article', 'https://realpython.com/python-f-strings/', 'Real Python', '12 min read'),
                            ('Python Input and Output Documentation', 'doc', 'https://docs.python.org/3/tutorial/inputoutput.html', 'Python.org', '10 min read')
                        ],
                        'practice': {
                            'title': 'Receipt Line Item Formatter',
                            'difficulty': 'easy',
                            'prompt_description': 'Given product name `item = "Wireless Mouse"`, `quantity = 2`, and `price = 24.99`, use f-strings to print a cleanly formatted receipt line with the total cost formatted to 2 decimal places.',
                            'starter_code': 'item = "Wireless Mouse"\nquantity = 2\nprice = 24.99\n# Calculate total and print formatted line:\n',
                            'solution_hint': 'Calculate total = quantity * price and print with f"{quantity}x {item} @ ${price:.2f} = ${total:.2f}"',
                            'solution_code': 'item = "Wireless Mouse"\nquantity = 2\nprice = 24.99\ntotal = quantity * price\nprint(f"{quantity}x {item:<16} @ ${price:.2f} each | Total: ${total:.2f}")'
                        }
                    },
                    {
                        'title': 'Python Operators: Arithmetic, Comparison & Logical',
                        'difficulty': 'beginner',
                        'estimated_minutes': 35,
                        'objectives': "Master arithmetic operators: `+`, `-`, `*`, `/`, `//` (floor division), `%` (modulo), `**` (exponentiation).\nUnderstand comparison operators and operator chaining (`10 < x <= 50`).\nMaster logical operators (`and`, `or`, `not`) and short-circuit evaluation.\nUnderstand identity (`is`) vs equality (`==`).",
                        'summary_content': """Operators form the fundamental mathematical and logical machinery of Python.

### Division Variations:
- True Division (`/`): Always returns a `float` (`7 / 2 -> 3.5`).
- Floor Division (`//`): Truncates toward negative infinity (`7 // 2 -> 3`, `-7 // 2 -> -4`).
- Modulo (`%`): Returns remainder (`7 % 2 -> 1`).
- Exponentiation (`**`): `2 ** 8 -> 256`.

### `==` (Value Equality) vs `is` (Identity Equality)
- `a == b` checks if the contents/values are equivalent.
- `a is b` checks if `a` and `b` reference the exact same object in memory (`id(a) == id(b)`).
- **Rule**: Always use `is` / `is not` when comparing against `None` (`if val is None:`).

### Short-Circuit Evaluation:
- `A and B`: If `A` is falsy, Python returns `A` immediately without evaluating `B`.
- `A or B`: If `A` is truthy, Python returns `A` immediately without evaluating `B`.""",
                        'code_snippet': """# Operator Chaining in Python
score = 85
if 80 <= score < 90:
    print("Grade B")

# Equality vs Identity
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 == list2)  # True (same elements)
print(list1 is list2)  # False (different memory addresses)

# Short-circuit default assignment:
user_input = ""
display_name = user_input or "Anonymous Student"
print(display_name)    # "Anonymous Student" """,
                        'key_takeaways': "Use // for integer floor division and / for standard float division.\n== checks value equality; is checks object identity in memory.\nAlways compare with None using: if x is None:\nPython supports elegant chained comparisons like 0 <= x < 100.",
                        'resources': [
                            ('Python Operators Overview', 'doc', 'https://docs.python.org/3/reference/expressions.html#comparisons', 'Python.org', '12 min read'),
                            ('Python is vs == Deep Dive', 'article', 'https://realpython.com/courses/python-is-identity-vs-equality/', 'Real Python', '8 min read')
                        ],
                        'practice': {
                            'title': 'Leap Year & Range Logic Evaluator',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `is_leap_year(year)` that returns `True` if a year is a leap year (divisible by 4, but not by 100 unless also divisible by 400), and `False` otherwise.',
                            'starter_code': 'def is_leap_year(year):\n    # Write logic using modulo and boolean operators\n    pass\n',
                            'solution_hint': 'A year is leap if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0).',
                            'solution_code': 'def is_leap_year(year):\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)'
                        }
                    },
                    {
                        'title': 'Type Conversion & Type Casting',
                        'difficulty': 'beginner',
                        'estimated_minutes': 25,
                        'objectives': "Differentiate between implicit type conversion (coercion) and explicit type casting.\nUse `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()` safely.\nHandle `ValueError` when converting malformed string inputs.\nUnderstand float-to-int truncation behavior.",
                        'summary_content': """Type casting converts a value from one data type into another.

### Implicit Conversion
Python automatically promotes types without data loss (e.g. adding an `int` and a `float` results in a `float`):
```python
x = 10    # int
y = 2.5   # float
z = x + y # 12.5 (float)
```

### Explicit Conversion Functions
- `int("42")` -> `42` (Note: `int("42.5")` raises `ValueError`; use `int(float("42.5"))` to truncate).
- `str(100)` -> `"100"`
- `float("3.14159")` -> `3.14159`
- `bool(0)` -> `False`, `bool("hello")` -> `True`""",
                        'code_snippet': """# Safe type conversion pattern
raw_input = "150"

try:
    quantity = int(raw_input)
    print(f"Valid integer: {quantity}")
except ValueError:
    print(f"Cannot convert '{raw_input}' to integer")

# Truncation vs Rounding
num = 9.99
print(int(num))       # 9 (truncates toward zero, does NOT round)
print(round(num))     # 10 (rounds to nearest integer)""",
                        'key_takeaways': "int() truncates floating point decimals without rounding; use round() for mathematical rounding.\nConverting a non-numeric string with int() throws a ValueError.\nImplicit conversion elevates int to float when combined with float operations.",
                        'resources': [
                            ('Python Type Casting Guide', 'article', 'https://www.w3schools.com/python/python_casting.asp', 'W3Schools', '5 min read'),
                            ('Handling Exceptions in Python Conversions', 'doc', 'https://docs.python.org/3/tutorial/errors.html', 'Python.org', '10 min read')
                        ],
                        'practice': {
                            'title': 'Safe String to Integer Converter',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `safe_str_to_int(val, default=0)` that converts `val` to an integer, returning `default` if conversion fails due to ValueError or TypeError.',
                            'starter_code': 'def safe_str_to_int(val, default=0):\n    # Write try-except block here\n    pass\n',
                            'solution_hint': 'Use a try-except ValueError block.',
                            'solution_code': 'def safe_str_to_int(val, default=0):\n    try:\n        return int(val)\n    except (ValueError, TypeError):\n        return default'
                        }
                    }
                ]
            },
            {
                'level_number': 2,
                'title': 'Control Flow & Loops',
                'tagline': 'Master decision making and iterative execution to build structured algorithms.',
                'description': 'Take full control of execution branching with if/elif/else, for loops with range and enumerate, while loops, and loop control keywords.',
                'topics': [
                    {
                        'title': 'Conditional Statements: if, elif, else',
                        'difficulty': 'beginner',
                        'estimated_minutes': 35,
                        'objectives': "Master single-branch and multi-branch decision structures.\nUnderstand proper ordering of conditions in `elif` chains.\nUse Python conditional expressions (ternary operator: `val if cond else other`).\nAvoid common anti-patterns like comparing booleans with `== True`.",
                        'summary_content': """Conditionals allow your Python program to execute different logic branches depending on whether boolean expressions evaluate to `True` or `False`.

### Structure:
```python
if condition_1:
    # Runs if condition_1 is True
elif condition_2:
    # Runs if condition_1 was False and condition_2 is True
else:
    # Runs if none of the above conditions met
```

### Python Ternary Operator:
```python
status = "Adult" if age >= 18 else "Minor"
```

### Clean Code Tip:
Avoid `if is_logged_in == True:`. Instead, write idiomatic Python: `if is_logged_in:`.""",
                        'code_snippet': """# Clean multi-branch condition
def calculate_shipping(order_amount, is_premium_member):
    if is_premium_member or order_amount >= 100:
        shipping_fee = 0.0
    elif order_amount >= 50:
        shipping_fee = 4.99
    else:
        shipping_fee = 9.99
    
    return shipping_fee

print(f"Shipping: ${calculate_shipping(65, False)}")  # $4.99""",
                        'key_takeaways': "Conditions are evaluated sequentially from top to bottom; the first True branch executes.\nAlways place more specific conditions before general conditions.\nUse the ternary expression for concise one-line value assignments.",
                        'resources': [
                            ('Python Conditional Statements', 'doc', 'https://docs.python.org/3/tutorial/controlflow.html#if-statements', 'Python.org', '10 min read'),
                            ('Python Ternary Operator in Practice', 'article', 'https://realpython.com/python-conditional-statements/', 'Real Python', '12 min read')
                        ],
                        'practice': {
                            'title': 'Student Grade Classifier',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `get_letter_grade(score)` that takes an integer score (0-100) and returns "A" (>=90), "B" (>=80), "C" (>=70), "D" (>=60), or "F" (<60). If score is outside 0-100, return "Invalid".',
                            'starter_code': 'def get_letter_grade(score):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Check for invalid bounds first, then check score in descending order.',
                            'solution_code': 'def get_letter_grade(score):\n    if not (0 <= score <= 100):\n        return "Invalid"\n    if score >= 90: return "A"\n    if score >= 80: return "B"\n    if score >= 70: return "C"\n    if score >= 60: return "D"\n    return "F"'
                        }
                    },
                    {
                        'title': 'for Loops, range() & enumerate()',
                        'difficulty': 'beginner',
                        'estimated_minutes': 40,
                        'objectives': "Master sequence iteration over strings, lists, tuples, and dictionaries.\nUnderstand the `range(start, stop, step)` generator function.\nUse `enumerate(iterable, start=0)` to cleanly track loop indices without manual counter variables.\nIterate over multiple sequences simultaneously using `zip()`.",
                        'summary_content': """In Python, `for` loops are fundamentally **collection iterators** (similar to `for-each` loops in other languages).

### The `range()` Function:
- `range(5)` -> `0, 1, 2, 3, 4` (stops before 5)
- `range(2, 8)` -> `2, 3, 4, 5, 6, 7`
- `range(10, 0, -2)` -> `10, 8, 6, 4, 2` (negative step for countdowns)

### Why `enumerate()` is Preferred Over `range(len(items))`:
Never write `for i in range(len(fruits)): print(fruits[i])`.
Always write: `for index, fruit in enumerate(fruits, start=1):`.""",
                        'code_snippet': """# Clean iteration with enumerate and zip
skills = ["Python", "Django", "SQL", "Git"]

print("--- Skills Checklist ---")
for idx, skill in enumerate(skills, start=1):
    print(f"{idx}. {skill}")

# Combining two lists with zip()
topics = ["Variables", "Loops", "Functions"]
times = [30, 45, 60]

for topic, mins in zip(topics, times):
    print(f"Study {topic} for {mins} mins")""",
                        'key_takeaways': "Python for loops iterate directly over items in an iterable.\nUse enumerate() whenever you need both the index and the item.\nUse zip() to iterate through two or more iterables in parallel.\nrange(start, stop, step) is lazy and generates numbers on demand without allocating full lists.",
                        'resources': [
                            ('Python for Loops Tutorial', 'doc', 'https://docs.python.org/3/tutorial/controlflow.html#for-statements', 'Python.org', '10 min read'),
                            ('How to Use enumerate() in Python', 'article', 'https://realpython.com/python-enumerate/', 'Real Python', '10 min read')
                        ],
                        'practice': {
                            'title': 'Ranked Leaderboard Formatter',
                            'difficulty': 'easy',
                            'prompt_description': 'Given a list of student names sorted by score, print a numbered leaderboard starting at rank 1 with medal emojis for top 3 (🥇, 🥈, 🥉).',
                            'starter_code': 'students = ["Alex", "Maya", "Rahul", "Sara", "David"]\n# Use enumerate to print formatted leaderboard:\n',
                            'solution_hint': 'Use enumerate(students, start=1) and check rank == 1, 2, 3 for medals.',
                            'solution_code': 'students = ["Alex", "Maya", "Rahul", "Sara", "David"]\nmedals = {1: "🥇", 2: "🥈", 3: "🥉"}\nfor rank, student in enumerate(students, start=1):\n    badge = medals.get(rank, f"#{rank}")\n    print(f"{badge} {student}")'
                        }
                    },
                    {
                        'title': 'while Loops & Sentinel Controlled Iteration',
                        'difficulty': 'beginner',
                        'estimated_minutes': 35,
                        'objectives': "Understand condition-based indefinite iteration with `while` loops.\nPrevent and diagnose infinite loops.\nImplement sentinel-controlled loops (e.g. user prompt termination, retry loops with backoff).\nUnderstand loop invariants and updating loop state variables.",
                        'summary_content': """A `while` loop continues executing as long as its condition remains `True`.

### When to use `while` vs `for`:
- Use `for` when you know the collection or number of iterations in advance.
- Use `while` when iteration depends on an external condition (user input, network polling, game loop, convergence condition).

### Avoiding Infinite Loops:
Ensure that every `while` loop has a path that causes the loop condition to evaluate to `False`, or contains an explicit `break` condition.""",
                        'code_snippet': """# Sentinel-controlled input loop simulation
attempts = 0
MAX_ATTEMPTS = 3
authenticated = False

while attempts < MAX_ATTEMPTS and not authenticated:
    attempts += 1
    # Simulated auth check
    pin = "1234"
    if pin == "1234":
        authenticated = True
        print(f"Access granted on attempt {attempts}!")

if not authenticated:
    print("Account locked due to excessive failed attempts.")""",
                        'key_takeaways': "while loops are for indefinite iteration where the end condition is dynamic.\nAlways ensure the condition variable changes inside the loop body to prevent infinite loops.\nCombine boolean flags with while loops for clean state machines.",
                        'resources': [
                            ('Python while Loops In-Depth', 'article', 'https://realpython.com/python-while-loop/', 'Real Python', '12 min read'),
                            ('Loop Control Patterns', 'video', 'https://www.youtube.com/watch?v=6iF8Xb7Z3wQ', 'Corey Schafer', '15 mins')
                        ],
                        'practice': {
                            'title': 'Collatz Conjecture Step Counter',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `collatz_steps(n)` that calculates how many steps it takes to reach 1. If n is even: n = n // 2. If n is odd: n = 3 * n + 1.',
                            'starter_code': 'def collatz_steps(n):\n    # Write while loop\n    pass\n',
                            'solution_hint': 'Initialize steps = 0, loop while n > 1, update n and increment steps.',
                            'solution_code': 'def collatz_steps(n):\n    steps = 0\n    while n > 1:\n        if n % 2 == 0:\n            n = n // 2\n        else:\n            n = 3 * n + 1\n        steps += 1\n    return steps'
                        }
                    },
                    {
                        'title': 'Loop Control: break, continue, pass & else clause',
                        'difficulty': 'beginner',
                        'estimated_minutes': 35,
                        'objectives': "Use `break` to immediately terminate the innermost loop.\nUse `continue` to skip the remainder of the current iteration.\nUse `pass` as a syntactic placeholder for future code.\nMaster Python's unique `for...else` and `while...else` construct.",
                        'summary_content': """Python gives you granular control over loop execution.

### Control Keywords:
- **`break`**: Exits the loop immediately.
- **`continue`**: Skips the remaining lines of the current iteration and jumps to the next iteration.
- **`pass`**: A null statement. Python interpreter executes it as a no-op.

### Python's `for...else` Construct:
In Python, loops can have an `else` block! The `else` block runs **only if the loop completed naturally without hitting a `break` statement**.
This is ideal for search algorithms where you want to execute fallback code if no match was found.""",
                        'code_snippet': """# Python's elegant for...else search pattern
target = "SQL"
technologies = ["HTML", "CSS", "Python", "Django"]

for tech in technologies:
    if tech == target:
        print(f"Found {target} in curriculum!")
        break
else:
    # Runs ONLY if the loop did NOT hit break
    print(f"{target} is not in the list. Need to add it!")""",
                        'key_takeaways': "break halts the loop; continue skips to the next cycle.\nfor...else executes the else block ONLY if the loop completes without hitting break.\npass is useful when creating empty function or class stubs during design.",
                        'resources': [
                            ('Python break, continue, and pass Guide', 'doc', 'https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops', 'Python.org', '10 min read'),
                            ('Understanding Python for...else', 'article', 'https://realpython.com/python-for-loop/#the-else-clause', 'Real Python', '8 min read')
                        ],
                        'practice': {
                            'title': 'Prime Number Checker with for...else',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `is_prime(n)` that returns True if n is prime (>1) and False otherwise using a for...else loop.',
                            'starter_code': 'def is_prime(n):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Check if n <= 1. Then loop d from 2 up to int(n**0.5) + 1. If n % d == 0: break. else: return True.',
                            'solution_code': 'def is_prime(n):\n    if n <= 1:\n        return False\n    for d in range(2, int(n**0.5) + 1):\n        if n % d == 0:\n            return False\n    return True'
                        }
                    }
                ]
            },
            {
                'level_number': 3,
                'title': 'Data Structures',
                'tagline': 'Master the core Python collections: Strings, Lists, Tuples, Sets, and Dictionaries.',
                'description': 'Understand how data is stored, indexed, mutated, sliced, and hashed in memory. Learn time complexity trade-offs for high-performance code.',
                'topics': [
                    {
                        'title': 'Python Strings: Slicing & Core Methods',
                        'difficulty': 'beginner',
                        'estimated_minutes': 40,
                        'objectives': "Master 0-based positive and negative string indexing and slicing `[start:stop:step]`.\nUnderstand string immutability in Python.\nMaster essential string methods: `.split()`, `.join()`, `.strip()`, `.replace()`, `.find()`, `.startswith()`, `.endswith()`.\nSanitize user text input cleanly.",
                        'summary_content': """Strings in Python are immutable sequences of Unicode characters.

### Slicing Syntax: `string[start:stop:step]`
- `text[0:4]` -> characters from index 0 to 3
- `text[::-1]` -> reverses the string efficiently
- `text[-3:]` -> last 3 characters of the string

### Essential String Methods:
- `s.strip()`: Removes leading/trailing whitespace.
- `s.split(",")`: Splits string into list on delimiter.
- `", ".join(items)`: Efficiently concatenates list of strings with separator.
- `s.replace(old, new)`: Returns a new string with replacements.
- `s.lower()`, `s.upper()`, `s.title()`: Case transformations.""",
                        'code_snippet': """# String manipulation showcase
url = "https://learninghub.dev/courses/python-fundamentals"

# Slicing domain and path
protocol = url[:5]
slug = url.split("/")[-1]
print(f"Slug: {slug.replace('-', ' ').title()}")  # Python Fundamentals

# String reversing with slice
word = "racecar"
is_palindrome = word == word[::-1]
print(f"Is '{word}' a palindrome? {is_palindrome}")""",
                        'key_takeaways': "Strings cannot be modified in place (they are immutable); methods return new string objects.\ntext[::-1] is the standard idiomatic way to reverse a string.\nAlways use delimiter.join(list_of_strings) instead of + in loops for O(N) performance.",
                        'resources': [
                            ('Python String Methods Reference', 'doc', 'https://docs.python.org/3/library/stdtypes.html#string-methods', 'Python.org', '15 min read'),
                            ('Python String Slicing Visualized', 'article', 'https://realpython.com/lessons/string-slicing/', 'Real Python', '8 min read')
                        ],
                        'practice': {
                            'title': 'Clean Slug Generator',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `generate_slug(title)` that strips whitespace, converts all letters to lowercase, and replaces spaces with hyphens (e.g. "  Learn Python Fast! " -> "learn-python-fast!").',
                            'starter_code': 'def generate_slug(title):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Use .strip().lower().replace(" ", "-")',
                            'solution_code': 'def generate_slug(title):\n    return title.strip().lower().replace(" ", "-")'
                        }
                    },
                    {
                        'title': 'Python Lists: CRUD, Slicing & Memory Mutability',
                        'difficulty': 'beginner',
                        'estimated_minutes': 45,
                        'objectives': "Understand list mutability and dynamic array resizing in memory.\nPerform CRUD operations: `.append()`, `.extend()`, `.insert()`, `.pop()`, `.remove()`, `del`.\nUnderstand sorting: `list.sort()` (in-place) vs `sorted(list)` (returns new list).\nAvoid shallow copy bugs when copying lists (`list.copy()` vs `deepcopy()`).",
                        'summary_content': """Lists are mutable, ordered sequences of arbitrary objects. In CPython, lists are implemented as dynamically-sized arrays of object pointers.

### Modifying Lists:
- `lst.append(x)`: Adds item to the end (amortized $O(1)$).
- `lst.extend([a, b])`: Appends all elements from iterable ($O(K)$).
- `lst.insert(0, x)`: Inserts at beginning ($O(N)$ - shifts all elements).
- `lst.pop()`: Removes and returns last element ($O(1)$).
- `lst.pop(0)`: Removes first element ($O(N)$).

### Sorting:
- `lst.sort(reverse=True)`: Sorts the list in place, returns `None`.
- `new_lst = sorted(lst, key=len)`: Leaves original untouched, returns a new sorted list.""",
                        'code_snippet': """# List operations and copy behavior
scores = [88, 95, 72, 100, 64]

scores.append(91)
scores.sort()
print(f"Sorted scores: {scores}")

# Avoid aliasing bug:
original = [1, 2, 3]
alias = original           # Points to same object!
clone = original.copy()    # Creates a separate shallow copy

clone.append(99)
print(f"Original: {original} | Clone: {clone}")""",
                        'key_takeaways': "Lists are mutable and maintain insertion order.\nlist.sort() modifies in-place; sorted(list) creates a new sorted list.\nAppending to the end is O(1); inserting at index 0 is O(N).\nCopying a list with list.copy() prevents accidental mutations of the original.",
                        'resources': [
                            ('Python Lists & Data Structures', 'doc', 'https://docs.python.org/3/tutorial/datastructures.html#more-on-lists', 'Python.org', '15 min read'),
                            ('Python Lists Deep Dive', 'video', 'https://www.youtube.com/watch?v=W8KRzm-HUcc', 'Corey Schafer', '25 mins')
                        ],
                        'practice': {
                            'title': 'Find Second Largest Unique Element',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `second_largest(numbers)` that returns the second largest unique number in a list of integers. Return None if fewer than 2 unique numbers exist.',
                            'starter_code': 'def second_largest(numbers):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Convert to set to remove duplicates, sort descending, and return index 1 if length >= 2.',
                            'solution_code': 'def second_largest(numbers):\n    unique = sorted(list(set(numbers)), reverse=True)\n    return unique[1] if len(unique) >= 2 else None'
                        }
                    },
                    {
                        'title': 'Tuples: Immutability & Unpacking Patterns',
                        'difficulty': 'beginner',
                        'estimated_minutes': 30,
                        'objectives': "Understand tuple immutability and when to choose tuples over lists.\nMaster sequence packing and unpacking (`x, y = point`).\nUse starred expression unpacking (`first, *rest, last = items`).\nUnderstand why tuples can be used as dictionary keys while lists cannot.",
                        'summary_content': """A tuple is an immutable, ordered sequence of elements. Once created, its items cannot be reassigned, added, or removed.

### Why Use Tuples?
1. **Data Integrity**: Protects fixed records (e.g. `(latitude, longitude)`, `(r, g, b)`) from accidental alteration.
2. **Performance**: Smaller memory footprint and faster instantiation than lists.
3. **Hashable**: Since tuples are immutable, they are hashable and can be dictionary keys or set elements (provided all nested elements are also immutable).

### Elegant Unpacking:
```python
user_record = ("Alex", "Chen", 21, "Student", "CA")
first, last, *details = user_record
```""",
                        'code_snippet': """# Tuples and Starred Unpacking
location = (37.7749, -122.4194)  # (lat, lon)
lat, lon = location
print(f"Latitude: {lat}, Longitude: {lon}")

# Starred unpacking
grades = [98, 85, 92, 78, 88, 95]
highest, *middle_grades, lowest = sorted(grades, reverse=True)
print(f"Top: {highest}, Bottom: {lowest}, Rest count: {len(middle_grades)}")""",
                        'key_takeaways': "Tuples are immutable; lists are mutable.\nSingle-element tuples require a trailing comma: (42,).\nTuples can be dictionary keys because they are hashable.\nStarred unpacking (a, *b, c = seq) captures arbitrary middle elements into a list.",
                        'resources': [
                            ('Python Tuples Overview', 'doc', 'https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences', 'Python.org', '10 min read'),
                            ('Lists vs Tuples in Python', 'article', 'https://realpython.com/python-lists-tuples/', 'Real Python', '12 min read')
                        ],
                        'practice': {
                            'title': 'Min, Max and Average Calculator',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `get_stats(numbers)` that returns a tuple of `(min_val, max_val, avg_val)` rounded to 2 decimal places for a non-empty list of numbers.',
                            'starter_code': 'def get_stats(numbers):\n    # Return (min, max, round(avg, 2))\n    pass\n',
                            'solution_hint': 'Use min(numbers), max(numbers), and round(sum(numbers)/len(numbers), 2)',
                            'solution_code': 'def get_stats(numbers):\n    return (min(numbers), max(numbers), round(sum(numbers) / len(numbers), 2))'
                        }
                    },
                    {
                        'title': 'Sets: Uniqueness & Mathematical Set Operations',
                        'difficulty': 'beginner',
                        'estimated_minutes': 35,
                        'objectives': "Understand sets as unordered collections of unique, hashable objects.\nAchieve $O(1)$ average-time membership lookup (`x in my_set`).\nMaster set operations: Union (`|`), Intersection (`&`), Difference (`-`), Symmetric Difference (`^`).\nUse set methods: `.add()`, `.remove()`, `.discard()`, `.issubset()`.",
                        'summary_content': """A Python `set` is an unordered collection that enforces unique elements with $O(1)$ average time complexity for additions, removals, and membership checks (`in`).

### Mathematical Set Operators:
- **Union (`A | B`)**: All elements in either A or B.
- **Intersection (`A & B`)**: Elements present in BOTH A and B.
- **Difference (`A - B`)**: Elements in A that are NOT in B.
- **Symmetric Difference (`A ^ B`)**: Elements in A or B, but NOT in both.

### Removing Elements:
- `s.remove(x)`: Removes `x`, but raises `KeyError` if `x` is not in the set.
- `s.discard(x)`: Removes `x` safely without raising an error if absent.""",
                        'code_snippet': """# Fast deduplication and set math
student_a_skills = {"Python", "Django", "SQL", "Git"}
student_b_skills = {"JavaScript", "React", "Python", "SQL"}

# Common skills (Intersection)
common = student_a_skills & student_b_skills
print(f"Shared skills: {common}")  # {'Python', 'SQL'}

# Skills unique to student A (Difference)
unique_to_a = student_a_skills - student_b_skills
print(f"Unique to Student A: {unique_to_a}")  # {'Django', 'Git'}""",
                        'key_takeaways': "Sets do not preserve order and cannot contain duplicate values.\n'item in my_set' runs in O(1) time vs O(N) for lists.\nUse discard() instead of remove() to avoid KeyError exceptions.\nSet elements must be immutable/hashable.",
                        'resources': [
                            ('Python Sets Guide', 'doc', 'https://docs.python.org/3/tutorial/datastructures.html#sets', 'Python.org', '10 min read'),
                            ('Sets in Python (Comprehensive Guide)', 'article', 'https://realpython.com/python-sets/', 'Real Python', '12 min read')
                        ],
                        'practice': {
                            'title': 'Find Common Prerequisites',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `find_common_topics(course1, course2)` that takes two lists of topic names and returns a sorted list of unique topics present in both courses.',
                            'starter_code': 'def find_common_topics(course1, course2):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Convert both lists to sets, find intersection &, and return sorted(list(intersection)).',
                            'solution_code': 'def find_common_topics(course1, course2):\n    return sorted(list(set(course1) & set(course2)))'
                        }
                    },
                    {
                        'title': 'Dictionaries: Hash Maps, Lookups & Iteration',
                        'difficulty': 'beginner',
                        'estimated_minutes': 45,
                        'objectives': "Understand Python dictionaries as hash tables with $O(1)$ key lookups.\nSafely retrieve values using `.get(key, default)` without throwing KeyError.\nMaster dictionary iteration: `.keys()`, `.values()`, and `.items()`.\nUse dictionary methods: `.setdefault()`, `.update()`, `.pop()`, and `dict | other_dict` (Python 3.9+ union).",
                        'summary_content': """Dictionaries (`dict`) are mutable collections of `key: value` pairs. Under the hood, Python dicts are compact hash tables with preserved insertion order (Python 3.7+).

### Safe Lookups:
Never access unknown keys with `data["key"]` unless you want a `KeyError`.
Use `data.get("key", default_value)`.

### Iterating Dictionaries:
```python
for key, value in user_dict.items():
    print(f"{key} -> {value}")
```

### Merging Dictionaries (Python 3.9+):
```python
defaults = {"theme": "light", "notifications": True}
user_prefs = {"theme": "dark"}
final_settings = defaults | user_prefs  # {'theme': 'dark', 'notifications': True}
```""",
                        'code_snippet': """# Dictionary operations showcase
student = {
    "name": "Alex",
    "track": "Python Backend",
    "completed_topics": 12,
}

# Safe lookup with default
badge = student.get("badge", "Starter Explorer")
print(f"Badge: {badge}")

# Word frequency counter using dict.get()
text = "python is great and python is fun"
word_counts = {}
for word in text.split():
    word_counts[word] = word_counts.get(word, 0) + 1

print(f"Word counts: {word_counts}")""",
                        'key_takeaways': "Dict keys must be immutable/hashable; values can be any type.\nUse dict.get(key, default) for safe retrieval.\nUse dict.items() for unpacking both keys and values in loops.\ndict1 | dict2 creates a merged dictionary in Python 3.9+.",
                        'resources': [
                            ('Python Dictionaries Tutorial', 'doc', 'https://docs.python.org/3/tutorial/datastructures.html#dictionaries', 'Python.org', '15 min read'),
                            ('Mastering Python Dictionaries', 'video', 'https://www.youtube.com/watch?v=daefaLgNkw0', 'Corey Schafer', '20 mins')
                        ],
                        'practice': {
                            'title': 'Frequency Counter for Error Logs',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `count_errors(log_entries)` that takes a list of error strings (e.g. ["404", "500", "404", "403"]) and returns a dictionary of error counts sorted by count descending.',
                            'starter_code': 'def count_errors(log_entries):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Count items using dict.get() or collections.Counter, then sort by value.',
                            'solution_code': 'def count_errors(log_entries):\n    counts = {}\n    for entry in log_entries:\n        counts[entry] = counts.get(entry, 0) + 1\n    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))'
                        }
                    }
                ]
            },
            {
                'level_number': 4,
                'title': 'Functions & Modular Code',
                'tagline': 'Write clean, reusable, testable code with Python functions and scoping rules.',
                'description': 'Master parameters, positional vs keyword arguments, variable argument unpacking (*args, **kwargs), return semantics, the LEGB scope model, and lambda functions.',
                'topics': [
                    {
                        'title': 'Defining Functions, Calling & Docstrings',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 35,
                        'objectives': "Define clean, single-responsibility functions using `def`.\nDocument functions using Google-style or PEP 257 docstrings.\nUse Python type hints (PEP 484) for parameters and return types.\nUnderstand function objects as first-class citizens in Python.",
                        'summary_content': """Functions are reusable blocks of organized code designed to perform a single logical task.

### Anatomy of a Professional Python Function:
```python
def calculate_discount(price: float, discount_percent: float = 10.0) -> float:
    \"\"\"
    Calculates the final discounted price.
    
    Args:
        price (float): Original item price.
        discount_percent (float): Discount percentage between 0 and 100.
        
    Returns:
        float: Price after applying the discount.
    \"\"\"
    if not (0 <= discount_percent <= 100):
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```""",
                        'code_snippet': """# Function with type hints and docstrings
def format_user_badge(username: str, score: int) -> str:
    \"\"\"Returns a formatted badge string based on score tier.\"\"\"
    tier = "Master" if score >= 90 else "Practitioner" if score >= 60 else "Novice"
    return f"[{tier}] {username.strip().title()}"

print(format_user_badge("alex_chen", 95))""",
                        'key_takeaways': "Functions should do one thing and do it well (Single Responsibility Principle).\nUse type hints to document expected input and return types.\nWrite docstrings to explain what the function does, its parameters, and return values.",
                        'resources': [
                            ('Python Functions Tutorial', 'doc', 'https://docs.python.org/3/tutorial/controlflow.html#defining-functions', 'Python.org', '15 min read'),
                            ('Docstrings and Type Hints in Python', 'article', 'https://realpython.com/documenting-python-code/', 'Real Python', '12 min read')
                        ],
                        'practice': {
                            'title': 'Email Validator Function',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `is_valid_email(email: str) -> bool` that checks if the string contains exactly one "@" symbol, has a dot "." after the "@", and has non-empty text before and after.',
                            'starter_code': 'def is_valid_email(email: str) -> bool:\n    # Write logic\n    pass\n',
                            'solution_hint': 'Check email.count("@") == 1, split on "@", verify user part and domain part containing "."',
                            'solution_code': 'def is_valid_email(email: str) -> bool:\n    if email.count("@") != 1:\n        return False\n    user, domain = email.split("@")\n    return bool(user) and ("." in domain) and not domain.startswith(".") and not domain.endswith(".")'
                        }
                    },
                    {
                        'title': 'Parameters, Arguments, *args & **kwargs',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 40,
                        'objectives': "Differentiate between positional arguments, keyword arguments, and default parameters.\nAvoid the dangerous mutable default argument trap (`def f(lst=[])`).\nMaster `*args` to accept arbitrary positional arguments as a tuple.\nMaster `**kwargs` to accept arbitrary keyword arguments as a dictionary.",
                        'summary_content': """Python gives extraordinary flexibility in parameter passing.

### The Mutable Default Trap (CRITICAL BUG TO AVOID):
```python
# BROKEN: list is shared across all function calls!
def add_item(item, basket=[]): 
    basket.append(item)
    return basket

# CORRECT: Use None as default and instantiate inside
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

### `*args` and `**kwargs`:
- `*args`: Collects extra positional arguments into a `tuple`.
- `**kwargs`: Collects extra keyword arguments into a `dict`.""",
                        'code_snippet': """# Flexible API builder using *args and **kwargs
def create_query(table: str, *columns, **filters):
    cols = ", ".join(columns) if columns else "*"
    conditions = " AND ".join([f"{k} = '{v}'" for k, v in filters.items()])
    query = f"SELECT {cols} FROM {table}"
    if conditions:
        query += f" WHERE {conditions}"
    return query

sql = create_query("users", "id", "username", "email", status="active", role="student")
print(sql)
# SELECT id, username, email FROM users WHERE status = 'active' AND role = 'student'""",
                        'key_takeaways': "NEVER use mutable objects ([], {}) as default argument values; use None instead.\n*args receives extra positional arguments as a tuple.\n**kwargs receives extra named keyword arguments as a dictionary.",
                        'resources': [
                            ('Python *args and **kwargs Explained', 'article', 'https://realpython.com/python-kwargs-and-args/', 'Real Python', '12 min read'),
                            ('Default Argument Pitfalls in Python', 'doc', 'https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments', 'Hitchhiker Guide', '8 min read')
                        ],
                        'practice': {
                            'title': 'Custom Logger with Variable Arguments',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `build_log(level, *messages, **metadata)` that formats a log string like "[LEVEL] msg1 | msg2 | meta_key=meta_val".',
                            'starter_code': 'def build_log(level, *messages, **metadata):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Join messages with " | " and join metadata items with "=". Format into f"[{level.upper()}] ..."',
                            'solution_code': 'def build_log(level, *messages, **metadata):\n    msg_part = " | ".join(str(m) for m in messages)\n    meta_part = " | ".join(f"{k}={v}" for k, v in metadata.items())\n    parts = [p for p in [msg_part, meta_part] if p]\n    return f"[{level.upper()}] " + " | ".join(parts)'
                        }
                    },
                    {
                        'title': 'Return Values, Multiple Returns & NoneType',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 30,
                        'objectives': "Understand that every Python function returns a value (`None` if no `return` is executed).\nReturn multiple values cleanly as packed tuples.\nUse early return / guard clause patterns to flatten nested if-statements.",
                        'summary_content': """In Python, when a function reaches the end of its body without encountering an explicit `return` statement, it implicitly returns `None`.

### Returning Multiple Values:
When you write `return a, b, c`, Python packs them into a single tuple `(a, b, c)`. The caller can unpack them directly:
```python
def divide_with_remainder(dividend, divisor):
    quotient = dividend // divisor
    remainder = dividend % divisor
    return quotient, remainder

q, r = divide_with_remainder(17, 5) # q=3, r=2
```

### Guard Clauses (Flatten Your Code):
Instead of deeply nesting `if-else` blocks, check error conditions first and return early.""",
                        'code_snippet': """# Guard clause pattern for clean code
def process_refund(user, transaction_id, amount):
    if not user.is_authenticated:
        return False, "Authentication required"
    if amount <= 0:
        return False, "Invalid refund amount"
    if not transaction_id:
        return False, "Transaction ID missing"
    
    # Process refund...
    return True, "Refund processed successfully"

success, msg = process_refund(demo_user, "TXN-902", 45.0)
print(f"Status: {success} - {msg}")""",
                        'key_takeaways': "Multiple returns return a tuple behind the scenes.\nFunctions without a return statement return None.\nUse guard clauses to exit early and avoid deeply nested if-else ladders.",
                        'resources': [
                            ('Python Return Statements Guide', 'article', 'https://realpython.com/python-return-statement/', 'Real Python', '10 min read'),
                            ('Refactoring: Replace Nested Conditional with Guard Clauses', 'article', 'https://refactoring.guru/replace-nested-conditional-with-guard-clauses', 'Refactoring Guru', '6 min read')
                        ],
                        'practice': {
                            'title': 'Min-Max Normalizer',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `normalize_scores(scores)` that finds min and max, and returns a tuple `(normalized_list, min_val, max_val)` where each score is scaled between 0.0 and 1.0. If all scores are equal, normalized list should be all 0.0s.',
                            'starter_code': 'def normalize_scores(scores):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Scale formula: (x - min_v) / (max_v - min_v) if max_v != min_v else 0.0',
                            'solution_code': 'def normalize_scores(scores):\n    if not scores:\n        return [], 0, 0\n    min_v, max_v = min(scores), max(scores)\n    diff = max_v - min_v\n    normalized = [round((x - min_v) / diff, 2) if diff != 0 else 0.0 for x in scores]\n    return normalized, min_v, max_v'
                        }
                    },
                    {
                        'title': 'Variable Scope & the LEGB Rule',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 35,
                        'objectives': "Master Python's LEGB scope lookup order: Local -> Enclosing -> Global -> Built-in.\nUnderstand when and why to avoid the `global` keyword.\nUse `nonlocal` inside nested closures.\nIdentify and resolve `UnboundLocalError`.",
                        'summary_content': """Scope determines where a variable is visible and accessible in your code.

### The LEGB Rule:
When Python looks up a variable name, it searches in this exact order:
1. **L - Local**: Variables defined inside the current function.
2. **E - Enclosing**: Variables in outer enclosing functions (in nested functions/closures).
3. **G - Global**: Module-level variables defined at the top level of the file.
4. **B - Built-in**: Python's pre-loaded symbols (`len`, `range`, `print`, `int`, etc.).

### Modifying Outer Variables:
- `global var_name`: Allows modifying a global variable from inside a function (use sparingly!).
- `nonlocal var_name`: Allows modifying a variable in the enclosing outer function from an inner closure.""",
                        'code_snippet': """# Closure using nonlocal
def make_counter(start=0):
    count = start
    def increment(step=1):
        nonlocal count
        count += step
        return count
    return increment

counter = make_counter(10)
print(counter())  # 11
print(counter(5)) # 16""",
                        'key_takeaways': "LEGB order: Local -> Enclosing -> Global -> Built-in.\nIf you assign to a variable inside a function, Python treats it as local unless declared global or nonlocal.\nAvoid global state in favor of parameters and return values.",
                        'resources': [
                            ('Python Scope & the LEGB Rule', 'article', 'https://realpython.com/python-scope-legb-rule/', 'Real Python', '14 min read'),
                            ('Closures and Variable Scopes', 'video', 'https://www.youtube.com/watch?v=swU3cBab408', 'Corey Schafer', '15 mins')
                        ],
                        'practice': {
                            'title': 'Stateful Running Average Generator',
                            'difficulty': 'medium',
                            'prompt_description': 'Create a function `make_averager()` that returns an inner function `averager(new_value)` which keeps track of the running total and count across calls and returns the current running average.',
                            'starter_code': 'def make_averager():\n    # Use closures and nonlocal or mutable list\n    pass\n',
                            'solution_hint': 'Initialize total = 0, count = 0, and use nonlocal in the inner function.',
                            'solution_code': 'def make_averager():\n    total = 0\n    count = 0\n    def averager(new_value):\n        nonlocal total, count\n        total += new_value\n        count += 1\n        return round(total / count, 2)\n    return averager'
                        }
                    },
                    {
                        'title': 'Lambda Functions, map(), filter() & sorted()',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 35,
                        'objectives': "Write concise anonymous single-expression functions with `lambda`.\nUse `sorted(iterable, key=lambda ...)` for complex sorting criteria.\nUnderstand `map()` and `filter()` and when list comprehensions are more readable.\nSort lists of dictionaries by custom keys.",
                        'summary_content': """A `lambda` is an anonymous inline function defined with `lambda args: expression`.

### Syntax:
`lambda x, y: x + y`

### Best Use Case for Lambdas: Custom Sort Keys
```python
students = [
    {"name": "Alex", "gpa": 3.8},
    {"name": "Maya", "gpa": 3.95},
    {"name": "Rahul", "gpa": 3.6},
]

# Sort by GPA descending
sorted_students = sorted(students, key=lambda s: s["gpa"], reverse=True)
```

### Comprehensions vs map/filter:
In modern Python, list comprehensions are generally preferred over `map()` and `filter()` for readability:
- `[x * 2 for x in nums]` (better than `map(lambda x: x*2, nums)`)
- `[x for x in nums if x > 0]` (better than `filter(lambda x: x>0, nums)`)""",
                        'code_snippet': """# Multi-key sorting with lambdas
products = [
    {"name": "Laptop", "category": "Tech", "price": 999},
    {"name": "Mouse", "category": "Tech", "price": 25},
    {"name": "Desk", "category": "Furniture", "price": 250},
    {"name": "Chair", "category": "Furniture", "price": 150},
]

# Sort by Category alphabetically, then by Price ascending
sorted_products = sorted(products, key=lambda p: (p["category"], p["price"]))
for p in sorted_products:
    print(f"[{p['category']}] {p['name']}: ${p['price']}")""",
                        'key_takeaways': "Lambda functions are restricted to a single expression.\nTheir most common and idiomatic use is as the key argument in sorted(), min(), and max().\nFor general transformations, list comprehensions are preferred over map() and filter().",
                        'resources': [
                            ('Python Lambda Functions Explained', 'article', 'https://realpython.com/python-lambda/', 'Real Python', '12 min read'),
                            ('Sorting How-To in Python', 'doc', 'https://docs.python.org/3/howto/sorting.html', 'Python.org', '15 min read')
                        ],
                        'practice': {
                            'title': 'Sort Students by Multiple Criteria',
                            'difficulty': 'medium',
                            'prompt_description': 'Given a list of student tuples `(name, grade_level, gpa)`, sort them primarily by `grade_level` descending (12 to 9), and secondarily by `gpa` descending.',
                            'starter_code': 'def sort_student_roster(students):\n    # Return sorted list\n    pass\n',
                            'solution_hint': 'Use sorted(students, key=lambda s: (-s[1], -s[2]))',
                            'solution_code': 'def sort_student_roster(students):\n    return sorted(students, key=lambda s: (-s[1], -s[2]))'
                        }
                    }
                ]
            },
            {
                'level_number': 5,
                'title': 'Intermediate Python & Robust Code',
                'tagline': 'Master file handling, context managers, exception hierarchies, and comprehensions.',
                'description': 'Bridge the gap between scripting and professional engineering: handle real-world filesystem operations safely, catch specific errors, and construct high-performance comprehensions.',
                'topics': [
                    {
                        'title': 'Modules, Packages & __name__ == "__main__"',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 35,
                        'objectives': "Understand how Python finds modules using `sys.path`.\nStructure reusable code with packages and `__init__.py`.\nMaster the `if __name__ == '__main__':` execution guard.\nAvoid circular import dependencies.",
                        'summary_content': """A **module** is simply a Python file (`.py`). A **package** is a directory containing modules and an `__init__.py` file.

### Why `if __name__ == "__main__":` is Essential:
When Python runs a file directly, it sets the special variable `__name__ = "__main__"`.
When the file is imported by another script (`import my_module`), `__name__` is set to the module's actual name (`"my_module"`).

Using this guard ensures that test code or script execution does not accidentally execute when someone imports functions from your file!""",
                        'code_snippet': """# math_utils.py module architecture
\"\"\"Reusable math helpers for learning applications.\"\"\"

def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b

# Code inside here runs ONLY when executed directly, NOT when imported
if __name__ == "__main__":
    print("Running internal self-tests...")
    assert add(2, 3) == 5
    assert multiply(4, 5) == 20
    print("All unit checks passed!")""",
                        'key_takeaways': "Every Python file is a module; directories with __init__.py are packages.\n__name__ is '__main__' only when the script is run directly from the command line.\nAlways use the name guard to prevent side-effects during imports.",
                        'resources': [
                            ('Python Modules and Packages Tutorial', 'doc', 'https://docs.python.org/3/tutorial/modules.html', 'Python.org', '15 min read'),
                            ('What Does if __name__ == "__main__" Do?', 'article', 'https://realpython.com/if-name-main-python/', 'Real Python', '8 min read')
                        ],
                        'practice': {
                            'title': 'Config Loader Module Pattern',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `parse_env_line(line)` that takes a string like "PORT=8000" or "DEBUG=True", strips whitespace, and returns a tuple `(key, value)`. Ignore empty lines or comments starting with "#".',
                            'starter_code': 'def parse_env_line(line):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Check if line is empty or starts with "#". Then split on "=" with maxsplit=1.',
                            'solution_code': 'def parse_env_line(line):\n    cleaned = line.strip()\n    if not cleaned or cleaned.startswith("#") or "=" not in cleaned:\n        return None\n    key, val = cleaned.split("=", 1)\n    return key.strip(), val.strip()'
                        }
                    },
                    {
                        'title': 'File Handling & Context Managers (with open)',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 40,
                        'objectives': "Read and write text files using `'r'`, `'w'`, `'a'`, and `'r+'` modes.\nUnderstand why context managers (`with open(...) as f:`) prevent resource leaks.\nIterate over large files line-by-line efficiently without loading entire files into RAM.\nUse `pathlib.Path` for cross-platform file path management.",
                        'summary_content': """File operations must always properly close OS file descriptors to prevent memory leaks and file lock errors.

### The `with` Statement (Context Manager):
The `with` statement automatically guarantees that `f.close()` is called when the block finishes—even if an exception occurs inside!

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:  # Memory efficient line-by-line streaming!
        process(line)
```

### Modern `pathlib`:
Use Python's built-in `pathlib.Path` instead of old `os.path`:
```python
from pathlib import Path
file_path = Path("reports") / "2026" / "summary.csv"
file_path.parent.mkdir(parents=True, exist_ok=True)
```""",
                        'code_snippet': """# Safe file reading and writing with pathlib
from pathlib import Path

data_dir = Path("scratch")
data_dir.mkdir(exist_ok=True)
log_file = data_dir / "app.log"

# Writing lines
with open(log_file, "w", encoding="utf-8") as f:
    f.write("[INFO] System initialized\n")
    f.write("[WARNING] High memory usage\n")

# Reading lines safely
if log_file.exists():
    with open(log_file, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            print(f"Line {idx}: {line.strip()}")""",
                        'key_takeaways': "Always open files using the 'with open(...) as f:' context manager.\nAlways specify encoding='utf-8' to avoid platform encoding bugs.\nIterating 'for line in f:' streams lines one-at-a-time with O(1) memory.\nUse pathlib.Path for clean, cross-platform path manipulation.",
                        'resources': [
                            ('Reading and Writing Files in Python', 'doc', 'https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files', 'Python.org', '15 min read'),
                            ('Python pathlib: Tame the File System', 'article', 'https://realpython.com/python-pathlib/', 'Real Python', '12 min read')
                        ],
                        'practice': {
                            'title': 'Word & Line Counter Utility',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `analyze_text_content(content_str)` that returns a dictionary `{"lines": num_lines, "words": num_words, "chars": num_chars}` for a given multi-line string.',
                            'starter_code': 'def analyze_text_content(content_str):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Use content_str.splitlines() for lines and content_str.split() for words.',
                            'solution_code': 'def analyze_text_content(content_str):\n    lines = content_str.splitlines()\n    words = content_str.split()\n    return {\n        "lines": len(lines),\n        "words": len(words),\n        "chars": len(content_str)\n    }'
                        }
                    },
                    {
                        'title': 'Exception Handling: try, except, else & finally',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 45,
                        'objectives': "Master the complete exception handling lifecycle (`try`, `except`, `else`, `finally`).\nCatch specific exceptions rather than using bare `except:` clauses.\nRaise custom exceptions using `raise ValueError(...)`.\nUnderstand the Python built-in exception hierarchy.",
                        'summary_content': """Exceptions represent runtime errors that disrupt the normal flow of execution.

### The 4 Blocks of Exception Handling:
1. **`try`**: Code that might trigger an exception.
2. **`except SpecificError as e`**: Handles that specific error type.
3. **`else`**: Runs **only if NO exception occurred** in the `try` block.
4. **`finally`**: Runs **always**, whether an exception occurred or not (used for cleanup).

### Best Practices:
- **Never use bare `except:`** (it catches `KeyboardInterrupt` and `SystemExit`, making programs impossible to terminate!).
- Keep `try` blocks as small as possible.""",
                        'code_snippet': """# Professional exception handling pattern
def calculate_ratio(numerator, denominator):
    try:
        num = float(numerator)
        den = float(denominator)
        result = num / den
    except ValueError as err:
        print(f"Invalid numeric input: {err}")
        return None
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    else:
        print("Calculation completed successfully.")
        return result
    finally:
        print("Ratio calculation attempt logged.")

print(calculate_ratio(10, 2))""",
                        'key_takeaways': "Catch specific exceptions like FileNotFoundError, ValueError, KeyError instead of generic Exception.\nThe 'else' block executes only when the try block succeeds without errors.\nThe 'finally' block is guaranteed to run, making it ideal for closing connections.\nRaise informative exceptions using raise ValueError('message').",
                        'resources': [
                            ('Python Errors and Exceptions', 'doc', 'https://docs.python.org/3/tutorial/errors.html', 'Python.org', '15 min read'),
                            ('Python Exceptions: An In-Depth Tutorial', 'article', 'https://realpython.com/python-exceptions/', 'Real Python', '14 min read')
                        ],
                        'practice': {
                            'title': 'Safe Key-Value Dictionary Extractor',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `safe_nested_lookup(d, *keys, default=None)` that traverses nested dictionaries safely without crashing if intermediate keys are missing or not dictionaries.',
                            'starter_code': 'def safe_nested_lookup(d, *keys, default=None):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Loop over keys with a current = d pointer, wrap access in try-except (KeyError, TypeError).',
                            'solution_code': 'def safe_nested_lookup(d, *keys, default=None):\n    current = d\n    for k in keys:\n        try:\n            current = current[k]\n        except (KeyError, TypeError, IndexError):\n            return default\n    return current'
                        }
                    },
                    {
                        'title': 'List, Dictionary & Set Comprehensions',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 40,
                        'objectives': "Master list comprehensions: `[expr for item in iterable if condition]`.\nBuild dictionary comprehensions: `{k: v for item in iterable}`.\nCreate set comprehensions: `{expr for item in iterable}`.\nAvoid overly complex nested comprehensions that sacrifice readability.",
                        'summary_content': """Comprehensions provide a concise, readable, and highly-optimized syntax for creating new collections from existing iterables.

### Syntax Patterns:
- **List Comprehension**: `[x**2 for x in numbers if x % 2 == 0]`
- **Dict Comprehension**: `{user.id: user.name for user in users if user.is_active}`
- **Set Comprehension**: `{word.lower() for word in text.split()}`

### Performance Note:
Comprehensions execute at C-speed in CPython because bytecode optimization avoids repeated method lookup overhead (like `.append()`).""",
                        'code_snippet': """# Modern comprehensions in action
topics = ["Variables", "Loops", "Functions", "OOP", "APIs"]

# List comprehension with filtering and transformation
short_topics = [t.upper() for t in topics if len(t) <= 4]
print(f"Short topics: {short_topics}")  # ['OOP', 'APIS']

# Dict comprehension: mapping topic name to its length
topic_lengths = {t: len(t) for t in topics}
print(f"Topic lengths: {topic_lengths}")

# Flattening a 2D matrix
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(f"Flattened: {flat}")  # [1, 2, 3, 4, 5, 6]""",
                        'key_takeaways': "Comprehensions are faster and more Pythonic than building lists with empty lists and loops.\nInclude 'if condition' at the end for filtering.\nKeep comprehensions readable: if a comprehension exceeds 2 lines, refactor to a standard loop.",
                        'resources': [
                            ('List Comprehensions in Python', 'article', 'https://realpython.com/list-comprehension-python/', 'Real Python', '12 min read'),
                            ('Python Data Structures Tutorial', 'doc', 'https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions', 'Python.org', '10 min read')
                        ],
                        'practice': {
                            'title': 'Filter and Invert Dictionary',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `invert_dict(d)` using a dict comprehension that swaps keys and values, but only for keys whose values are strings.',
                            'starter_code': 'def invert_dict(d):\n    # Use dict comprehension\n    pass\n',
                            'solution_hint': '{v: k for k, v in d.items() if isinstance(v, str)}',
                            'solution_code': 'def invert_dict(d):\n    return {v: k for k, v in d.items() if isinstance(v, str)}'
                        }
                    },
                    {
                        'title': 'Working with JSON & Python Dictionaries',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 35,
                        'objectives': "Serialize Python objects to JSON strings using `json.dumps()`.\nDeserialize JSON strings to Python objects using `json.loads()`.\nRead and write JSON files directly with `json.dump()` and `json.load()`.\nFormat pretty-printed JSON with `indent=2`.",
                        'summary_content': """JSON (JavaScript Object Notation) is the universal format for REST APIs and configuration files. Python's built-in `json` module provides seamless two-way conversion.

### Conversion Mapping:
- JSON `{}` $\longleftrightarrow$ Python `dict`
- JSON `[]` $\longleftrightarrow$ Python `list`
- JSON `"string"` $\longleftrightarrow$ Python `str`
- JSON `123.4` $\longleftrightarrow$ Python `float` / `int`
- JSON `true` / `false` $\longleftrightarrow$ Python `True` / `False`
- JSON `null` $\longleftrightarrow$ Python `None`

### Methods:
- `json.loads(s)`: Load from **s**tring.
- `json.dumps(obj, indent=2)`: Dump to **s**tring.
- `json.load(f)`: Load from **f**ile.
- `json.dump(obj, f)`: Dump to **f**ile.""",
                        'code_snippet': """import json

student_profile = {
    "student_id": 1042,
    "name": "Alex Chen",
    "skills": ["Python", "Django", "SQL"],
    "is_graduated": False,
    "mentor": None
}

# Convert Python dict to formatted JSON string
json_string = json.dumps(student_profile, indent=2)
print("Serialized JSON:\n", json_string)

# Parse JSON string back to Python dict
parsed_data = json.loads(json_string)
print("Parsed Name:", parsed_data["name"])""",
                        'key_takeaways': "json.loads() and json.dumps() work with strings (s stands for string).\njson.load() and json.dump() work directly with file objects.\nJSON null maps to Python None; JSON true/false map to Python True/False.",
                        'resources': [
                            ('Python JSON Module Documentation', 'doc', 'https://docs.python.org/3/library/json.html', 'Python.org', '12 min read'),
                            ('Working with JSON Data in Python', 'article', 'https://realpython.com/python-json/', 'Real Python', '14 min read')
                        ],
                        'practice': {
                            'title': 'API Response Parser',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `extract_usernames(json_response_str)` that parses a JSON string containing a list of user objects `[{"id": 1, "username": "alex"}, ...]` and returns a list of all usernames.',
                            'starter_code': 'import json\n\ndef extract_usernames(json_response_str):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Use json.loads() and a list comprehension [u["username"] for u in users if "username" in u]',
                            'solution_code': 'import json\n\ndef extract_usernames(json_response_str):\n    try:\n        data = json.loads(json_response_str)\n        return [item["username"] for item in data if isinstance(item, dict) and "username" in item]\n    except (json.JSONDecodeError, TypeError):\n        return []'
                        }
                    }
                ]
            },
            {
                'level_number': 6,
                'title': 'Object-Oriented Programming (OOP)',
                'tagline': 'Model complex real-world systems with classes, inheritance, dunder methods, and encapsulation.',
                'description': 'Master the four pillars of OOP in Python: Encapsulation, Abstraction, Inheritance, and Polymorphism. Learn how self works, write clean constructors, and leverage Python magic methods.',
                'topics': [
                    {
                        'title': 'Classes, Objects & the self Parameter',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 45,
                        'objectives': "Understand classes as blueprints and objects as stateful instances.\nUnderstand what `self` represents (the explicit instance pointer passed to methods).\nInstantiate objects and access attributes and methods.\nUnderstand how Python transforms `obj.method()` into `Class.method(obj)` behind the scenes.",
                        'summary_content': """Object-Oriented Programming allows you to bundle related data (attributes) and behavior (methods) together into cohesive entities called **objects**.

### The `self` Parameter:
In Python, instance methods always take `self` as their first parameter. `self` is a reference to the specific instance currently invoking the method.

```python
class Student:
    def study(self, topic: str):
        print(f"{self.name} is studying {topic}!")
```

When you call `alex.study("Python")`, Python internally executes `Student.study(alex, "Python")`.""",
                        'code_snippet': """# Defining a clean Python class
class LearningGoal:
    def __init__(self, title: str, target_hours: int):
        self.title = title
        self.target_hours = target_hours
        self.hours_completed = 0
    
    def log_study(self, hours: int):
        self.hours_completed += hours
        progress_pct = (self.hours_completed / self.target_hours) * 100
        print(f"Logged {hours} hrs for {self.title}. Progress: {progress_pct:.1f}%")

goal = LearningGoal("Python Master Path", 60)
goal.log_study(15)""",
                        'key_takeaways': "A class is the blueprint; an object is an individual instance of that class.\nself explicitly passes the current instance to instance methods.\nInstance attributes are stored in the instance's __dict__ namespace.",
                        'resources': [
                            ('Python Classes and OOP Tutorial', 'doc', 'https://docs.python.org/3/tutorial/classes.html', 'Python.org', '15 min read'),
                            ('Object-Oriented Programming in Python', 'article', 'https://realpython.com/python3-object-oriented-programming/', 'Real Python', '16 min read')
                        ],
                        'practice': {
                            'title': 'Bank Account Class Implementation',
                            'difficulty': 'easy',
                            'prompt_description': 'Create a `BankAccount` class with an `owner` string and `balance` float. Include `deposit(amount)` and `withdraw(amount)` methods. Prevent withdrawing more than the current balance.',
                            'starter_code': 'class BankAccount:\n    # Implement constructor, deposit, withdraw\n    pass\n',
                            'solution_hint': 'Initialize self.owner and self.balance. In withdraw, check if amount <= self.balance.',
                            'solution_code': 'class BankAccount:\n    def __init__(self, owner: str, balance: float = 0.0):\n        self.owner = owner\n        self.balance = float(balance)\n    \n    def deposit(self, amount: float):\n        if amount > 0:\n            self.balance += amount\n        return self.balance\n        \n    def withdraw(self, amount: float):\n        if 0 < amount <= self.balance:\n            self.balance -= amount\n            return True\n        return False'
                        }
                    },
                    {
                        'title': 'Constructors (__init__) & Instance vs Class Attributes',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 40,
                        'objectives': "Master the `__init__` constructor method for initializing instance state.\nDifferentiate between Instance Attributes (unique per object) and Class Attributes (shared across all instances).\nAvoid the shared mutable class attribute trap.\nUse `@classmethod` and `@staticmethod` appropriately.",
                        'summary_content': """When an object is created (`obj = MyClass()`), Python calls `__new__` to allocate memory, and then `__init__` to initialize its attributes.

### Instance vs Class Attributes:
- **Instance Attribute**: Defined on `self` inside `__init__`. Unique to each instance.
- **Class Attribute**: Defined directly inside the class body. Shared across **all** instances of that class.

```python
class Course:
    platform_name = "LearningHub" # Class attribute (shared)
    
    def __init__(self, title):
        self.title = title        # Instance attribute (unique)
```""",
                        'code_snippet': """# Instance vs Class Attributes in Practice
class StudentTracker:
    # Class attribute: tracks total students across the platform
    total_registered = 0
    
    def __init__(self, username: str):
        self.username = username # Instance attribute
        StudentTracker.total_registered += 1
    
    @classmethod
    def get_community_size(cls):
        return f"Total students enrolled: {cls.total_registered}"

s1 = StudentTracker("Alex")
s2 = StudentTracker("Maya")
print(StudentTracker.get_community_size()) # Total students enrolled: 2""",
                        'key_takeaways': "Instance attributes belong to self; class attributes belong to the class.\nDo not use mutable class attributes (like class-level lists) unless intentionally sharing state.\nClass methods use @classmethod and take cls as their first argument.",
                        'resources': [
                            ('Python Class Attributes vs Instance Attributes', 'article', 'https://realpython.com/lessons/class-and-instance-attributes/', 'Real Python', '10 min read'),
                            ('Classmethods and Staticmethods', 'video', 'https://www.youtube.com/watch?v=rq8cL2XMM5M', 'Corey Schafer', '15 mins')
                        ],
                        'practice': {
                            'title': 'Inventory Item with Low Stock Counter',
                            'difficulty': 'medium',
                            'prompt_description': 'Create an `Item` class with instance attributes `name`, `stock_quantity`, and `reorder_threshold`. Add a class attribute `low_stock_items = []`. Whenever an item is instantiated with `stock_quantity <= reorder_threshold`, add its name to `low_stock_items`.',
                            'starter_code': 'class Item:\n    low_stock_items = []\n    # Implement constructor\n',
                            'solution_hint': 'In __init__, check if stock_quantity <= reorder_threshold, then Item.low_stock_items.append(self.name)',
                            'solution_code': 'class Item:\n    low_stock_items = []\n    def __init__(self, name: str, stock_quantity: int, reorder_threshold: int = 5):\n        self.name = name\n        self.stock_quantity = stock_quantity\n        self.reorder_threshold = reorder_threshold\n        if self.stock_quantity <= self.reorder_threshold:\n            Item.low_stock_items.append(self.name)'
                        }
                    },
                    {
                        'title': 'Inheritance, Method Overriding & super()',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 45,
                        'objectives': "Implement single and multi-level inheritance to eliminate code duplication.\nOverride parent class methods to provide specialized behavior in child classes.\nUse `super().__init__(...)` to cleanly delegate initialization to parent classes.\nCheck inheritance relationships with `isinstance()` and `issubclass()`.",
                        'summary_content': """Inheritance enables a child class to inherit attributes and methods from a parent class, promoting code reuse.

### The `super()` Function:
`super()` provides a clean way to access methods from the parent class without hardcoding the parent class name:

```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class Mentor(User):
    def __init__(self, username, email, specialty):
        super().__init__(username, email) # Initialize base attributes
        self.specialty = specialty
```""",
                        'code_snippet': """# Inheritance in action
class CourseResource:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url
    
    def get_summary(self):
        return f"{self.title} ({self.url})"

class VideoResource(CourseResource):
    def __init__(self, title: str, url: str, duration_minutes: int):
        super().__init__(title, url)
        self.duration_minutes = duration_minutes
    
    # Method overriding
    def get_summary(self):
        return f"[VIDEO - {self.duration_minutes}m] {self.title}"

vid = VideoResource("Python OOP Breakdown", "https://learninghub.dev/v/101", 18)
print(vid.get_summary())""",
                        'key_takeaways': "Inheritance promotes 'is-a' relationships (VideoResource is-a CourseResource).\nAlways call super().__init__() in the child class constructor.\nUse method overriding when a child class requires specialized behavior.",
                        'resources': [
                            ('Inheritance in Python OOP', 'doc', 'https://docs.python.org/3/tutorial/classes.html#inheritance', 'Python.org', '12 min read'),
                            ('Supercharge Your Classes With Python super()', 'article', 'https://realpython.com/python-super/', 'Real Python', '15 min read')
                        ],
                        'practice': {
                            'title': 'Employee and Manager Hierarchy',
                            'difficulty': 'easy',
                            'prompt_description': 'Create a base `Employee` class (`name`, `base_salary`) with method `get_total_compensation()`. Create a child `Manager` class that adds `bonus_pct` (e.g. 0.20) and overrides `get_total_compensation()` using super().',
                            'starter_code': 'class Employee:\n    pass\n\nclass Manager(Employee):\n    pass\n',
                            'solution_hint': 'In Manager, return super().get_total_compensation() * (1 + self.bonus_pct)',
                            'solution_code': 'class Employee:\n    def __init__(self, name: str, base_salary: float):\n        self.name = name\n        self.base_salary = base_salary\n    def get_total_compensation(self):\n        return self.base_salary\n\nclass Manager(Employee):\n    def __init__(self, name: str, base_salary: float, bonus_pct: float = 0.15):\n        super().__init__(name, base_salary)\n        self.bonus_pct = bonus_pct\n    def get_total_compensation(self):\n        return super().get_total_compensation() * (1 + self.bonus_pct)'
                        }
                    },
                    {
                        'title': 'Polymorphism & Magic / Dunder Methods',
                        'difficulty': 'advanced',
                        'estimated_minutes': 45,
                        'objectives': "Understand Python's duck typing philosophy: 'If it walks like a duck and quacks like a duck, it is a duck.'\nImplement essential dunder methods: `__str__` (for users) vs `__repr__` (for developers).\nImplement sequence protocols: `__len__` and `__getitem__`.\nImplement equality and comparison operators: `__eq__`, `__lt__`.",
                        'summary_content': """**Dunder** (Double Underscore) methods allow your custom classes to integrate directly with Python's built-in syntax (e.g. `len(obj)`, `print(obj)`, `obj1 == obj2`, `for item in obj:`).

### Key Dunder Methods:
- **`__str__(self)`**: User-friendly representation printed by `print(obj)` or `str(obj)`.
- **`__repr__(self)`**: Unambiguous developer representation used in debugging/REPL.
- **`__len__(self)`**: Enables `len(obj)`.
- **`__getitem__(self, index)`**: Enables `obj[index]` indexing and automatic looping!
- **`__eq__(self, other)`**: Enables `obj1 == obj2` comparison.""",
                        'code_snippet': """# Implementing a custom Pythonic Deck of Topics
class StudyTopicCollection:
    def __init__(self, title: str, topics: list):
        self.title = title
        self.topics = topics
    
    def __str__(self):
        return f"Study Deck: '{self.title}' ({len(self.topics)} topics)"
    
    def __repr__(self):
        return f"StudyTopicCollection(title={self.title!r}, count={len(self.topics)})"
    
    def __len__(self):
        return len(self.topics)
    
    def __getitem__(self, index):
        return self.topics[index]

deck = StudyTopicCollection("Week 1 Python", ["Syntax", "Variables", "Loops"])
print(str(deck))      # Study Deck: 'Week 1 Python' (3 topics)
print(len(deck))      # 3
print(deck[0])        # Syntax (Indexing works out of the box!)""",
                        'key_takeaways': "Dunder methods hook your classes into Python core syntax.\n__str__ is for clean human display; __repr__ is for exact developer debugging.\nImplementing __len__ and __getitem__ automatically makes your object iterable and indexable.",
                        'resources': [
                            ('Python Data Model and Dunder Methods', 'doc', 'https://docs.python.org/3/reference/datamodel.html#special-method-names', 'Python.org', '20 min read'),
                            ('Python Dunder Methods Guide', 'article', 'https://realpython.com/operator-function-overloading/', 'Real Python', '15 min read')
                        ],
                        'practice': {
                            'title': 'Vector 2D Math Class with Dunder Methods',
                            'difficulty': 'medium',
                            'prompt_description': 'Create a `Vector2D` class with `x` and `y` coordinates. Implement `__repr__`, `__add__` (vector addition: Vector2D(x1+x2, y1+y2)), and `__eq__`.',
                            'starter_code': 'class Vector2D:\n    # Implement __init__, __repr__, __add__, __eq__\n    pass\n',
                            'solution_hint': 'In __add__, return Vector2D(self.x + other.x, self.y + other.y)',
                            'solution_code': 'class Vector2D:\n    def __init__(self, x: float, y: float):\n        self.x = x\n        self.y = y\n    def __repr__(self):\n        return f"Vector2D({self.x}, {self.y})"\n    def __add__(self, other):\n        return Vector2D(self.x + other.x, self.y + other.y)\n    def __eq__(self, other):\n        return isinstance(other, Vector2D) and self.x == other.x and self.y == other.y'
                        }
                    },
                    {
                        'title': 'Encapsulation & Property Decorators (@property)',
                        'difficulty': 'advanced',
                        'estimated_minutes': 40,
                        'objectives': "Understand Python privacy conventions (`_protected` vs `__private` name mangling).\nImplement managed getters, setters, and deleters using the `@property` decorator.\nValidate attribute assignments transparently without breaking existing API contracts.\nCreate computed read-only properties.",
                        'summary_content': """Encapsulation restricts direct access to an object's internal representation, bundling state and validation methods together.

### The `@property` Decorator:
In Java or C++, you write tedious getter/setter methods (`getAge()`, `setAge(val)`).
In Python, `@property` allows you to write Pythonic attribute access (`student.gpa = 3.9`) while internally executing validation logic!

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self._score = score
        
    @property
    def score(self):
        return self._score
        
    @score.setter
    def score(self, value):
        if not (0 <= value <= 100):
            raise ValueError("Score must be between 0 and 100")
        self._score = value
```""",
                        'code_snippet': """# Encapsulation with computed read-only properties
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    @property
    def area(self) -> float:
        \"\"\"Computed property: calculated dynamically on access.\"\"\"
        return self.width * self.height
    
    @property
    def is_square(self) -> bool:
        return self.width == self.height

rect = Rectangle(10, 20)
print(f"Area: {rect.area}")       # 200 (Accessed like an attribute!)
print(f"Is Square? {rect.is_square}") # False""",
                        'key_takeaways': "Use a single leading underscore (_name) to signal internal protected attributes by convention.\nUse @property for computed attributes and clean validation.\nProperties allow you to add validation later without changing how callers access the attribute.",
                        'resources': [
                            ('Python @property Decorator In-Depth', 'article', 'https://realpython.com/python-property/', 'Real Python', '14 min read'),
                            ('Getters, Setters and Properties in Python', 'video', 'https://www.youtube.com/watch?v=jCzT9XFZ5bw', 'Corey Schafer', '15 mins')
                        ],
                        'practice': {
                            'title': 'Temperature Converter with Validation',
                            'difficulty': 'medium',
                            'prompt_description': 'Create a `Temperature` class that stores `_celsius`. Implement a `@property celsius` getter and setter that raises `ValueError("Below absolute zero!")` if value < -273.15. Add a read-only property `fahrenheit` calculated as `(celsius * 9/5) + 32`.',
                            'starter_code': 'class Temperature:\n    # Implement class with property\n    pass\n',
                            'solution_hint': 'Define @property celsius, @celsius.setter with validation, and @property fahrenheit.',
                            'solution_code': 'class Temperature:\n    def __init__(self, celsius: float = 0.0):\n        self.celsius = celsius\n    @property\n    def celsius(self):\n        return self._celsius\n    @celsius.setter\n    def celsius(self, value: float):\n        if value < -273.15:\n            raise ValueError("Below absolute zero!")\n        self._celsius = value\n    @property\n    def fahrenheit(self):\n        return (self._celsius * 9/5) + 32'
                        }
                    }
                ]
            },
            {
                'level_number': 7,
                'title': 'Practical Python & Software Engineering',
                'tagline': 'Build real-world applications: Virtual environments, REST APIs, SQLite, and Testing.',
                'description': 'Master the professional Python ecosystem: manage isolated dependencies with venv and pip, make HTTP requests to third-party REST APIs, interact with databases using sqlite3, write unit tests, and build an internship-ready GitHub portfolio.',
                'topics': [
                    {
                        'title': 'Virtual Environments (venv) & Package Management (pip)',
                        'difficulty': 'intermediate',
                        'estimated_minutes': 30,
                        'objectives': "Understand why isolated virtual environments prevent dependency conflicts between projects.\nCreate and activate virtual environments using Python's built-in `venv`.\nInstall and manage third-party packages using `pip`.\nGenerate and install from `requirements.txt` for reproducible builds.",
                        'summary_content': """When building multiple Python projects, different applications may require incompatible versions of third-party libraries (e.g. Django 4 vs Django 5).

### Creating and Activating `venv`:
```bash
# 1. Create a virtual environment folder named .venv
python -m venv .venv

# 2. Activate it:
# Windows (PowerShell):
.venv\\Scripts\\Activate.ps1
# Mac/Linux:
source .venv/bin/activate
```

### Managing Dependencies:
```bash
# Install a library:
pip install requests django

# Freeze current environment dependencies to file:
pip freeze > requirements.txt

# Install all dependencies on another machine:
pip install -r requirements.txt
```""",
                        'code_snippet': """# requirements.txt standard format
# Core Web and API Frameworks
django>=5.0.0
requests>=2.31.0
python-dotenv>=1.0.0

# Testing and Code Quality
pytest>=8.0.0
black>=24.0.0
flake8>=7.0.0""",
                        'key_takeaways': "Always use a dedicated virtual environment for every Python project.\nNever commit the .venv directory to Git (add it to .gitignore).\nUse 'pip freeze > requirements.txt' so teammates can replicate your exact environment.",
                        'resources': [
                            ('Python Virtual Environments: A Primer', 'article', 'https://realpython.com/python-virtual-environments-a-primer/', 'Real Python', '14 min read'),
                            ('Installing Python Modules with pip', 'doc', 'https://docs.python.org/3/installing/index.html', 'Python.org', '10 min read')
                        ],
                        'practice': {
                            'title': 'Requirements File Dependency Parser',
                            'difficulty': 'easy',
                            'prompt_description': 'Write a function `parse_requirements(req_text)` that takes the text content of a `requirements.txt` file and returns a list of clean package names with versions stripped (e.g. "django>=5.0.0" -> "django"). Ignore blank lines and comments.',
                            'starter_code': 'def parse_requirements(req_text):\n    # Write logic\n    pass\n',
                            'solution_hint': 'Split on newline, strip, ignore empty or lines starting with "#", split on ">=", "==", "<=".',
                            'solution_code': 'def parse_requirements(req_text):\n    packages = []\n    for line in req_text.splitlines():\n        clean = line.strip()\n        if not clean or clean.startswith("#"):\n            continue\n        for op in [">=", "==", "<=", "~=", ">", "<"]:\n            if op in clean:\n                clean = clean.split(op)[0].strip()\n                break\n        packages.append(clean)\n    return packages'
                        }
                    },
                    {
                        'title': 'Consuming REST APIs with requests',
                        'difficulty': 'advanced',
                        'estimated_minutes': 45,
                        'objectives': "Understand HTTP methods: GET, POST, PUT, DELETE.\nUse the `requests` library to fetch JSON payloads from public APIs.\nHandle query parameters, request headers, and authentication tokens.\nCheck HTTP status codes (`response.status_code`, `response.raise_for_status()`) and handle timeouts.",
                        'summary_content': """Modern web apps and backend services communicate by exchanging JSON over HTTP via REST APIs.

### The `requests` Workflow:
```python
import requests

try:
    response = requests.get(
        "https://api.github.com/users/octocat",
        timeout=5 # Always specify timeout to prevent hanging!
    )
    response.raise_for_status() # Raises HTTPError if status code is 4xx or 5xx
    data = response.json()      # Parses response body into Python dictionary
    print(f"User: {data['name']}, Public Repos: {data['public_repos']}")
except requests.exceptions.RequestException as err:
    print(f"Network / API Error: {err}")
```""",
                        'code_snippet': """import requests

def fetch_top_github_repos(language: str = "python", limit: int = 5):
    \"\"\"Fetches top trending repositories on GitHub for a given language.\"\"\"
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}",
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        res = requests.get(url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        items = res.json().get("items", [])
        return [{"name": item["name"], "stars": item["stargazers_count"]} for item in items]
    except requests.RequestException as e:
        return [{"error": str(e)}]""",
                        'key_takeaways': "Always specify a timeout (e.g. timeout=10) on network requests.\nUse response.raise_for_status() to catch 404/500 HTTP errors.\nresponse.json() decodes JSON directly into Python dictionaries and lists.",
                        'resources': [
                            ('Python Requests: Making HTTP Requests', 'article', 'https://realpython.com/python-requests/', 'Real Python', '16 min read'),
                            ('Requests Official Documentation', 'doc', 'https://requests.readthedocs.io/en/latest/', 'Requests Docs', '15 min read')
                        ],
                        'practice': {
                            'title': 'API Status Health Checker',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `check_endpoints_health(endpoints_list)` that takes a list of URLs and returns a dict mapping `{url: status_code_or_error_str}`.',
                            'starter_code': 'def check_endpoints_health(endpoints_list):\n    # Simulate or use requests\n    pass\n',
                            'solution_hint': 'Iterate through URLs, wrap requests.get(url, timeout=3) in try-except, return status_code.',
                            'solution_code': 'def check_endpoints_health(endpoints_list):\n    results = {}\n    for url in endpoints_list:\n        try:\n            import requests\n            res = requests.get(url, timeout=3)\n            results[url] = res.status_code\n        except Exception as e:\n            results[url] = f"Error: {type(e).__name__}"\n    return results'
                        }
                    },
                    {
                        'title': 'SQLite Database Interaction with sqlite3',
                        'difficulty': 'advanced',
                        'estimated_minutes': 45,
                        'objectives': "Connect to lightweight SQLite databases using Python's built-in `sqlite3` module.\nCreate tables, execute parameterized SQL queries, and prevent SQL injection.\nCommit database transactions and properly close cursors/connections using context managers.\nFetch rows as tuples or dictionary-like `sqlite3.Row` mappings.",
                        'summary_content': """Python includes built-in support for SQLite, a serverless, zero-configuration SQL database engine.

### Safe Parameterized Queries (Prevent SQL Injection!):
**NEVER** format SQL with f-strings (`f"SELECT * FROM users WHERE name = '{input}'"`).
Always use parameter placeholders (`?` in SQLite):

```python
import sqlite3

with sqlite3.connect("app.db") as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT)")
    
    # Safe parameterized insert:
    cursor.execute("INSERT INTO notes (title) VALUES (?)", ("My Python Note",))
    conn.commit()
```""",
                        'code_snippet': """import sqlite3

def init_learning_db():
    conn = sqlite3.connect(":memory:") # In-memory database for testing
    conn.row_factory = sqlite3.Row     # Enables dict-like access: row["topic"]
    
    cursor = conn.cursor()
    cursor.execute(\"\"\"
        CREATE TABLE topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            mastery_level INTEGER DEFAULT 0
        )
    \"\"\")
    
    # Batch insert with executemany
    sample_data = [("Variables", 5), ("Loops", 4), ("Functions", 3)]
    cursor.executemany("INSERT INTO topics (title, mastery_level) VALUES (?, ?)", sample_data)
    conn.commit()
    
    # Query back
    cursor.execute("SELECT title, mastery_level FROM topics WHERE mastery_level >= ?", (4,))
    rows = cursor.fetchall()
    for row in rows:
        print(f"Mastered: {row['title']} (Level {row['mastery_level']})")
    
    conn.close()

init_learning_db()""",
                        'key_takeaways': "Never concatenate raw strings into SQL queries; always use parameterized ? placeholders.\nconn.row_factory = sqlite3.Row allows column access by name.\nAlways commit transactions using conn.commit() or use connection context managers.",
                        'resources': [
                            ('Python sqlite3 Standard Library Documentation', 'doc', 'https://docs.python.org/3/library/sqlite3.html', 'Python.org', '15 min read'),
                            ('Data Management with Python and SQLite', 'article', 'https://realpython.com/python-sqlite-sqlalchemy/', 'Real Python', '16 min read')
                        ],
                        'practice': {
                            'title': 'Student Bookmark SQLite Repository',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `save_student_bookmark(conn, user_id, topic_title, url)` that creates a `bookmarks` table if not exists and inserts a new bookmark row using parameterized SQL.',
                            'starter_code': 'def save_student_bookmark(conn, user_id, topic_title, url):\n    # Write parameterized SQL execution\n    pass\n',
                            'solution_hint': 'CREATE TABLE IF NOT EXISTS bookmarks (id INTEGER PRIMARY KEY, user_id INT, topic TEXT, url TEXT); INSERT INTO bookmarks VALUES (?, ?, ?)',
                            'solution_code': 'def save_student_bookmark(conn, user_id, topic_title, url):\n    cur = conn.cursor()\n    cur.execute("""\n        CREATE TABLE IF NOT EXISTS bookmarks (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            user_id INTEGER,\n            topic_title TEXT,\n            url TEXT\n        )\n    """)\n    cur.execute("INSERT INTO bookmarks (user_id, topic_title, url) VALUES (?, ?, ?)", (user_id, topic_title, url))\n    conn.commit()\n    return cur.lastrowid'
                        }
                    },
                    {
                        'title': 'Writing Unit Tests with unittest & pytest',
                        'difficulty': 'advanced',
                        'estimated_minutes': 40,
                        'objectives': "Understand automated unit testing and the Test-Driven Development (TDD) cycle (Red-Green-Refactor).\nWrite test suites using Python's built-in `unittest.TestCase`.\nUse test assertions: `assertEqual`, `assertTrue`, `assertIn`, `assertRaises`.\nDiscover why `pytest` is widely preferred in industry.",
                        'summary_content': """Automated tests verify that your code functions correctly and prevent regressions when refactoring.

### Built-in `unittest` Framework:
```python
import unittest

def add(a, b):
    return a + b

class TestMathOperations(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

if __name__ == "__main__":
    unittest.main()
```

### Running Tests:
Run `python -m unittest discover` from your project root.""",
                        'code_snippet': """import unittest

def calculate_grade(score: int) -> str:
    if not (0 <= score <= 100):
        raise ValueError("Score out of range")
    return "A" if score >= 90 else "B" if score >= 80 else "Pass"

class TestGradeCalculator(unittest.TestCase):
    def test_grade_a(self):
        self.assertEqual(calculate_grade(95), "A")
    
    def test_grade_boundary(self):
        self.assertEqual(calculate_grade(90), "A")
        self.assertEqual(calculate_grade(89), "B")
        
    def test_invalid_score_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_grade(105)
        with self.assertRaises(ValueError):
            calculate_grade(-5)

if __name__ == "__main__":
    unittest.main()""",
                        'key_takeaways': "Tests give confidence when refactoring and shipping code.\nTest edge cases, boundary conditions, and invalid inputs.\nUse self.assertRaises() as a context manager to verify that expected errors are raised.",
                        'resources': [
                            ('Python unittest Framework Documentation', 'doc', 'https://docs.python.org/3/library/unittest.html', 'Python.org', '15 min read'),
                            ('Getting Started With Testing in Python', 'article', 'https://realpython.com/python-testing/', 'Real Python', '16 min read')
                        ],
                        'practice': {
                            'title': 'Test Suite for String Normalizer',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a unittest test case class `TestSlugifier` with tests for empty string handling, uppercase transformation, and special character stripping for a slugify function.',
                            'starter_code': 'import unittest\n\nclass TestSlugifier(unittest.TestCase):\n    # Implement test methods\n    pass\n',
                            'solution_hint': 'Define test_empty_string, test_spaces_to_hyphens, test_lowercase.',
                            'solution_code': 'import unittest\n\ndef simple_slugify(text):\n    return text.strip().lower().replace(" ", "-")\n\nclass TestSlugifier(unittest.TestCase):\n    def test_basic_slug(self):\n        self.assertEqual(simple_slugify("Hello World"), "hello-world")\n    def test_whitespace_stripping(self):\n        self.assertEqual(simple_slugify("  Python Tips  "), "python-tips")\n    def test_empty_string(self):\n        self.assertEqual(simple_slugify(""), "")'
                        }
                    },
                    {
                        'title': 'Practical Mini-Projects & GitHub Portfolio Blueprint',
                        'difficulty': 'advanced',
                        'estimated_minutes': 50,
                        'objectives': "Design and architect 3 portfolio-grade Python projects.\nStructure a professional Git repository with README.md, .gitignore, license, and docstrings.\nUnderstand how to showcase problem-solving and clean code in technical interviews.\nDeploy Python applications to public cloud hosting.",
                        'summary_content': """Recruiters and engineering managers do not look for generic tutorial clones (like basic to-do apps). They look for projects that solve real problems and demonstrate software engineering maturity.

### Top 3 Portfolio Project Ideas:
1. **Personalized Learning & Revision Engine** (e.g. LearningHub!): Demonstrates database models, full-stack integration, algorithms, and personalized memory tracking.
2. **Automated REST API Data Pipeline & Visualizer**: Fetches data from multiple public APIs, processes and cleans the data, stores in SQLite/PostgreSQL, and serves insights.
3. **CLI Developer Tool**: A command-line tool packaged on PyPI with rich argument parsing (`argparse`), colored terminal output (`rich`), and automated tests.

### Repository Checklist:
- `README.md` with architecture diagram, screenshots, and setup instructions.
- `.gitignore` (excluding `.venv`, `__pycache__`, `.env`, `db.sqlite3`).
- Clean modular code with docstrings and type hints.
- Passing test suite.""",
                        'code_snippet': """# Clean CLI tool entry point architecture
import argparse
import sys

def build_parser():
    parser = argparse.ArgumentParser(description="LearningHub CLI Study Assistant")
    parser.add_argument("--topic", required=True, help="Python topic name to review")
    parser.add_argument("--flashcard", action="store_true", help="Launch flashcard revision")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    print(f"Preparing study session for: {args.topic} (Flashcard mode: {args.flashcard})")

if __name__ == "__main__":
    main()""",
                        'key_takeaways': "Build projects that solve actual personal or domain problems.\nA stellar README with visual demos and clear architecture is your #1 resume asset.\nWrite clean, tested, documented code with zero hardcoded API keys.",
                        'resources': [
                            ('Building a Great Python Portfolio', 'article', 'https://realpython.com/python-project-ideas/', 'Real Python', '15 min read'),
                            ('How to Write a Professional README', 'article', 'https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/', 'freeCodeCamp', '10 min read')
                        ],
                        'practice': {
                            'title': 'CLI Flashcard Quiz Runner',
                            'difficulty': 'medium',
                            'prompt_description': 'Write a function `run_quiz(questions_dict)` that loops through questions `{question: answer}`, checks user answers case-insensitively, and returns the final score percentage.',
                            'starter_code': 'def run_quiz(questions_dict, user_answers_list):\n    # Calculate score\n    pass\n',
                            'solution_hint': 'Compare each user answer with corresponding dict value stripped and lowered.',
                            'solution_code': 'def run_quiz(questions_dict, user_answers_list):\n    if not questions_dict:\n        return 0.0\n    correct = 0\n    for (q, a), user_a in zip(questions_dict.items(), user_answers_list):\n        if str(user_a).strip().lower() == str(a).strip().lower():\n            correct += 1\n    return round((correct / len(questions_dict)) * 100, 1)'
                        }
                    }
                ]
            }
        ]

        total_topics_created = 0
        total_resources_created = 0
        total_practice_created = 0
        all_topics = []

        for lvl_data in levels_data:
            level_obj, _ = Level.objects.get_or_create(
                learning_path=python_path,
                level_number=lvl_data['level_number'],
                defaults={
                    'title': lvl_data['title'],
                    'tagline': lvl_data['tagline'],
                    'description': lvl_data['description'],
                    'order': lvl_data['level_number']
                }
            )

            for order_idx, topic_data in enumerate(lvl_data['topics'], start=1):
                topic_obj, _ = Topic.objects.get_or_create(
                    level=level_obj,
                    title=topic_data['title'],
                    defaults={
                        'order': order_idx,
                        'difficulty': topic_data['difficulty'],
                        'estimated_minutes': topic_data['estimated_minutes'],
                        'objectives': topic_data['objectives'],
                        'summary_content': topic_data['summary_content'],
                        'code_snippet': topic_data['code_snippet'],
                        'key_takeaways': topic_data['key_takeaways'],
                        'is_active': True
                    }
                )
                all_topics.append(topic_obj)
                total_topics_created += 1

                # Resources
                for res_order, (r_title, r_type, r_url, r_source, r_time) in enumerate(topic_data.get('resources', []), start=1):
                    Resource.objects.update_or_create(
                        topic=topic_obj,
                        order=res_order,
                        defaults={
                            'title': r_title,
                            'resource_type': r_type,
                            'url': r_url,
                            'author_or_source': r_source,
                            'duration_or_read_time': r_time,
                            'is_recommended': True,
                        }
                    )
                    total_resources_created += 1

                # Practice Problem
                p_data = topic_data.get('practice')
                if p_data:
                    PracticeProblem.objects.get_or_create(
                        topic=topic_obj,
                        title=p_data['title'],
                        defaults={
                            'difficulty': p_data['difficulty'],
                            'platform': 'learninghub',
                            'prompt_description': p_data['prompt_description'],
                            'starter_code': p_data['starter_code'],
                            'solution_hint': p_data['solution_hint'],
                            'solution_code': p_data['solution_code'],
                            'order': 1
                        }
                    )
                    total_practice_created += 1

        self.stdout.write(self.style.SUCCESS(f"[OK] Created {len(levels_data)} Levels, {total_topics_created} Topics, {total_resources_created} Resources, and {total_practice_created} Practice Problems."))

        # 4. Create Daily Tasks (30-day curriculum cycle)
        daily_task_templates = [
            (1, "Install Python & Write First Script", "learn", "Set up local Python environment and verify installation with 'import this'.", 30, all_topics[0]),
            (1, "Record Personal Mental Model of Bytecode", "understand", "Write down in your own words how the Python interpreter executes code.", 15, all_topics[0]),
            (2, "Master Variables & Reference Memory", "learn", "Understand object references and Python variable assignment rules.", 30, all_topics[1]),
            (2, "Practice Variable Swapping", "practice", "Solve the variable swap problem using Pythonic tuple unpacking.", 20, all_topics[1]),
            (3, "Explore Core Primitive Types & Truthiness", "learn", "Study ints, floats, booleans, and truth value testing.", 35, all_topics[2]),
            (3, "Log Any Confusions on Float Precision", "review", "Record any doubts regarding floating point arithmetic precision.", 15, all_topics[2]),
            (4, "Master f-strings & Print Formatting", "learn", "Learn string interpolation and number precision alignment.", 30, all_topics[3]),
            (4, "Build Receipt Formatter Exercise", "practice", "Complete the practice challenge for receipt formatting.", 25, all_topics[3]),
            (5, "Understand Arithmetic & Logical Operators", "learn", "Master floor division, modulo, and chained comparisons.", 30, all_topics[4]),
            (5, "Differentiate 'is' vs '==' in Memory", "understand", "Write down your own real-world analogy for identity vs value equality.", 15, all_topics[4]),
            (6, "Type Conversion & Safe Casting", "learn", "Learn how to convert strings to numbers safely without crashing.", 25, all_topics[5]),
            (6, "Level 1 Milestone Revision", "complete", "Review all 6 fundamental topics and mark comfort levels.", 30, all_topics[5]),
            (7, "Control Flow with if, elif & else", "learn", "Master multi-branch conditionals and ternary expressions.", 35, all_topics[6]),
            (8, "for Loops & range() Generator", "learn", "Iterate over collections cleanly without manual index counters.", 40, all_topics[7]),
            (8, "Solve Leaderboard Formatter with enumerate()", "practice", "Build a ranked leaderboard formatter using enumerate.", 20, all_topics[7]),
            (9, "while Loops & Sentinel Termination", "learn", "Implement condition-driven iteration and prevent infinite loops.", 35, all_topics[8]),
            (10, "Loop Control: break, continue & for...else", "learn", "Master search loop patterns using Python's unique for...else.", 35, all_topics[9]),
            (11, "Python Strings & Slicing Magic", "learn", "Master [start:stop:step] slicing and core string manipulation methods.", 40, all_topics[10]),
            (12, "Python Lists: CRUD & Mutability", "learn", "Learn list append, extend, pop, sort, and avoid alias mutation bugs.", 45, all_topics[11]),
            (13, "Tuples & Starred Unpacking Patterns", "learn", "Understand immutability and unpack records cleanly.", 30, all_topics[12]),
            (14, "Sets & Mathematical Operations", "learn", "Use O(1) set lookups, unions, and intersections.", 35, all_topics[13]),
            (15, "Dictionaries: Fast Lookups & Iteration", "learn", "Master hash maps, dict.get(), and dictionary merging.", 45, all_topics[14]),
            (16, "Define Functions with Type Hints & Docstrings", "learn", "Write clean, reusable functions with PEP 484 type hints.", 35, all_topics[15]),
            (17, "*args, **kwargs & the Mutable Default Trap", "learn", "Master flexible parameter passing and avoid shared default bugs.", 40, all_topics[16]),
            (18, "Variable Scoping & the LEGB Rule", "learn", "Master Local, Enclosing, Global, and Built-in scope lookups.", 35, all_topics[18]),
            (19, "Lambdas & Custom Sorting Keys", "learn", "Use anonymous functions inside sorted(), min(), and max().", 35, all_topics[19]),
            (20, "File Handling & Safe Context Managers", "learn", "Read and write files cleanly using 'with open(...) as f:'.", 40, all_topics[21]),
            (21, "Exception Handling: try, except, else, finally", "learn", "Write bulletproof error handling code.", 45, all_topics[22]),
            (22, "List & Dictionary Comprehensions", "learn", "Transform and filter data with idiomatic comprehensions.", 40, all_topics[23]),
            (23, "Classes, Objects & the self Parameter", "learn", "Model entities with classes and understand self.", 45, all_topics[25]),
            (24, "Inheritance & super() Delegation", "learn", "Build object hierarchies without repeating code.", 45, all_topics[27]),
            (25, "Magic / Dunder Methods (__str__, __len__)", "learn", "Hook custom classes into Python syntax with dunder methods.", 45, all_topics[28]),
            (26, "@property Decorators & Validation", "learn", "Implement managed getters and setters with clean syntax.", 40, all_topics[29]),
            (27, "Virtual Environments & pip Package Management", "learn", "Isolate project dependencies with venv and requirements.txt.", 30, all_topics[30]),
            (28, "Consuming REST APIs with requests", "learn", "Fetch live data from JSON web services with timeouts.", 45, all_topics[31]),
            (29, "SQLite Database Operations in Python", "learn", "Store and query structured relational data safely with sqlite3.", 45, all_topics[32]),
            (30, "Cap-stone Project Architecture & Portfolio", "complete", "Package your Python projects for job readiness and review.", 60, all_topics[34]),
        ]

        for day_num, t_title, t_type, t_desc, t_mins, t_ref in daily_task_templates:
            DailyTask.objects.get_or_create(
                learning_path=python_path,
                day_number=day_num,
                title=t_title,
                defaults={
                    'task_type': t_type,
                    'description': t_desc,
                    'estimated_minutes': t_mins,
                    'topic_ref': t_ref,
                    'order': 1
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Created 30+ structured Daily Learning Tasks."))

        # 5. Create 30-Day Python Bootcamp
        bootcamp_obj, _ = Bootcamp.objects.get_or_create(
            slug='python-30-day-bootcamp',
            defaults={
                'title': 'Python 30-Day Intensive Bootcamp',
                'tagline': 'A daily hands-on roadmap designed to take you from hello world to building complete applications.',
                'description': '30 structured daily milestones with bite-sized concepts, coding assignments, and check-offs to build unwavering daily momentum.',
                'total_days': 30,
                'icon': 'rocket',
                'is_active': True
            }
        )

        bootcamp_days_data = [
            (1, "Python Installation & First Script", "Set up your Python environment, explore the REPL, and print your first output.", "Install Python 3.11+\nUnderstand the difference between compilation and interpretation\nRun your first .py file from terminal", "Write a script that outputs a personalized greeting and calculates your daily study target hours.", all_topics[0]),
            (2, "Variables & Memory Models", "Master variable naming, assignment, and memory references.", "Understand Python variables as dynamic references\nLearn PEP 8 snake_case rules\nUse UPPER_CASE for constants", "Create 5 variables representing a student profile and print them using clean formatting.", all_topics[1]),
            (3, "Data Types & Truthiness", "Understand integers, floats, strings, booleans, and None.", "Master arbitrary-precision integers\nLearn why 0.1 + 0.2 has float precision nuances\nTest truthy and falsy values", "Build a truthiness inspector that classifies 6 different test values.", all_topics[2]),
            (4, "Modern String Formatting (f-strings)", "Master modern formatted string literals in Python.", "Format numbers with fixed decimals (:.2f)\nAlign text with padding\nEmbed arithmetic inside f-strings", "Format a multi-line shopping receipt with aligned columns and totals.", all_topics[3]),
            (5, "Operators & Identity", "Master arithmetic, comparison, logical operators, and 'is' vs '=='.", "Use // for floor division and % for modulo\nChain comparisons (0 <= x < 100)\nDifferentiate object identity from value equality", "Write an algorithm that tests whether a given year is a leap year.", all_topics[4]),
            (6, "Type Conversion & Safe Casting", "Convert data between types and handle ValueError cleanly.", "Understand implicit vs explicit conversion\nUse int(), float(), str(), bool() safely\nWrap casting in try-except blocks", "Build a safe user age input validator with default fallback.", all_topics[5]),
            (7, "Decision Making: if, elif, else", "Build branching logic with multi-condition evaluations.", "Structure clean if-elif-else ladders\nUse Python ternary operator\nAvoid redundant boolean comparisons", "Build an automated shipping fee calculator based on cart value and membership tier.", all_topics[6]),
            (8, "Looping with for & enumerate()", "Iterate sequences and access indices cleanly.", "Use range(start, stop, step)\nUse enumerate(list, start=1)\nIterate two lists simultaneously with zip()", "Generate a formatted leaderboard with medals for the top 3 participants.", all_topics[7]),
            (9, "while Loops & Condition Controls", "Master condition-based iteration and sentinel loops.", "Write robust while loops without infinite cycles\nImplement retry limits\nUpdate loop state variables", "Implement a number guessing game simulation with a 5-attempt limit.", all_topics[8]),
            (10, "Loop Controls & for...else", "Use break, continue, pass, and Python's unique for...else construct.", "Terminate loops early with break\nSkip iterations with continue\nRun fallback code with for...else", "Write a prime number finder using the for...else pattern.", all_topics[9]),
            (11, "Strings Mastery & Slicing", "Slice and manipulate text like a pro.", "Master [start:stop:step] slicing\nReverse strings with [::-1]\nUse .split(), .join(), .strip()", "Write a clean URL slug generator that normalizes titles into URL slugs.", all_topics[10]),
            (12, "Lists: Dynamic Arrays & Mutability", "Create, modify, sort, and slice Python lists.", "Perform list CRUD operations\nUnderstand shallow vs deep copies\nDifferentiate list.sort() from sorted(list)", "Write a function that finds the second largest unique value in a list.", all_topics[11]),
            (13, "Tuples & Starred Unpacking", "Leverage immutable records and flexible unpacking.", "Protect fixed data with tuples\nUse starred unpacking: first, *mid, last\nUse tuples as dictionary keys", "Create a function returning (min, max, average) as an unpacked tuple.", all_topics[12]),
            (14, "Sets & Fast Membership Checks", "Leverage O(1) hash sets and mathematical set operations.", "Eliminate duplicates instantly with set()\nPerform union, intersection, and difference\nUse .discard() instead of .remove()", "Find common prerequisites between two courses using set intersection.", all_topics[13]),
            (15, "Dictionaries: Hash Maps & Key Lookups", "Store and query key-value pairs with O(1) performance.", "Use dict.get(key, default) for safe lookups\nIterate with dict.items()\nMerge dictionaries with the | operator", "Build a word and error frequency counter for server log strings.", all_topics[14]),
            (16, "Functions & Type Annotations", "Write modular, single-responsibility functions.", "Define functions with def and return\nUse PEP 484 type hints for parameters and return types\nWrite PEP 257 docstrings", "Write an email validation function with comprehensive type annotations.", all_topics[15]),
            (17, "Advanced Arguments: *args & **kwargs", "Handle dynamic argument counts and avoid default argument bugs.", "Collect positional args into tuple with *args\nCollect keyword args into dict with **kwargs\nNever use mutable default arguments", "Build a flexible custom log message generator that accepts arbitrary metadata.", all_topics[16]),
            (18, "Variable Scope & LEGB Hierarchy", "Understand where variables live and how Python resolves them.", "Master Local, Enclosing, Global, and Built-in scopes\nUnderstand closures and the nonlocal keyword\nAvoid global state mutations", "Build a stateful running average calculator closure.", all_topics[18]),
            (19, "Lambdas & Higher-Order Functions", "Write anonymous functions for sorting and mapping.", "Write concise lambda expressions\nSort lists of dictionaries by custom multi-criteria keys\nUnderstand when list comprehensions are preferred", "Sort a list of student records by grade level descending and GPA descending.", all_topics[19]),
            (20, "File I/O & Context Managers", "Read and write files safely without memory leaks.", "Use with open(...) as f: context managers\nStream large files line by line\nUse pathlib.Path for cross-platform file paths", "Write a text file analyzer that counts lines, words, and characters.", all_topics[21]),
            (21, "Robust Error Handling", "Build crash-proof applications with structured exceptions.", "Use try, except, else, and finally\nCatch specific exceptions rather than bare except\nRaise descriptive exceptions with raise ValueError()", "Build a safe nested dictionary lookup helper that never raises KeyError.", all_topics[22]),
            (22, "List & Dict Comprehensions", "Transform data with high-speed, idiomatic comprehensions.", "Write list comprehensions with filters\nBuild inverted dictionaries with dict comprehensions\nCreate set comprehensions", "Filter and invert a configuration dictionary using a one-line dict comprehension.", all_topics[23]),
            (23, "OOP: Classes & Objects", "Model domain concepts with classes, attributes, and methods.", "Understand the blueprint vs instance relationship\nMaster the self parameter\nInitialize instance state", "Build a BankAccount class with deposit, withdraw, and balance checking.", all_topics[25]),
            (24, "Constructors & Attributes", "Manage instance vs class-level state.", "Initialize state inside __init__\nTrack shared counts with class attributes\nUse @classmethod and @staticmethod", "Build an inventory tracker that flags low-stock items via a class attribute.", all_topics[26]),
            (25, "Inheritance & Method Overriding", "Extend existing classes and specialize child behavior.", "Derive child classes from base classes\nDelegate parent initialization with super().__init__()\nOverride methods for specialized behavior", "Create an Employee and Manager hierarchy calculating total compensation.", all_topics[27]),
            (26, "Dunder Methods & Pythonic Protocols", "Hook custom classes into Python built-in operators.", "Implement __str__ and __repr__\nImplement __len__ and __getitem__ for sequence behavior\nImplement __eq__ and __add__", "Build a 2D Vector class supporting vector addition (+) and equality (==).", all_topics[28]),
            (27, "@property Decorators & Validation", "Implement clean attribute getters and setters with validation.", "Protect attributes with leading underscores\nCreate read-only computed properties with @property\nValidate assignments with @prop.setter", "Build a Temperature class that converts Celsius to Fahrenheit with absolute zero validation.", all_topics[29]),
            (28, "Virtual Environments & Package Management", "Isolate Python dependencies cleanly.", "Create and activate virtual environments with venv\nInstall packages with pip\nExport and install dependencies with requirements.txt", "Generate a clean requirements.txt parser that extracts package names.", all_topics[30]),
            (29, "REST APIs & Database Storage", "Connect to external APIs and store results in SQLite.", "Make HTTP requests with timeouts using requests\nExecute parameterized SQL queries with sqlite3\nPrevent SQL injection vulnerabilities", "Build a script that fetches data from an API and persists records into an SQLite table.", all_topics[31]),
            (30, "Full-Stack Project Capstone & Review", "Review your full learning journey and plan next steps.", "Complete a comprehensive curriculum review\nRefactor personal notes and resolve any lingering doubts\nPublish your Python project portfolio on GitHub", "Package a complete Python project with README, tests, and documentation.", all_topics[34]),
        ]

        for b_day, b_title, b_sum, b_goals, b_assign, b_ref in bootcamp_days_data:
            BootcampDay.objects.get_or_create(
                bootcamp=bootcamp_obj,
                day_number=b_day,
                defaults={
                    'title': b_title,
                    'topic_ref': b_ref,
                    'concept_summary': b_sum,
                    'learning_goals': b_goals,
                    'practice_assignment': b_assign,
                    'estimated_minutes': 60
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Created 30-Day Python Bootcamp Curriculum."))

        # 6. Create Mentor Guidance Articles and Tips
        mentor_articles = [
            (
                "How to Escape Tutorial Hell & Actually Think Like a Programmer",
                "strategy",
                "The #1 trap beginner programmers face is passively watching hundreds of hours of coding tutorials without building independent muscle memory. Here is the proven 3-phase framework to break free.",
                """### What is 'Tutorial Hell'?
Tutorial hell happens when you can follow along with a video tutorial smoothly, but the moment you open a blank code editor, you freeze and have no idea what to type first.

### Why It Happens:
Watching someone else code activates passive recognition rather than active retrieval. Your brain feels like it understands because the instructor already solved the hard part: structuring the problem.

### The 3-Phase Escape Framework:
1. **The 20-Minute No-Copy Rule**: When watching a tutorial, watch in 10-minute blocks without typing. Then pause the video and reproduce the code from memory and reasoning alone.
2. **Break and Mod**: Whenever a tutorial project is finished, force yourself to make 3 significant modifications (e.g. add a new feature, change the database, add error handling).
3. **Build the 'Ugly Version 1'**: Pick a tiny real problem you face. Write the code without looking up full solutions. It's okay if it looks messy—refactoring comes after working functionality.""",
                "Never copy-paste code from a video without explaining every line out loud.\nAlways modify every tutorial project by adding at least 2 custom features.\nEmbrace the blank editor: outline the logic in plain English before writing code.\nRecord what confused you in your Personal Learning Memory immediately.",
                True
            ),
            (
                "Debugging Secrets from Senior Engineers: How to Fix Any Python Error",
                "debugging",
                "Errors and tracebacks are not failures; they are the exact roadmap Python gives you to fix your code. Learn how to read tracebacks, use print debugging effectively, and isolate bugs systematically.",
                """### Reading Python Tracebacks Like a Pro
Beginners often look at the top of a traceback and panic. **Senior engineers look at the very bottom line first.**

The bottom line tells you:
1. **The Error Type**: e.g., `IndexError`, `KeyError`, `TypeError`, `AttributeError`
2. **The Exact Message**: e.g., `list index out of range` or `'NoneType' object has no attribute 'get'`

### The Systematic 4-Step Debugging Protocol:
1. **Read the bottom line**: What failed?
2. **Read the line number**: In which file and line did Python halt?
3. **Inspect the variables**: Print `type()` and `repr()` of the variables right before the failing line.
4. **Isolate the hypothesis**: Change ONE variable or condition at a time and re-run.""",
                "Always read Python tracebacks starting from the bottom line, not the top.\nPrint both the value and type of variables when debugging: print(f'{val=} {type(val)=}').\nDo not guess solutions randomly: form a single hypothesis, test it, and verify.\nLog your recurring mistakes in the LearningHub Mistake Tracker so you never repeat them.",
                True
            ),
            (
                "The Python Internship Blueprint: What Hiring Managers Actually Care About",
                "interview",
                "What distinguishes a strong college candidate from hundreds of generic applicants? Practical engineering habits, clean code readability, and deep conceptual clarity.",
                """### What Hiring Managers Look For:
1. **Can you explain basic concepts simply?** If asked 'What is the difference between a list and a tuple?', can you explain memory mutability, hashability, and performance trade-offs clearly?
2. **Do you write idiomatic Python?** Do you use list comprehensions, f-strings, and `enumerate()`, or are you writing C-style code in Python?
3. **Do your projects have depth?** One polished project with unit tests, clear documentation, and persistent data is worth ten half-finished clones.
4. **How do you handle being stuck?** Good candidates talk through their reasoning, ask clarifying questions, and test edge cases.""",
                "Master Python fundamental data structures and their time complexity.\nEnsure your GitHub projects have stellar READMEs, setup steps, and tests.\nPractice explaining technical concepts in plain English using simple analogies.\nKnow how to discuss mistakes you made and how you resolved them.",
                True
            ),
            (
                "The Top 10 Python Gotchas Every Beginner Stumbles Into",
                "mistakes",
                "Save hours of frustration by learning the 10 most common subtle Python pitfalls before they bite your code.",
                """### 1. The Mutable Default Argument Trap
`def append_to(item, target=[]):` creates a list that persists across calls! Always use `target=None`.

### 2. Modifying a List While Iterating Over It
Modifying `lst` while running `for item in lst:` skips elements because indices shift. Iterate over `lst.copy()` or use a comprehension.

### 3. Confusing `is` with `==`
`a == b` checks equality; `a is b` checks memory identity. Only use `is` for `None` checks.

### 4. Floating Point Rounding
`0.1 + 0.2 != 0.3`. Use `math.isclose()` for float comparisons.

### 5. Shadowing Built-In Names
Naming a variable `list = [1, 2]` breaks Python's built-in `list()` function in that scope!""",
                "Never use mutable default arguments ([], {}) in functions.\nNever modify a list while iterating over it in a for loop.\nDo not name variables after Python built-ins like list, str, dict, id, max.\nUse math.isclose() when comparing floating point numbers.",
                False
            ),
            (
                "Building Resume-Worthy Python Projects That Stand Out",
                "projects",
                "How to pick, design, architect, and ship Python projects that grab recruiters' attention and survive technical deep-dives.",
                """### The Golden Rule of Portfolio Projects:
**Build for an actual user (even if that user is just yourself).**

### What Makes a Project Stand Out:
- **Real Problem**: An app that solves a specific student pain point (e.g. revision tracking) stands out far more than another generic calculator.
- **Architectural Cleanliness**: Clean folder structure, separated models/views/services, and environment variables for secrets.
- **Test Coverage**: Having even 5-10 solid unit tests signals professional engineering maturity.
- **Live Demo & Clear Docs**: If a recruiter can click a link or follow 2 commands to test your app, your interview rate skyrockets.""",
                "Pick projects with genuine utility over generic clones.\nStructure repositories with clean separation of concerns and no hardcoded secrets.\nInclude interactive documentation and setup instructions.\nBe prepared to explain the toughest bug you solved in the project during interviews.",
                False
            ),
            (
                "How to Maintain Daily Coding Consistency Without Burnout",
                "strategy",
                "Consistency beats intensity every single time. Here is how to maintain a 30-day streak by designing micro-habits that survive busy exam weeks.",
                """### The 20-Minute Minimum Rule:
On your busiest days (exams, travel, fatigue), commit to just **20 minutes of focused Python learning**. Review one flashcard topic, write down one Personal Learning Memory note, or solve one easy practice problem.

Maintaining the unbroken habit of daily progress is 10x more valuable than coding for 8 hours on Sunday and doing nothing for the next six days.""",
                "Set a sustainable daily goal (30 to 45 minutes) rather than overwhelming targets.\nUse the LearningHub Daily Learning Plan to know your exact task immediately.\nProtect your streak: on busy days, complete at least one micro-task.\nTrack your progress visually to reinforce positive momentum.",
                False
            )
        ]

        for a_title, a_cat, a_sum, a_content, a_rules, a_feat in mentor_articles:
            MentorArticle.objects.get_or_create(
                title=a_title,
                defaults={
                    'category': a_cat,
                    'summary': a_sum,
                    'content': a_content,
                    'actionable_rules': a_rules,
                    'is_featured': a_feat,
                    'read_time_minutes': 5
                }
            )

        mentor_tips = [
            ("The Rubber Duck Technique", "When stuck on a logic bug, explain your code line-by-line out loud to an inanimate object (or a friend). The act of speaking forces your brain to examine assumptions you took for granted.", "Debugging"),
            ("PEP 8 Whitespace Rule", "Always use 4 spaces per indentation level in Python. Never mix tabs and spaces, as it causes subtle IndentationError bugs.", "Syntax"),
            ("The Principle of Least Surprise", "Write code that does exactly what a developer reading it would expect. Avoid clever one-liners if a 3-line readable function is clearer.", "Clean Code"),
            ("Memory Analogy for Tuples", "Think of a list as an open whiteboard you can erase and rewrite; think of a tuple as a printed stone tablet that is permanent and immutable.", "Mental Model"),
            ("Premature Optimization", "Make it work, make it right, make it fast—in that exact order. Don't worry about microsecond performance before your program is correct and clean.", "Strategy"),
            ("Active Recall Revision", "When revising a topic, write down everything you remember about it BEFORE looking at the notes. Active recall creates 3x stronger memory pathways than re-reading.", "Learning")
        ]

        for t_idx, (t_title, t_tip, t_cat) in enumerate(mentor_tips, start=1):
            MentorTip.objects.get_or_create(
                title=t_title,
                defaults={
                    'short_tip': t_tip,
                    'category': t_cat,
                    'icon': 'lightbulb',
                    'order': t_idx
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Created Mentor Guidance Articles and Tips."))

        # 7. Create Student Stories (Testimonials)
        stories_data = [
            ("Priya Sharma", "2nd Year Computer Science Student", "#3B82F6", "PS", "Before LearningHub, I had 50 bookmarked YouTube videos and zero direction. The Personal Learning Memory feature changed everything—now when I revise, I review my own mental models instead of re-watching hour-long videos!", "Cracked Backend Python Internship", 1),
            ("Marcus Vance", "Self-Taught Developer", "#10B981", "MV", "The daily planner eliminates decision fatigue. I open LearningHub, see my exact 45-minute plan for the day, code, track my mistakes, and see real tangible progress every single evening.", "Landed Junior Software Engineer Role", 2),
            ("Ananya Patel", "Information Technology Major", "#8B5CF6", "AP", "The Revision Recommendation Engine noticed I was making mistakes in nested loops and flagged it for review right before my college lab exam. I scored an A+!", "Scored A+ in Python Lab & Coursework", 3),
            ("Liam O'Connor", "Data Science Aspirant", "#F59E0B", "LO", "The AI assistant actually uses my logged doubts and analogies to explain tricky concepts in terms I already understand. It feels like having a personal senior mentor available 24/7.", "Built 3 Open-Source Python Data Projects", 4),
        ]

        for name, role, color, init, quote, outcome, ord_val in stories_data:
            StudentStory.objects.get_or_create(
                name=name,
                defaults={
                    'role_or_college': role,
                    'avatar_color': color,
                    'initials': init,
                    'quote': quote,
                    'outcome': outcome,
                    'order': ord_val
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Created Student Success Stories."))

        # 8. Seed Rich Demo Progress & Personal Learning Memory for demo_student
        self.stdout.write(self.style.NOTICE("Populating rich student journey for 'demo_student'..."))

        # Topic 1: Intro to Python -> Completed, Strong
        p1, _ = UserTopicProgress.objects.get_or_create(user=demo_user, topic=all_topics[0])
        p1.status = 'completed'
        p1.understanding_level = 'strong'
        p1.is_completed = True
        p1.completed_at = timezone.now() - datetime.timedelta(days=4)
        p1.times_reviewed = 2
        p1.save()

        PersonalLearningMemory.objects.get_or_create(
            user=demo_user,
            topic=all_topics[0],
            defaults={
                'what_i_understood': "Python compiles source code into .pyc bytecode, which is executed line-by-line by the PVM. Indentation is mandatory syntax, not optional formatting.",
                'my_own_explanation': "Python is like a smart translator who reads your recipe line by line and directs the kitchen staff immediately, rather than waiting for the whole cookbook to be published.",
                'real_life_analogy': "Like an interpreter at the UN translating a live speech into another language in real time.",
                'my_code_example': "import sys\nprint(f'Running Python {sys.version.split()[0]} on {sys.platform}')",
                'what_confused_me': "Initially confused why Python creates __pycache__ folders until I understood bytecode caching.",
                'what_helped_me': "Typing 'import this' in terminal and reading the Zen of Python."
            }
        )

        # Topic 2: Variables -> Completed, Comfortable
        p2, _ = UserTopicProgress.objects.get_or_create(user=demo_user, topic=all_topics[1])
        p2.status = 'completed'
        p2.understanding_level = 'comfortable'
        p2.is_completed = True
        p2.completed_at = timezone.now() - datetime.timedelta(days=3)
        p2.save()

        PersonalLearningMemory.objects.get_or_create(
            user=demo_user,
            topic=all_topics[1],
            defaults={
                'what_i_understood': "Variables in Python are named tags or pointers attached to objects in heap memory. Assigning b = a makes both variables point to the same object.",
                'my_own_explanation': "Variables are sticky name tags you slap onto boxes in memory. Multiple sticky tags can be placed on the exact same box.",
                'real_life_analogy': "Two people having nicknames for the exact same physical house.",
                'my_code_example': "x = [1, 2, 3]\ny = x\nprint(id(x) == id(y)) # True",
                'what_confused_me': "Why mutating a list through variable b also changes variable a.",
                'what_helped_me': "Visualizing memory pointers on PythonTutor.com and understanding list.copy()."
            }
        )

        # Topic 3: Core Data Types -> Completed, Need Revision
        p3, _ = UserTopicProgress.objects.get_or_create(user=demo_user, topic=all_topics[2])
        p3.status = 'completed'
        p3.understanding_level = 'need_revision'
        p3.is_completed = True
        p3.completed_at = timezone.now() - datetime.timedelta(days=2)
        p3.save()

        PersonalLearningMemory.objects.get_or_create(
            user=demo_user,
            topic=all_topics[2],
            defaults={
                'what_i_understood': "Python ints have infinite precision. Floats follow IEEE 754 and have binary rounding caveats. None represents the absence of a value.",
                'my_own_explanation': "Integers are exact counting numbers; floats are approximations like measuring water with a ruler; None is an empty seat.",
                'real_life_analogy': "Trying to write 1/3 in decimal (0.3333...) is why computers can't store 0.1 perfectly in binary.",
                'my_code_example': "import math\nprint(math.isclose(0.1 + 0.2, 0.3)) # True!",
                'what_confused_me': "Why 0.1 + 0.2 == 0.3 evaluates to False in standard equality.",
                'what_helped_me': "Using math.isclose() whenever checking float values."
            }
        )

        # Log an active doubt for Topic 3
        LearningDoubt.objects.get_or_create(
            user=demo_user,
            topic=all_topics[2],
            doubt_text="When should I use decimal.Decimal instead of standard float for financial calculations?",
            defaults={
                'is_resolved': False
            }
        )

        # Topic 4: Input & Output -> Completed, Strong
        p4, _ = UserTopicProgress.objects.get_or_create(user=demo_user, topic=all_topics[3])
        p4.status = 'completed'
        p4.understanding_level = 'strong'
        p4.is_completed = True
        p4.completed_at = timezone.now() - datetime.timedelta(days=1)
        p4.save()

        # Topic 5: Operators -> In Progress, Need Revision
        p5, _ = UserTopicProgress.objects.get_or_create(user=demo_user, topic=all_topics[4])
        p5.status = 'in_progress'
        p5.understanding_level = 'need_revision'
        p5.is_completed = False
        p5.save()

        # Log a mistake for Topic 5
        LearningMistake.objects.get_or_create(
            user=demo_user,
            topic=all_topics[4],
            mistake_description="Used single '=' instead of '==' inside an if condition check, causing a SyntaxError in Python.",
            defaults={
                'correction_or_lesson': "In Python, '=' is strictly for variable assignment and cannot appear inside condition expressions. Always use '==' for equality checks.",
                'error_type': 'syntax',
                'code_snippet': "# Broken:\n# if status = 'active':\n\n# Correct:\nif status == 'active':\n    print('Welcome back!')"
            }
        )

        # Log a solved practice submission
        p_prob1 = PracticeProblem.objects.filter(topic=all_topics[0]).first()
        if p_prob1:
            UserPractice.objects.get_or_create(
                user=demo_user,
                problem=p_prob1,
                defaults={
                    'status': 'solved',
                    'my_solution_code': 'name = "Alex Chen"\ngoal = "Master Python Backend Engineering"\nhours_in_year = 365 * 24\nprint(f"Student: {name}")\nprint(f"Goal: {goal}")\nprint(f"Hours: {hours_in_year}")',
                    'reflection_notes': "Super simple, verified that f-strings calculate expressions directly inside curly braces.",
                    'time_spent_minutes': 5,
                    'solved_at': timezone.now() - datetime.timedelta(days=3)
                }
            )

        # Log bookmarks for demo_student
        res_sample = Resource.objects.filter(topic=all_topics[0]).first()
        if res_sample:
            Bookmark.objects.get_or_create(user=demo_user, resource=res_sample)

        res_sample2 = Resource.objects.filter(topic=all_topics[2]).first()
        if res_sample2:
            Bookmark.objects.get_or_create(user=demo_user, resource=res_sample2)

        # Log bootcamp progress for day 1 and 2
        day1 = BootcampDay.objects.filter(day_number=1).first()
        if day1:
            UserBootcampProgress.objects.get_or_create(
                user=demo_user,
                bootcamp_day=day1,
                defaults={
                    'is_completed': True,
                    'submission_notes': "Set up Python 3.11 in VS Code, ran test script successfully.",
                    'completed_at': timezone.now() - datetime.timedelta(days=2)
                }
            )

        day2 = BootcampDay.objects.filter(day_number=2).first()
        if day2:
            UserBootcampProgress.objects.get_or_create(
                user=demo_user,
                bootcamp_day=day2,
                defaults={
                    'is_completed': True,
                    'submission_notes': "Practiced variable assignments and verified memory identities.",
                    'completed_at': timezone.now() - datetime.timedelta(days=1)
                }
            )

        self.stdout.write(self.style.SUCCESS("[DONE] LearningHub Database successfully populated with complete production-grade data!"))
