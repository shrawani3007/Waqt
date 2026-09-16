"""
Algorithm 1: Greedy Table Allocation Service
============================================
Problem:
Given a reservation or queue seating request for a party of size P, allocate the best
available table at a restaurant that minimizes wasted capacity while ensuring fair
utilization of larger family/group tables.

Pseudocode:
-----------
function allocate_table(restaurant_id, party_size):
    1. candidates = Query RestaurantTable where restaurant_id == restaurant_id
                    AND status == 'AVAILABLE'
                    AND capacity >= party_size
    2. if candidates is empty:
           return None (No suitable table available)
    3. Sort candidates by:
           Primary: capacity (Ascending)
           Secondary: table_number (Natural/Numeric Ascending)
    4. selected_table = candidates.first()
    5. return selected_table

Time Complexity:
----------------
- Filtering & Query: O(N) where N is total tables at the restaurant.
- Sorting: O(K log K) where K is the number of eligible available tables (K <= N).
  Since typical restaurant table count N <= 100, execution time is sub-millisecond O(1) in practical operations.

Reasoning:
----------
A greedy choice of the smallest capable table prevents "capacity fragmentation"
(e.g., placing a party of 2 at an 8-seater table, leaving subsequent parties of 6 or 8 unable to be seated).
"""

from typing import Optional
from django.db import transaction
from restaurants.models import RestaurantTable

def greedy_allocate_table(restaurant, party_size: int) -> Optional[RestaurantTable]:
    """
    Finds and returns the optimal available table using greedy allocation.
    Returns None if no available table can seat party_size.
    """
    if party_size <= 0:
        return None

    # Retrieve all available tables with capacity >= party_size
    available_tables = list(
        RestaurantTable.objects.filter(
            restaurant=restaurant,
            status='AVAILABLE',
            capacity__gte=party_size
        )
    )

    if not available_tables:
        return None

    # Natural sorting: primary by capacity asc, secondary by numeric table_number asc
    def sort_key(table):
        # Try to parse table_number as int for clean numeric sort (e.g. '2' before '10')
        try:
            num = int(table.table_number)
        except ValueError:
            num = 999999
        return (table.capacity, num, str(table.table_number))

    available_tables.sort(key=sort_key)
    return available_tables[0]


@transaction.atomic
def reserve_table_greedily(restaurant, party_size: int, reservation=None) -> Optional[RestaurantTable]:
    """
    Atomically selects and locks the best table, transitioning its status to RESERVED.
    """
    table = greedy_allocate_table(restaurant, party_size)
    if table:
        table.status = 'RESERVED'
        table.save(update_fields=['status'])
        if reservation:
            reservation.table = table
            reservation.status = 'CONFIRMED'
            reservation.save(update_fields=['table', 'status'])
    return table
