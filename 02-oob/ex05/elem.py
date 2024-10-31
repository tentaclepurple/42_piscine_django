#!/usr/bin/python3


class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.
    
    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        This method returns a string where certain HTML characters are escaped.
        """
        # Escape special HTML characters
        text = super().__str__()
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')

        return text.replace('\n', '\n<br />\n')


class Elem:
    '''
        Use example:

        docum = Elem('html', content=[
            Elem('body', content=[
                Elem('div', content=Text('Hola'))
            ])
        ])
        print(docum)

        # Flujo de llamadas recursivas (simplificado):
        1. docum.__str__() 
        → "<html>"
        2. body.__str__()
            → "<body>"
            3. div.__str__()
                → "<div>"
                4. Text('Hello').__str__()
                    → "Hello"
                ← "<div>Hello</div>"
            ← "<body><div>Hello</div></body>"
        ← "<html><body><div>Hello</div></body></html>"
    '''
    class ValidationError(Exception):
        def __init__(self) -> None:
            super().__init__("Error")

    def __init__(self, tag: str = 'div', attr: dict = {}, content=None, tag_type: str = 'double'):
        self.tag = tag
        self.attr = attr
        self.content = []
        if not (self.check_type(content) or content is None):
            raise self.ValidationError
        if type(content) == list:
            self.content = content
        elif content is not None:
            self.content.append(content)
        if (tag_type != 'double' and tag_type != 'simple'):
            raise self.ValidationError
        self.tag_type = tag_type

    def __str__(self):
        attr = self.__make_attr()
        result = "<{tag}{attr}".format(tag=self.tag, attr=attr)
        if self.tag_type == 'double':
            result += ">{content}</{tag}>".format(
                content=self.__make_content(), tag=self.tag)
        elif self.tag_type == 'simple':
            result += " />"
        return result

    def __make_attr(self):
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        if len(self.content) == 0:
            return ""
        result = "\n"
        for elem in self.content:
            if (len(str(elem)) != 0):
                result += "{elem}\n".format(elem=elem)
        result = "  ".join(line for line in result.splitlines(True))
        if len(result.strip()) == 0:
            return ''
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))


def my_test():
    elem = Elem(tag='html', content=[
                Elem(tag='head', content=Elem(tag='title', content=Text('"Hello ground!"'))), 
                Elem(tag='body', content=[
                    Elem(tag='h1', content=Text('"Oh no, not again!"')), 
                    Elem(tag='img', tag_type='simple', attr={'src':'http://i.imgur.com/pfp3T.jpg'})
                ])
            ])
    print(elem)


if __name__ == '__main__':
    my_test()
