import time, math

# Node class for data
class Node:
    def __init__(self):
        self.children = {}              # char → Node
        self.is_end_of_word = False     # indicates if node is end of a word
        self.count = 0                  # number of times word is used
        self.last_used = time.time()    # timestamp of last usage
        self.cache = []                 # cache for top-k words

# functions for Trie to use

# Compute score
def score(node, alpha=0.3, beta=0.5):
    freq = math.log(node.count + 1)             # log frequency to lower impact of high counts
    age = time.time() - node.last_used          # time since last used
    recency_score = 1 / ( 1 + age )             # recency score, more recent = higher score
    return alpha * freq + beta * recency_score  # return weighted score.

# update cache
def update_cache(node, word, k=5, trie_root=None):
    # Helper to get node for a word
    def get_node_for_word(root, word):
        current = root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        return current if current.is_end_of_word else None

    # Build list of (word, score) for all words in cache + new word
    words = set(node.cache)
    words.add(word)
    scored = []
    for w in words:
        n = get_node_for_word(trie_root if trie_root else node, w)
        if n:
            scored.append((w, score(n)))
    # Sort and keep top k
    scored.sort(key=lambda x: x[1], reverse=True)
    node.cache = [w for w, s in scored[:k]]

# Trie class 
class Trie:
    #initialize root
    def __init__(self):
        self.root = Node()
    
    # Insert a word into the trie
    def insert(self, word):
        if not isinstance(word, str):
            raise TypeError("insert expects a string")

        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = Node()
            current = current.children[char]

        #update node properties
        current.is_end_of_word = True
        current.count += 1
        current.last_used = time.time()

        # update cache for each node along the path
        node = self.root
        for c in word:
            update_cache(node, word, trie_root=self.root)
            node = node.children[c]

    #Prefix search Function
    def prefix_search(self, prefix):
        if not isinstance(prefix, str):
            raise TypeError("prefix_search expects a string")

        # traverse the prefix
        current = self.root
        for char in prefix:
            if char in current.children:
                current = current.children[char]
            else:
                return []  # prefix not found

        # collect all words under this node
        results = []

        def dfs(node, path):
            if node.is_end_of_word:
                results.append(prefix + path)
            for char, child_node in node.children.items():
                dfs(child_node, path + char)

        dfs(current, "")
        return results

        #Exact Search Function, returns true if word exists, false otherwise
    def exact_search(self, word):
        current = self.root
        if not isinstance(word, str):
            raise TypeError("exact_search expects a string")
            
        for char in word:
            if char in current.children:
                current = current.children[char]
            else:
                return False
            
        return current.is_end_of_word
    
    #delete function
    def delete(self, word):
        if not isinstance(word, str):
            raise TypeError("delete expects a string")
        
        # Helper functio for recursion
        def _delete(node, word, depth):
            if node is None:
                return False
            
            if depth == len(word):
                if node.is_end_of_word == False:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete_child = _delete(node.children[char], word, depth + 1)

            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0
            
            return False
        
        _delete(self.root, word, 0)

    #increment count functon
    def increment_count(self, word):
        current = self.root

        if not isinstance(word, str):
            raise TypeError("increment_count expects a string")

        for char in word:
            if char not in current.children:
                return False   # word not found
            current = current.children[char]
    
        if current.is_end_of_word:
            current.count += 1
            current.last_used = time.time()

            # Update cache along the path
            node = self.root
            for c in word:
                update_cache(node, word, trie_root=self.root)
                node = node.children[c]

            return True
        return False
    
    def auto_complete(self, prefix):
        current = self.root
        word = prefix

        # Helper function inside auto_complete
        def count(prefix):
            if not isinstance(prefix, str):
                raise TypeError("prefix_search expects a string")

            current = self.root
            for char in prefix:
                if char in current.children:
                    current = current.children[char]
                else:
                    return []  # prefix not found

            results = []
            def dfs(node, path):
                if node.is_end_of_word:
                    results.append((prefix + path, score(node)))
                for char, child_node in node.children.items():
                    dfs(child_node, path + char)

            dfs(current, "")
            
            return results
        
        # main autocomplete logic
        if(current.cache == []):
            
            if not isinstance(prefix, str):
                raise TypeError("auto_complete expects a string")
    
            words = count(word)  
            words.sort(key=lambda x: x[1], reverse=True)
            update_cache(current, word)
            return [w for w, c in words][:1]
        else:
            current = self.root
            for char in prefix:
                if char not in current.children:
                    return []
                current = current.children[char]
                
            return current.cache