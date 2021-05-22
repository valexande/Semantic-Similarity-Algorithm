import textdistance
import requests
from similarity import similarityHousehold
from pdc import distComm
from tfidf import tfidfValue
from sort import sortDisplay

class Web():

    def __init__(self, entity, list_objects):
        self.entity = entity
        self.list_objects = list_objects


    def Remove(self,duplicate):
        final = []
        for num in duplicate:
            if num not in final:
                final.append(num)
        return final

    def myfunc(self, term):
        return 'http://api.conceptnet.io/c/en/' + term + '?offset=0&limit=1000'

    def main_web(self):
        print("\nWait a second please, I am searching on the web....\n")
        lst = []
        lst2 = []
        property_values = self.myfunc(self.entity)
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
        similarity = similarityHousehold(lst2, lst, [self.entity], lst3)
        cleaned_entities_first = similarity.cleaning_entities()
        cleaned_entities_second, weights_of_entities = similarity.cleaning_entities_second(cleaned_entities_first[1], cleaned_entities_first[0])
        cleaned_final, weight_final = similarity.grounding(cleaned_entities_second, weights_of_entities)
        new_cleaned_final, new_weight_final = similarity.strong_related(cleaned_final, weight_final)

        property_distance_comment = distComm(new_cleaned_final, [self.entity], new_weight_final)
        comment_boxes_perceived, comment_boxes_common, comment_boxes_not_common = property_distance_comment.relations()


        score_sender = tfidfValue(comment_boxes_perceived, comment_boxes_common, comment_boxes_not_common, weight_final)
        final_score_common, final_score_not_common = score_sender.tf_idf_accumulator()


        sorted_final = sortDisplay(final_score_common, final_score_not_common, self.entity)
        hash_final_sorted = sorted_final.display()