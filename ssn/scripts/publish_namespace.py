"""Publish SOSA/SSN into the w3c/ns namespace tree: the files, and the rules.

Every ontology file in this repository belongs to the 2023 edition.  This
script does the two mechanical halves of publishing them under
https://www.w3.org/ns/, and neither is decided by a hand-written table: both
come from what the files and the specification themselves declare.

**The files.**  Each ontology is copied to the place its IRI names, with the
RDF/XML alternative beside it::

    ontology IRI   http://www.w3.org/ns/sosa/act/
    destination    <ns>/sosa/2023/act/sosa-act.ttl  + .rdf  + .html stub

    ontology IRI   http://www.w3.org/ns/sosa/oboe          (no trailing slash)
    destination    <ns>/sosa/2023/oboe.ttl          + .rdf

    ontology IRI   http://www.w3.org/ns/sosa/system-capability-properties#
    destination    <ns>/sosa/2023/system-capability-properties.ttl + .rdf

An `owl:versionIRI`, when a file declares one, wins over that derivation.

**The rules.**  A term IRI must serve the latest edition that declares the
term, and a term IRI no edition declares must answer 404 — so the server has
to know the terms.  Into a delimited block of each `.htaccess` concerned, the
script writes the rules that say so: to the anchor of the specification for a
client that wants HTML, to the version IRI of the module that defines the term
for everyone else.  It reads the 2023 terms here, the 2017 terms from the
namespace tree itself, and the anchors from the specification, where every
term is marked up as::

    <section class="specterm sosa" id="SOSAActuator">
        <h5><dfn>sosa:Actuator</dfn></h5>
        <p class="crossreference"><strong>IRI:</strong> http://www.w3.org/ns/sosa/Actuator

Only what lies between the markers is written.  Everything else in an
`.htaccess` is hand-written and left alone.

Where the namespace repository is
---------------------------------
The default assumes `ns` and `sdw-sosa-ssn` are checked out side by side::

    .../W3C/
        ns/                 <- the namespace tree, github.com/w3c/ns
        sdw-sosa-ssn/       <- this repository

Pass `--ns-repo` for any other layout.

Usage::

    python3 ssn/scripts/publish_namespace.py --dry-run
    python3 ssn/scripts/publish_namespace.py
    python3 ssn/scripts/publish_namespace.py --prune

`--prune` deletes the files of a managed edition subtree that this run did not
write — what an ontology leaves behind when it is renamed or withdrawn.
"""

import argparse
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

# rdflib walks its store through dictionaries keyed by terms, so the order in
# which it serialises depends on the hash seed of the interpreter.  Left alone,
# every run would rewrite every RDF/XML file with the same triples in another
# order, and the namespace tree would show hundreds of meaningless changes.
if os.environ.get("PYTHONHASHSEED") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "0"})

from rdflib import Graph, OWL, RDF, RDFS, URIRef
from rdflib.compare import to_canonical_graph

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "ssn"
SOURCE_DIRS = [SPEC_DIR / "rdf" / "ontology", SPEC_DIR / "rdf" / "vocabularies"]

NS = "http://www.w3.org/ns/"
EDITION = "2023"
PREVIOUS_EDITION = "2017"

# The only two namespaces this repository is responsible for.  An ontology that
# claims an IRI under /ns/ but outside of them is reported, never placed: the
# rest of w3c/ns belongs to other working groups.
ROOTS = ("sosa", "ssn")

# The files this script owns inside an edition subtree.  Anything else found
# there — `.htaccess`, above all — is left alone.
MANAGED_SUFFIXES = (".ttl", ".rdf", ".html", ".jsonld", ".nt", "")

# Where each edition is specified.  The 2023 anchors are read from the
# specification itself; the 2017 ones followed a convention per module, which
# is read off the rewrite rules that edition shipped with.
SPEC_URL = {"2017": "https://www.w3.org/TR/vocab-ssn/",
            "2023": "https://www.w3.org/TR/vocab-ssn-2023/"}
ANCHOR_PREFIX_2017 = {
    "sosa/": "SOSA",
    "ssn/": "SSN",
    "sosa/sampling/": "SAMP",
    "sosa/prov/": "PROV",
    "ssn/systems/": "SSNSYSTEM",
    "ssn/ext/": "SSN",
}

