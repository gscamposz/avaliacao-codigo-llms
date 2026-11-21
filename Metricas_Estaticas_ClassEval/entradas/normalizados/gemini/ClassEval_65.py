class NumberWordFormatter:
    """
    This is a class that provides to convert numbers into their corresponding English word representation, including handling the conversion of both the integer and decimal parts, and incorporating appropriate connectors and units.
    """

    def __init__(self):
        """
        Initialize NumberWordFormatter object.
        """
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
                            "EIGHTEEN",
                            "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
        self.NUMBER_SUFFIX = ["k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"]

    def format(self, x):
        """
        Converts a number into words format
        :param x: int or float, the number to be converted into words format
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format(123456)
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        if isinstance(x, float):
            s = repr(x)
        else:
            s = str(x)
        return self.format_string(s)

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        s = x.strip()
        if not s:
            return ""

        negative = False
        if s.startswith("-"):
            negative = True
            s = s[1:].strip()
        elif s.startswith("+"):
            s = s[1:].strip()

        if "." in s:
            int_part, dec_part = s.split(".", 1)
        else:
            int_part, dec_part = s, ""

        int_part = int_part.lstrip("0")
        if not int_part:
            int_words = "ZERO"
        else:
            groups = []
            for idx in range(len(int_part), 0, -3):
                start = max(0, idx - 3)
                chunk = int_part[start:idx]
                groups.append(chunk)

            parts = []
            for i, chunk in enumerate(groups):
                chunk_val = int(chunk)
                if chunk_val == 0:
                    continue
                three_words = self.trans_three(chunk)
                scale = self.parse_more(i)
                if scale:
                    parts.append(f"{three_words} {scale}".strip())
                else:
                    parts.append(three_words)

            parts.reverse()
            int_words = " ".join(parts).strip()

        if negative:
            int_words = f"MINUS {int_words}"

        if dec_part:
            dec_words_list = []
            for ch in dec_part:
                if ch.isdigit():
                    d = int(ch)
                    dec_words_list.append("ZERO" if d == 0 else self.NUMBER[d])
            if dec_words_list:
                return f"{int_words} POINT {' '.join(dec_words_list)} ONLY"

        return f"{int_words} ONLY"

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        s = s.zfill(2)[-2:]
        if s[0] == "0":
            return self.NUMBER[int(s[1])]
        if s[0] == "1":
            return self.NUMBER_TEEN[int(s[1])]
        ten_word = self.NUMBER_TEN[int(s[0]) - 1]
        one_word = self.NUMBER[int(s[1])]
        if one_word:
            return f"{ten_word} {one_word}"
        return ten_word

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        s = s.zfill(3)[-3:]
        hundred_digit = int(s[0])
        rest = s[1:]
        two_words = self.trans_two(rest)
        if hundred_digit == 0:
            return two_words
        hundred_words = f"{self.NUMBER[hundred_digit]} HUNDRED"
        if two_words:
            return f"{hundred_words} AND {two_words}"
        return hundred_words

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        if 0 <= i < len(self.NUMBER_MORE):
            return self.NUMBER_MORE[i]
        return ""