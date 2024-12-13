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
class PositionLabel(Label):
    def __init__(self, *args, antenna = False, antinode = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_antenna = reactive(antenna)
        self.has_antinode = reactive(antinode)
        self.add_class("position")

    def watch_has_antenna(self, has_antenna: bool):
        if has_antenna:
            self.add_class("antenna")
        else:
            self.remove_class("antenna")

    def watch_has_antinode(self, has_antinode: bool):
        if has_antinode:
            self.add_class("antinode")
        else:
            self.remove_class("antinode")

class LoadScreen(ModalScreen["Self.LoadMessage"]):
    BINDINGS = [("escape", "give_up", "Cancel")]

    class LoadMessage(Message):
        def __init__(self, path: Path | str):
            self.path = path
            super().__init__()

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
        ('q', 'quit', 'Quit')]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalGroup()
        yield Footer()

    async def on_mount(self):
        await self.run_action('file_screen')

    def action_file_screen(self) -> None:
        def load_file(message: LoadScreen.LoadMessage | None) -> None:
            if message is None: return

            with open(message.path, "r") as f:
                data = f.readlines()
            
            map = AntennaMap(data)
            _antinodes = map.calc_all_antinodes()
            assert map.antennas is not None

            display = cast(VerticalGroup, self.query_one("VerticalGroup"))
            display.remove_children()
            for line in range(map.num_lines):
                labels = []
                for char in range(map.num_chars):
                    _symbol = "."
                    _classes = ""
                    for name, val in map.antennas.items():
                        if (line, char) in val: 
                            _symbol = name
                            _classes += " antenna"
                            break
                    if (line, char) in _antinodes:
                        if _symbol == ".": _symbol = "#"
                        _classes += " antinode"

                    labels.append(PositionLabel(renderable=str(_symbol), classes=_classes, name=f"({line},{char})"))
                        
                display.mount(HorizontalGroup(*labels))

        self.push_screen(LoadScreen(), load_file)
    
    def compose_demo(self) -> ComposeResult:
        yield Header()
        for i in range(2):
            yield(HorizontalGroup(
                *[PositionLabel(renderable=str(i), classes="", name=f"({i},{j})") for j in range(12)]  
            ))
        for i in range(3):
            yield(HorizontalGroup(
                *[PositionLabel(renderable=str(i), classes="antinode", name=f"({i},{j})") for j in range(12)]  
            ))
        for i in range(4):
            yield(HorizontalGroup(
                *[PositionLabel(renderable=str(i), classes="antenna", name=f"({i},{j})") for j in range(10)]  
            ))
        yield Footer()    


if __name__ == "__main__":
    app = AntennaApp()
    app.run()