from rdflib import Graph, Namespace, RDF, RDFS, OWL

# Define namespace
EX = Namespace("http://example.org/research/")

# Initialize graph
g = Graph()
g.bind("ex", EX)
g.bind("rdfs", RDFS)

# === Class definitions ===
classes = [
    "Author", "Reviewer", "Paper", "City", "Edition", "Volume", "Venue",
    "Conference", "Workshop", "Journal", "Publication", "Proceedings"
]

for cls in classes:
    g.add((EX[cls], RDF.type, RDFS.Class))

# === Subclass relationships ===
subclasses = [
    ("Reviewer", "Author"),
    # Here all paper types are as well part of a recurring venue, as also an individual publication
    ("Journal", "Venue"),
    ("Journal", "Publication"),
    ("Conference", "Venue"),
    ("Conference", "Publication"),
    ("Workshop", "Venue"),
    ("Workshop", "Publication"),
    ("Proceedings", "Publication"),
    ("Volume", "Publication")
]

for sub, sup in subclasses:
    g.add((EX[sub], RDFS.subClassOf, EX[sup]))

# === Property definitions ===
properties = {
    "writes": ("Author", "Paper"),
    "hasCorrespondingAuthor": ("Paper", "Author"),
    "hasCoAuthor": ("Paper", "Author"),
    "reviewedBy": ("Paper", "Reviewer"),
    "cites": ("Paper", "Paper"),
    "publishedIn": ("Paper", "Publication"), 

    "isEditionOf": ("Edition", "Venue"),
    "hasProceedings": ("Edition", "Proceedings"),
    "hasVolume": ("Journal", "Volume"),
    "hasVolumeNumber": ("Volume", None),
    "heldIn": ("Edition", "City"),
    "heldInYear": ("Edition", None),  # Used by Volume too

    "name": (["Venue", "Author", "City"], None),
    "title": ("Paper", None),
    "abstract": ("Paper", None),
    "citationCount": ("Paper", None),
    "year": ("Paper", None),
}

for prop, (domain, range_) in properties.items():
    prop_uri = EX[prop]
    g.add((prop_uri, RDF.type, RDF.Property))

    # Domain
    if isinstance(domain, list):
        for d in domain:
            g.add((prop_uri, RDFS.domain, EX[d]))
    elif domain:
        g.add((prop_uri, RDFS.domain, EX[domain]))

    # Range
    if range_:
        if isinstance(range_, str) and range_ in EX:
            g.add((prop_uri, RDFS.range, EX[range_]))
        elif range_ is None:
            g.add((prop_uri, RDFS.range, RDFS.Literal))
        else:
            g.add((prop_uri, RDFS.range, EX[range_]))



# Additional OWL Constraints

# Functional Property: Each paper has exactly one corresponding author
g.add((EX["hasCorrespondingAuthor"], RDF.type, OWL.FunctionalProperty))

# Make the Reviwe relation an inverse Property: reviewedBy goes with reviews
g.add((EX["reviewedBy"], OWL.inverseOf, EX["reviews"]))
g.add((EX["reviews"], RDF.type, RDF.Property))

#Including a citation influence transitivity here:
# Transitive property for indirect citation reasoning
g.add((EX["hasIndirectCitation"], RDF.type, RDF.Property))
g.add((EX["hasIndirectCitation"], RDF.type, OWL.TransitiveProperty))
g.add((EX["hasIndirectCitation"], RDFS.domain, EX["Paper"]))
g.add((EX["hasIndirectCitation"], RDFS.range, EX["Paper"]))

# Save TBox
g.serialize("TBOX/BDMA12L-B1-KamaliLassim+Grigat-tbox.ttl", format="turtle")
print("BDMA12L-B1-KamaliLassim+Grigat-tbox.ttl")