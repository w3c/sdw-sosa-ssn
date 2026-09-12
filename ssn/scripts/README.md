# Repository scripts

| Script | What it does |
|---|---|
| [`check_repository.ldpy`](check_repository.ldpy) | Repository integrity: unused chapters and images, unreferenced data files, dangling internal links, Turtle that does not parse, the consistency of the ontology itself (term definitions, labels, domains and ranges, deprecation, documentation anchors, prefixes, examples), whether the Turtle and the prose still say the same thing, and whether each module is in OWL 2 DL and has no class an instance would contradict. Run by CI on every push. |
| [`publish_namespace.py`](publish_namespace.py) | Copies the ontology files to the place where `https://www.w3.org/ns/` must serve them, in a checkout of [w3c/ns](https://github.com/w3c/ns), and writes the RDF/XML beside each one. Every destination is derived from the ontology IRI and the version IRI the file declares. Assumes `ns` and this repository sit side by side; pass `--ns-repo` otherwise. |
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

The OWL 2 DL checks also need `owlapy` and a Java runtime — see below. Without
either, they report themselves skipped and the rest of the script still runs.

`validate.py` is ordinary Python and needs `pyshacl` and `rdflib`.

## Comparing the Turtle with the prose

Each term is described twice — as `skos:definition` in Turtle, and as prose in
the chapter that documents it — and the two drift apart one edit at a time.
`check_repository.ldpy` compares them paragraph by paragraph and reports what
no longer matches, with the nearest prose alongside:

```text
- SOSAProcedure (ssn/chapters/Common.html)
    turtle: A Procedure is re-usable, and might be applied in many Actuations, Observations, or Samplings. ...
      last changed 2025-07-12 30a00ae3 Sync definitions between HTML and TTL representations
    prose (more recent):  A Procedure is re-usable, and might be applied in many Executions (Actuations, Observations, or Samplings). ...    [96% alike]
      last changed 2025-07-23 077d50a9 Tweak Procedure definition and notes
```

Each side is traced with `git blame`, down to the lines that carry that
paragraph rather than the whole file, and the one edited last is marked
`(more recent)` — usually the side holding the intended wording, the other
being the one that was forgotten.

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

## OWL 2 DL, and classes nothing can be an instance of

SOSA/SSN is an OWL 2 DL ontology. That is what keeps reasoning decidable, and
what the reasoners the specification expects are built for; and it is a
syntactic condition, so losing it costs nothing visible. An annotation property
nobody declared, an IRI used as two kinds of property at once — the Turtle
still parses, the documentation still renders, and the ontology is no longer in
the profile it claims.

The other question needs a reasoner. A class is *unsatisfiable* when the axioms
leave no room for an instance: saying that anything is one makes the whole
ontology inconsistent, and from an inconsistent ontology everything follows.
Nothing in the Turtle says so, and reading rarely finds it; only classification
does.

```sh
pip install owlapy         # and a Java runtime, for the OWL API and HermiT
```

Both questions are asked of a module *and its imports*, through the OWL API and
HermiT that [owlapy](https://github.com/dice-group/owlapy) puts on a JVM. Every
`owl:imports` is resolved to the file in this repository that declares that
ontology IRI or version IRI, so the check never reaches the network — and a
module whose imports it cannot resolve that way is listed as not checked rather
than fetched. That is what leaves the alignments out: they import DOLCE, SAREF,
PROV and schema.org, which are neither ours to keep in the profile nor worth a
download on every push.

A profile violation is reported against the module that holds the offending
axiom, once, even though it takes every importing module out of the profile
too:

```text
=== Modules with OWL 2 DL profile violations ===
- ssn/rdf/ontology/extensions/sosa-oms.ttl — 174 violation(s)
    77 × illegal punning: http://www.opengis.net/def/ont/modspec/implements
    ...
```

The profile check only warns, for now: every module carries violations that
predate it, listed in
[#528](https://github.com/w3c/sdw-sosa-ssn/issues/528). The reasoning checks
are fatal — the ontology is coherent today, and that is worth keeping.
