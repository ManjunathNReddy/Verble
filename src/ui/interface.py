from abc import ABC, abstractmethod

class UI(ABC):
    @abstractmethod
    def display_text(self, text, color=None): pass

    @abstractmethod
    def get_input(self, prompt): pass

    @abstractmethod
    def show_guess_result(self, guess, validity): pass

    @abstractmethod
    def show_hint(self, indices, word): pass

    @abstractmethod
    def show_link(self, url): pass

    @abstractmethod
    def pause(self): pass
