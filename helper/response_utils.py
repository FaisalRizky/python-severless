from collections import OrderedDict

def build_success_response(data_list, current_page=1, total_pages=1, total_items=0, items_per_page=10):
    """
    Build a structured JSON success response with a consistent order.

    Parameters:
    - data_list: The main data content as a list.
    - current_page: Current page number for pagination (default is 1).
    - total_pages: Total number of pages available (default is 1).
    - total_items: Total number of items available (default is 0).
    - items_per_page: Number of items per page (default is 10).

    Returns:
    - OrderedDict: An ordered dictionary representing the JSON success response.
    """
    response = OrderedDict([
        ("status", "Success"),
        ("message", "Data retrieved successfully"),
        ("data", data_list),
        ("pagination", OrderedDict([
            ("current_page", current_page),
            ("total_pages", total_pages),
            ("total_items", total_items),
            ("items_per_page", items_per_page)
        ]))
    ])
    
    return response
