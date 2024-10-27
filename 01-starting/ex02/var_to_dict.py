def convert_list_to_dict(pairs):
    musician_dict = {}
    for name, year in pairs:
        if year in musician_dict:
            musician_dict[year] += " " + name
        else:
            musician_dict[year] = name
    return musician_dict


def display_dict(dictionary):
    for year, names in dictionary.items():
        print(f"{year} : {names}")


def main():
    d = [
        ('Hendrix', '1942'),
        ('Allman', '1946'),
        ('King', '1925'),
        ('Clapton', '1945'),
        ('Johnson', '1911'),
        ('Berry', '1926'),
        ('Vaughan', '1954'),
        ('Cooder', '1947'),
        ('Page', '1944'),
        ('Richards', '1943'),
        ('Hammett', '1962'),
        ('Cobain', '1967'),
        ('Garcia', '1942'),
        ('Beck', '1944'),
        ('Santana', '1947'),
        ('Ramone', '1948'),
        ('White', '1975'),
        ('Frusciante', '1970'),
        ('Thompson', '1949'),
        ('Burton', '1939')
    ]

    musician_dict = convert_list_to_dict(d)
    display_dict(musician_dict)


if __name__ == '__main__':
    main()
