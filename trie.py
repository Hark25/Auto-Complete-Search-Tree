import time, math, re, string, json 

# Node class for data
class Node:
    def __init__(self):
        self.children = {}              # char → Node
        self.is_end_of_word = False     # indicates if node is end of a word
        self.count = 0                  # number of times word is used
        self.last_used = time.time()    # timestamp of last usage
        self.cache = []                 # cache for top-k words

# functions for Trie or REPL to use


#normalize input
def normalize(text: str, mode: str = "word") -> str:
   
    if not isinstance(text, str):
        return "normalize requires a string"

    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)

    if mode == "word":
        punct_without_apostrophe = string.punctuation.replace("'", "")
        pattern = "[" + re.escape(punct_without_apostrophe) + "]"
        text = re.sub(pattern, "", text)

    return text


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

    # Build list of words and score for all words in cache and new word
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


### Trie class ###
class Trie:
    ##initialize root
    def __init__(self):
        self.root = Node()
    

    ## Insert a word into the trie
    def insert(self, word):
        if not isinstance(word, str):
            raise TypeError("insert expects a string")
        
        #normalize
        word = normalize(word, mode='word')

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


    ## Bulk load function
    def Bulk_Load(self, filename):
        
        #helper to set values to node
        def _get_node(self, text, mode="word"):
            text = normalize(text, mode)
            current = self.root
            for char in text:
                if char in current.children:
                    current = current.children[char]
                else:
                    return None
            return current

        #main bulk load logic
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Bulk load expects a list")

        for entry in data:
            word = entry["word"]
            count = int(entry.get("count", 0))
            ts = float(entry.get("timestamp", time.time()))

            self.insert(word)
            
            node = _get_node(self, word, mode='word')
            if node:
                node.count = count
                node.last_used = ts
    

    #Bulk Save Function
    def Bulk_save(self, filename):

        data = []

        def dfs(node, path):
            if node.is_end_of_word:
                data.append({
                    "word": path,
                    "count": node.count,
                    "timestamp": node.last_used
                })

            for char, child_node in node.children.items():
                dfs(child_node, path + char)
        
        dfs(self.root, "")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


    ## Prefix search Function
    def prefix_search(self, prefix):
        if not isinstance(prefix, str):
            raise TypeError("prefix_search expects a string")

        #normalize
        prefix = normalize(prefix, mode='word')

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


    ## Exact Search Function, returns true if word exists, false otherwise
    def exact_search(self, word):
        if not isinstance(word, str):
            raise TypeError("exact_search expects a string")
        
        #normalize
        word = normalize(word, mode='word')

        current = self.root
        for char in word:
            if char in current.children:
                current = current.children[char]
            else:
                return False
            
        return current.is_end_of_word
    

    ## delete function (not used in REPL, but useful for testing and future features if needed)
    def delete(self, word):
        if not isinstance(word, str):
            raise TypeError("delete expects a string")
        
        #normalize
        word = normalize(word, mode='word')

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


    ## increment count functon
    def increment_count(self, word):
        if not isinstance(word, str):
            raise TypeError("increment_count expects a string")

        current = self.root

        #normalize
        word = normalize(word, mode='word')

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
    

    ## Main-Autocomplete function
    def auto_complete(self, prefix):    
        current = self.root

        #normalize
        prefix = normalize(prefix, mode='word')

        #search cache for word
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
                
        return current.cache