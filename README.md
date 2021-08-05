# Google Autocomplete Project
##### Dini Deutsch & Rivki Levy
## Description
The goal of the project was to provide 
an autocomplete service for a huge data 
source.
This is done by a system that can run win two different modes:
* ingestion mode - the program will read the data and store it in a file, formed as a trie of the words in the resource
with their filepath and some more relevant information so runtime will be short and retrieving the data will be efficient.
* query mode - the program will read the trie file into an actual trie and then waits for user input. When it
gets an input it search until it gets five matches. if less then five returned it will try to search for
completions with one letter missed\replaced\added.
 

## Usage
###### within a project
first edit the mode to ingestion/query by sending it through the argv.

then use a code like this:
```python
import Main
import sys
main = Main(sys.argv[1])
main.run("some_file.txt", "some_resource.txt")
```
###### by cmd
```
python project_path (mode = query/ingestion)
```
