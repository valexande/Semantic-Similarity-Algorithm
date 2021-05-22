
class sortDisplay():

    def __init__(self, scores_common, scores_not_common, perceived):
        self.scores_common = scores_common
        self.scores_not_common = scores_not_common
        self.perceived = perceived

    def Remove(self, duplicate):
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
            sorted_hash_with_properties[entity] = list_sorted_entities

        print(sorted_hash_with_properties)

        return sorted_hash_with_properties




