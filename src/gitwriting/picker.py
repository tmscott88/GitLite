"""
Picker class with some modifications to suit my project 
* Forked from aisk/pick: https://github.com/aisk/pick/tree/master/src/pick
"""

import curses
import textwrap
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Container, Generic, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union

__all__ = ["Picker", "pick", "Option"]


@dataclass
class Option:
    """Used to populate a Picker"""
    label: str
    value: Any = None
    description: Optional[str] = None
    enabled: bool = True


KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"))
KEYS_DOWN = (curses.KEY_DOWN, ord("j"))
KEYS_SELECT = (curses.KEY_RIGHT, ord(" "))

SYMBOL_CIRCLE_FILLED = "(x)"
SYMBOL_CIRCLE_EMPTY = "( )"

OPTION_T = TypeVar("OPTION_T", str, Option)
PICK_RETURN_T = Tuple[OPTION_T, int]

Position = namedtuple('Position', ['y', 'x'])

@dataclass
class Picker(Generic[OPTION_T]):
    """The grande picker class"""
    options: Sequence[OPTION_T]
    title: Optional[str] = None
    indicator: str = "*"
    default_index: int = 0
    selected_indicies: List[int] = field(init=False, default_factory=list)
    index: int = field(init=False, default=0)
    screen: Optional["curses._CursesWindow"] = None
    position: Position = Position(0, 0)
    quit_keys: Optional[Union[Container[int], Iterable[int]]] = None

    def __post_init__(self) -> None:
        if len(self.options) == 0:
            raise ValueError("options should not be an empty list")

        if self.default_index >= len(self.options):
            raise ValueError("default_index should be less than the length of options")

        if all(isinstance(option, Option) and not option.enabled for option in self.options):
            raise ValueError(
                "all given options are disabled, you must at least have one enabled option."
            )

        self.index = self.default_index
        option = self.options[self.index]
        if isinstance(option, Option) and not option.enabled:
            self.move_down()

    def move_up(self) -> None:
        """Move the cursor up"""
        while True:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.options) - 1
            option = self.options[self.index]
            if not isinstance(option, Option) or option.enabled:
                break

    def move_down(self) -> None:
        """Move the cursor down"""
        while True:
            self.index += 1
            if self.index >= len(self.options):
                self.index = 0
            option = self.options[self.index]
            if not isinstance(option, Option) or option.enabled:
                break

    def get_selected(self) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
        """return the current selected option as a tuple: (option, index)"""
        return self.options[self.index], self.index

    def get_title_lines(self, *, max_width: int = 80) -> List[str]:
        """Get title lines"""
        if self.title:
            return textwrap.fill(self.title, max_width - 2, drop_whitespace=False).split("\n") + [""]
        return []

    def get_option_lines(self) -> List[str]:
        """Get option lines"""
        lines: List[str] = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            option_as_str = option.label if isinstance(option, Option) else option
            lines.append(f"{prefix} {option_as_str}")

        return lines

    def get_lines(self, *, max_width: int = 80) -> Tuple[List[str], int]:
        """Get total lines"""
        title_lines = self.get_title_lines(max_width=max_width)
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self, screen: "curses._CursesWindow") -> None:
        """draw the curses ui on the screen, handle scroll if needed"""
        screen.erase()
        y, x = self.position  # start point

        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines(max_width=max_x)

        # calculate how many lines we should scroll, relative to the top
        scroll_top = 0
        if current_line > max_rows:
            scroll_top = current_line - max_rows

        lines_to_draw = lines[scroll_top : scroll_top + max_rows]

        description_present = False
        for option in self.options:
            if isinstance(option, Option) and option.description is not None:
                description_present = True
                break

        title_length = len(self.get_title_lines(max_width=max_x))

        for i, line in enumerate(lines_to_draw):
            if description_present and i > title_length:
                screen.addnstr(y, x, line, max_x // 2 - 2)
            else:
                screen.addnstr(y, x, line, max_x - 2)
            y += 1

        option = self.options[self.index]
        if isinstance(option, Option) and option.description is not None:
            description_lines = textwrap.fill(option.description, max_x // 2 - 2).split('\n')

            for i, line in enumerate(description_lines):
                screen.addnstr(i + title_length, max_x // 2, line, max_x - 2)

        screen.refresh()

    def run_loop(
        self, screen: "curses._CursesWindow"
    ) -> Union[List[PICK_RETURN_T], PICK_RETURN_T]:
        while True:
            self.draw(screen)
            c = screen.getch()
            if self.quit_keys is not None and c in self.quit_keys:
                return None, -1
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                return self.get_selected()

    def config_curses(self) -> None:
        """Configure curses"""
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
        except curses.error:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()

    def _start(self, screen: "curses._CursesWindow"):
        self.config_curses()
        return self.run_loop(screen)

    def start(self):
        """Start the process"""
        if self.screen:
            # Given an existing screen
            # don't make any lasting changes
            last_cur = curses.curs_set(0)
            ret = self.run_loop(self.screen)
            if last_cur:
                curses.curs_set(last_cur)
            return ret
        return curses.wrapper(self._start)


def pick(
    options: Sequence[OPTION_T],
    title: Optional[str] = None,
    indicator: str = "->",
    default_index: int = 0,
    screen: Optional["curses._CursesWindow"] = None,
    position: Position = Position(0, 0),
    quit_keys: Optional[Union[Container[int], Iterable[int]]] = None,
):
    """Define picker attributes"""
    picker: Picker = Picker(
        options,
        title,
        indicator,
        default_index,
        screen,
        position,
        quit_keys,
    )
    return picker.start()
