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
    ontology_folder = Path("ssn/rdf/ontology/core")
    ttl_files = sorted(ontology_folder.glob("*.ttl"))
    term_definitions = defaultdict(set)
    ontology_declarations = {}

    for ttl_file in ttl_files:
        try:
            g = Graph()
            g.parse(ttl_file, format="turtle")

            # Find ontology IRI
            ontology_iris = list(g.subjects(RDF.type, OWL.Ontology))
            if not ontology_iris:
                print(f"⚠️  No ontology IRI found in {ttl_file}")
                continue

            ontology_iri = ontology_iris[0]
            ontology_declarations[ttl_file] = ontology_iri

            # Find terms defined by this ontology
            for s, p, o in g:
                for term in (s, p, o):
                    if isinstance(term, URIRef) and (
                        str(term).startswith(SOSA_NS) or str(term).startswith(SSN_NS)
                    ):
                        # Check if explicitly defined by this ontology
                        if (term, RDFS.isDefinedBy, ontology_iri) in g:
                            term_definitions[term].add(ttl_file)
                            
        except Exception as e:
            print(f"❌ Error parsing {ttl_file}: {e}")

    # Print ontology declarations
    print("=== Ontology Declarations ===")
    for file, iri in ontology_declarations.items():
        print(f"- {file}: <{iri}>")

    # Check for duplicates
    print("\n=== Term Definition Duplicates ===")
    duplicates = {term: files for term, files in term_definitions.items() if len(files) > 1}
    if not duplicates:
        print("No duplicate term definitions 🎉")
    else:
        for term, files in duplicates.items():
            print(f"- {term} defined in:")
            for f in files:
                print(f"    - {f}")

    return term_definitions, len(duplicates) > 0  # return True if issues found

def check_examples_terms_defined(core_terms):
    example_folder = Path("ssn/rdf/examples")
    undefined_terms = defaultdict(set)  # term → set of example files using it

    for ttl_file in example_folder.glob("*.ttl"):
        try:
            g = Graph()
            g.parse(ttl_file, format="turtle")

            for s, p, o in g:
                for term in (s, p, o):
                    if isinstance(term, URIRef) and (
                        str(term).startswith(SOSA_NS) or str(term).startswith(SSN_NS)
                    ):
                        if term not in core_terms:
                            undefined_terms[term].add(ttl_file)

        except Exception as e:
            print(f"❌ Error parsing example file {ttl_file}: {e}")

    print("\n=== Undefined SOSA/SSN Terms in Examples ===")
    if not undefined_terms:
        print("All SOSA/SSN terms in examples are properly defined 🎉")
        return False  # no issues
    else:
        for term, files in undefined_terms.items():
            print(f"- {term} used in:")
            for f in files:
                print(f"    - {f}")
        return True  # issues found


if __name__ == "__main__":
    has_issue = False

    print("=== Unused HTML Chapter Files ===")
    unused_htmls = find_unused_html_chapters()
    if not unused_htmls:
        print("None 🎉")
    else:
        has_issue = True
        for f in unused_htmls:
            print("-", f)

    print("\n=== Unreferenced Image Files ===")
    unreferenced_images = find_unreferenced_images()
    if not unreferenced_images:
        print("All images are referenced 🎉")
    else:
        has_issue = True
        for f in unreferenced_images:
            print("-", f)
  
    print("\n=== Invalid TTL Files ===")
    invalid_ttls = find_invalid_ttl_files()
    if not invalid_ttls:
        print("All valid 🎉")
    else:
        has_issue = True
        for f, err in invalid_ttls:
            print(f"- {f} ✗ Error: {err}")

    print("\n=== Unreferenced TTL Files ===")
    unreferenced_ttls = find_unreferenced_ttl_files()
    if not unreferenced_ttls:
        print("All referenced 🎉")
    else:
        has_issue = True
        for f in unreferenced_ttls:
            print("-", f)

    print("\n=== Ontology Term Uniqueness Check ===")
    term_definitions, len_duplicates = check_defined_terms()
    if len_duplicates:
        has_issue = True
    
    if check_examples_terms_defined(term_definitions):
        has_issue = True
        
    sys.exit(1 if has_issue else 0)
