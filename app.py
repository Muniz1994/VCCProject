import ifcopenshell
import pandas

ifc_file = ifcopenshell.open('20160125WestRiverSide Hospital-Ifc2x3-Autodesk_Hospital_Metric_Structural_2015.ifc')



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

print(data.head())

