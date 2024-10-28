from typing import Literal
entities = Literal[
    "PERSON", 
    "ORGANISATION", 
    "LOCATION", 
    "TECHNOLOGY", 
    "ECONOMIC_FACTOR", 
    "EVENT", 
    "SURVEY", 
    "TOPIC", 
    "PROJECT", 
    "RESOURCE", 
    "GOAL"
]

relations = Literal[
    "WORKS_FOR", 
    "HAS_SUBSIDIARY", 
    "MERGES_WITH", 
    "PRODUCES", 
    "LOCATED_IN", 
    "PARTICIPATES_IN", 
    "CONDUCTS", 
    "HOSTS", 
    "PARTICIPATED_BY", 
    "MENTIONS", 
    "USED_BY", 
    "AFFECTS", 
    "IMPACTS", 
    "PARTNER_OF", 
    "USES_TECHNOLOGY", 
    "SUPPLIES_RESOURCE", 
    "HAS_PROJECT", 
    "HAS_GOAL", 
    "INVESTS_IN", 
    "DECOMMISSIONED"
]

schema = {
    "PERSON": [
        "WORKS_FOR",      # (Person)-[:WORKS_FOR]->(Organisation)
        "PARTICIPATES_IN",# (Person)-[:PARTICIPATES_IN]->(Event)
        "CONDUCTS"        # (Person)-[:CONDUCTS]->(Survey)
    ],
    "ORGANISATION": [
        "HAS_SUBSIDIARY",  # (Organisation)-[:HAS_SUBSIDIARY]->(Organisation)
        "MERGES_WITH",     # (Organisation)-[:MERGES_WITH]->(Organisation)
        "PRODUCES",        # (Organisation)-[:PRODUCES]->(Resource/Technology)
        "LOCATED_IN",      # (Organisation)-[:LOCATED_IN]->(Location)
        "HOSTS",           # (Organisation)-[:HOSTS]->(Event)
        "USED_BY",         # (Organisation)-[:USED_BY]->(Technology)
        "AFFECTS",         # (Organisation)-[:AFFECTS]->(EconomicFactor)
        "IMPACTS",         # (Organisation)-[:IMPACTS]->(EconomicFactor)
        "PARTNER_OF",      # (Organisation)-[:PARTNER_OF]->(Organisation)
        "USES_TECHNOLOGY", # (Organisation)-[:USES_TECHNOLOGY]->(Technology)
        "SUPPLIES_RESOURCE",# (Organisation)-[:SUPPLIES_RESOURCE]->(Resource)
        "HAS_PROJECT",     # (Organisation)-[:HAS_PROJECT]->(Project)
        "HAS_GOAL",        # (Organisation)-[:HAS_GOAL]->(Goal)
        "INVESTS_IN",      # (Organisation)-[:INVESTS_IN]->(Project)
        "DECOMMISSIONED"   # (Organisation)-[:DECOMMISSIONED]->(Facility)
    ],
    "LOCATION": [
        "LOCATED_IN"       # (Entity)-[:LOCATED_IN]->(Location) (e.g., Organisation, Project)
    ],
    "TECHNOLOGY": [
        "USED_BY",         # (Technology)-[:USED_BY]->(Organisation)
        "PRODUCES",        # (Technology)-[:PRODUCES]->(Resource)
        "USES_TECHNOLOGY"  # (Technology)-[:USES_TECHNOLOGY]->(Organisation/Project)
    ],
    "ECONOMIC_FACTOR": [
        "AFFECTS",         # (EconomicFactor)-[:AFFECTS]->(Entity)
        "IMPACTS"          # (EconomicFactor)-[:IMPACTS]->(Entity)
    ],
    "EVENT": [
        "PARTICIPATES_IN", # (Entity)-[:PARTICIPATES_IN]->(Event)
        "HOSTS",           # (Event)-[:HOSTS]->(Organisation)
        "PARTICIPATED_BY"  # (Event)-[:PARTICIPATED_BY]->(Person)
    ],
    "SURVEY": [
        "MENTIONS",        # (Survey)-[:MENTIONS]->(Topic)
        "CONDUCTED_BY"     # (Survey)-[:CONDUCTED_BY]->(Person/Organisation)
    ],
    "TOPIC": [
        "MENTIONS"         # (Entity)-[:MENTIONS]->(Topic)
    ],
    "PROJECT": [
        "LOCATED_IN",      # (Project)-[:LOCATED_IN]->(Location)
        "USES_TECHNOLOGY", # (Project)-[:USES_TECHNOLOGY]->(Technology)
        "HAS_GOAL",        # (Project)-[:HAS_GOAL]->(Goal)
        "INVESTS_IN"       # (Organisation)-[:INVESTS_IN]->(Project)
    ],
    "RESOURCE": [
        "SUPPLIES_RESOURCE",# (Resource)-[:SUPPLIES_RESOURCE]->(Organisation)
        "PRODUCES_RESOURCE" # (Resource)-[:PRODUCES_RESOURCE]->(Organisation)
    ],
    "GOAL": [
        "HAS_GOAL"         # (Entity)-[:HAS_GOAL]->(Goal)
    ]
}