class Intern:

    def __init__(self, name="My name? I’m nobody, an intern, I have no name."):
        self.name = name

    def __str__(self):
        return self.name

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")

	#returns an instance of the inner class Coffee
    def make_coffee(self):
        return self.Coffee()


if __name__ == "__main__":

	intern1 = Intern()
	print(intern1)
	intern2 = Intern("Mark")
	print(intern2)

	coffee = intern2.make_coffee()
	print(coffee)

	try:
		intern1.work()
	except Exception as e:
		print(e)  # Muestra el mensaje de excepción
