from typing import Type
from datetime import datetime

from .order import Order, Item

from epos.document import EposDocument
from epos.elements import *


def epos_to_order(doc: EposDocument) -> Order:
    # Hope syntax of Dorst stays the same
    header = doc.body[:24]
    body = doc.body[24:-16]
    footer = doc.body[-16:]

    order = create_order_metadata(header, footer)

    # parsing of the body => all the items on the order
    body_lenght = len(body)
    index = 0
    print(f'{body_lenght = } elements')
    while index < body_lenght:
        # When finding a feed tag, this means we got all items for this production location.
        # Under this there is the 'line image' and then another feed of 20 units
        # Following then is again a list of all the items in the order that are not needed at this production location
        if body[index].tag == 'feed':
            break

        # Items always start with text element of 4 characters: '2x  ' or '14x ' or '135x'
        # If needed the can be changed to a regex match instead of checking lenght
        if body[index].tag != 'text' or len(body[index].text) != 4:
            raise ValueError(f"Can't find start of item, got {body[index].tag} {body[index].text} instead")

        item = match_item(body[index:index+5])
        index += 5

        # Is there an subitem? Always starts with 4 spaces
        while (index < body_lenght
               and body[index].text.startswith(' '*4)):
            item.subitem = match_subitem(body[index:index+2])
            index += 2

        order.items.append(item)

    # print(order)
    return order


def match_header(header: list[Type[BaseElement]]):
    """
    Fetch info from the first 24 elements of a dorst order.

    Table, payment_status, order_number, payment_method, printer_name and printer_location
    """

    if len(header) != 24:
        raise ValueError(f"Found {len(header)} objects in header, 25 required")

    match header:
        case [
            Text(smooth=True),
            Text(width=2, height=2),
            Text(text=table),  # Match
            Feed(unit=15),
            Text(text=payment_status),  # Match
            Text(),  # 480 of 456?
            Text(text=order_number),  # Match
            Feed(unit=15),
            Text(width=1, height=1),
            Text(reverse=False, underline=False, bold=True),
            Text(text=payment_method),  # Match
            Text(text=customer),  # Match
            # Text(),  # ??
            Text(text='\n'),
            Text(reverse=False, underline=False, bold=False),
            Feed(unit=49),
            Text(width=2, height=2),
            Text(text=printer_location),  # Match
            Feed(unit=49),
            Text(width=1, height=1),
            Feed(unit=20),
            Image(width=576, height=34),
            Feed(unit=20),
            Text(width=1, height=1),
            Text(align=Align.LEFT),
        ]:
            return (
                table.strip(),
                payment_status.strip(),
                int(order_number.strip("#\n ")),  # '#1234\n'
                payment_method.strip(),
                customer.strip(),
                printer_location.strip(),
            )
        case _:
            raise ValueError("Failed to parse header")


def match_footer(footer):
    if len(footer) != 16:
        raise ValueError(f"Found {len(footer)} objects in footer, 16 required")
    match footer:
        case [
            Feed(unit=20),
            Image(width=576, height=34),
            Feed(unit=20),
            Text(reverse=False, underline=False, bold=False),
            Feed(unit=20),
            Feed(unit=10),
            Text(),
            Text(text=total_price),  # Match
            Feed(unit=20),
            Image(width=576, height=34),
            Feed(unit=20),
            Text(width=1, height=1),
            Text(text=total_amount),  # Match
            Text(text=order_time),  # Match
            Feed(unit=40),
            Cut(),
        ]:
            return (
                int(float(total_price.strip().replace(',', '.'))*100),
                int(total_amount.replace('Totaal aantal stuks:', '').strip()),
                datetime.strptime(order_time.strip(), 'Besteld op %d/%m/%Y om %H:%M')
            )
        case _:
            raise ValueError("Can't match the footer")


def create_order_metadata(header, footer) -> Order:
    order = Order()

    header_data = match_header(header)
    order.table_name = header_data[0]
    order.payment_status = header_data[1]
    order.order_num = header_data[2]
    order.payment_method = header_data[3]
    order.customer = header_data[4]
    order.prepare_location = header_data[5]

    footer_data = match_footer(footer)
    order.total_price_cents = footer_data[0]
    order.total_items_amount = footer_data[1]
    order.order_datetime = footer_data[2]

    return order


def match_item(item):
    if len(item) != 5:
        raise ValueError(f"Found {len(item)} objects in item, 5 required")
    match item:
        case [
            Text(text=amount),  # Match
            Text(reverse=False, underline=False, bold=True),
            Text(text=product),  # Match
            Text(reverse=False, underline=False, bold=False),
            Text(text=price),  # Match
        ]:
            return Item(
                amount=amount.strip('\n x'),
                product_name=product.strip(),
                price_cents=int(float(price.strip().replace(",", "."))*100)
            )
        case _:
            raise ValueError("Can't match the item")


def match_subitem(subitem) -> str:
    if len(subitem) != 2:
        raise ValueError(f"Found {len(subitem)} objects in subitem, 2 required")
    match subitem:
        case [
            Text(text=subproduct),
            Feed(unit=10),
        ]:
            return subproduct.strip()
        case _:
            raise ValueError("Can't match the subitem")


