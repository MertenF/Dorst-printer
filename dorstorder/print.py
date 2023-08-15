from abc import ABC
from typing import Type
from decimal import Decimal
from datetime import datetime

from escpos.printer import Network

from dorstorder.order import Order, Item

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
        name = f'{self.order.customer:.{max_len}}'
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
        total_price = f'{self.order.total_price_cents:>7}\n'.replace('.', ',')
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
        item_price = item.price_cents/100
        price = '{0:>7}\n'.format(f'{item_price:.2f}'.replace('.', ','))
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
        'koude': 500,
        'kleine': 600,

        'ham': 50,

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
        total_price = f'{self.order.total_price_cents:>7}\n'.replace('.', ',')
        total_amount = f'Totaal aantal stuks:{len(self.order.items)}\n'
        order_time = f'Besteld op {self.order.order_datetime:%d/%m/%Y om %H:%M}\n'

        payment_status = f'{self.order.payment_status:.{self.max_len2}}'

        order_number = f'Order #{self.order.order_num}\n'

        if self.order.payment_method == 'Betalen bij ober':
            pay_meth = 'Betaald aan de kassa'
        else:
            pay_meth = self.order.payment_method
        payment_method = f'{pay_meth:.{self.max_len}}\n'

        name = f'{self.order.customer:.{self.max_len}}\n'
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
        item_price = item.price_cents/100
        price = '{0:>7}\n'.format(f'{item_price:.2f}'.replace('.', ','))

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


def print_snackkot(printer: Network, order: Order):

    printer.set(bold=False, custom_size=True, height=4, width=4, smooth=True, font='a')
    printer.text(f'Order {order.order_num}\n')
    printer.set(bold=True, custom_size=True, height=2, width=2)
    printer.text('Orderbewijs - Klant\n')
    printer.set(bold=False, height=1, width=1)
    printer.text('Bij te houden tot je bestelling gemaakt is\n')
    printer.cut()

    printer.set(bold=False, custom_size=True, height=4, width=4, smooth=True, font='a')
    printer.text(f'Order {order.order_num}\n')

    printer.set(custom_size=True, height=3, width=3, smooth=True)
    printer.text('Snackbon\n')

    printer.set(height=1, width=1, smooth=True)
    printer.text('-'*42)
    printer.text('\n')

    printer.set(bold=True)
    for item in order.items:
        printer.text(f'{item.amount}x')
        printer.text(' '*(3-len(str(item.amount))))

        printer.text(f'{item.product_name: <31}')

        price = '{0:>7}\n'.format(f'{item.price_cents/100:.2f}'.replace('.', ','))
        printer.text(price)
    printer.set(height=1, width=1)
    printer.text('-'*42)
    printer.text('\n')


    printer.set(bold=True, height=1, width=1)
    printer.text('1) Geef deze bon af aan het snackkot\n')
    printer.text('2) Wacht tot je bestelling gereed is\n')

    printer.text('-' * 42)
    printer.text('\n')

    printer.set(height=1, width=1)
    order_time = f'Besteld op {order.order_datetime:%d/%m/%Y om %H:%M}\n'
    printer.text(order_time)
    printer.text(f'Aantal stuks: {len(order.items)}\n')
    printer.cut()


def print_snackkot_hoera(printer: Network):
    printer.set(bold=False, custom_size=True, height=2, width=2, smooth=True, font='a')
    printer.text('Hoera het werkt!\n')
    printer.set(bold=False, custom_size=True, height=1, width=1, smooth=True, font='a')
    printer.text("""
    Lorem Ipsum is slechts een proeftekst uit het drukkerij- en zetterijwezen. Lorem Ipsum is de standaard proeftekst in deze bedrijfstak sinds de 16e eeuw, toen een onbekende drukker een zethaak met letters nam en ze door elkaar husselde om een font-catalogus te maken. Het heeft niet alleen vijf eeuwen overleefd maar is ook, vrijwel onveranderd, overgenomen in elektronische letterzetting. Het is in de jaren '60 populair geworden met de introductie van Letraset vellen met Lorem Ipsum passages en meer recentelijk door desktop publishing software zoals Aldus PageMaker die versies van Lorem Ipsum bevatten.
    """)



if __name__ == '__main__':
    ip = '10.0.0.14'
    printer = Network(ip, timeout=6)
    print(printer.is_online())
    order = Order(
        table_name='T15',
        order_num=2000,
        order_datetime=datetime.now(),
        total_items_amount=5,
        items=[
            Item(
                amount=1,
                product_name='Frietjes',
                price_cents=400,
            ),
            Item(
                amount=3,
                product_name='Curryworst',
                price_cents=450,
            ),
            Item(
                amount=1,
                product_name='Hamburger',
                price_cents=400,
            ),
        ],
    )

    print_snackkot(printer, order)