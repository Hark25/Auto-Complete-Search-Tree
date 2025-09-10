from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from trie import Trie

trie = Trie()

# preload some words
for w in ["i", "love", "cats", "dogs", "icecream"]:
    trie.insert(w)

class TrieCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.get_word_before_cursor()
        # auto_complete returns list of words
        for w in trie.auto_complete(text):
            yield Completion(w, start_position=-len(text))

session = PromptSession(completer=TrieCompleter())

print("Start typing. Autocomplete appears automatically. Ctrl+C to exit.")

while True:
    try:
        line = session.prompt("> ")  # user types a full line
        print(f"You typed: {line}")

        # split the line into words and add/increment in trie
        for word in line.split():
            if trie.exact_search(word):
                trie.increment_count(word)
            else:
                trie.insert(word)
                trie.increment_count(word)  # first usage

    except KeyboardInterrupt:
        print("\nBye!")
        break


