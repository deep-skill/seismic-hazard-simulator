Summary of crustal fault source model inputs:

coords:
- Coordinates exported from GIS for the geometry of each crustal fault (adopted from INGEMMET, simplified into one trace per fault)

logic_trees:
- Logic tree images for each different group of crustal faults sources

Excel files:
Shallow_Crustal_Faults_NearSite_20231210.xlsx:
- Input parameters (geometry and activity) for crustal faults < 50 km from sites and >= 0.1 mm/yr slip rate
- Occurrence rates calculated using Python code included in Excel file 
- Range of Mmax values for different branches is included in corresponding Excel file: fault_mmax_FaultsNearSite.csv
- Branching matches the corresponding logic tree in the logic_trees folder

Shallow_Crustal_Faults_Distant_20231210.xlsx:
- Input parameters (geometry and activity) for crustal faults > 50 km from sites, or < 50 from sites and < 0.1 mm/yr slip rate
- Occurrence rates calculated using Python code included in Excel file 
- Range of Mmax values for different branches is included in corresponding Excel file: fault_mmax_FaultsDistant.csv
- Branching matches the corresponding logic tree in the logic_trees folder


