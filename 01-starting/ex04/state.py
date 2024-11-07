import sys


def get_state_by_capital(capital):
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

    # Reverse the capital_cities dictionary to search by capital
    reversed_capitals = {v: k for k, v in capital_cities.items()}
    
    #print(reversed_capitals)

    if capital in reversed_capitals:
        state_code = reversed_capitals[capital]
        for state, code in states.items():
            if code == state_code:
                return state
    else:
        return "Unknown capital city"


def main():
    if len(sys.argv) != 2:
        return
    
    capital = sys.argv[1]
    
    state = get_state_by_capital(capital)
    print(state)


if __name__ == '__main__':
    main()
