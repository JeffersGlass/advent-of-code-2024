from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widgets import Footer, Header, Label, Static, DirectoryTree
from textual.widget import Widget

from day8part1 import load_data

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
    BINDINGS = [("escape", "app.pop_screen", "Cancel")]

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


class AntennaApp(App):

    CSS_PATH = "antennas.tcss"
    SCREENS = {"load": LoadScreen}
    BINDINGS = [
        ("l", "file_screen", "Select Data File"),
        ('q', 'quit', 'Quit')]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield PositionLabel("Hello world")
        yield Footer()

    def action_file_screen(self) -> None:
        def load_file(message: LoadScreen.LoadMessage | None) -> None:
            if message is None: return
            cast(PositionLabel, self.query_one("PositionLabel")).update(str(message.path))

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