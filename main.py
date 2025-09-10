from trie import Trie

def main():
    trie = Trie()
    print("Simple Trie REPL. Type 'help' for commands, 'exit' to quit.")

    while True:
        command = input("> ").strip().split(" ", 1)  # split into [cmd, arg]
        cmd = command[0].lower()

        if cmd == "exit":
            print("Goodbye!")
            break

        elif cmd == "help":
            print("Commands:")
            print("  insert <word>         - Insert a word into the trie")
            print("  search <word>         - Check if a word exists (exact search)")
            print("  autocomplete <prefix> - Get top 3 completions for a prefix")
            print("  use <word>            - Increment usage count for a word")
            print("  exit                  - Quit the program")

        elif cmd == "insert" and len(command) > 1:
            word = command[1]
            trie.insert(word)
            print(f'Inserted "{word}".')

        elif cmd == "search" and len(command) > 1:
            word = command[1]
            found = trie.exact_search(word)
            print(f'"{word}" found? {found}')

        elif cmd == "autocomplete" and len(command) > 1:
            prefix = command[1]
            results = trie.auto_complete(prefix)
            print("Completions:", results)

        elif cmd == "use" and len(command) > 1:
            word = command[1]
            if trie.increment_count(word):
                print(f'Incremented usage for "{word}".')
            else:
                print(f'"{word}" not found in trie.')

        else:
            print("Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    main()


