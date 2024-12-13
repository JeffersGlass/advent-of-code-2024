from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, Static
from textual.widget import Widget

class PositionLabel(Label):

    def __init__(self, antenna = False, antinode = False, *args, **kwargs):
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

class AntennaApp(App):

    CSS_PATH = "antennas.tcss"
    
    def compose(self) -> ComposeResult:
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