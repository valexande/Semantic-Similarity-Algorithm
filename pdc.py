from ontologyFile.webHelp.dbpWiki import get_comment_boxes
from nltk.corpus import wordnet as wn


class distComm():

    def Remove(self, duplicate):
        final = []
        for num in duplicate:
            if num not in final:
                final.append(num)
        return final

    def __init__(self, list_with_property_entities, perceived, weights_entities):
        self.list_with_property_entities = list_with_property_entities
        self.perceived = perceived
        self.weights_entities = weights_entities

    def relations(self):

        hypernym_of_perceived = {}
        word_net = wn.synsets(self.perceived[0])
        word_net_entity = word_net[0]
        word_net_hypernym = word_net_entity.hypernyms()
        if word_net_hypernym != []:
            if hypernym_of_perceived.get(word_net_hypernym[0].name()) == None:
                hypernym_of_perceived.setdefault(word_net_hypernym[0].name(), []).append(self.perceived[0])
            else:
                hypernym_of_perceived[word_net_hypernym[0].name()].append(self.perceived[0])
        else:
            if hypernym_of_perceived.get('No Hypernym Returned') == None:
                hypernym_of_perceived.setdefault('No Hypernym Returned', []).append(self.perceived[0])
            else:
                hypernym_of_perceived['No Hypernym Returned'].append(self.perceived[0])
            word_net_hypernym = wn.synsets('entity')

        for property in self.list_with_property_entities:
                self.list_with_property_entities[property] = self.Remove(self.list_with_property_entities[property])

        ## The case where a common hypernym for the perceived entity and the returned entities exist
        common_hypernym = {}
        for property in self.list_with_property_entities:
            if self.list_with_property_entities[property] != []:
                for entity in self.list_with_property_entities[property]:
                    word_net_common = wn.synsets(entity)
                    if len(word_net_common) > 0:
                        word_net_entity_common = word_net_common[0]
                        word_net_hypernym_common = word_net_entity_common.hypernyms()
                        if word_net_hypernym_common != [] and word_net_hypernym_common[0].name() == word_net_hypernym[0].name():
                            if common_hypernym.get(word_net_hypernym_common[0].name()) == None:
                                common_hypernym.setdefault(word_net_hypernym_common[0].name(), []).append([entity, property, 2])
                            else:
                                common_hypernym[word_net_hypernym_common[0].name()].append([entity, property, 2])


        ##Get the not common hypernyms or even the case where no hypernym is returned
        depth1 = 0
        helper_perceived_hypernym = ""
        for hypernym in hypernym_of_perceived:
            for entity in hypernym_of_perceived[hypernym]:
                depth1 = wn.synsets(entity)[0].max_depth()
                helper_perceived_hypernym = wn.synsets(entity)[0]

        not_common_hypernym = {}
        for property in self.list_with_property_entities:
            if self.list_with_property_entities[property] != []:
                for entity in self.list_with_property_entities[property]:
                    distance = 0
                    word_net_not_common = wn.synsets(entity)
                    depth2 = 0
                    if len(word_net_not_common) > 0:
                        word_net_entity_not_common = word_net_not_common[0]
                        word_net_hypernym_not_common = word_net_entity_not_common.hypernyms()
                        depth2 = word_net_entity_not_common.max_depth()
                        lowest_common_word_net = word_net_entity_not_common.lowest_common_hypernyms(helper_perceived_hypernym)
                                                                                                                                ## The ones that have distance 1 have hypernymthe perceived entity
                        if len(lowest_common_word_net) == 1:                                                                    ## The one that have distance 2 in this case
                            depth3 = lowest_common_word_net[0].max_depth()
                            helper_distance_1 = depth2 - depth3
                            helper_distance_2 = depth1 - depth3
                            distance = helper_distance_1 + helper_distance_2
                        else:
                            distance = 30
                        if word_net_hypernym_not_common != [] and word_net_hypernym_not_common[0].name() == word_net_hypernym_not_common[0].name():
                            if not_common_hypernym.get(word_net_hypernym_not_common[0].name()) == None:
                                not_common_hypernym.setdefault(word_net_hypernym_not_common[0].name(), []).append([entity, property, distance])
                            else:
                                not_common_hypernym[word_net_hypernym_not_common[0].name()].append([entity, property, distance])
                        if word_net_hypernym_not_common == []:
                            if not_common_hypernym.get('No Hypernym Returned') == None:
                                not_common_hypernym.setdefault('No Hypernym Returned', []).append([entity, property, 30])
                            else:
                                not_common_hypernym['No Hypernym Returned'].append([entity, property, 30])

        ## Give the distance between the perceived and the entities that have common superclass
        for hypernym in common_hypernym:
            if hypernym in not_common_hypernym:
                del not_common_hypernym[hypernym]

        ## Remove the overlapping enities from both hashmaps
        for hypernym in common_hypernym:
            length_common_hypernym = range(len(common_hypernym[hypernym]))
            for entity in length_common_hypernym:
                if self.perceived[0] == common_hypernym[hypernym][entity][0]:
                    common_hypernym[hypernym][entity] = []

        for hypernym in not_common_hypernym:
            length_common_not_hypernym = range(len(not_common_hypernym[hypernym]))
            for entity in length_common_not_hypernym:
                if not_common_hypernym[hypernym][entity][2] == 0:
                    not_common_hypernym[hypernym][entity] = []

        ## DBpedia and Wikipedia knowledge extraction
        perceived = self.perceived[0]

        comment_boxes_sender = get_comment_boxes(not_common_hypernym, common_hypernym, perceived)
        comment_box_preceived, comment_box_common, comment_box_not_common = comment_boxes_sender.dbpedia_wikipedia_comment_boxes()
        return comment_box_preceived, comment_box_common, comment_box_not_common
