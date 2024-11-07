import sys


def search_location(query):
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

    state_to_capital = {state: capital_cities[code] for state, code in states.items()}
    capital_to_state = {capital: state for state, capital in state_to_capital.items()}

    query = query.strip().lower()

    if query in (state.lower() for state in states):
        state_name = next(state for state in states if state.lower() == query)
        return f"{state_to_capital[state_name]} is the capital of {state_name}"
    elif query in (capital.lower() for capital in capital_to_state):
        capital_name = next(capital for capital in capital_to_state if capital.lower() == query)
        return f"{capital_name} is the capital of {capital_to_state[capital_name]}"
    else:
        return f"{query} is neither a capital city nor a state"


def main():
    if len(sys.argv) != 2:
        return 

    args = sys.argv[1]
    /
        
    queries = args.split(',')
    
    for query in queries:
        if query: 
            result = search_location(query)
            print(result)


if __name__ == '__main__':
    main()
