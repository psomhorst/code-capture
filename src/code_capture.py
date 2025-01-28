from bunch_py3 import Bunch
import inspect
import linecache
import itertools
from typing import Callable, Optional, Type
from types import TracebackType


class CodeCapture:
    key: str
    store = Bunch()

    def __init__(
            self,
            key: str,
            line_processor: Callable[[str], Optional[str]] = None
    ) -> None:
        """Create a new CodeCapture instance.
        
        Args:
            key: The key to store the captured code under.
            line_processor: An optional function that pre-processes each line of code
                before storing it. The line_processor function can return None to
                omit the line from the captured code.
        """
        self.key = key
        self.line_processor = line_processor

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]], 
        exc_value: Optional[BaseException], 
        traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        cf = inspect.currentframe().f_back
        filename = cf.f_code.co_filename
        line_number = cf.f_lineno
        lines = []
        indent = None

        for i in itertools.count(start=1):
            line = linecache.getline(filename, line_number + i)

            if self.line_processor:
                line = self.line_processor(line)
                if line is None:
                    continue

            line_indent = len(line) - len(line.lstrip())

            if indent is None:
                indent = line_indent
            elif (line_indent < indent and len(line.strip()) > 0) or line == "":
                break

            if line == "\n":  # preserve newlines
                lines.append(line)
            else:
                lines.append(line[indent:])

        content = "".join(lines)
        self.store[self.key] = content
