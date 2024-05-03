#!/usr/bin/env python3
"""2.Hypermedia pagination"""
import csv
from math import ceil
from typing import Tuple, List, Dict, Union


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """The function should return a tuple of size two containing a start index
    and an end index corresponding to the range of indexes to return in a list
    for those particular pagination parameters"""
    start = (page - 1) * page_size
    end = page * page_size
    return(start, end)


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
        """finds the correct indexes to paginate the dataset correctly
        and return the appropriate page of the dataset"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        i_range = index_range(page, page_size)
        start = i_range[0]
        end = i_range[1]

        if end > len(self.dataset()):
            return []
        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """returns a dictionary containing data set pagination info"""
        data = self.get_page(page, page_size)

        if self.get_page(page + 1, page_size) == []:
            next_page = None
        else:
            next_page = (page + 1)

        if page == 1:
            prev_page = None
        else:
            prev_page = (page - 1)

        total_pages = ceil(len(self.dataset()) / page_size)

        return {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
