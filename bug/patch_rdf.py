import sys

START = b"<rdf:RDF"
END = b"</rdf:RDF>"

with open("test.xml", "rb") as f:
    patch = f.read()

with open(sys.argv[1], "rb") as f:
    data = f.read()

patched = data[:data.index(START)] + patch + data[data.index(END)+len(END):]

with open(sys.argv[2], "wb") as f:
    f.write(patched)
