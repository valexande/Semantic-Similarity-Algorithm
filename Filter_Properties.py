from nltk.corpus import wordnet as wn
class Property_Fill():

    def __init__(self, perceived):
        self.perceived = perceived

    def property_filter(self):

        word_net = wn.synsets(self.perceived)[0]
        depth = min([len(path) for path in word_net.hypernym_paths()])
        if depth > 3:
            while depth > 3:
                filter = word_net.hypernyms()
                word_net = filter[0]
                depth = depth - 1
        else:
            filter = "default"

        filter = filter[0].name()
        filter_properties = []
        if filter in ['group.n.01', 'set.n.02']:
            filter_properties = [('/r/IsA', 1), ('/r/PartOf', 2), ('/r/UsedFor', 3), ('/r/AtLocation', 4), ('/r/LocatedNear', 5),\
                                 ('/r/MadeOf', 6), ('/r/CapableOf', 7), ('/r/HasA', 8), ('/r/CreatedBy', 9), ('/r/ReceivesAction', 10),\
                                 ('/r/SimilarTo', 11), ('/r/DistinctFrom', 12), ('/r/CausesDesire', 13), ('/r/Desires', 14), ('/r/RelatedTo', 15)]
        elif filter in ['attribute.n.02', 'psychological_feature.n.01']:
            filter_properties = [('/r/UsedFor', 1), ('/r/AtLocation', 2), ('/r/LocatedNear', 3), ('/r/CapableOf', 4), ('/r/ReceivesAction', 5),\
                                 ('/r/MadeOf', 6), ('/r/SimilarTo', 7), ('/r/CreatedBy', 8), ('/r/IsA', 9), ('/r/PartOf', 10),\
                                 ('/r/HasA', 11), ('/r/CausesDesire', 12), ('/r/DistinctFrom', 13), ('/r/Desires', 14), ('/r/RelatedTo', 15)]
        elif filter in ['relation.n.01']:
            filter_properties = [('/r/SimilarTo', 1), ('/r/DistinctFrom', 2), ('/r/IsA', 3), ('/r/PartOf', 4), ('/r/HasA', 5),\
                                 ('/r/ReceivesAction', 6), ('/r/CapableOf', 7), ('/r/CreatedBy', 8), ('/r/UsedFor', 9), ('/r/MadeOf', 10),\
                                 ('/r/LocatedNear', 11), ('/r/AtLocation', 12), ('/r/CausesDesire', 13), ('/r/Desires', 14), ('/r/RelatedTo', 15)]
        elif filter in ['measure.n.02']:
            filter_properties = [('/r/UsedFor', 1), ('/r/MadeOf', 2), ('/r/IsA', 3), ('/r/PartOf', 4), ('/r/CapableOf', 5),\
                                 ('/r/ReceivesAction', 6), ('/r/HasA', 7), ('/r/AtLocation', 8), ('/r/LocatedNear', 9), ('/r/SimilarTo', 10),\
                                 ('/r/DistinctFrom', 11), ('/r/CreatedBy', 12), ('/r/CausesDesire', 13), ('/r/Desires', 14), ('/r/RelatedTo', 15)]
        elif filter in ['communication.n.02']:
            filter_properties = [('/r/Desires', 1), ('/r/CausesDesire', 2), ('/r/CreatedBy', 3), ('/r/CapableOf', 4), ('/r/HasA', 5),\
                                 ('/r/IsA', 6), ('/r/PartOf', 7), ('/r/ReceivesAction', 8), ('/r/UsedFor', 9), ('/r/MadeOf', 10),\
                                 ('/r/SimilarTo', 11), ('/r/DistinctFrom', 12), ('/r/AtLocation', 13), ('/r/NearLocation', 14), ('/r/RelatedTo', 15)]
        elif filter in ['thing.n.12', 'object.n.01']:
            filter_properties = [('/r/UsedFor', 1), ('/r/AtLocation', 2), ('/r/NearLocation', 3), ('/r/MadeOf', 4), ('/r/CreatedBy', 5),\
                                 ('/r/CapableOf', 6), ('/r/CauseDesire', 7), ('/r/PartOf', 8), ('/r/HasA', 9), ('/r/IsA', 10),\
                                 ('/r/Desires', 11), ('/r/SimilarTo', 12), ('/r/DistinctFrom', 13), ('/r/ReceivesAction', 14), ('/r/RelatedTo', 15)]
        elif filter in ['causal_agent.n.01', 'process.n.06']:
            filter_properties = [('/r/CapableOf', 1), ('/r/UsedFor', 2), ('/r/HasA', 3), ('/r/Desires', 4), ('/r/CausesDesire', 5),\
                                 ('/r/CreatedBy', 6), ('/r/MadeOf', 7), ('/r/PartOf', 8), ('/r/IsA', 9), ('/r/ReceivesAction', 10),\
                                 ('/r/AtLocation', 11), ('/r/LocatedNear', 12), ('/r/SimilarTo', 13), ('/r/DistinctFrom', 14), ('/r/RelatedTo', 15)]
        elif filter in ['matter.n.03']:
            filter_properties = [('/r/MadeOf', 1), ('/r/CreatedBy', 2), ('/r/PartOf', 3), ('/r/ReceivesAction', 4), ('/r/UsedFor', 5),\
                                 ('/r/CapableOf', 6), ('/r/AtLocation', 7), ('/r/LocationNear', 8), ('/r/HasA', 9), ('/r/IsA', 10),\
                                 ('/r/Desires', 11), ('/r/CausesDesire', 12), ('/r/SimilarTo', 13), ('/r/DistinctFrom', 14), ('/r/RelatedTo', 15)]
        if filter_properties == []:
            filter_properties = ["default"]
        return filter_properties
