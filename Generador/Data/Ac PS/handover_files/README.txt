Summary of handover files:

GMMs:
- OpenQuake Python files for WSP-updated GMMs (.py) - save into your local openquake > hazardlib > gsim folder
- OpenQuake GMM logic tree file (.xml)
- Logic tree images (crustal GMMs, subduction GMMs)

MagScalingRelationship:
- watson2023.py - save into your local openquake > hazardlib > scalerel folder
- Magnitude-area scaling relationship that defines a preferred value approximately at the midpoint of published relationships
- Includes a constant standard deviation intended to cover the range of results from published relationships
- See draft report for further details

SourceModels:
- Source model input parameters for each source type (interface, in-slab, crustal faults, crustal area / distributed)
- Further details provided in README.txt files within each sub-folder