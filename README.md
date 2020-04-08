# Semantic-Similarity-Algorithm
The semantic similarity algorithm tries to find semantically related entities from ConceptNet, DBpedia, and WordNet

by Alexandros Vassiliades, Nick Bassiliades

We have developed semantic similarity algortihm, which given a word that is part of the English language tries to find semantically
related entities from the web ontologies ConceptNet, DBpedia, and WordNet. Moreover, the algorithm classifies each entity based on the 
properties that exist in the ConceptNet Knowledge Graph. Additionally, with respect to each property the entities are sorted based on
a semantic similarity metric that takes into consideration the similarity of DBpedia commnet Boxes, the WordNet path distance, and 
the crowdsource defined weights from ConceptNet. We could say that our algorithm is in the field of Semantic Mathcing Algorithms.

Example:
          coffee IsA: stimulant, beverage, liquid, drink
          coffee AtLocation: mug, office, desk, caf, kitchen
          coffee RelatedTo: cappuccino, iced_coffee, irish_coffee, turkish_coffee, brazil, plant,           caffeine
          coffee UsedFor: refill, wake_up, pleasure
          
The properties when given another word apart from coffee might be more, similarly the entities in each property
