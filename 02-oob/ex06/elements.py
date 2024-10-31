from elem import Elem, Text


class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='html', content=content, attr=attr)


class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='head', content=content, attr=attr)


class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='body', content=content, attr=attr)


class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='title', content=content, attr=attr)


class Meta(Elem):
    def __init__(self, attr={}):
        super().__init__(tag='meta', attr=attr, tag_type='simple')


class Img(Elem):
    def __init__(self, attr={}):
        super().__init__(tag='img', attr=attr, tag_type='simple')


class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='table', content=content, attr=attr)


class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='th', content=content, attr=attr)


class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='tr', content=content, attr=attr)


class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='td', content=content, attr=attr)


class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='ul', content=content, attr=attr)


class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='ol', content=content, attr=attr)


class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='li', content=content, attr=attr)


class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='h1', content=content, attr=attr)


class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='h2', content=content, attr=attr)


class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='p', content=content, attr=attr)


class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='div', content=content, attr=attr)


class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag='span', content=content, attr=attr)


class Hr(Elem):
    def __init__(self, attr={}):
        super().__init__(tag='hr', attr=attr, tag_type='simple')


class Br(Elem):
    def __init__(self, attr={}):
        super().__init__(tag='br', attr=attr, tag_type='simple')


def test1():
    return Html([Head(), Body()])


def test2():
    return P(Text("Paragraph text"))


def test3():
    return H1(Text("Header"))


def test4():
    return Img(attr={'src': 'image.png'})


def test5():
    html = Html([
    Head(Title(Text("Hello ground!"))),
    Body([
        H1(Text("Oh no, not again!")),
        Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    return html


def test_elements():
    tests = [test1, test2, test3, test4, test5]
    for test in tests:
        print('\n---------\n')
        print(test())
    print('\n---------\n')

if __name__ == '__main__':
    
    test_elements()