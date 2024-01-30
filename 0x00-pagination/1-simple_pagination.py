#!/usr/bin/env python3
"""
Module with a simple helper function for pagination
"""

import csv
from typing import List


index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Return the appropriate page of the dataset.

        Parameters:
        - page: The page number (1-indexed).
        - page_size: The number of items per page.

        Returns:
        A list of rows for the specified page.
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0
        dataset = self.dataset()
        start, end = index_range(page, page_size)
        if (end > len(dataset)):
            return []
        pageList = []
        for page in range(start, end):
            pageList.append(dataset[page])
        return pageList
