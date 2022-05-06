# Versuch 1.2 - Aufgabe 6

def main():
	pipe = open("/dev/servoblaster", "a")
	while 1:
		servo_num = input("Enter servo number (0 or 1): ")
		pw_percentage = input("Enter pulse width (in %): ")
		pipe.write(str(servo_num) + "=" + str(pw_percentage) + "%\n")
		pipe.flush()
		print("\nAdjusted pulse width of servo " + str(servo_num) + " to " + str(pw_percentage) + "%.\n\n")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pipe.close()
		print("\nProgram closed!")
