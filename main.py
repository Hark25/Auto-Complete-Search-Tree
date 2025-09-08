from trie import Trie

trie = Trie()
trie.insert("cat")
trie.insert("car")
trie.insert("cart")
trie.insert("dog")

print(trie.prefix_search("ca"))  # ['cat', 'car', 'cart']
print(trie.prefix_search("do"))  # ['dog']
print(trie.prefix_search("z"))   # []

print(trie.exact_search("cat"))   # True
print(trie.exact_search("ca"))    # False 
print(trie.exact_search("car"))   # True
print(trie.exact_search("cart"))  # True
print(trie.exact_search("fish"))   # False

print(trie.exact_search("dog"))  # True
trie.delete("dog")
print(trie.exact_search("dog")) # False
