# Open the .dat file
# with open('C:\Users\gaurav\Desktop\Metatrader5\apis\bases\Default\symbols\leverages-1004.dat', 'r') as file:
# with open('C:\\Users\\gaurav\\Desktop\\Metatrader5\\apis\\bases\\Default\\symbols\\leverages-1004.dat', 'r') as file:
with open('C:\\Users\\JAYESH\\Desktop\\mt5_python\\bases\\Default\\subscriptions\\subscriptions-1000.dat', 'r') as file:
    # Read and print the contents line by line
    for line in file:
        print(line.strip())  # Use strip() to remove any leading/trailing whitespace

# Alternatively, if the file is small and you want to read all contents at once:
# with open('file.dat', 'r') as file:
#     contents = file.read()
#     print(contents)

# If the .dat file contains binary data, you can open it in binary mode ('rb') and read binary data using the read() method.
