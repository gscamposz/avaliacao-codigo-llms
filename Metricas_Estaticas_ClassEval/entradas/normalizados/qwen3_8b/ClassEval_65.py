class NumberToWords:
    def __init__(self):
        self.NUMBER = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]

    def trans_two(self, s):
        first = int(s[0])
        second = int(s[1])
        if first == 0:
            if second == 0:
                return "ZERO"
            else:
                return self.NUMBER[second]
        elif first == 1:
            return self.NUMBER_TEEN[second]
        else:
            tens = self.NUMBER_TEN[first - 1]
            if second == 0:
                return tens
            else:
                return f"{tens} {self.NUMBER[second]}"

    def trans_three(self, s):
        hundreds = int(s[0])
        tens = int(s[1])
        units = int(s[2])
        result = []

        if hundreds > 0:
            result.append(f"{self.NUMBER[hundreds]} HUNDRED")
            if tens * 10 + units > 0:
                result.append("AND")
                result.append(self.trans_two(f"{tens}{units}"))
        else:
            result.append(self.trans_two(f"{tens}{units}"))

        return " ".join(result)


converter = NumberToWords()
print(converter.trans_two("23"))     # "TWENTY THREE"
print(converter.trans_two("05"))     # "FIVE"
print(converter.trans_two("10"))     # "TEN"
print(converter.trans_two("15"))     # "FIFTEEN"
print(converter.trans_two("100"))    # Error: Input is not two digits

print(converter.trans_three("123"))  # "ONE HUNDRED AND TWENTY THREE"
print(converter.trans_three("000"))  # "ZERO"
print(converter.trans_three("023"))  # "TWENTY THREE"
print(converter.trans_three("100"))  # "ONE HUNDRED"
print(converter.trans_three("101"))  # "ONE HUNDRED AND ONE"
