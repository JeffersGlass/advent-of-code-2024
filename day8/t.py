from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widgets import Footer, Header, Label, Static, DirectoryTree
from textual.widget import Widget

from day8part1 import AntennaMap

from pathlib import Path
from typing import Self, cast
from warnings import warn
class PositionLabel(Label):
    has_antinode = reactive(False)
    selected = reactive(False)

    def __init__(self, *args, antenna = False, antinode = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_antinode = antinode

    def watch_has_antinode(self, has_antinode: bool):
        if has_antinode:
            self.add_class("antinode")
        else:
            self.remove_class("antinode")

    def watch_selected(self, selected: bool):
        if selected:
            self.add_class("selected")
        else:
            self.remove_class("selected")

class LoadScreen(ModalScreen):
    BINDINGS = [("escape", "give_up", "Cancel")]

    class LoadMessage(Message):
        def __init__(self, path: Path | str):
            super().__init__()
            self.path = path

    def compose(self):
        yield Header(name="Select a data file")
        yield DirectoryTree('.')
        yield Footer()

    @on(DirectoryTree.FileSelected)
    def load_file(self, message: DirectoryTree.FileSelected):
        self.dismiss(message)

    def action_give_up(self):
        self.dismiss(None)

class AntennaApp(App):
    CSS_PATH = "antennas.tcss"
    SCREENS = {"load": LoadScreen}
    BINDINGS = [
        ("l", "file_screen", "Select Data File"),
        ('q', 'quit', 'Quit'),
        ('down', 'down_key'),
        ('up', 'up_key'),
        ('left', 'left_key'),
        ('right', 'right_key'),
        ('escape', 'clear_selection')
        ]
    
    selected_cell = reactive((-1, -1))
    debug_msg = reactive("Debug", init=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map: AntennaMap | None = None
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalGroup()
        yield Label(self.debug_msg, id="debug")
        yield Label("Result", id="result")
        yield Footer()
    
    def debug(self, s: str):
        self.debug_msg = s

    def watch_debug_msg(self, next):
        cast(Label, self.query_one("#debug")).update(next)            

    async def on_mount(self):
        await self.run_action('file_screen')

    def action_file_screen(self) -> None:
        def load_file(message: LoadScreen.LoadMessage | None) -> None:
            if message is None: return

            with open(message.path, "r") as f:
                data = f.readlines()
            
            self.map = AntennaMap(data)
            _antinodes = self.map.calc_all_resonant_nodes()
            assert self.map.antennas
            assert _antinodes
            cast(Label, self.query_one("#result")).update(f"{len(_antinodes)=}")
            self.debug(" ".join(str(s) for s in _antinodes))
            assert all(type(a[0]) == int and type(a[1]) == int for a in _antinodes)

            display = cast(VerticalGroup, self.query_one("VerticalGroup"))
            display.remove_children()
            for line in range(self.map.num_lines):
                labels = []
                for char in range(self.map.num_chars):
                    _symbol = "."
                    _classes: list[str] = []
                    for name, val in self.map.antennas.items():
                        if (line, char) in val: 
                            _symbol = name
                            break
                    if (line, char) in _antinodes:
                        if _symbol == ".": _symbol = "#"
                    new_label = PositionLabel(renderable=str(_symbol), id=f"l{line}_{char}", antinode=(line, char) in _antinodes)

                    
                    labels.append(new_label)
                        
                display.mount(HorizontalGroup(*labels))

        self.push_screen(LoadScreen(), load_file)

    def watch_selected_cell(self, previous: tuple[int, int], next: tuple[int, int]):
        if not self.map: return
        if next != (-1, -1) and not self.map.inbound(*next): return

        if previous is not None and self.map.inbound(*previous):
            line, char = previous[0], previous[1]
            previous_cell = cast(PositionLabel, self.query_exactly_one(f"#l{line}_{char}"))
            previous_cell.selected = False
        
        if next == (-1, -1): return
        
        line, char = next[0], next[1]
        next_cell = cast(PositionLabel, self.query_exactly_one(f"#l{line}_{char}"))
        next_cell.selected = True
        self.debug(f"Selected: {self.selected_cell} Classes: {", ".join(next_cell.classes)}")

    def do_arrow_key(self, delta: tuple[int, int]):
        if not self.map: return
        if self.selected_cell == (-1, -1):
            self.selected_cell = (0, 0)
            return
        
        next_line, char = self.selected_cell[0] + delta[0], self.selected_cell[1] + delta[1]
        if self.map.inbound(next_line, char):
            self.selected_cell = (next_line, char)

    def action_clear_selection(self):
        self.selected_cell = (-1, -1)

    def action_down_key(self):
        self.do_arrow_key((1, 0))

    def action_up_key(self):
        self.do_arrow_key((-1, 0))

    def action_left_key(self):
        self.do_arrow_key((0, -1))

    def action_right_key(self):
        self.do_arrow_key((0, 1))

if __name__ == "__main__":
    app = AntennaApp()
    app.run()