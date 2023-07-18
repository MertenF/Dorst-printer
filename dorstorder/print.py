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

    def generate(self) -> EposDocument:
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

class ScoutsFormat(BaseFormat):
    img_line = Image(
        width=576,
        height=34,
        text='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8B//8A//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+B//+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    )
    max_len = 41 # max char width
    max_len2 = 20 # max char with double size

    sort_weight = {
        'mosselen': 100,
        'scoutsbootje': 200,
        'balletjes': 300,
        'goulash': 400,

        'friet': 10,
        'brood': 20,
        'kind': 15,

        'mosselsaus': 1010,
        'mayonaise': 1020,
        'ketchup': 1030,
    }

    def __init__(self, *args, **kwargs):
        self.saus_ordered = False
        self.items_printed = ['Mosselsaus', 'Mayonaise', 'Ketchup']
        super().__init__(*args, **kwargs)

    def header(self) -> tuple:

        table = f'{self.order.table_name:.{self.max_len2}}'

        header_elements = (
            Text(smooth=True),
            Text(width=1, height=1),
            Text('Vlaamse Kermis 2023 - Scouts WVB\n'),
            Feed(unit=10),
            Text(width=4, height=4),
            Text(text=table),  # Variable
            Feed(unit=20),
            #self.img_line,
            #Feed(unit=20),
            Text(width=1, height=1),
            Text(align=Align.LEFT),
            Text('\n'),
        )
        return header_elements

    def footer(self) -> tuple:
        total_price = f'{self.order.total_price:>7}\n'.replace('.', ',')
        total_amount = f'Totaal aantal stuks:{self.order.total_items_amount}\n'
        order_time = f'Besteld op {self.order.order_datetime:%d/%m/%Y om %H:%M}\n'

        payment_status = f'{self.order.payment_status:.{self.max_len2}}'

        order_number = f'Order #{self.order.order_num}\n'

        if self.order.payment_method == 'Betalen bij ober':
            pay_meth = 'Betaald aan de kassa'
        else:
            pay_meth = self.order.payment_method
        payment_method = f'{pay_meth:.{self.max_len}}\n'

        name = f'{self.order.customer_name:.{self.max_len}}\n'
        printer_location = f'{self.order.prepare_location:<{self.max_len2}.{self.max_len2}}\n'

        footer_elements = (
            # Totaal kader
            Feed(unit=20),
            self.img_line,
            Feed(unit=20),
            Text(reverse=False, underline=False, bold=False),
            Text(' ' * 4 + 'TOTAAL' + ' ' * 31),
            Text(text=total_price),  # Variable
            Feed(unit=20),
            self.img_line,
            Feed(unit=20),

            # Real footer
            Text(width=1, height=1),
            Text(text=order_number),  # Variable
            Text(text=payment_method),  # Variable
            Text(text=name),  # Variable
            Text(text=printer_location),  # Variable
            Text(text=total_amount),  # Variable
            Text(text=order_time),  # Variable
            Feed(unit=40),
            Cut(),
        )
        return footer_elements

    def body(self) -> tuple:
        body_elements = []

        def item_weight(item):
            weight = 0
            for w in item.product_name.split(' '):
                weight += self.sort_weight.get(w.lower(), 0)
            return weight

        items = sorted(self.order.items, key=item_weight)
        for item in items:
            body_elements.extend(self.dorst_item(item))
        return tuple(body_elements)

    def dorst_item(self, item: Item):
        amount = f'{item.amount}x'
        amount += ' '*(4-len(amount))
        product = f'{item.product_name}'
        product_space = ' ' * (37-len(product))
        print(repr(product), repr(product_space))
        product_key = item.product_name.split(' ')[0]
        price = '{0:>7}\n'.format(f'{item.price:.2f}'.replace('.', ','))

        el = []
        # line prefix
        is_saus = any(s for s in ('Mosselsaus', 'Mayonaise', 'Ketchup') if s in product)
        if not self.saus_ordered and is_saus:
            el.append(self.img_line)
            el.append(Feed(unit=20))
            self.saus_ordered = True

        if product_key not in self.items_printed:
            el.append(Text(f'{product_key:-^48}\n')) # center with '-'
            self.items_printed.append(product_key)

        # start of line
        el.append(Text(reverse=False, underline=False, bold=True))
        el.append(Text(text=amount))
        # product name prefix
        if 'brood' in product or 'kind' in product:
            el.append(Text(reverse=True))

        # product name
        el.append(Text(text=product))

        # product name suffix
        if 'brood' in product or 'kind' in product:
            el.append(Text(reverse=False))

        # product space
        el.append(Text(text=product_space))

        # end of line
        el.append(Text(reverse=False, underline=False, bold=False))
        el.append(Text(text=price))

        if item.subitem:
            subproduct = f'    {item.subitem:<37.37}\n'
            el.append(Text(text=subproduct))
            el.append(Feed(unit=10))

        return tuple(el)
