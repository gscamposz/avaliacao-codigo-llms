
class Words2Numbers:
    """
    The class provides a text-to-number conversion utility,
    allowing conversion of written numbers (in words) to
    their numerical representation.
    """

    def __init__(self):
        """
        Initialize the word lists and dictionaries required
        for conversion.
        """
        self.numwords = {}
        self.units = [
            "zero", "one", "two", "three", "four", "five",
            "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen",
            "fifteen", "sixteen", "seventeen", "eighteen",
            "nineteen",
        ]
        self.tens = [
            "", "", "twenty", "thirty", "forty",
            "fifty", "sixty", "seventy", "eighty", "ninety"
        ]
        self.scales = [
            "hundred", "thousand", "million",
            "billion", "trillion"
        ]

        self.numwords["and"] = (1, 0)

        for idx, word in enumerate(self.units):
            self.numwords[word] = (1, idx)

        for idx, word in enumerate(self.tens):
            self.numwords[word] = (1, idx * 10)

        for idx, word in enumerate(self.scales):
            self.numwords[word] = (10 ** (idx * 3 or 2), 0)

        self.ordinal_words = {
            'first': 1,
            'second': 2,
            'third': 3,
            'fifth': 5,
            'eighth': 8,
            'ninth': 9,
            'twelfth': 12
        }

        self.ordinal_endings = [
            ('ieth', 'y'),
            ('th', '')
        ]

    def text2int(self, textnum):
        """
        Convert the word string to the corresponding
        integer string.
        :param textnum: string, the word string to be converted
        :return: string, the final converted integer string
        >>> w2n = Words2Numbers()
        >>> w2n.text2int("thirty-two")
        '32'
        """
        if not isinstance(textnum, str):
            raise ValueError("Input must be a string")

        textnum = textnum.lower().strip()

        if not textnum:
            raise ValueError("Input cannot be empty")

        current = 0
        result = 0

        words = textnum.replace("-", " ").split()

        for word in words:
            if word in self.ordinal_words:
                scale = 1
                increment = self.ordinal_words[word]

            elif word in self.numwords:
                scale, increment = self.numwords[word]

            else:
                converted = None

                for ending, replacement in self.ordinal_endings:
                    if word.endswith(ending):
                        candidate = (
                            word[:-len(ending)] + replacement
                        )

                        if candidate in self.numwords:
                            converted = candidate
                            break

                if converted is None:
                    raise ValueError(
                        "Illegal word: " + word
                    )

                scale, increment = self.numwords[converted]

            if scale == 100:
                current = max(1, current) * scale

            elif scale > 100:
                current = (current + increment) * scale
                result += current
                current = 0

            else:
                current += increment

        return str(result + current)

    def is_valid_input(self, textnum):
        """
        Check if the input text contains only valid words
        that can be converted into numbers.
        :param textnum: The input text containing words
                        representing numbers.
        :return: True if input is valid, False otherwise.
        >>> w2n = Words2Numbers()
        >>> w2n.is_valid_input("thirty-two")
        False
        """
        if not isinstance(textnum, str):
            return False

        textnum = textnum.lower().strip()

        if not textnum:
            return False

        words = textnum.split()

        for word in words:
            if word in self.numwords:
                continue

            if word in self.ordinal_words:
                continue

            valid_ordinal = False

            for ending, replacement in self.ordinal_endings:
                if word.endswith(ending):
                    candidate = (
                        word[:-len(ending)] + replacement
                    )

                    if candidate in self.numwords:
                        valid_ordinal = True
                        break

            if not valid_ordinal:
                return False

        return True
