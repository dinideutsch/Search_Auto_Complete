import pickle
import sys
from auto_complete.auto_complete import AutoComplete


class Main:
    """This is the main class, which run the project and manages the user interface"""

    def __init__(self, mode):
        self.mode = mode
        self.auto_complete = AutoComplete("")

    def run(self, path_data, resources):
        try:
            if self.mode == "ingestion":
                self.auto_complete.ingestion(resources, path_data)
            elif self.mode == "query":
                with open(path_data, "rb") as f:
                    trie = pickle.load(f)
                seq = ""
                current_input = ""
                print("The system is ready")
                while True:
                    print("Enter your text: ", end="")
                    while current_input != "#":
                        current_input = input(f"{seq} ")
                        seq += " " + current_input
                        lst = self.auto_complete.get_best_k_completions(trie, seq, path_data)
                        print_k_args(lst, len(lst))

                    seq = " "
            else:
                raise Exception("illegal mode. please choose ingestion/query")
        except Exception as e:
            print(e)


def print_k_args(lst, k):
    for i in range(min(k, 5)):
        print(f"{i + 1}. {lst[i]}")


if __name__ == '__main__':
    main = Main(sys.argv[1])
    main.run("trie.txt", "resource")