BEGIN = "# BEGIN generated term rules — ssn/scripts/publish_namespace.py"
END = "# END generated term rules"

STUB = """Dummy file to allow content negotiation. When the content negotiation
results in a match for this file, a rule in .htaccess catches it and
yields a redirect instead.
"""


class NoHome(Exception):
    """The ontology IRI does not name a place in the SOSA/SSN namespace tree."""


# ---------------------------------------------------------------------------
# Where a module goes
# ---------------------------------------------------------------------------

def destination(ontology_iri, version_iri, edition):
    """Return (directory, basename, flat) relative to the namespace repository.

    `directory` is where the file goes, `basename` the name it takes there,
    without a suffix, and `flat` says whether the module is a file sitting in
    its parent namespace rather than a directory of its own.
    """
    iri = str(ontology_iri)
    if not iri.startswith(NS):
        raise NoHome(f"{iri} is not under {NS}")

    rest = iri[len(NS):]
    flat = not rest.endswith("/")           # a term-less IRI, or a hash namespace
    segments = [s for s in rest.rstrip("#/").split("/") if s]
    if not segments or segments[0] not in ROOTS:
        raise NoHome(f"{iri} is under {NS} but outside {' and '.join(ROOTS)}")

    root, tail = segments[0], segments[1:]

    if version_iri is not None:
        version_rest = str(version_iri)
        if not version_rest.startswith(NS):
            raise NoHome(f"version IRI {version_iri} is not under {NS}")
        directory_segments = [s for s in version_rest[len(NS):].rstrip("#/").split("/") if s]
    else:
        directory_segments = [root, edition] + tail

    if flat:
        # sosa/2023/oboe.ttl — the file is named by the last segment and sits
        # in the directory above, exactly as sosa/oboe.ttl did in 2017.
        return Path(*directory_segments[:-1]), directory_segments[-1], True

    # sosa/2023/act/sosa-act.ttl — the name spells out the path of the IRI, so
    # that it can be read back from the URL being served.
    return Path(*directory_segments), "-".join([root] + tail), False


def expected_version_iri(ontology_iri, edition):
    rest = str(ontology_iri)[len(NS):]
    root, _, tail = rest.partition("/")
    return URIRef(f"{NS}{root}/{edition}/{tail}")


# ---------------------------------------------------------------------------
# What the files declare
# ---------------------------------------------------------------------------

def declared_ontology(path):
    """Return (graph, ontology IRI, version IRI) for one Turtle file."""
    graph = Graph().parse(path, format="turtle")
    ontologies = sorted(graph.subjects(RDF.type, OWL.Ontology))
    if len(ontologies) != 1:
        raise ValueError(f"{len(ontologies)} owl:Ontology declarations, expected 1")
    ontology = ontologies[0]
    versions = sorted(graph.objects(ontology, OWL.versionIRI))
    if len(versions) > 1:
        raise ValueError(f"{len(versions)} owl:versionIRI declarations, expected at most 1")
    return graph, ontology, versions[0] if versions else None


def module_iris(graph):
    """The IRIs in a graph that name a module rather than a term."""
    return ({str(s) for s in graph.subjects(RDF.type, OWL.Ontology)}
            | {str(o) for o in graph.objects(None, OWL.versionIRI)}
            | {str(o) for o in graph.objects(None, OWL.imports)}
            | {str(o) for o in graph.objects(None, OWL.priorVersion)})


def terms_of(graph, ontology):
    """The SOSA/SSN terms a module graph declares, as {term: ontology IRI}.

    A term is a subject in our namespaces the graph says something about: it
    carries a type or a label here, rather than being merely mentioned.
    """
    modules = module_iris(graph)
    found = {}
    for subject in set(graph.subjects()):
        if not isinstance(subject, URIRef) or not str(subject).startswith(NS):
            continue
        if str(subject) in modules:
            continue
        if (subject, RDF.type, None) in graph or (subject, RDFS.label, None) in graph:
            found[str(subject)] = str(ontology)
    return found


