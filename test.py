import unittest
from trie import Trie

class TestTrie(unittest.TestCase):

    def setUp(self):
        # create a new Trie before each test
        self.trie = Trie()
        self.trie.insert("cat")
        self.trie.insert("car")
        self.trie.insert("cart")
        self.trie.insert("dog")

    def test_insert_and_search(self):
        # Test that inserted words are found with prefix search
        self.assertIn("cat", self.trie.prefix_search("ca"))
        self.assertIn("car", self.trie.prefix_search("ca"))
        self.assertIn("cart", self.trie.prefix_search("ca"))
        self.assertIn("dog", self.trie.prefix_search("do"))

    def test_prefix_search_empty(self):
        # Prefix not in trie should return empty list
        self.assertEqual(self.trie.prefix_search("z"), [])

    def test_prefix_search_partial(self):
        # Partial prefix returns correct words
        results = self.trie.prefix_search("c")
        self.assertCountEqual(results, ["cat", "car", "cart"])

    def test_type_error_insert(self):
        # Insert non-string should raise TypeError
        with self.assertRaises(TypeError):
            self.trie.insert(123)

    def test_type_error_prefix_search(self):
        # Prefix search non-string should raise TypeError
        with self.assertRaises(TypeError):
            self.trie.prefix_search(456)

if __name__ == "__main__":
    unittest.main()
