from elements import Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Elem, Text


class Page:
    def __init__(self, elem: Elem()) -> None:
        if not isinstance(elem, Elem):
            raise Elem.ValidationError()
        self.elem = elem

    def __str__(self) -> str:
        result = ""
        if isinstance(self.elem, Html):
            result += "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result

    def write_to_file(self, path: str) -> None:
        f = open(path, "w")
        f.write(self.__str__())

    def is_valid(self) -> bool:
        return self.__recursive_check(self.elem)

    def __recursive_check(self, elem: Elem) -> bool:
        
        if not isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li,
                                H1, H2, P, Div, Span, Hr, Br, Text)):
            return False

        if isinstance(elem, Text) or isinstance(elem, Meta):
            return True

        if isinstance(elem, Html):
            if len(elem.content) == 2 and isinstance(elem.content[0], Head) and isinstance(elem.content[1], Body):
                if all(self.__recursive_check(el) for el in elem.content):
                    return True
            
        elif isinstance(elem, Head):
            title_count = [isinstance(el, Title) for el in elem.content].count(True)
            if title_count == 1 and all(self.__recursive_check(el) for el in elem.content):
                return True

        elif isinstance(elem, (Body, Div)):
            valid_content = all(isinstance(el, (H1, H2, Div, Table, Ul, Ol, Span, Text)) for el in elem.content)
            if valid_content and all(self.__recursive_check(el) for el in elem.content):
                return True

        elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
            if len(elem.content) == 1 and isinstance(elem.content[0], Text):
                return True

        elif isinstance(elem, P):
            if all(isinstance(el, Text) for el in elem.content):
                return True

        elif isinstance(elem, Span):
            valid_content = all(isinstance(el, (Text, P)) for el in elem.content)
            if valid_content and all(self.__recursive_check(el) for el in elem.content):
                return True

        elif isinstance(elem, (Ul, Ol)):
            if len(elem.content) > 0 and all(isinstance(el, Li) for el in elem.content):
                return True

        elif isinstance(elem, Tr) and len(elem.content) > 0:
            has_th = any(isinstance(el, Th) for el in elem.content)
            has_td = any(isinstance(el, Td) for el in elem.content)

            if has_th and has_td:
                return False

            if all(isinstance(el, (Th, Td)) for el in elem.content):
                return True

        elif isinstance(elem, Table):
            if all(isinstance(el, Tr) for el in elem.content):
                if all(self.__recursive_check(el) for el in elem.content):
                    return True

        return False


def run_tests():

    print("\n=== Starting HTML validation tests ===\n")
    tests_passed = 0
    total_tests = 0


    def run_test(name, test_func):
        nonlocal tests_passed, total_tests
        total_tests += 1
        try:
            result = test_func()
            if result:
                print(f"✓ {name}")
                tests_passed += 1
            else:
                print(f"✗ {name}")
        except Exception as e:
            print(f"✗ {name} - Error: {str(e)}")


    # 1. Test valid basic HTML structure
    def test_valid_html():
        html = Html([
            Head([Title([Text("Test Title")])]),
            Body([H1([Text("Main Title")])])
        ])
        page = Page(html)
        return page.is_valid()
    run_test("Valid basic HTML structure", test_valid_html)


    # 2. Test Head with multiple Titles (should fail)
    def test_multiple_titles():
        html = Html([
            Head([
                Title([Text("Title 1")]),
                Title([Text("Title 2")])
            ]),
            Body([H1([Text("Content")])])
        ])
        page = Page(html)
        return not page.is_valid()
    run_test("Head with multiple Titles (should fail)", test_multiple_titles)


    # 3. Test Body with valid content
    def test_valid_body_content():
        html = Html([
            Head([Title([Text("Test")])]),
            Body([
                H1([Text("Title")]),
                Div([Text("Content")]),
                Table([Tr([Td([Text("Cell")])])]),
                Ul([Li([Text("Item")])])
            ])
        ])
        page = Page(html)
        return page.is_valid()
    run_test("Body with valid content", test_valid_body_content)


    # 4. Test Tr with mixed Th and Td (should fail)
    def test_mixed_tr_content():
        html = Html([
            Head([Title([Text("Test")])]),
            Body([
                Table([
                    Tr([
                        Th([Text("Header")]),
                        Td([Text("Data")])
                    ])
                ])
            ])
        ])
        page = Page(html)
        return not page.is_valid()
    run_test("Tr with mixed Th and Td (should fail)", test_mixed_tr_content)


    # 5. Test empty list (should fail)
    def test_empty_list():
        html = Html([
            Head([Title([Text("Test")])]),
            Body([Ul([])])
        ])
        page = Page(html)
        return not page.is_valid()
    run_test("Empty Ul list (should fail)", test_empty_list)


    # 6. Test Span with valid content
    def test_valid_span():
        html = Html([
            Head([Title([Text("Test")])]),
            Body([
                Span([
                    Text("Text"),
                    P([Text("Paragraph")])
                ])
            ])
        ])
        page = Page(html)
        return page.is_valid()
    run_test("Span with valid content", test_valid_span)


    # 7. Test file writing
    def test_file_writing():
        html = Html([
            Head([Title([Text("Test")])]),
            Body([H1([Text("Title")])])
        ])
        page = Page(html)
        try:
            page.write_to_file("test.html")
            return True
        except:
            return False
    run_test("File writing functionality", test_file_writing)


    # 8. Test invalid element
    def test_invalid_element():
        class InvalidElem(Elem):
            def __init__(self):
                super().__init__(tag='invalid', attr={}, content=None, tag_type='double')
        
        try:
            page = Page(InvalidElem())
            return not page.is_valid()
        except:
            return True
    run_test("Invalid element handling", test_invalid_element)

    # Results summary
    print(f"\n=== Test Summary ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Success rate: {(tests_passed/total_tests)*100:.2f}%")


if __name__ == "__main__":
    run_tests()
