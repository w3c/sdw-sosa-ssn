# Repository scripts

| Script | What it does |
|---|---|
| [`check_repository.ldpy`](check_repository.ldpy) | Repository integrity: unused chapters and images, unreferenced data files, dangling internal links, Turtle that does not parse, the consistency of the ontology itself (term definitions, labels, domains and ranges, deprecation, documentation anchors, prefixes, examples), and whether the Turtle and the prose still say the same thing. Run by CI on every push. |
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

## Comparing the Turtle with the prose

Each term is described twice — as `skos:definition` in Turtle, and as prose in
the chapter that documents it — and the two drift apart one edit at a time.
`check_repository.ldpy` compares them paragraph by paragraph and reports what
no longer matches, with the nearest prose alongside:

```text
- SOSAExecutionCollection (ssn/chapters/Common.html)
    turtle: The following consistency rules apply with respect to the execution properties listed above:
    prose:  The following consistency rules apply to the Execution properties listed above:    [91% alike]
```

The comparison is on the text alone. Markup, HTML entities, whitespace, the
flavour of dash or quote, and the numbering of a list are normalised away, and
so is the way a term is named: the prose writes `sosa:ActuationCollection`
where the Turtle spells out "Actuation Collection", and neither is a change of
meaning. **Wording and punctuation are not normalised**, because those are the
content — so the report is an editorial worklist, not a failure, and the check
only ever warns.

Two groups are deliberately out of scope: deprecated terms, and the two
property registries in `rdf/vocabularies/`, which are rendered as tables with
no prose per term.
