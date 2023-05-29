from abc import ABC
from typing import Type
from decimal import Decimal
from datetime import datetime

from .order import Order, Item

from epos.document import EposDocument
from epos.elements import *


class BaseFormat(ABC):
    def __init__(self, order: Order):
        self.order = order
    
    def print(self) -> EposDocument:
        doc = EposDocument()

        doc.body.extend(self.header())
        doc.body.extend(self.body())
        doc.body.extend(self.footer())

        return doc



    def header(self):
        pass
    def body(self):
        pass
    def footer(self):
        pass

class DorstFormat(BaseFormat):
    img_line = Image(
        width=576,
        height=34,
        text='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8A//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    )
    def header(self) -> tuple:
        max_len = 41
        max_len2 = 20
        table = f'{self.order.table_name:.{max_len2}}'
        payment_status = f'{self.order.payment_status:.{max_len2}}'
        order_number = f'#{self.order.order_num}\n'
        payment_method = f'{self.order.payment_method:.{max_len}}\n'
        name = f'{self.order.customer_name:.{max_len}}'
        printer_location = f'{self.order.prepare_location:<{max_len2}.{max_len2}}'

        header_elements = (
            Text(smooth=True),
            Text(width=2, height=2),
            Text(text=table),  # Variable
            Feed(unit=15),
            Text(text=payment_status),  # Variable
            Text(x=456),
            Text(text=order_number),  # Variable
            Feed(unit=15),
            Text(width=1, height=1),
            Text(reverse=False, underline=False, bold=True),
            Text(text=payment_method),  # Variable
            Text(text=name),  # Variable
            Text(),
            Text(text='\n'),
            Text(reverse=False, underline=False, bold=False),
            Feed(unit=49),
            Text(width=2, height=2),
            Text(text=printer_location),  # Variable
            Feed(unit=49),
            Text(width=1, height=1),
            Feed(unit=20),
            self.img_line,
            Feed(unit=20),
            Text(width=1, height=1),
            Text(align=Align.LEFT),
        )
        return header_elements

    def footer(self) -> tuple:
        total_price = f'{self.order.total_price:>7}\n'.replace('.', ',')
        total_amount = f'Totaal aantal stuks:{self.order.total_items_amount}\n'
        order_time = f'Besteld op {self.order.order_datetime:%d/%m/%Y om %H:%M}\n'

        footer_elements = (
            Feed(unit=20),
            self.img_line,
            Feed(unit=20),
            Text(reverse=False, underline=False, bold=False),
            Feed(unit=20),
            Feed(unit=10),
            Text(' '*4 + 'TOTAAL' + ' '*31),
            Text(text=total_price),  # Variable
            Feed(unit=20),
            self.img_line,
            Feed(unit=20),
            Text(width=1, height=1),
            Text(text=total_amount),  # Variable
            Text(text=order_time),  # Variable
            Feed(unit=40),
            Cut(),
        )
        return footer_elements

    def body(self) -> tuple:
        body_elements = []
        for item in self.order.items:
            body_elements.extend(self.dorst_item(item))
        return tuple(body_elements)

    def dorst_item(self, item: Item):
        amount = f'{item.amount}x'
        amount += ' '*(4-len(amount))
        product = f'{item.product_name:<37}'
        price = '{0:>7}\n'.format(f'{item.price:.2f}'.replace('.', ','))
        item_elements = [
            Text(text=amount),  # Variable
            Text(reverse=False, underline=False, bold=True),
            Text(text=product),  # Variable
            Text(reverse=False, underline=False, bold=False),
            Text(text=price),  # Variable
        ]

        if item.subitem:
            subproduct = f'    {item.subitem:<37.37}\n'
            item_elements.append(Text(text=subproduct))
            item_elements.append(Feed(unit=10))

        return tuple(item_elements)
