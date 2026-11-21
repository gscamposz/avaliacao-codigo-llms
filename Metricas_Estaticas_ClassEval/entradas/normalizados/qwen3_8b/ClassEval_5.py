import re

class AutomaticGuitarSimulator:
    def __init__(self, text):
        """
        Initialize the class with a string of musical notes.
        
        Args:
            text (str): A string containing musical notes in the format 'ChordDigitSequence'.
        """
        self.play_text = text

    def interpret(self, display=False):
        """
        Parse the input text into a list of dictionaries, each containing a chord and its associated tune.
        
        Args:
            display (bool): If True, prints the interpreted data (not used in this version).
        
        Returns:
            list: A list of dictionaries, each with keys 'Chord' and 'Tune'.
        """
        segments = self.play_text.split()
        result = []

        for segment in segments:
            match = re.fullmatch(r'([A-Za-z]+)(\d+)', segment)
            if match:
                chord = match.group(1)
                tune = match.group(2)
                result.append({'Chord': chord, 'Tune': tune})

        return result

    def display(self, key, value):
        """
        Generate a formatted string for a chord and its associated tune.
        
        Args:
            key (str): The chord (e.g., 'C', 'Em').
            value (str): The associated digit sequence (e.g., '53231323').
        
        Returns:
            str: A formatted string for display.
        """
        return f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"


simulator = AutomaticGuitarSimulator("C53231323 Em43231323 F43231323 G63231323")

# Interpret the input
interpreted = simulator.interpret()
print(interpreted)
# Output:
# [{'Chord': 'C', 'Tune': '53231323'}, {'Chord': 'Em', 'Tune': '43231323'}, ...]

# Display a specific chord and tune
print(simulator.display("C", "53231323"))
# Output:
# Normal Guitar Playing -- Chord: C, Play Tune: 53231323
