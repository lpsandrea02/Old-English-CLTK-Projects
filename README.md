# Old English CLTK projects

**1. Old English Alliteration finder** <br/>
*AlliterateLine(str)* analyses line of Old English poetry and returns the alliterating words + alliteration count <br/>
*AlliterateText(filename)* analyses file and returns alliterating words + count with line numbers 

<ins>Key issues:</ins> 
- Stopwords is not an exhaustive list for unstressed Old English words (usually prepositions etc.) <br/>
   ✏️Extended list of stopwords for þ/ð variations <br/>
   ✏️Implemented POS tagger to exclude conjunctions/prepositions/pronouns unless the only alliteration in the line <br/>
- Prefixes are stressed variably depending on word class <br/>
   ✏️Implemented POS tagger to differentiate verb/adverb prefixes (always unstressed) <br/>
    - Not efficient at distinguishing between prefixes and bound morphemes (e.g. geascian vs gear) <br/>
- POS tagger is not always accurate - errors in filtering 
