
class NumberWordFormatter:
    """
    This is a class that provides to convert numbers into their
    corresponding English word representation, including handling
    the conversion of both the integer and decimal parts.
    """

    def __init__(self):
        """
        Initialize NumberWordFormatter object.
        """
        self.NUMBER = [
            "", "ONE", "TWO", "THREE", "FOUR",
            "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"
        ]
        self.NUMBER_TEEN = [
            "TEN", "ELEVEN", "TWELVE", "THIRTEEN",
            "FOURTEEN", "FIFTEEN", "SIXTEEN",
            "SEVENTEEN", "EIGHTEEN", "NINETEEN"
        ]
        self.NUMBER_TEN = [
            "TEN", "TWENTY", "THIRTY", "FORTY",
            "FIFTY", "SIXTY", "SEVENTY",
            "EIGHTY", "NINETY"
        ]
        self.NUMBER_MORE = [
            "", "THOUSAND", "MILLION", "BILLION"
        ]
        self.NUMBER_SUFFIX = [
            "k", "w", "", "m", "", "", "b", "",
            "", "t", "", "", "p", "", "", "e"
        ]

    def format(self, x):
        """
        Converts a number into words format.
        :param x: int or float
        :return: str
        >>> formatter = NumberWordFormatter()
        >>> formatter.format(123456)
        'ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY'
        """
        return self.format_string(str(x))

    def format_string(self, x):
        """
        Converts a string representation of a number
        into words format.
        :param x: str
        :return: str
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        'ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY'
        """
        x = str(x).strip()

        if not x:
            return "ZERO ONLY"

        negative = x.startswith("-")

        if x[0:1] in ("-", "+"):
            x = x[1:]

        if "." in x:
            integer_part, decimal_part = x.split(".", 1)
        else:
            integer_part = x
            decimal_part = ""

        integer_part = integer_part or "0"

        if not integer_part.isdigit():
            raise ValueError("Invalid number")

        if decimal_part and not decimal_part.isdigit():
            raise ValueError("Invalid decimal number")

        integer_part = integer_part.lstrip("0") or "0"

        if integer_part == "0":
            result = "ZERO"
        else:
            groups = []

            while integer_part:
                groups.append(integer_part[-3:])
                integer_part = integer_part[:-3]

            words = []

            for i in range(len(groups) - 1, -1, -1):
                group = groups[i]

                if int(group) == 0:
                    continue

                group_words = self.trans_three(group)
                suffix = self.parse_more(i)

                if suffix:
                    group_words += " " + suffix

                words.append(group_words)

            result = " ".join(words)

        if decimal_part and int(decimal_part) != 0:
            decimal_words = []

            for digit in decimal_part:
                decimal_words.append(
                    self.NUMBER[int(digit)] if digit != "0"
                    else "ZERO"
                )

            result += " POINT " + " ".join(decimal_words)

        if negative and (
            result != "ZERO"
        ):
            result = "MINUS " + result

        return result + " ONLY"

    def trans_two(self, s):
        """
        Converts a two-digit number into words format.
        :param s: str
        :return: str
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        'TWENTY THREE'
        """
        num = int(s)

        if num == 0:
            return ""

        if num < 10:
            return self.NUMBER[num]

        if num < 20:
            return self.NUMBER_TEEN[num - 10]

        tens = num // 10
        ones = num % 10

        result = self.NUMBER_TEN[tens - 1]

        if ones:
            result += " " + self.NUMBER[ones]

        return result

    def trans_three(self, s):
        """
        Converts a three-digit number into words format.
        :param s: str
        :return: str
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        'ONE HUNDRED AND TWENTY THREE'
        """
        num = int(s)

        if num == 0:
            return ""

        if num < 100:
            return self.trans_two(str(num))

        hundreds = num // 100
        remainder = num % 100

        result = self.NUMBER[hundreds] + " HUNDRED"

        if remainder:
            result += " AND " + self.trans_two(
                str(remainder)
            )

        return result

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix
        based on the index.
        :param i: int
        :return: str
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        'THOUSAND'
        """
        if i < 0:
            return ""

        if i < len(self.NUMBER_MORE):
            return self.NUMBER_MORE[i]

        extended = [
            "TRILLION", "QUADRILLION", "QUINTILLION",
            "SEXTILLION", "SEPTILLION", "OCTILLION",
            "NONILLION", "DECILLION"
        ]

        index = i - len(self.NUMBER_MORE)

        if index < len(extended):
            return extended[index]

        return "TEN TO THE POWER OF " + str(i * 3)
