from main import QuailCompression
from analyse import analyse

s = "Eggbert grew a berry"
bit_str = QuailCompression.encode(s)
QuailCompression.write("qc.txt", bit_str)

read_bit_str = QuailCompression.read("qc.txt")
print(QuailCompression.decode(read_bit_str))