from itertools import chain
import re
import sys
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from collections import defaultdict

CHAPTERS_DIR = Path("ssn/chapters")
TTL_EXT = ".ttl"
SSN_NS = "http://www.w3.org/ns/ssn/"
SOSA_NS = "http://www.w3.org/ns/sosa/"

# Identify unreferenced HTML files in chapters/
def find_unused_html_chapters():
    html_ref_pattern = re.compile(r'data-include=["\']\.\/chapters\/(.*?)\.html["\']')
    chapter_files = {f.stem for f in CHAPTERS_DIR.glob("*.html")}
    referenced_chapters = set()

    for file in Path(".").rglob("*.html"):
        if CHAPTERS_DIR in file.parents:
            continue
        with open(file, encoding="utf-8") as f:
            content = f.read()
            referenced_chapters.update(html_ref_pattern.findall(content))

    unused = chapter_files - referenced_chapters
    return [CHAPTERS_DIR / (f + ".html") for f in sorted(unused)]


# Identify .ttl files that fail to load via rdflib
def find_invalid_ttl_files():
    invalid_files = []
    for file in Path(".").rglob(f"*{TTL_EXT}"):
        try:
            g = Graph()
            g.parse(file, format="turtle")
        except Exception as e:
            invalid_files.append((file, str(e)))
    return invalid_files


# Identify .ttl files not referenced in any HTML via href or data-include
def find_unreferenced_ttl_files():
    ttl_files = {f.resolve() for f in Path(".").rglob(f"*{TTL_EXT}")}
    ttl_files = set(filter(lambda f: "ontology" not in str(f), ttl_files))
    referenced = set()
    ttl_ref_pattern = re.compile(r'(?:href|data-include)=["\']([^"\']+?\.ttl)["\']')

    for file in Path(".").rglob("*.html"):
        with open(file, encoding="utf-8") as f:
            content = f.read()
            matches = ttl_ref_pattern.findall(content)
            for match in matches:
                # Discard absolute URLs
                if re.match(r"^\w+://", match):  # e.g., http://, https://, file://
                    continue
                resolved_path = (Path("ssn") / Path(match)).resolve()
                if resolved_path in ttl_files:
                    referenced.add(resolved_path)

    unreferenced = ttl_files - referenced
    return sorted(unreferenced)

# Find unreferenced images
def find_unreferenced_images():
    image_dir = Path("ssn/images")
    allowed_exts = {".svg", ".png", ".jpg", ".jpeg", ".gif"}
    all_images = {f.resolve() for f in image_dir.glob("*") if f.is_file() and f.suffix.lower() in allowed_exts}
    referenced = set()

    # Match src="images/..." or src="./images/..."
    img_ref_pattern = re.compile(r'src=["\'](?:\.\/)?images\/([^"\']+)["\']')

    for html_file in Path("ssn/chapters").rglob("*.html"):
        with open(html_file, encoding="utf-8") as f:
            content = f.read()
            matches = img_ref_pattern.findall(content)
            for filename in matches:
                resolved_path = (Path("ssn/images") / filename).resolve()
                if resolved_path in all_images:
                    referenced.add(resolved_path)

    unreferenced = all_images - referenced
    return sorted(unreferenced)

