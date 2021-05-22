from nltk.corpus import wordnet as wn

class similarityHousehold():


    def Remove(self, duplicate):
        final = []
        for num in duplicate:
            if num not in final:
                final.append(num)
        return final

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def __init__(self, entities, properties, perceived, weights):
        self.entities = entities
        self.properties = properties
        self.perceived = perceived
        self.weights = weights

    def cleaning_entities(self):
        property_list = self.Remove(self.properties)
        list1 = []
        entity_property = {}
        for i in range(len(self.entities)):
            first_cleaning = self.entities[i].replace('/a/[', '').replace(']', '')
            for j in range(len(self.properties)):
                if self.properties[j] + '/' in first_cleaning:
                    second_cleaning = first_cleaning.replace(self.properties[j] + '/', '').replace(',', '')
                    if entity_property.get(self.properties[j]) == None:
                        entity_property.setdefault(self.properties[j], []).append(second_cleaning)
                    else:
                        entity_property[self.properties[j]].append(second_cleaning)
                    break
            list1.append((second_cleaning, self.weights[i]))

        list_properties = ['/r/RelatedTo', '/r/AtLocation', '/r/UsedFor', '/r/IsA']
        new_hash_entity_property = {}
        for property in entity_property:
            if property in list_properties:
                new_hash_entity_property[property] = entity_property[property]
        return list1, new_hash_entity_property

    def cleaning_entities_second(self, entities_observed, perceived_weights):


        for observed in entities_observed:
            for entity in range(len(entities_observed[observed])-1, -1, -1):
                if not (entities_observed[observed][entity].count("/en/") == 2):
                    del entities_observed[observed][entity]
                else:
                    for perceived_entity in self.perceived:
                        if (('/c/en/' + perceived_entity + '/') in entities_observed[observed][entity]):
                            entities_observed[observed][entity] = entities_observed[observed][entity].replace('/c/en/' + perceived_entity + '/', '')
                        if (('/c/en' + perceived_entity + '/n/') in entities_observed[observed][entity]):
                            entities_observed[observed][entity] = entities_observed[observed][entity].replace('/c/en/' + perceived_entity + '/n/', '')


        for observed in entities_observed:
            annotator = 0
            for i in entities_observed[observed]:
                if ('wn/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('wn/', '_')
                if ('/n/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('/n/', '')
                if ('/v/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('/v/', '')
                if ('/a/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('/a/', '')
                if ('/c/en/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('/c/en/', '')
                if ('n/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('n/', '')
                if ('/' in i):
                    entities_observed[observed][annotator] = entities_observed[observed][annotator].replace('/', '')
                annotator += 1

        for observed in entities_observed:
            entities_observed[observed] = self.Remove(entities_observed[observed])
            for i in entities_observed[observed]:
                if self.hasNumbers(i) == True:
                    entities_observed[observed].remove(i)

        helper_list_weights = []
        for property in entities_observed:
            for entity in entities_observed[property]:
                helper_list_weights.append(entity)

        list_with_weights = []
        for entity in helper_list_weights:
            for weight in perceived_weights:
                if entity in weight[0]:
                    list_with_weights.append((entity, weight[1]))

        return entities_observed, list_with_weights

    def grounding(self, cleaned_entities, weigths_of_entities):

        listWordNet = ['.n.01', '.v.01', '.a.01', '.r.01']
        for observed in cleaned_entities:
            for i in range(len(cleaned_entities[observed])-1, -1, -1):
                wordNet = wn.synsets(cleaned_entities[observed][i])
                if wordNet != []:
                    wordnet_entity = wordNet[0].name()
                    for j in listWordNet:
                        if j in wordnet_entity:
                            cleaned_entities[observed][i] = wordnet_entity.replace(j, '')
                            break
                else:
                    del cleaned_entities[observed][i]

        helper_list_weight = []
        for property in cleaned_entities:
            for entity in cleaned_entities[property]:
                helper_list_weight.append(entity)

        helper_weight_final = []
        for weight in weigths_of_entities:
            for helper in helper_list_weight:
                if helper in weight[0]:
                    helper_weight_final.append((helper, weight[1]))

        visited = set()
        weight_final = []
        for entity1, emtity2 in helper_weight_final:
            if not entity1 in visited:
                visited.add(entity1)
                weight_final.append((entity1, emtity2))

        return cleaned_entities, weight_final

    def strong_related(self, cleaned_final, weight_final):
        weight_final = sorted(weight_final, key=lambda x: x[1], reverse=True)
        new_cleaned_hash = {}
        if len(weight_final) > 10:
            weight_final = set(weight_final[:10])
            for property in cleaned_final:
                cleaned_final[property] = self.Remove(cleaned_final[property])

            for property in cleaned_final:
                for entity in cleaned_final[property]:
                    for strong_entity in weight_final:
                        if strong_entity[0] == entity:
                            if new_cleaned_hash.get(property) == None:
                                new_cleaned_hash.setdefault(property, []).append(entity)
                            else:
                                new_cleaned_hash[property].append(entity)
        else:
            for property in cleaned_final:
                new_cleaned_hash[property] = self.Remove(cleaned_final[property])

        help = []
        for property in new_cleaned_hash:
            for entity in new_cleaned_hash[property]:
                help.append((entity, property))

        visited = set()
        output = []
        for a, b in help:
            if not a in visited:
                visited.add(a)
                output.append((a, b))

        new_cleaned_hash = {}
        for tup in output:
            if new_cleaned_hash.get(tup[1]) == None:
                new_cleaned_hash.setdefault(tup[1], []).append(tup[0])
            else:
                new_cleaned_hash[tup[1]].append(tup[0])

        return new_cleaned_hash, weight_final



