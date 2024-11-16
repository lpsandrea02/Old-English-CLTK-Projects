"""
Old English Alliteration finder based on Old Norse cltk.prosody.non by Clément Besnier
AlliterateLine(str) analyses line of Old English poetry and returns the alliterating words + alliteration count
AlliterateText(filename) analyses file and returns alliterating words + count with line numbers

-Andrea Lo
"""

from cltk import NLP 
pipeline = NLP(language='ang', suppress_banner=True)
from cltk.stops.ang import STOPS
from cltk.tag.pos import POSTag
ang_tagger=POSTag('ang')

#Phonology lists: Need to change this into access of CLTK phonology data
consonants= ["b", "c", "ċ", "ç", "d", "ð", "f", "g", "ġ", "ɣ", "h", "j", "k", "l", "l̥", "m", "n", "n̥", "ŋ", "p", "r", "r̥", "s", "t", "t͡ʃ", "d͡ʒ", "θ", "ʃ", "w", "ʍ", "x", "þ", "ƿ"]
vowels = ['i', 'ī', 'y', 'ȳ', 'u', 'ū', 'e', 'ē', 'o', 'ō', 'æ', 'ǣ', 'a', 'ā', "ø"]
diphthongs = ["ea", "ēa", "ie", "īe", "eo", "ēo", "io", "īo"]
digraphs = ["cg", "sc","st","sp"]
#verb prefix list based on Minkova (2008) Prefixation and Stress
verb_prefixes= ('a', 'æt', 'geond', 'ful', 'in', 'mis', 'of', 'ofer', 'on', 'or', 'oþ', 'þurh', 'tō', 'under', 'wiþ')

#FUNCTION FOR TEXT NORMALISATION
import string
def normalizer(text): 
    """
    >>> normalizer("‘Hwæt sceal ic winnan?’ cwæð he, ‘nis me wihtæ þearf")
    'hwæt sceal ic winnan cwæð he nis me wihtæ þearf'
    """
    #strip numbers & punctuation
    text=text.translate(text.maketrans("","",string.punctuation))
    text=text.translate(text.maketrans("","",string.digits))
    text=text.lower()
    return text

#ADJUST STOPWORD values
STOPS=STOPS[:179] #first 179 stopwords excluding number words e.g. twegen…
# extension of stop words for poetry - including interchangeable þ/ð
stops_for_poetry = ['þa',  'þy',  'þonne',  'þas',  'þis',  'þin',  'þū',  'þīn',  'þē',  'þec',  'þæt',  'þæs',  'þǣre',  'þǣm',  'þām',  'þone',  'þā',  'þȳ',  'þē',  'þon',  'þāra',  'þǣra',  'þes',  'þēos',  'þisse',  'þeosse',  'þises',  'þisses',  'þisum',  'þissum',  'þisne',  'þās',  'þīs',  'þȳs',  'þissa',  'þeossa',  'þeosum',  'þeossum', 'ymb', 'hæfde', 'hie', 'him', 'his']  # to be completed
STOPS.extend(stops_for_poetry)

