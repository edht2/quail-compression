from main import QuailCompression
 

 
s = "Eggbert is lord!"
tree, bit_str = QuailCompression.encode(s)
print(tree, bit_str)
print(QuailCompression.decode(tree, bit_str))
