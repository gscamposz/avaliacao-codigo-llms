class PageUtil:
    def __init__(self, data, page_size):
        """
        Initialize the PageUtil with data and a page size.
        
        Parameters:
        - data (list): The list of items to be paginated.
        - page_size (int): Number of items per page.
        """
        self.data = data
        self.page_size = page_size
        self.total_items = len(data)
        self.total_pages = (self.total_items + self.page_size - 1) // self.page_size

    def get_page(self, page_number):
        """
        Retrieve a specific page of data.
        
        Parameters:
        - page_number (int): The 1-based index of the page to retrieve.
        
        Returns:
        - list: The items for the specified page.
        """
        start = (page_number - 1) * self.page_size
        end = start + self.page_size
        return self.data[start:end]

    def get_page_info(self, page_number):
        """
        Get metadata and content for a specific page.
        
        Parameters:
        - page_number (int): The 1-based index of the page to retrieve.
        
        Returns:
        - dict: A dictionary containing the page metadata and data.
        """
        data = self.get_page(page_number)
        return {
            "current_page": page_number,
            "per_page": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1,
            "has_next": page_number < self.total_pages,
            "data": data
        }

    def search(self, keyword):
        """
        Search for items that match the given keyword.
        
        Parameters:
        - keyword (str): The string to search for in the items.
        
        Returns:
        - dict: A dictionary containing search results and metadata.
        """
        results = [item for item in self.data if keyword in str(item)]
        total_results = len(results)
        total_pages = (total_results + self.page_size - 1) // self.page_size
        return {
            "keyword": keyword,
            "total_results": total_results,
            "total_pages": total_pages,
            "results": results
        }


# Example usage
data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
page_size = 3
page_util = PageUtil(data, page_size)

# Get page 2
print(page_util.get_page(2))  # Output: [4, 5, 6]

# Get page info for page 2
print(page_util.get_page_info(2))
# Output:
# {
#     'current_page': 2,
#     'per_page': 3,
#     'total_pages': 3,
#     'total_items': 9,
#     'has_previous': True,
#     'has_next': True,
#     'data': [4, 5, 6]
# }

# Search for '5'
print(page_util.search('5'))
# Output:
# {
#     'keyword': '5',
#     'total_results': 1,
#     'total_pages': 1,
#     'results': [5]
# }
