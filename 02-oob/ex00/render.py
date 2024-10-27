import os
import sys
import re
import settings


def main():
    
    if (len(sys.argv) != 2):
        return print("Argument number error")
    
    path = sys.argv[1]
    regex = re.compile(".*\.template")
    

    if not regex.match(path):
        return print("Extension error. '.template'")
    if not os.path.isfile(path):
        return print(f"File error")
    
    with open(path, "r") as f:
        template = "".join(f.readlines())

    file = template.format(
        name=settings.name, surname=settings.surname, title=settings.title,
        age=settings.age, profession=settings.profession)
    
    regex = re.compile("(\.template)")
    path = "".join([path[0:regex.search(path).start()], ".html"])
    
    with open(path, "w") as f:
        f.write(file)


if __name__ == '__main__':
    main()
