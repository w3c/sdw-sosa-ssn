# Repository scripts

| Script | What it does |
|---|---|
| [`check_repository.ldpy`](check_repository.ldpy) | Repository integrity: unused chapters and images, unreferenced data files, dangling internal links, Turtle that does not parse, and the consistency of the ontology itself — term definitions, labels, domains and ranges, deprecation, documentation anchors, prefixes, examples. Run by CI on every push. |
| [`all_terms.ldpy`](all_terms.ldpy) | Lists every term SOSA/SSN defines, by kind. With `--dul`, also writes `dul.definitions.md` from a fetched copy of DOLCE+DnS Ultralite. |
| [`validate.py`](validate.py) | SHACL validation of the ontology and the examples. |

## Running them

The two `.ldpy` files are written in
[Linked-Data Python](https://linked-data-python.readthedocs.io), a superset of
Python whose syntax includes Turtle — so an RDF query reads as the Turtle
pattern it matches, rather than as a chain of rdflib calls:

```ldpy
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@graph merged
for term, ontology in m{ ?term rdfs:isDefinedBy ?ontology }:
    ...
```

```sh
pip install linked-data-python
python -m ldpy ssn/scripts/check_repository.ldpy
python -m ldpy ssn/scripts/all_terms.ldpy
```

`validate.py` is ordinary Python and needs `pyshacl` and `rdflib`.
