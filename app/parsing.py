from dataclasses import dataclass, field

from xml.etree import ElementTree
from app.config import namespaces
from epos.document import EposDocument
from epos.elements import *


@dataclass
class ParseResult:
    empty: bool = False
    parameters: dict = field(default_factory=dict)
    document: EposDocument = None


def parse_xml(data: str) -> ParseResult:
    dom = ElementTree.fromstring(data)
    res = ParseResult()

    header = dom.find('./s:Header', namespaces)
    if header:
        for element in header:
            if remove_ns(element.tag) == 'parameter':
                for parameter in element:
                    name = remove_ns(parameter.tag)
                    res.parameters[name] = parameter.text
                    print(f'"{name}" is "{parameter.text}"')
                    # todo Do something with parameters here?
            else:
                print('Unknown header element:')
                print_element_info(element)

    body = dom.find('./s:Body', namespaces)
    if body:
        for element in body:
            if element.tag == add_ns('response'):
                print('Parsing response')
            elif element.tag == add_ns('epos-print'):
                if len(element) == 0:
                    print('Empty epos-print element')
                    res.empty = True
                else:
                    print('Parsing epos-print')
                    res.document = create_epos_document(element)
            else:
                print('Unknown element! Info:')
                print_element_info(element)
                ElementTree.dump(element)

    return res


def create_epos_document(root) -> EposDocument:
    doc = EposDocument()
    for elem in root:
        match remove_ns(elem.tag):
            case 'text':
                EposElement = Text()
            case 'feed':
                EposElement = Feed()
            case 'image':
                EposElement = Image()
            case 'logo':
                EposElement = Logo()
            case 'barcode':
                EposElement = Barcode()
            case 'symbol':
                EposElement = Symbol()
            case 'page':
                EposElement = Page()
            case 'area':
                EposElement = Area()
            case 'direction':
                EposElement = Direction()
            case 'position':
                EposElement = Position()
            case 'rectangle':
                EposElement = Rectangle()
            case 'cut':
                EposElement = Cut()
            case 'pulse':
                EposElement = Pulse()
            case 'sound':
                EposElement = Sound()
            case 'command':
                EposElement = Command()
            case 'recovery':
                EposElement = Recovery()
            case 'reset':
                EposElement = Reset()
            case _:
                print(f'Element {remove_ns(elem.tag)} unknown!')
                raise ValueError('Unknown')

        for attribute, value in elem.attrib.items():
            setattr(EposElement, attribute, value)
        if elem.text:
            EposElement.text = elem.text
        doc.add_body(EposElement)

        #print_element_info(elem)

    return doc


def convert_attr(attr: str):
    pass


def add_ns(tag: str) -> str:
    return f'{{{namespaces["epos-print"]}}}{tag}'


def remove_ns(tag: str) -> str:
    return tag.replace(f'{{{namespaces["epos-print"]}}}', '')


def print_element_info(element: ElementTree.Element):
    print(f'{remove_ns(element.tag).upper()} ', end='')
    if element.attrib:
        for k,v in element.attrib.items():
            print(f'{k}={v} ', end='')
    if element.text:
        print(f'{repr(element.text)}', end='')
    print()


if __name__ == '__main__':
    pass