def previous_edition(ns_repo):
    """What the 2017 edition serves, read from the namespace tree itself.

    Returns its terms, as {term: module IRI}, and its modules.
    """
    terms, modules = {}, set()
    for root in ROOTS:
        for path in sorted((ns_repo / root / PREVIOUS_EDITION).rglob("*.ttl")):
            try:
                graph, ontology, _ = declared_ontology(path)
            except Exception:
                continue
            terms.update(terms_of(graph, ontology))
            modules.add(str(ontology))
    return terms, modules


# ---------------------------------------------------------------------------
# Where the specification defines each term
# ---------------------------------------------------------------------------

TERM_SECTION = re.compile(
    r'<section[^>]*class="[^"]*specterm[^"]*"[^>]*id="([^"]+)"(.*?)</section>', re.S)
TERM_IRI = re.compile(r'IRI:</strong>\s*([^\s<]+)')


def spec_anchors():
    """{term IRI: anchor} for every term the 2023 specification defines."""
    anchors = {}
    for path in sorted(SPEC_DIR.rglob("*.html")):
        if "usage" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for anchor, body in TERM_SECTION.findall(text):
            iri = TERM_IRI.search(body)
            if iri:
                anchors[iri.group(1)] = anchor
    return anchors


def local_name(term):
    return re.split(r"[/#]", term)[-1]


def namespace_of(term):
    """`sosa/prov/` for http://www.w3.org/ns/sosa/prov/hadProcedure."""
    return term[len(NS):].rsplit("/", 1)[0] + "/"


def anchor_prefix(term, anchor):
    """The part of an anchor that is not the local name of the term."""
    name = local_name(term)
    return anchor[:-len(name)] if anchor.endswith(name) else None


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------

def path_of(iri):
    """`/ns/sosa/2023/obs/` for http://www.w3.org/ns/sosa/2023/obs/.

    Redirects that stay inside the namespace tree are written as paths, not
    as absolute URLs: Apache completes them with the host it was asked, so
    the same rules serve www.w3.org and a container on localhost.
    """
    return iri[len("http://www.w3.org"):].rstrip("#")


def module_rules(root, modules):
    """Rules for the module IRIs of one namespace.

    Everything a namespace serves is ruled from its own `.htaccess`, with the
    path of the module in the pattern: `^oms/?$`, not an `.htaccess` of its
    own in a directory that holds nothing.  Creating those directories would
    hand the request to mod_dir, which answers a directory named without its
    trailing slash with a permanent redirect — precisely what this namespace
    must not do.
    """
    lines, own = [], None
    for iri, edition in sorted(modules.items()):
        rest = iri[len(NS) + len(root) + 1:].rstrip("#")
        target = path_of(str(expected_version_iri(iri, edition)))
        if not rest:
            own = (target, edition)
            continue
        lines.append(f"RewriteRule  ^{rest.rstrip('/')}/?$  {target}  [R=303,L]")

    head = []
    if own:
        head = [f"# The IRI of this namespace serves its most recent edition ({own[1]}).",
                "",
                f"RewriteRule  ^$  {own[0]}  [R=303,L]",
                ""]
    if lines:
        head += ["# Each module of this namespace serves the most recent edition",
                 "# that has it.", ""]
        head += lines + [""]
    return head


