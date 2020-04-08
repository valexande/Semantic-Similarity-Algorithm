from Similarity_Pre_Process import *
from Property_Distance_CommentBox import *
from TFIDF_Compiler import *
from Sorting_and_Display import *
import requests

f = open("MiniTest.txt", "r")
f1 = f.readlines()
startinglist = []
for x in f1:
    x = x.rstrip('\n')
    startinglist.append(x)

f.close()

def Remove(duplicate):
    final = []
    for num in duplicate:
        if num not in final:
            final.append(num)
    return final


class ConceptNet:

    def __init__(self, term, uri):
        self.term = term
        self.uri = uri

    def myfunc(self):
        return 'http://api.conceptnet.io/c/en/' + self.term + '?offset=0&limit=1000'

    def myfunc1(self):
        return 'http://conceptnet.io/c/en/' + self.term + '?rel=' + self.uri + '&limit=10'

for i in startinglist:
    list1 = [i]
    print(list1)

    for i in range(len(list1)):
        list1[i] = list1[i].lower()
    lst = []
    lst2 = []
    for i in range(len(list1)):
        object = ConceptNet(list1[i], [])
        property_values = object.myfunc()
        respone = requests.get(property_values)
        obj = respone.json()
        lst0 = []
        for relation in obj['edges']:
            if ('wordnet' in relation['sources'][0]['@id']) or ('verbosity' in relation['sources'][0]['@id']):
                lst0.append(1)
            else:
                lst0.append(0)

        lst = [relation['rel']['@id'] for relation in obj['edges']]
        lst2 = [relation['@id'] for relation in obj['edges']]
        lst3 = [relation['weight'] for relation in obj['edges']]


    list_with_properties = []
    similarity = Find_Similarity(lst2, lst, list1, lst3)
    cleaned_entities_first = similarity.cleaning_entities()
    cleaned_entities_second, weights_of_entities = similarity.cleaning_entities_second(cleaned_entities_first[1], cleaned_entities_first[0])
    cleaned_final, weight_final = similarity.grounding(cleaned_entities_second, weights_of_entities)

    property_distance_comment = prop_dist_comm(cleaned_final, list1, weight_final)
    comment_boxes_perceived, comment_boxes_common, comment_boxes_not_common = property_distance_comment.relations()

    score_sender = tf_idf(comment_boxes_perceived, comment_boxes_common, comment_boxes_not_common, weight_final)
    final_score_common, final_score_not_common = score_sender.tf_idf_accumulator()

    sorted_final = final_sorting_display(final_score_common, final_score_not_common, list1[0])
    sorted_final.display()