import sys

sys.path.insert(0, "./local_lib")

print("sys.path:", sys.path)


from path import Path


def main():
	output_path = 'exercise_folder/exercise_file.txt'
	try:
		Path.makedirs('exercise_folder')
	except FileExistsError as e:
		print(e)
	Path.touch(output_path)
	file = Path(output_path)
	file.write_lines(['https://en.wikipedia.org/wiki/Monkey_Island', 'https://en.wikipedia.org/wiki/Maniac_Mansion'])
	print("Script executed")


if __name__ == '__main__':
	main()
