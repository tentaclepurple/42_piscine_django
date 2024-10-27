import sys


def get_capital_city(state):
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    if state in states:
        state_code = states[state]
        return capital_cities[state_code]
    else:
        return "Unknown state"


def main():
    if len(sys.argv) != 2:
        return 
    
    state = sys.argv[1]
    
    capital = get_capital_city(state)
    print(capital)


if __name__ == '__main__':
    main()
