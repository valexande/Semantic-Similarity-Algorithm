from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity

class tfidfValue():

    def __init__(self, perceived_comment_box, common_comment_box, not_common_comment_box,  weight_of_entities):
        self.peceived_comment_box = perceived_comment_box
        self.common_comment_box = common_comment_box
        self.not_common_comment_box = not_common_comment_box
        self.weight_of_entities = weight_of_entities


    def tokenize(self, text):
        tokens = word_tokenize(text)
        stems = []
        for item in tokens: stems.append(PorterStemmer().stem(item))
        return stems

    def Remove(self, duplicate):
        final = []
        for num in duplicate:
            if num not in final:
                final.append(num)
        return final
    def tf_idf_accumulator(self):


        tf_idf_score_common = {}
        for common in self.common_comment_box:
            text = self.peceived_comment_box
            result_common_tf_idf = 0
            text.append(common)
            text_helper = [" ".join(self.tokenize(txt.lower())) for txt in text]
            vectorizer_common = TfidfVectorizer()
            matrix_common = vectorizer_common.fit_transform(text_helper).todense()
            result_common_tf_idf = cosine_similarity(matrix_common[0], matrix_common[1])
            common_box = self.common_comment_box[common][0]
            common_box.append(result_common_tf_idf[0][0])
            text.pop(1)
            text_helper = []
            if tf_idf_score_common.get(self.common_comment_box[common][0][0]) == None:
                tf_idf_score_common.setdefault(self.common_comment_box[common][0][0], []).append(common_box)
            else:
                tf_idf_score_common[self.common_comment_box[common][0][0]].append(common_box)


        tf_idf_score_not_common = {}
        for not_common in self.not_common_comment_box:
            for entity in range(len(self.not_common_comment_box[not_common])):
                text = self.peceived_comment_box
                result_not_common_tf_idf = 0
                text.append(not_common)
                text_helper = [" ".join(self.tokenize(txt.lower())) for txt in text]
                vectorizer_not_common = TfidfVectorizer()
                matrix_not_common = vectorizer_not_common.fit_transform(text_helper).todense()
                result_not_common_tf_idf = cosine_similarity(matrix_not_common[0], matrix_not_common[1])
                common_not_box = self.not_common_comment_box[not_common][entity]
                common_not_box.append(result_not_common_tf_idf[0][0])
                text_helper = []
                if tf_idf_score_not_common.get(self.not_common_comment_box[not_common][entity][0]) == None:
                    tf_idf_score_not_common.setdefault(self.not_common_comment_box[not_common][entity][0], []).append(common_not_box)
                else:
                    tf_idf_score_not_common[self.not_common_comment_box[not_common][entity][0]].append(common_not_box)
                text.pop(1)



        tf_idf_common_with_weights = {}
        for entity in tf_idf_score_common:
            k = 0
            for entity1, entity2 in self.weight_of_entities:
                if entity == entity1:
                    k = entity2
            tf_idf_score_common[entity][0].append(k)
            if tf_idf_common_with_weights.get(entity) == None:
                tf_idf_common_with_weights.setdefault(entity, []).append(tf_idf_score_common[entity])
            else:
                tf_idf_common_with_weights[entity].append(tf_idf_score_common[entity])

        tf_idf_not_common_with_weights = {}
        for entity in tf_idf_score_not_common:
            k = 0
            for entity1, entity2 in self.weight_of_entities:
                if entity == entity1:
                    k = entity2
            tf_idf_score_not_common[entity][0].append(k)
            if tf_idf_not_common_with_weights.get(entity) == None:
                tf_idf_not_common_with_weights.setdefault(entity, []).append(tf_idf_score_not_common[entity])
            else:
                tf_idf_not_common_with_weights[entity].append(tf_idf_score_not_common[entity])

        final_score_common_hash = {}
        for entity in tf_idf_score_common:
            list_helper_final_common = []
            final_score_common = 1/(tf_idf_score_common[entity][0][2] + 1) + tf_idf_score_common[entity][0][3] + tf_idf_score_common[entity][0][4]
            list_helper_final_common.append(tf_idf_score_common[entity][0][1])
            list_helper_final_common.append(final_score_common)
            if final_score_common_hash.get(entity) == None:
                final_score_common_hash.setdefault(entity, []).append(list_helper_final_common)
            else:
                final_score_common_hash[entity].append(list_helper_final_common)


        final_score_not_common_hash = {}
        for entity in tf_idf_score_not_common:
            list_helper_final_not_common = []
            final_score_not_common = 1 / (tf_idf_score_not_common[entity][0][2] + 1) + tf_idf_score_not_common[entity][0][3] + tf_idf_score_not_common[entity][0][4]
            list_helper_final_not_common.append(tf_idf_score_not_common[entity][0][1])
            list_helper_final_not_common.append(final_score_not_common)
            if final_score_not_common_hash.get(entity) == None:
                final_score_not_common_hash.setdefault(entity, []).append(list_helper_final_not_common)
            else:
                final_score_not_common_hash[entity].append(list_helper_final_not_common)

        for entity in final_score_common_hash:
            if entity in final_score_not_common_hash:
                del final_score_not_common_hash[entity]

        return final_score_common_hash, final_score_not_common_hash