def rule_block(root, terms, modules, anchors, documented_in_2017, notes):
    """The generated rules of one namespace: its modules, then its terms.

    `terms` maps a term IRI to (edition, module IRI).  Terms are grouped by
    the path they hang from and by their destination: the anchor prefix of the
    specification for a client that wants HTML, the module that defines them
    for everyone else.  Grouping keeps the block readable — a line per module
    rather than a line per term.
    """
    html = defaultdict(list)        # (path, edition, prefix) -> local names
    unanchored = defaultdict(list)  # (path, edition) -> local names
    graphs = defaultdict(list)      # (path, module version IRI) -> local names

    for term, (edition, module) in sorted(terms.items()):
        name = local_name(term)
        path = term[len(NS) + len(root) + 1:-len(name)]      # "" or "oms/"
        namespace = f"{root}/{path}"
        anchor_edition = edition
        if edition == EDITION:
            anchor = anchors.get(term)
            if anchor is None and term in documented_in_2017:
                # The 2023 edition declares the term but documents it nowhere:
                # every ssn: term it keeps is deprecated, and deprecated terms
                # have no section of their own.  Send the reader to the last
                # edition that does define it rather than to a page where the
                # term does not appear.
                anchor_edition = PREVIOUS_EDITION
                anchor = ANCHOR_PREFIX_2017.get(namespace, "") + name
                notes.append(f"{term}: no anchor in {edition}, sent to {PREVIOUS_EDITION}")
        else:
            anchor = ANCHOR_PREFIX_2017.get(namespace, "") + name
        prefix = anchor_prefix(term, anchor) if anchor else None
        if prefix is None:
            unanchored[(path, edition)].append(name)
            notes.append(f"{term}: documented in no edition, sent to the {edition} specification")
        else:
            html[(path, anchor_edition, prefix)].append(name)
        graphs[(path, str(expected_version_iri(module, edition)))].append(name)

    def alternation(names):
        return "|".join(sorted(names))

    lines = [BEGIN,
             f"# {len(modules)} module(s) and {len(terms)} term(s) of /ns/{root}/,",
             "# written from the ontologies and from the anchors of the",
             "# specification.  Do not edit by hand.",
             ""]
    lines += module_rules(root, modules)
    lines += ["# A client that wants HTML goes to the anchor where the edition",
              "# that defines the term defines it.", ""]
    for (path, edition, prefix), names in sorted(html.items()):
        lines += ["RewriteCond  %{HTTP_ACCEPT}  text/html [NC]",
                  f"RewriteRule  ^{path}({alternation(names)})$  "
                  f"{SPEC_URL[edition]}#{prefix}$1  [R=303,NE,L]",
                  ""]
    for (path, edition), names in sorted(unanchored.items()):
        lines += ["# Deprecated terms have no anchor of their own.",
                  "RewriteCond  %{HTTP_ACCEPT}  text/html [NC]",
                  f"RewriteRule  ^{path}({alternation(names)})$  "
                  f"{SPEC_URL[edition]}  [R=303,L]",
                  ""]

    lines += ["# Every other client goes to the module that defines the term.", ""]
    for (path, module), names in sorted(graphs.items()):
        lines += [f"RewriteRule  ^{path}({alternation(names)})$  "
                  f"{path_of(module)}  [R=303,L]",
                  ""]
    lines.append(END)
    return "\n".join(lines) + "\n"


HEADER = """######################################################################
# Rewrite rules for the {namespace} namespace.
#
# Ontologies and rules developed by the Spatial Data on the Web WG.
######################################################################

RewriteEngine On

"""


def write_block(path, namespace, block, dry_run):
    """Replace the generated block of one .htaccess, leaving the rest alone."""
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = HEADER.format(namespace=f"/ns/{namespace}/")
    if BEGIN in text:
        start = text.index(BEGIN)
        stop = text.index(END) + len(END) + 1
        text = text[:start] + block + text[stop:]
    else:
        text = text.rstrip("\n") + "\n\n" + block
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return path.exists()


# ---------------------------------------------------------------------------
# Placing the files
# ---------------------------------------------------------------------------

def stable_xml(graph, path):
    """Write RDF/XML that only changes when the graph does.

    Blank node labels are made to depend on the graph rather than on the run,
    the triples are sorted, and the prefixes are bound in a fixed order.  With
    a fixed hash seed, that is enough for two runs to produce the same bytes.
    """
    ordered = Graph()
    for prefix, namespace in sorted(graph.namespaces()):
        ordered.bind(prefix, namespace)
    for triple in sorted(to_canonical_graph(graph), key=lambda t: tuple(str(x) for x in t)):
        ordered.add(triple)
    ordered.serialize(destination=path, format="pretty-xml")


def source_files():
    files = []
    for directory in SOURCE_DIRS:
        files += sorted(directory.rglob("*.ttl"))
    return files


