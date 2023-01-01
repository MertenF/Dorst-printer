from .order import Order

from epos.document import EposDocument
from epos.elements import *


def epos_to_order(doc: EposDocument) -> Order:
    order = Order()




    for element in doc.body:
        if element.tag == 'text':
            if not element.text:
                continue








    return order



