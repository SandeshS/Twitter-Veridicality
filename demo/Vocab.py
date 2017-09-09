# Author: Alan Ritter

class Vocab:
    def __init__(self, vocabFile=None):
        self.locked = False
        self.nextId = 0
        self.word2id = {} #TODO - change this to feature2id
        self.id2word = {}
        if vocabFile:
            for line in open(vocabFile):
                line  = line.strip('\n')
                (word, wid) = line.split('\t')
                self.word2id[word] = int(wid)
                self.id2word[wid] = word
                self.nextId = max(self.nextId, int(wid) + 1)
    
    def GetID(self, word):
        if not self.word2id.has_key(word):
            if self.locked:
                return -1
            else:
                self.word2id[word] = self.nextId
                self.id2word[self.word2id[word]] = word
                self.nextId += 1
        return self.word2id[word]

    def HasWord(self, word):
        return self.word2id.has_key(word)
    
    def HasId(self, wid):
        return self.id2word.has_key(wid)
    
    def GetWord(self, wid):
        return self.id2word[wid]

    def SaveVocab(self, vocabFile):
        fOut = open(vocabFile, 'w')
        for word in self.word2id.keys():
            fOut.write("%s\t%s\n" % (word, self.word2id[word]))
    
    def GetVocabSize(self):
        return self.nextId
    
    def GetWords(self):
        return self.word2id.keys()

    def Lock(self):
        self.locked = True
