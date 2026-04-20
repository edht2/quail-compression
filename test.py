from main import QuailCompression
from analyse import analyse

s = "Eggbert grew a berry"
bit_str = QuailCompression.encode(s)

print(bit_str)
analyse(bit_str, hint=True)

print(QuailCompression.decode(bit_str))
