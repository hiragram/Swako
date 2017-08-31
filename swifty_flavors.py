import re

def typeName(property):
    primitive = typeNameString(property.type)
    if primitive != None:
        return primitive

    if property.type == "array":
        elementName = typeNameString(property.itemType)
        return "Array<" + elementName + ">"

def typeNameString(typeName):
    if typeName == "integer":
        return "Int"
    elif typeName == "string":
        return "String"
    elif typeName == "boolean":
        return "Bool"
    elif typeName == "array":
        return None
    else:
        m = re.search(r"#/definitions/(.*)", typeName)
        return m.group(1)