from langchain_core.tools import tool
from ddgs import DDGS
from langchain_experimental.tools import PythonREPLTool

# ============
# Calculator Tool
# ==============
@tool
def calculator(first_nums: float, second_nums: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_nums + second_nums
        elif operation == "sub":
            result = first_nums - second_nums
        elif operation == "mul":
            result = first_nums * second_nums
        elif operation == "div":
            if second_nums == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_nums / second_nums
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"Answer": result}
    except Exception as e:
        return {"Error": str(e)}
    


# ============
# Web Search Tool
# ==============
@tool
def web_search(query: str,max_result:int) -> dict:
    """
    Search the web using DuckDuckGo and return results.
    """

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=max_result
                )
            )

        if not results:
            return "No results found."

        formatted_results = []

        for i, result in enumerate(results, start=1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No Title')}\n"
                f"URL: {result.get('href', 'N/A')}\n"
                f"Snippet: {result.get('body', 'N/A')}\n"
            )

        return {"Answer":"\n".join(formatted_results)}

    except Exception as e:
        return { "Error":f"Search failed: {str(e)}"}




# ============
# Pyhton REPL Tool
# ==============
py_repl = PythonREPLTool()

FORBIDDEN = ["import", "__import__", "open(", "eval(", "exec(", "compile(", "os.", "sys.", "subprocess", "shutil",
    "socket", "requests", "urllib", "pathlib", "pickle", "ctypes", "globals(", "locals(", "vars(", "input(", ]

@tool
def python_repl(code: str) -> dict:
    """Execute simple Python code safely."""
    try:
        code_lower = code.lower()

        for item in FORBIDDEN:
            if item.lower() in code_lower:
                return f"Blocked: '{item}' is not allowed."

        return {str(py_repl.invoke(code))}

    except Exception as e:
        return {f"Error: {e}"}
