from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia
import urllib


class get_comment_boxes():

    def __init__(self, common_hypernym, not_common_hypernym, perceived):
        self.common_hypernym = common_hypernym
        self.not_common_hypernym = not_common_hypernym
        self.perceived = perceived

    def dbpedia_wikipedia_comment_boxes(self):
        list_comment_perceived = []
        self.perceived = self.perceived.capitalize()
        sparql_perceived = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql_perceived.setQuery(""" PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
                            SELECT DISTINCT ?comment WHERE{
                            ?entry rdfs:label \"""" + self.perceived + """\"@en. 
                            ?entry dbpedia-owl:abstract ?comment
                            FILTER(lang (?comment) = 'en')}
                        """)
        sparql_perceived.setReturnFormat(JSON)
        results_perceived = sparql_perceived.query().convert()
        comment_perceived = results_perceived['results']['bindings']
        if results_perceived['results']['bindings'] != []:
            list_comment_perceived.append(comment_perceived[0]['comment']['value'])
        else:
            entity_comment_perceived = wikipedia.search(self.perceived)
            if entity_comment_perceived != []:
                try:
                    comment_perceived = wikipedia.page(entity_comment_perceived)
                    list_comment_perceived.append(comment_perceived.summary)
                except Exception as e:
                    comment_perceived_exception = e.options[0]
                    comment_perceived1 = wikipedia.page(comment_perceived_exception)
                    list_comment_perceived.append(comment_perceived1)
        if 'WikipediaPage'.lower() in str(list_comment_perceived[0]).lower():
            helper_wikipedia = str(list_comment_perceived[0]).replace('<WikipediaPage ', '').replace('>', '')
            print(helper_wikipedia)
            wikipedia_comment = wikipedia.page(helper_wikipedia)
            list_comment_perceived = []
            list_comment_perceived.append(wikipedia_comment.summary)


        ## Seems ok a hashmap that has as key the comment boxes of the common hypernym entities
        ## and values there exists list in the form of ['entity', 'relation_connected_to_perceived', 'distance to perceived']
        hash_common_hypernym = {}
        for property in self.common_hypernym:
            for entity in self.common_hypernym[property]:
                if entity != []:
                    entity_value = entity[0].capitalize()
                    comment_common_hypernym = " "
                    sparql_common_hypernym = SPARQLWrapper("http://dbpedia.org/sparql")
                    sparql_common_hypernym.setQuery(""" PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
                                        SELECT DISTINCT ?comment WHERE{
                                        ?entry rdfs:label \"""" + entity_value + """\"@en. 
                                        ?entry dbpedia-owl:abstract ?comment
                                        FILTER(lang (?comment) = 'en')}
                                    """)
                    sparql_common_hypernym.setReturnFormat(JSON)
                    results_common_hypernym = sparql_common_hypernym.query().convert()
                    comment_common_hypernym = results_common_hypernym['results']['bindings']
                    if comment_common_hypernym != []:
                        comment_common_hypernym_helper = comment_common_hypernym[0]
                        comment_common_hypernym_helper_final = comment_common_hypernym_helper['comment']['value']
                        if hash_common_hypernym.get(comment_common_hypernym_helper_final) == None:
                            hash_common_hypernym.setdefault(comment_common_hypernym_helper_final, []).append(entity)
                        else:
                            hash_common_hypernym[comment_common_hypernym_helper_final].append(entity)
                    else:
                        try:
                            entity_common_hypernym = wikipedia.search(entity_value)
                        except Exception as e:
                            pass
                        if entity_common_hypernym != []:
                            try:
                                entity_common = wikipedia.page(entity_common_hypernym[0])
                                if hash_common_hypernym.get(entity_common.summary) == None:
                                    hash_common_hypernym.setdefault(entity_common.summary, []).append(entity)
                                else:
                                    hash_common_hypernym[entity_common.summary].append(entity)
                            except wikipedia.exceptions.DisambiguationError or wikipedia.exceptions.PageError or urllib.error as e:
                                entity_common_second = e.options[0]
                                try:
                                    entity_common_second_comment = wikipedia.page(entity_common_second)
                                    if hash_common_hypernym.get(entity_common_second_comment.summary) == None:
                                        hash_common_hypernym.setdefault(entity_common_second_comment.summary, []).append(entity)
                                    else:
                                        hash_common_hypernym[entity_common_second_comment.summary].append(entity)
                                except Exception as e:
                                    if hash_common_hypernym.get('0') == None:
                                        hash_common_hypernym.setdefault('0', []).append(entity)
                                    else:
                                        hash_common_hypernym['0'].append(entity)
                        else:
                            if hash_common_hypernym.get('0') == None:
                                hash_common_hypernym.setdefault('0', []).append(entity)
                            else:
                                hash_common_hypernym['0'].append(entity)

        ## Seems ok a hashmap that has as key the comment boxes of the not common hypernym entities
        ## and values there exists list in the form of ['entity', 'relation_connected_to_perceived', 'distance to perceived']


        not_common_hypernym = {}
        for property in self.not_common_hypernym:
            for entity in self.not_common_hypernym[property]:
                if entity != []:
                    entity_value = entity[0].capitalize()
                    try:
                        comment_not_common_hypernym = " "
                        sparql_not_common_hypernym = SPARQLWrapper("hash_common_hypernymhttp://dbpedia.org/sparql")
                        sparql_not_common_hypernym.setQuery(""" PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
                                            SELECT DISTINCT ?comment WHERE{
                                            ?entry rdfs:label \"""" + entity_value + """\"@en. 
                                            ?entry dbpedia-owl:abstract ?comment
                                            FILTER(lang (?comment) = 'en')}
                                        """)
                        sparql_not_common_hypernym.setReturnFormat(JSON)
                        results_not_common_hypernym = sparql_not_common_hypernym.query().convert()
                        comment_not_common_hypernym = results_not_common_hypernym['results']['bindings'][0]['comment']['value']
                        if not_common_hypernym.get(comment_not_common_hypernym.summary) == None:
                            not_common_hypernym.setdefault(comment_not_common_hypernym.summary, []).append(entity)
                        else:
                            not_common_hypernym[comment_not_common_hypernym.summary].append(entity)

                    except Exception as e:
                        try:
                            entity_not_common_hypernym = wikipedia.search(entity_value)
                        except Exception as e:
                            pass
                        if entity_not_common_hypernym != []:
                            try:
                                entity_not_common = wikipedia.page(entity_not_common_hypernym[0])
                                if not_common_hypernym.get(entity_not_common.summary) == None:
                                    not_common_hypernym.setdefault(entity_not_common.summary, []).append(entity)
                                else:
                                    not_common_hypernym[entity_not_common.summary].append(entity)
                            except wikipedia.exceptions.DisambiguationError or wikipedia.exceptions.PageError or urllib.error as e:
                                entity_not_common_second = e.options[0]
                                try:
                                    entity_not_common_second_comment = wikipedia.page(entity_not_common_second)
                                    if not_common_hypernym.get(entity_not_common_second_comment.summary) == None:
                                        not_common_hypernym.setdefault(entity_not_common_second_comment.summary,
                                                                       []).append(entity)
                                    else:
                                        not_common_hypernym[entity_not_common_second_comment.summary].append(entity)
                                except Exception as e:
                                    if not_common_hypernym.get('0') == None:
                                        not_common_hypernym.setdefault('0', []).append(entity)
                                    else:
                                        not_common_hypernym['0'].append(entity)
                        else:
                            if not_common_hypernym.get('0') == None:
                                not_common_hypernym.setdefault('0', []).append(entity)
                            else:
                                not_common_hypernym['0'].append(entity)


        return  list_comment_perceived, hash_common_hypernym, not_common_hypernym