#Takes 1 line to analyse for alliteration
class Line:
    def __init__(self, text):
        self.text = text
        self.syllabified = [] 
        self.alliterations = []
        self.n_alliterations = 0
        self.first_sounds = [] #[(first sound, word), (f,w), ..] 
        self.postagged = {} #{word:pos, word:pos}
    
    def tokenize(self):
        processed=pipeline.analyze(self.text)
        self.tokenized_text = processed.tokens
        return self.tokenized_text

    def find_pos(self):
        for word in self.tokenized_text:
            #find POS tag of the word
            #issue: POS tag does not detect many words
            postagged=ang_tagger.tag_ngram_123_backoff(word) #pos tagger generates result [('word', 'POS')]
            self.postagged[word]=postagged[0][1]

    #find first stressed sound of each word, attached with word info
    def find_first_sounds(self):
        #first_sounds = [(first sound, word), (f,w), ..] 
        
        for word in self.tokenized_text:
            postag=str(self.postagged[word])
            
            #Establish baseword for alliteration
            #all words beginning with prefixed ge-, be-, for- are stressed on 2nd syllable
            #non-exhaustive rudimentary filtering of compounds e.g. 'gear', 'geomor' - but also incorrectly filters out 'geascian' etc. 
            if word.startswith(('ge', 'ġe', 'be','for')) and len(word)>2 and word[2] not in ('a', 'o'): 
                baseword=word[2:]
            #verbs & adverbs are usually not stressed on selected prefixes
            elif word.startswith(verb_prefixes) and postag.startswith(('V','D')):
                baseword=word[2:] 
            elif word.startswith('ymb') and postag.startswith(('V','D')):
                baseword=word[3:]
            else:
                baseword=word

            #Extract first stressed sound of each word to create dict entry {first_sound:original_word}
            if baseword.startswith(tuple(digraphs)): 
                self.first_sounds.append((baseword[0:1], word))
            #all old english vowels alliterate 
            elif baseword.startswith(tuple(diphthongs)) or baseword.startswith(tuple(vowels)): 
                self.first_sounds.append(('vowel', word))
            elif baseword.startswith(tuple(consonants)):
                self.first_sounds.append((baseword[0:1], word))

        return self.first_sounds

    def find_alliterations(self):
        """
        Alliterations is the repetition of a same sound pattern (usually the first sound) of important words.
        Excludes: most stopwords & prefixes
        Vowels alliterate with each other, consonant g can alliterate with ġ, ċ with c, 
        """
        self.n_alliterations = 0 #count - number of alliterations
        self.alliterations = [] #list of alliteration

        #dictionary with key:values - (first_sound: words that alliterate)
        alliterator={}

        for sound in self.first_sounds:
                first_sound=sound[0]
                word=sound[1]

                #if the sound is a vowel / diphthong
                if first_sound== 'vowel': 
                    alliterator.setdefault('vowel', []).append(word)
                
                #consonant g can alliterate with ġ, ċ with c, þ with ð (used interchangeably in OE)
                elif first_sound in ('g','ġ'):
                    alliterator.setdefault('gsounds', []).append(word)
                elif first_sound in ('ċ','c'):
                    alliterator.setdefault('csounds', []).append(word)
                elif first_sound in ('þ','ð'):
                    alliterator.setdefault('thsounds', []).append(word)

                elif first_sound in digraphs:
                    alliterator.setdefault(first_sound, []).append(word)
                elif first_sound in consonants:
                    alliterator.setdefault(first_sound, []).append(word)

        #list of ALL alliteration clusters [(first_sound, [word1, word2...]), ()]
        a_clusters= alliterator.items()
        
        #filter rarely stressed: stopwords, pos tagged conjunction/preposition/pronoun/relatives - unless they are the only alliteration in the line
        #used to remove alliteration clusters based on unstressed words e.g. "miltse 'þon' māran 'þearfe' ġewrec nū mihtiġ dryhten"
        #errors: filter removes some actual alliterations 
        if len(a_clusters)>1:
            for cluster in a_clusters: #(first_sound, [words,])
                for word in cluster[1]: 
                    #find POS of the word
                    postag=str(self.postagged[word])
                    if word in STOPS or postag.startswith(('C','R','P')):
                        cluster[1].remove(word) 

        #alliteration is when the cluster count >1
        for cluster in a_clusters:
            if len(cluster[1])>1:
                self.alliterations.append(cluster[1])
        
        for lists in self.alliterations:
            self.n_alliterations+=len(lists)

        #reinforced alliteration has priority over accidental groups
        return self.alliterations.sort(reverse=True, key=len), self.n_alliterations
    

#reads a line for alliteration
def AlliterateLine(line):
    line=normalizer(line) 
    e=Line(line)
    e.tokenize()
    e.find_pos()
    e.find_first_sounds()
    e.find_alliterations()
    print(e.text)
    print(e.alliterations)
    print('Alliteration count:', e.n_alliterations)

#reads a file for alliteration
def AlliterateText():
    text=[]
    inp=str(input('Enter filename:'))
    with open(inp) as fhand:
        for line in fhand:
            text.append(line.strip().rstrip())
    
    print('no.  line')
    for i,line in enumerate(text):
        line=normalizer(line) 
        e=Line(line)
        e.tokenize()
        e.find_pos()
        e.find_first_sounds()
        e.find_alliterations()
        print(i, '  ', e.text)
        print('    ', e.alliterations, e.n_alliterations)        

#example sentence
sent1="sigor ond sōðne ġelēafan  þæt iċ mid þȳs sweorde mōte"
sent2="swa wynlic wæs his wæstm on heofonum þæt him com from weroda drihtne"

AlliterateLine(sent1)
AlliterateText() #e.g. text_samples/Genesis_B.txt
