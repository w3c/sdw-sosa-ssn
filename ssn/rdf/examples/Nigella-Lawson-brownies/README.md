# Nigella Lawson Brownies – p-plan/SSN-SOSA-PROV-O Alignment Demonstration

This example demonstrates a complete implementation of the p-plan/SSN-SOSA-PROV-O alignment framework for process modelling.

## Architectural Levels

### 1. Planning Level
The abstract recipe as a reusable plan:
- `plan:nigella-brownies` – the main plan (recipe)
- Steps (`p-plan:Step`) that decompose the process
- Sub-plans (`p-plan:isSubPlanOfPlan`) that hierarchically elaborate each step (melting, chopping, mixing, baking, quality check)
- Variables (`p-plan:Variable`) for ingredients, intermediate products, and the final product
- Procedures (`sosa:Procedure`) to be implemented

### 2. Deployment Level
Concrete implementation in a specific context:
- `kitchen:kitchen-geert` as the platform
- Systems (kitchen appliances) that implement procedures
- Standing deployment of assets on a platform

### 3. Execution Level
Actual execution with traceability:
- Activities (`prov:Activity`), actuations (`sosa:Actuation`) and observations (`sosa:Observation`)
- Concrete entities as instantiations of plan variables
- Time-bound execution with start and end times
- Traceability via `p-plan:correspondsToStep`, `p-plan:correspondsToVariable` and `prov:wasDerivedFrom`

## Key Concepts

### Variables and Entities
- Variables at plan level describe abstract requirements
- Entities at execution level are concrete instantiations
- `p-plan:correspondsToVariable` establishes the relation between abstract and concrete

### Procedures and Systems
- Procedures defined in the plan
- Systems implement procedures
- Actuators execute procedures during execution

### Time and Sequence
- Explicit start and end times
- `p-plan:isPrecededBy` for step ordering
- `prov:wasInformedBy` for activity dependencies

## Conformance

Strictly follows:
- p-plan for process modelling
- SSN-SOSA for sensors and actuators
- PROV-O for provenance
- Separation of abstract planning from concrete execution
