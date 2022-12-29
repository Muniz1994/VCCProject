import time
start_time = time.time()
import ifcopenshell
import pandas
import ifcopenshell.util.pset
from ifcopenshell.util.selector import Selector


# Abertura de ficheiro IFC
ifc_file = ifcopenshell.open('20160125WestRiverSide Hospital-Ifc2x3-Autodesk_Hospital_Metric_Structural_2015.ifc')

selector = Selector()

columns_2 = selector.parse(ifc_file, '.IfcColumn[Identification.Name = "UC-Universal Column-Column:356x368x177UC:158538"]')

print(columns_2)


# Query do
columns = ifc_file.by_type('IfcColumn')

# print(columns[0].IsDefinedBy)

names, quantities, volumes, types = [], [], [], []

for column in columns:

    for x in column.IsDefinedBy:

        if x.is_a() == 'IfcRelDefinesByProperties':

            if x.RelatingPropertyDefinition.is_a() == 'IfcElementQuantity':

                for quantity in x.RelatingPropertyDefinition.Quantities:

                    if quantity.is_a() == 'IfcQuantityVolume':

                        names.append(column.Name)
                        quantities.append(quantity.Name)
                        volumes.append(quantity.VolumeValue)
                        types.append(column.ObjectType)


data = pandas.DataFrame({
    "Type":types,
    "Name":names,
    "Quantity":quantities,
    "Volume":volumes
})

# print(data.sum())
# print(data.describe())
# print(data.head())

data_2 = data.groupby(by="Name")

# print(data_2.describe())

data.plot.hist()

with pandas.ExcelWriter('output.xlsx') as writer:

    data.to_excel(writer, sheet_name='folha1')

print("--- %s seconds ---" % (time.time() - start_time))

