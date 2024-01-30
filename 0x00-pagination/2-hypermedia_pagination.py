#!/usr/bin/env python3
"""
Module with a simple helper function for pagination
"""

import csv
import math
from typing import List, Dict, Optional


index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a databasees.
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

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()
        if (end_index > len(dataset)):
            return []
        pageList = []
        for page in range(start_index, end_index):
            pageList.append(dataset[page])
        return pageList

    def get_hyper(self, page: int = 1, page_size: int = 10):
        """
        Return a dictionary with hypermedia pagination information.

        Parameters:
        - page: The page number (1-indexed).
        - page_size: The number of items per page.

        Returns:
        A dictionary with hypermedia pagination information.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
