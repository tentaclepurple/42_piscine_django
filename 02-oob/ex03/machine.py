import random
from beverages import *


class CoffeeMachine:

    def __init__(self):
        self.served_drinks = 0

    class EmptyCup(HotBeverage):
        name = "empty cup"
        price = 0.90
        
        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def repair(self):
        self.served_drinks = 0

    def serve(self, beverage_class: HotBeverage) -> HotBeverage:
        if self.served_drinks >= 10:
            raise CoffeeMachine.BrokenMachineException()
        
        self.served_drinks += 1

        return (
            beverage_class()
            if random.choice([True, True, False])
            else CoffeeMachine.EmptyCup()
        )


def tests():
    machine = CoffeeMachine()
    beverages = [Coffee, Tea, Chocolate, Cappuccino]

    i = 0
    user_input = ''
    while user_input.lower() != 'q':
        user_input = input("Press enter to continue... or 'q' to quit\n")
        i += 1
        
        print(f"Epoch {i}")
        try:
            drink = machine.serve(random.choice(beverages))
            print(drink)
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            machine.repair()
            print("Machine repaired!")
        print()


if __name__ == '__main__':
    try:
        tests()
    except Exception as e:
        print(e)
        print("Exiting...")
        exit(1)
