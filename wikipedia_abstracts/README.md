wikipedia_abstracts
===================

Fetches, parses, and does awesome things with Wikipedia abstracts

wiki_abstract.py contains a bunch of functions for fetching pages from Wikipedia and formating them into readable plaintext

keyterms.py takes a list of words as input and returns a list of the words and their Wikipedia definitions. This is great for defining long lists of keyterms for class.

what.py is an extention that prints out the Wikipedia definition of a given word.
To setup, place a copy of this in your /usr/local/bin folder, and rename it 'what'. Make it executable by running 'sudo chmod +x what'. Now, you can simply type 'what is [whatever]' into bash to instantly research topics!

keyterms.txt is an example input file for keyterms.py

extended_keyterms.txt is an example output for keyterms.py
