
filename = input("Enter the filename: ")

filename += ".txt"

try:
    with open(filename,'r') as f:
        print("Successfully opened " + filename)
    f.close()
except:
    print("File cannot be found.")