def place(source, graph, directory, basename, flat, ns_repo, dry_run):
    """Write the Turtle, the RDF/XML and, for a directory module, the stub."""
    target_dir = ns_repo / directory
    turtle = target_dir / f"{basename}.ttl"
    written = [turtle, target_dir / f"{basename}.rdf"]

    # A module served from its own directory needs the dummy HTML file that
    # content negotiation matches on, so that a browser asking for the
    # namespace is redirected to the specification.  A flat module has none:
    # its HTML clients are served by the rules of the directory above, and a
    # client that insists on HTML gets a 406, as sosa/oboe did in 2017.
    stub = None if flat else target_dir / f"{basename}.html"
    if stub is not None:
        written.append(stub)

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
        # The Turtle is copied verbatim: its comments, its prefixes and its
        # layout are part of what the working group publishes.
        shutil.copyfile(source, turtle)
        # Two source files are readable by their owner only; a copy that
        # inherited that would be a 403 from the server.
        turtle.chmod(0o644)
        stable_xml(graph, target_dir / f"{basename}.rdf")
        if stub is not None:
            stub.write_text(STUB, encoding="utf-8")

    return written


EDITION_HTACCESS = """\
######################################################################
# Rewrite rules for {version_iri}
#
# Written by ssn/scripts/publish_namespace.py.  Do not edit by hand.
######################################################################

RewriteEngine On

######################################################################
# Set the Content-Disposition HTTP header to improve "save as" dialogs
######################################################################
<Files {base}.rdf>
    Header set Content-Disposition "inline; filename={base}.rdf"
</Files>

<Files {base}.ttl>
    Header set Content-Disposition "inline; filename={base}.ttl"
</Files>

######################################################################
# {base}.html exists only so that content negotiation has an HTML
# variant to match.  Its content is never returned: the rule below
# catches it and redirects to the specification instead.  Its lower qs
# keeps clients with no preference on Turtle or RDF/XML.
######################################################################
<Files {base}.html>
    ForceType text/html;qs=0.998
</Files>

######################################################################
# Get rid of any non-empty query string that is not of the form ?term=...
######################################################################
RewriteCond  %{{QUERY_STRING}}  !=""
RewriteCond  %{{QUERY_STRING}}  !^term=
RewriteRule  ^(.*)$  $1?

######################################################################
# A request for the version IRI, i.e. for the directory, is a request
# for one of the {base}.* files.  Content negotiation decides which.
######################################################################
RewriteRule  ^$  {base}?term= [N]

######################################################################
# The HTML variant was chosen: redirect to the specification of this
# edition.  Terms are not served from a version IRI, so there is no
# fragment to add here.
######################################################################
RewriteCond  %{{QUERY_STRING}}  ^(term=)?$
RewriteRule  ^{base}\\.html$  {spec}  [R=303,QSD,NE,L]
"""


