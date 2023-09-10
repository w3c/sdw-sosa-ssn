import sys
from pathlib import Path
import pyshacl
from rdflib import Graph

ONT_PATH = Path('ssn/rdf')
ONT_SHAPES = Path('ssn/shapes/ontology')
EXAMPLES_PATH = Path('ssn/examples')
EXAMPLES_SHAPES = Path('ssn/shapes/examples')

ont_shapes_graph = Graph()
examples_shapes_graph = Graph()

ont_shapes_fns = list(ONT_SHAPES.glob('*.shacl'))
print("Using ontology SHACL files:\n - {}".format('\n - '.join(str(fn) for fn in ont_shapes_fns)))
# Read SHACL shapes
for fn in ont_shapes_fns:
    ont_shapes_graph.parse(fn, format='ttl')

examples_shapes_fns = list(EXAMPLES_SHAPES.glob('*.shacl'))
print("Using example SHACL files:\n - {}".format('\n - '.join(str(fn) for fn in examples_shapes_fns)))
for fn in examples_shapes_fns:
    examples_shapes_graph.parse(fn, format='ttl')

global_result = True
# Validate ontology
for fn in ONT_PATH.glob('*.ttl'):
    print(f"Validating ontology file {fn}...", end=' ')
    data_graph = Graph().parse(fn)
    result, result_graph, result_text = pyshacl.validate(data_graph=data_graph, shacl_graph=ont_shapes_graph, advanced=True)
    if not result:
        print('[ERROR]')
        global_result = False
        print(f"== Errors found while validating ontology file {fn} ==\n{result_text}", file=sys.stderr)
    else:
        print("[OK]")

# Validate examples
for fn in EXAMPLES_PATH.glob('*.ttl'):
    print(f"Validating example file {fn}...", end=' ')
    data_graph = Graph().parse(fn)
    result, result_graph, result_text = pyshacl.validate(data_graph=data_graph, shacl_graph=ont_shapes_graph, advanced=True)
    if not result:
        print('[ERROR]')
        global_result = False
        print(f"== Errors found while validating example file =={fn}:\n{result_text}", file=sys.stderr)
    else:
        print('[OK]')

if not global_result:
    print("\nValidation errors were encountered", file=sys.stderr)
    sys.exit(-1)