# Check defined terms
def check_defined_terms():
    ttl_files = sorted(chain(Path("ssn/rdf/ontology/core").rglob("*.ttl"),
                             Path("ssn/rdf/ontology/extensions").rglob("*.ttl"),
                             Path("ssn/rdf/vocabularies").rglob("*.ttl")))
    term_to_ontos_using_term = defaultdict(set)
    term_to_ontos_defining_term = defaultdict(set)
    onto_to_file_declaring_onto = {}
    onto_to_terms_defined_in_onto = defaultdict(set)

    for ttl_file in ttl_files:
        try:
            g = Graph()
            g.parse(ttl_file, format="turtle")

            # Find ontology IRI
            ontology_iris = list(g.subjects(RDF.type, OWL.Ontology))
            if len(ontology_iris) == 0:
                print(f"⚠️  No ontology declaration found in {ttl_file}")
                continue
            if len(ontology_iris) > 1:
                print(f"⚠️  >1 ontology declaration found in {ttl_file}")
                continue

            ontology_iri = ontology_iris[0]
            onto_to_file_declaring_onto[ontology_iri] = ttl_file

            # Find terms defined by this ontology
            terms = set()
            for triple in g:
                for t in triple:
                    if not isinstance(t, URIRef) or not (t.startswith(SOSA_NS) or t.startswith(SSN_NS)):
                        continue
                    terms.add(t)
            for term in terms:
                term_to_ontos_using_term[term].add(ttl_file)
                for o in g.objects(term, RDFS.isDefinedBy):
                    term_to_ontos_defining_term[term].add(o)
                    onto_to_terms_defined_in_onto[o].add(term)
                
        except Exception as e:
            print(f"❌ Error parsing {ttl_file}: {e}")

    # Print ontology declarations
    print("\n=== Ontology Declarations ===")
    for iri, file in onto_to_file_declaring_onto.items():
        print(f"- <{iri}>: {file}")

    # Check for duplicates term definitions
    print("\n=== Term Definitions ===")
    duplicates = {term: ontos for term, ontos in term_to_ontos_defining_term.items() if len(ontos) > 1}
    if not duplicates:
        print("No duplicate term definitions 🎉")
    else:
        print(f"❌ Term definition duplicates")
        for term, ontos in duplicates.items():
            print(f"- {term} defined in:")
            for onto in ontos:
                print(f"    - {onto}")
        
    # Check for undefined terms
    not_defined = {term for term, ontos in term_to_ontos_defining_term.items() if len(ontos) == 0}
    if not not_defined:
        print("No term undefined 🎉")
    else:
        print(f"❌ Missing term declarations")
        for term in not_defined:
            print(f"- {term} not defined but used in:")
            for ttl_file in term_to_ontos_using_term[term]:
                print(f"    - {ttl_file}")

    # Check terms defined in a non-declared ontology
    onto_doesnt_exist = defaultdict(set)
    for term, ontos in term_to_ontos_defining_term.items():
        for onto in ontos:
            if onto not in onto_to_file_declaring_onto:
                onto_doesnt_exist[onto].add(term)
    if not onto_doesnt_exist:
        print("All terms defined in existing ontologies 🎉")
    else:
        print(f"❌ some terms are defined in a non-declared ontology")
        for onto in onto_doesnt_exist:
            print(f"- {onto} is declared nowhere but the following terms are declared to be defined in it:")
            for term in onto_doesnt_exist[onto]:
                print(f"    - {term}")
        
    # List all term definitions
    print("\n=== All Term Definitions ===")
    for term in sorted(term_to_ontos_defining_term):
        onto = next(iter(term_to_ontos_defining_term[term]), None)
        ttl_file = onto_to_file_declaring_onto.get(onto, None)
        print(f"- {term} defined in {onto} which is declared in {ttl_file}")

    # List all term definitions
    print("\n=== Term Definitions Per File ===")
    for onto in sorted(onto_to_terms_defined_in_onto):
        ttl_file = onto_to_file_declaring_onto.get(onto, None)
        for term in sorted(onto_to_terms_defined_in_onto[onto]):
            print(f"- {ttl_file} declares {term}")

    issues = bool(duplicates) or bool(not_defined) or bool(onto_doesnt_exist)
    return term_to_ontos_defining_term, onto_to_terms_defined_in_onto, issues  # return True if issues found

def check_examples_terms_defined(term_to_ontos_defining_term, onto_to_terms_defined_in_onto):
    example_folder = Path("ssn/rdf/examples")
    undefined_terms = defaultdict(set)  # term → set of example files using it
    terms_present_in_some_example = set()

    for ttl_file in example_folder.glob("*.ttl"):
        try:
            g = Graph()
            g.parse(ttl_file, format="turtle")

            for triple in g:
                for t in triple:
                    if not isinstance(t, URIRef) or not (t.startswith(SOSA_NS) or t.startswith(SSN_NS)):
                        continue
                    terms_present_in_some_example.add(t)
                    if t not in term_to_ontos_defining_term and t not in onto_to_terms_defined_in_onto:
                        undefined_terms[t].add(ttl_file)

        except Exception as e:
            print(f"❌ Error parsing example file {ttl_file}: {e}")

    print("\n=== Undefined SOSA/SSN Terms in Examples ===")
    if not undefined_terms:
        print("All SOSA/SSN terms in examples are properly defined 🎉")
    else:
        print(f"❌ some terms in examples are not defined:")
        for t, files in undefined_terms.items():
            print(f"- {t} used in:")
            for f in files:
                print(f"    - {f}")

    print("\n=== SOSA/SSN Terms not present in Examples ===")
    terms_absent_from_examples = set(term_to_ontos_defining_term).difference(terms_present_in_some_example)
    if not terms_absent_from_examples:
        print("All SOSA/SSN terms are present in some example 🎉")
    else:
        print(f"⚠️ some terms are not present in any example:")
        for term in sorted(terms_absent_from_examples):
            print(f"- {term}")
    
    return bool(undefined_terms)

if __name__ == "__main__":
    has_issue = False

    print("=== Unused HTML Chapter Files ===")
    unused_htmls = find_unused_html_chapters()
    if not unused_htmls:
        print("None 🎉")
    else:
        for f in unused_htmls:
            print(f"- {f}")

    print("\n=== Unreferenced Image Files ===")
    unreferenced_images = find_unreferenced_images()
    if not unreferenced_images:
        print("All images are referenced 🎉")
    else:
        for f in unreferenced_images:
            print(f"- {f}")
  
    print("\n=== Invalid TTL Files ===")
    invalid_ttls = find_invalid_ttl_files()
    if not invalid_ttls:
        print("All valid 🎉")
    else:
        has_issue = True
        for f, err in invalid_ttls:
            print(f"- {f} ❌ Error: {err}")

    print("\n=== Unreferenced TTL Files ===")
    unreferenced_ttls = find_unreferenced_ttl_files()
    if not unreferenced_ttls:
        print("All referenced 🎉")
    else:
        for f in unreferenced_ttls:
            print(f"- {f}")

    term_definitions, onto_to_terms_defined_in_onto, issues = check_defined_terms()
    has_issue |= issues
    
    if check_examples_terms_defined(term_definitions, onto_to_terms_defined_in_onto):
        has_issue = True
        
    sys.exit(1 if has_issue else 0)
