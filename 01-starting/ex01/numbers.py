def display_numbers(filename):
    with open(filename, 'r') as file:
        content = file.read()
        
        numbers = content.split(',')
        
        for number in numbers:
            print(number.strip())


if __name__ == '__main__':
    try:
        display_numbers('numbers.txt')
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {e}")
