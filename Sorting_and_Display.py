from Filter_Properties import *


class final_sorting_display():

    def __init__(self, scores_common, scores_not_common, perceived):
        self.scores_common = scores_common
        self.scores_not_common = scores_not_common
        self.perceived = perceived

    def Remove(self,duplicate):
        final = []
        for num in duplicate:
            if num not in final:
                final.append(num)
        return final

    def display(self):
        self.scores_common.update(self.scores_not_common)

        score_property_oriented_hash = {}
        for entity in self.scores_common:
            list_entity = []
            list_entity = [entity]
            list_entity.append(self.scores_common[entity][0][1])
            list_entity = tuple(list_entity)
            if score_property_oriented_hash.get(self.scores_common[entity][0][0]) == None:
                score_property_oriented_hash.setdefault(self.scores_common[entity][0][0], []).append(list_entity)
            else:
                score_property_oriented_hash[self.scores_common[entity][0][0]].append(list_entity)

        sorted_hash_with_properties = {}
        for entity in score_property_oriented_hash:
            list_sorted_entities = []
            score_property_oriented_hash[entity] = self.Remove(score_property_oriented_hash[entity])
            list_sorted_entities = sorted(score_property_oriented_hash[entity], key=lambda x: x[1], reverse=True)
            if sorted_hash_with_properties.get(entity) == None:
                sorted_hash_with_properties.setdefault(entity, []).append(list_sorted_entities)
            else:
                sorted_hash_with_properties[entity].append(list_sorted_entities)


        filter_propertiee = Property_Fill(self.perceived)
        filter = filter_propertiee.property_filter()


        new_hash = {}
        for property in sorted_hash_with_properties:
            for entity in filter:
                if str(property) == str(entity[0]):
                    new_hash[entity] = sorted_hash_with_properties[property][0]
                    break
        list_filter = []
        for property in new_hash:
            list_filter.append(property)
        list_filter = sorted(list_filter, key=lambda x: x[1], reverse=False)
        for property in list_filter:
            print(str(property[0].replace('/r/', '')) + " " + str(new_hash[property]))

        """
        results = open('Results_Semantic_Similarity5.txt', 'a+')
        for property in sorted_hash_with_properties:
            property_clean = property.replace('/r/', '')
            if (property_clean.lower() == 'IsA'.lower()) or (property_clean.lower() == 'HasContext'.lower()) or (property_clean.lower() == 'HasA'.lower()) or \
                (property_clean.lower() == 'HasPrerequisite'.lower()) or (property_clean.lower() == 'ReceivesAction'.lower()) or\
                (property_clean.lower() == 'Causes'.lower()) or (property_clean.lower() == 'Desires'.lower()) or (property_clean.lower() == 'CausesDesire'.lower()):
                print(self.perceived + ' ' + property_clean)
                results.write(self.perceived + ' ' + property_clean + ': ')

            elif property_clean.lower() == 'HasContext'.lower():
                print(self.perceived + ' ' + property_clean)
                results.write(self.perceived + ' ' + property_clean + ': ')

            else:
                print(self.perceived + ' is ' + property_clean)
                results.write(self.perceived + ' is ' + property_clean + ': ')
            if len(sorted_hash_with_properties[property][0]) > 0:
                length = len(sorted_hash_with_properties[property][0]) - 1
                for entity in range(len(sorted_hash_with_properties[property][0])):
                    print(sorted_hash_with_properties[property][0][entity][0])
                    results.write(sorted_hash_with_properties[property][0][entity][0])
                    if entity == length:
                        results.write('.')
                    else:
                        results.write(', ')
            else:
                print('Nothing')
                results.write('Nothing')
            results.write("\n")
        results.write("\n")
        results.write("\n")
        results.write("\n")
        results.close()
        """



