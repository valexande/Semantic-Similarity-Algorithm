from nltk.corpus import wordnet as wn

class Find_Similarity():


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

        entity_property.pop('/r/Synonym', None)
        entity_property.pop('/r/Antonym', None)
        entity_property.pop('/r/NotHasProperty', None)
        entity_property.pop('/r/ExternalURL', None)
        entity_property.pop('/r/EtymologicallyDerivedFrom', None)
        entity_property.pop('/r/FormOf', None)
        entity_property.pop('/r/HasSubevent', None)
        entity_property.pop('/r/HasFirstSubevent', None)
        entity_property.pop('/r/HasLastSubevent', None)
        entity_property.pop('/r/DistinctFrom', None)
        entity_property.pop('/r/SymbolOf', None)
        entity_property.pop('/r/DefinedAs', None)
        entity_property.pop('/r/Causes', None)
        entity_property.pop('/r/HasPrerequisite', None)
        entity_property.pop('/r/HasProperty', None)
        entity_property.pop('/r/MotivatedByGoal', None)
        entity_property.pop('/r/ObstructedBy', None)
        entity_property.pop('/r/DerivedFrom', None)
        entity_property.pop('/r/MannerOf', None)
        entity_property.pop('/r/HasContext', None)
        entity_property.pop('/r/EtymologicallyRelatedTo', None)

        return list1, entity_property

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



