import io
import contextlib
import traceback


def run_python(code: str) -> str:
    """
    Execute Python code and return captured stdout.
    """

    stdout = io.StringIO()

    namespace = {
        "__name__": "__main__",
    }

    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, namespace)

        output = stdout.getvalue()

        if not output.strip():
            output = "(no output)"

        return output[-8000:]

    except Exception:
        return traceback.format_exc()[-8000:]