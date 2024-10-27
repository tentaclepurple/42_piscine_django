import sys

def parse_file(filename):
    elements = []
    with open(filename, "r") as f:
        for line in f:
            name, properties = line.strip().split(" = ")
            properties = dict(prop.strip().split(":") for prop in properties.split(","))
            properties['name'] = name
            elements.append(properties)
    return elements


def generate_table(f, element) -> None:
    f.write('<td style="border: 1px solid black; padding:10px">\n')
    f.write(f'<h4>{element["name"]}</h4>\n')
    f.write('<ul>\n')
    f.write(f'<li>No {element["number"]}</li>\n')
    f.write(f'<li>{element["small"]}</li>\n')
    f.write(f'<li>{element["molar"]}</li>\n')
    f.write(f'<li>{element["electron"]} electron(s)</li>\n')
    f.write('</ul>\n')
    f.write('</td>\n')


def generate_html(elements, output_filename) -> None:
    with open(f"./{output_filename}", "w") as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n')
        f.write('<head>\n')
        f.write('<meta charset="UTF-8">\n')
        f.write('<title>Periodic table HTML</title></head>\n')        
        f.write('<body>\n')
        f.write('<table>\n')

        for i, element in enumerate(elements):
            position = int(element["position"])
            if position == 0:
                f.write('<tr>\n')

            generate_table(f, element)

            if i + 1 < len(elements):
                next_position = int(elements[i + 1]["position"])
                if next_position !=0 and position + 1 != next_position:
                    f.write(f'<td colspan={next_position - position - 1} style="border: 0px;"></td>\n')

            if position == 17:
                f.write('</tr>\n')

        f.write('</table>\n')
        f.write('</body>\n')
        f.write('</html>\n')


if __name__ == "__main__":
    input_filename = "periodic_table.txt"
    output_filename = "periodic_table.html"

    elements = parse_file(input_filename)

    generate_html(elements, output_filename)
