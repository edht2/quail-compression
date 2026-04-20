from main import QuailCompression
from colorama import Back

s = "Eggbert grew a berry in 35 days"
bit_str = QuailCompression.encode(s)

print(bit_str)



print(QuailCompression.decode(bit_str))
