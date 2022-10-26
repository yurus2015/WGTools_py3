#modificators

action_category = "Objects"
action_label = "Object Exporter"

#running procedure


import objectExport.objectsExporter
reload(objectExport.objectsExporter)
objectExport.objectsExporter.main()
