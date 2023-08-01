from dataclasses import dataclass, field
import datetime


@dataclass
class Item:
    amount: int = None
    product_name: str = None
    price_cents: int = None
    subitem: str = None


@dataclass
class PrepareLocation:
    location_name: str = ''
    items: list[Item] = field(default_factory=list)


@dataclass
class Order:
    table_name: str = ''
    payment_status: str = ''
    order_num: int = None
    payment_method: str = ''
    customer: str = ''
    prepare_location: str = ''
    total_price_cents: int = None
    total_items_amount: int = None
    order_datetime: datetime.datetime = None
    # prepare_locations: list[PrepareLocation] = field(default_factory=list)
    items: list[Item] = field(default_factory=list)
