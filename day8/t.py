from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label

class PositionLabel(Label):
    has_antenna = reactive(False)
    has_antinode = reactive(False)

    def compose(self):
        r

class AntennaApp(App):

    CSS_PATH = "antennas.tcss"
    
    def compose(self) -> ComposeResult:
        yield Header()
        for i in range(10):
            yield(HorizontalGroup(
                *[PositionLabel(str(i), classes="position", name=f"({i},{j})") for j in range(10)]  
            ))
        yield Footer()

    


if __name__ == "__main__":
    app = AntennaApp()
    app.run()