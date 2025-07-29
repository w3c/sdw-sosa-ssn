import os
import yaml

# Define the prefixes
prefixes = {
    "ex": "http://example.org/sosa/",
    "qudt": "http://qudt.org/",
    "qudt-1-1": "http://qudt.org/",
    "unit": "http://qudt.org/vocab/unit/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "sh": "http://www.w3.org/ns/shacl#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "sosa": "http://www.w3.org/ns/sosa/",
    "ssn-system": "http://www.w3.org/ns/ssn/systems/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "time": "http://www.w3.org/2006/time#"
}

def generate_examples(directory):
    examples = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".ttl"):
            examples.append({
                "title": filename,
                "snippets": [
                    {
                        "language": "ttl",
                        "ref": f"https://w3c.github.io/sdw-sosa-ssn/ssn/rdf/examples/{filename}"
                    }
                ]
            })
    return examples

def write_yaml_file(output_path, prefixes, examples):
    with open(output_path, "w") as f:
        yaml.dump({"prefixes": prefixes, "examples": examples}, f, sort_keys=False)

if __name__ == "__main__":
    input_dir = "."  # Change this to the directory containing your TTL files if needed
    output_file = "examples.yaml"

    examples = generate_examples(input_dir)
    write_yaml_file(output_file, prefixes, examples)
    print(f"examples.yaml written with {len(examples)} examples.")
