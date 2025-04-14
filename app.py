from textual.app import App, ComposeResult
from textual.widgets import Digits, Button
from textual.reactive import reactive
from textual.containers import HorizontalGroup, VerticalGroup
from time import monotonic

# https://github.com/Textualize/textual
# https://textual.textualize.io/tutorial/
# a lot of code taken from above two sources for the sake of practice and learning.

class TimeDisplay(Digits):

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        self.total = 0
        self.time = 0

    class Stopwatch(HorizontalGroup):

        def on_button_pressed(self, event: Button.Pressed) -> None:
            button_id = event.button.id
            time_display = self.query_one(TimeDisplay)
            if button_id == "start":
                time_display.start()
                self.add_class("started")
            elif button_id == "stop":
                time_display.stop()
                self.remove_class("started")
            elif button_id == "reset":
                time_display.reset()
                

        def compose(self) -> ComposeResult:
            yield Button("Start", id="start", variant="success")
            yield Button("Pause", id="stop", variant="error")
            yield Button("Reset", id="reset")
            yield TimeDisplay()

class App(App):
    
    CSS_PATH = "timer.tcss"
    
    def compose(self) -> ComposeResult:
        yield VerticalGroup(TimeDisplay.Stopwatch())


if __name__ == "__main__":
    app = App()
    app.run()