from collections import Counter

class DataStatistics:
    def mean(self, data):
        """
        Compute the mean (average) of the input data.
        
        Args:
            data (list): A list of numerical values.
        
        Returns:
            float: The mean value, rounded to two decimal places.
        """
        total = sum(data)
        count = len(data)
        average = total / count
        return round(average, 2)
    
    def median(self, data):
        """
        Compute the median of the input data.
        
        Args:
            data (list): A list of numerical values.
        
        Returns:
            float: The median value, rounded to two decimal places.
        """
        sorted_data = sorted(data)
        n = len(data)
        if n % 2 == 1:
            median_val = sorted_data[n // 2]
        else:
            median_val = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        return round(median_val, 2)
    
    def mode(self, data):
        """
        Compute the mode(s) of the input data.
        
        Args:
            data (list): A list of numerical values.
        
        Returns:
            list: A list of mode(s), each as a float.
        """
        counts = Counter(data)
        max_freq = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_freq]
        return [float(x) for x in modes]


stats = DataStatistics()
data = [1, 2, 3, 4, 5]

print("Mean:", stats.mean(data))     # Output: 3.0
print("Median:", stats.median(data)) # Output: 3.0
print("Mode:", stats.mode(data))     # Output: [2.0, 3.0] (if data is [1,2,3,3,4,5])
