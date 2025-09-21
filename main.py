from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from trie import Trie, normalize

trie = Trie()
trie.Bulk_Load("data.json")

class TrieCompleter(Completer):
    def get_completions(self, document, complete_event):
        #get wor before cursor
        text = document.get_word_before_cursor()
        for w in trie.auto_complete(text):
            yield Completion(w, start_position=-len(text))

session = PromptSession(completer=TrieCompleter())

print("Start typing. Autocomplete appears automatically. Ctrl+C to exit.")

while True:
    try:
        line = session.prompt("> ")  # user types a full line
        print(f"You typed: {line}")

        phrase = line.strip()
        if trie.exact_search(phrase):
            trie.increment_count(phrase)
        else:
            trie.insert(phrase)
            trie.increment_count(phrase)

        # split the line into words and add/increment in trie
        for word in phrase.split():
            if trie.exact_search(word):
                trie.increment_count(word)
            else:
                trie.insert(word)
                trie.increment_count(word)  # first usage

    except KeyboardInterrupt:
        trie.Bulk_save("data.json")
        print("\nBye!")
        break