def write_edition_htaccess(ns_repo, directory, basename, version_iri, spec, dry_run):
    """The .htaccess of a module directory inside an edition subtree."""
    path = ns_repo / directory / ".htaccess"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            EDITION_HTACCESS.format(base=basename, version_iri=version_iri, spec=spec),
            encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--ns-repo", type=Path, default=REPO.parent / "ns",
                        help="checkout of github.com/w3c/ns (default: ../ns)")
    parser.add_argument("--edition", default=EDITION,
                        help=f"edition these files belong to (default: {EDITION})")
    parser.add_argument("--dry-run", action="store_true",
                        help="say what would be written, write nothing")
    parser.add_argument("--prune", action="store_true",
                        help="delete managed files this run did not write")
    args = parser.parse_args()

    ns_repo = args.ns_repo.resolve()
    if not (ns_repo / "sosa").is_dir() or not (ns_repo / "ssn").is_dir():
        print(f"❌ {ns_repo} does not look like a checkout of w3c/ns", file=sys.stderr)
        return 2

    placed = {}                    # written path -> source file
    homeless, problems, warnings = [], [], []
    silent = 0                     # files that declare no owl:versionIRI
    by_root = defaultdict(list)
    current_terms = {}
    edition_directories = []

    for source in source_files():
        relative = source.relative_to(REPO)
        try:
            graph, ontology, version = declared_ontology(source)
        except Exception as error:
            problems.append((relative, str(error)))
            continue

        if version is not None:
            expected = expected_version_iri(ontology, args.edition)
            if version != expected:
                warnings.append(
                    f"{relative}: declares owl:versionIRI <{version}>, "
                    f"expected <{expected}> for edition {args.edition} — "
                    f"the declared one is used")
        else:
            # Not a warning: every file in this repository belongs to the
            # edition being placed, whether or not it says so in RDF.
            silent += 1

        try:
            directory, basename, flat = destination(ontology, version, args.edition)
        except NoHome as error:
            homeless.append((relative, str(error)))
            continue

        for path in place(source, graph, directory, basename, flat,
                          ns_repo, args.dry_run):
            if path in placed:
                problems.append((relative, f"{path} already written from {placed[path]}"))
            placed[path] = relative
        by_root[directory.parts[0]].append((f"{directory}/{basename}", ontology))
        current_terms.update(terms_of(graph, ontology))
        if not flat:
            edition_directories.append(
                (directory, basename, str(version or expected_version_iri(ontology, args.edition))))

    for directory, basename, version_iri in edition_directories:
        path = write_edition_htaccess(ns_repo, directory, basename, version_iri,
                                      SPEC_URL[args.edition], args.dry_run)
        placed[path] = "generated"

    stale = []
    for root in ROOTS:
        subtree = ns_repo / root / args.edition
        if not subtree.is_dir():
            continue
        for path in sorted(subtree.rglob("*")):
            if path.is_file() and path.suffix in MANAGED_SUFFIXES and path not in placed:
                stale.append(path)
                if args.prune and not args.dry_run:
                    path.unlink()

    print(f"=== Placed in {ns_repo} ===")
    for root in ROOTS:
        for target, ontology in sorted(by_root[root]):
            print(f"- {target}.ttl, .rdf  <-  <{ontology}>")

    # The rules.  A term is served by the latest edition that declares it; a
    # hash namespace needs no rule at all, since the fragment never reaches
    # the server.
    previous_terms, previous_modules = previous_edition(ns_repo)
    served = {term: (PREVIOUS_EDITION, module) for term, module in previous_terms.items()}
    served.update({term: (args.edition, module) for term, module in current_terms.items()})
    served = {term: value for term, value in served.items() if "#" not in term}

    # A module, like a term, is served by the most recent edition that has it.
    editions = {iri: PREVIOUS_EDITION for iri in previous_modules}
    editions.update({str(iri): args.edition for _, iri in
                     ((root, ontology) for root in by_root for _, ontology in by_root[root])})

    # Everything a namespace serves is ruled from its own .htaccess.
    terms_by_root, modules_by_root = defaultdict(dict), defaultdict(dict)
    for term, value in served.items():
        terms_by_root[term[len(NS):].split("/")[0]][term] = value
    for iri, edition in editions.items():
        modules_by_root[iri[len(NS):].split("/")[0]][iri] = edition

    anchors = spec_anchors()
    notes = []

    print("\n=== Rules ===")
    for root in ROOTS:
        terms = terms_by_root[root]
        modules = modules_by_root[root]
        path = ns_repo / root / ".htaccess"
        write_block(path, root,
                    rule_block(root, terms, modules, anchors, set(previous_terms), notes),
                    args.dry_run)
        print(f"- /ns/{root + '/':<8} {len(modules):>2} module(s), {len(terms):>3} term(s)"
              f"  ->  {path.relative_to(ns_repo)}")

    if homeless:
        print("\n=== No home under /ns/sosa/ or /ns/ssn/ ===")
        for relative, reason in homeless:
            print(f"- {relative}: {reason}")

    if silent:
        print(f"\n{silent} file(s) declare no owl:versionIRI; "
              f"edition {args.edition} taken from this repository.")

    if warnings:
        print("\n=== Warnings ===")
        for warning in warnings:
            print(f"- {warning}")

    if notes:
        print(f"\n=== {len(notes)} term(s) the {args.edition} specification does not anchor ===")
        for note in notes[:4]:
            print(f"- {note}")
        if len(notes) > 4:
            print(f"  … and {len(notes) - 4} more")

    if stale:
        verb = "Deleted" if args.prune and not args.dry_run else "Left behind by an earlier run"
        print(f"\n=== {verb} ===")
        for path in stale:
            print(f"- {path.relative_to(ns_repo)}")
        if not args.prune:
            print("  (run again with --prune to delete them)")

    if problems:
        print("\n=== Problems ===")
        for relative, message in problems:
            print(f"- {relative}: {message}")
        return 1

    total = len({p for p in placed if p.suffix == ".ttl"})
    print(f"\n✅ {total} ontologies placed, {len(served)} terms ruled"
          f"{' (dry run)' if args.dry_run else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
