# Old English CLTK projects

**1. Old English Alliteration finder**

*AlliterateLine(str)* analyses line of Old English poetry and returns the alliterating words + alliteration count
*AlliterateText(filename)* analyses file and returns alliterating words + count with line numbers
<ins>Key issues:</ins> \n
- Stopwords is not an exhaustive list for unstressed Old English words (usually prepositions etc.)\n
   ✏️Extended list of stopwords for þ/ð variations \n
   ✏️Implemented POS tagger to exclude conjunctions/prepositions/pronouns unless the only alliteration in the line \n
- Prefixes are stressed variably depending on word class \n
   ✏️Implemented POS tagger to differentiate verb/adverb prefixes (always unstressed) \n
    - Not efficient at distinguishing between prefixes and bound morphemes (e.g. geascian vs gear) \n
- POS tagger is not always accurate - errors in filtering 
