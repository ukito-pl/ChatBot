# -*- coding: utf-8 -*-
from annoy import AnnoyIndex
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_vectors_web_lg')

f = 300
t = AnnoyIndex(f)  # Length of item vector that will be indexed

#Building tree (it takes couple of minutes), comment this part if tree is already built
source_file = open("dane/movie_lines.txt", "r")
for line in source_file:
    fields = line.split(" +++$+++ ")
    id = fields[0]
    text = fields[4]
    id = id.replace("L","")
    #print id, text
    text = text.decode('ISO-8859-15')
    sentence = nlp(text)
    t.add_item(int(id), sentence.vector)
source_file.close()

t.build(10) # 10 trees
t.save('nns_tree.ann')
print "build succesfull"


#save IDs of movie lines which have response
has_response = []
conv_file = open("dane/movie_conversations.txt", "r")
for line in conv_file:
    fields = line.split(" +++$+++ ")
    conv = fields[3]
    conv = conv.replace("'", "")
    conv = conv.replace("L", "")
    conv = conv.replace("\n", "")
    conv = conv.replace("[", "")
    conv = conv.replace("]", "")
    conv = conv.replace("]", "")
    conv = conv.split(", ")
    i = 0
    while (i + 1 < len(conv)):
        has_response.append(int(conv[i]))
        i = i+1



#main program, load user query, represent it as a vector, find nearest neighbor,
#find resposne to that nearest neighbor (if such response exist) and print it as an answer to user query
u = AnnoyIndex(f)
u.load('nns_tree.ann')
print "tree loaded"
print "Start a conversation!"
while True:
    query = raw_input('You:')
    query = query.decode('ISO-8859-15')
    query = nlp(query)
    n = 3
    nns = u.get_nns_by_vector(query.vector, n)
    #print(nns)
    responded = False
    i = 0
    while not responded and (i < n):
        best_neighbor = nns[i]
        if best_neighbor in has_response:
            response_id = best_neighbor + 1
            #print response_id
            source_file = open("dane/movie_lines.txt", "r")
            for line in source_file:
                fields = line.split(" +++$+++ ")
                id = fields[0]
                text = fields[4]
                id = int(id.replace("L",""))
                text = text.decode('ISO-8859-15')
                if (response_id == id):
                    print "Bulabot:",text.replace("\n","")
                    responded = True

        else:
            i = i + 1
