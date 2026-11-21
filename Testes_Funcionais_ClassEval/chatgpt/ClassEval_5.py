
import re


class AutomaticGuitarSimulator:
    def __init__(self, text) -> None:
        """
        Initialize the score to be played
        :param text: str, score to be played
        """
        self.play_text = text

    def interpret(self, display=False):
        """
        Interpret the music score to be played.
        :param display: bool, whether to print the interpreted score
        :return: list of dict containing Chord and Tune
        """
        if not self.play_text or not self.play_text.strip():
            return []

        play_list = []

        for item in self.play_text.split():
            match = re.fullmatch(r"([A-Za-z]+)([0-9]+)", item)

            if match:
                chord, tune = match.groups()

                play_list.append({
                    "Chord": chord,
                    "Tune": tune
                })

                if display:
                    self.display(chord, tune)

        return play_list

    def display(self, key, value):
        """
        Print out chord and play tune.
        :param key: str, chord
        :param value: str, play tune
        :return: str
        """
        result = (
            f"Normal Guitar Playing -- Chord: {key}, "
            f"Play Tune: {value}"
        )
        print(result)
        return result
