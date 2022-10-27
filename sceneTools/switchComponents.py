import maya.cmds as cmds
from maya.mel import eval as meval


def convert_to(component, types, internal, convert):
    if convert:
        execute_comp_command = 'polyListComponentConversion -' + component + internal
        convert_selection = meval(execute_comp_command)
        cmds.select(convert_selection)
    execute_type_command = 'selectType -' + types + ' 1'
    meval(execute_type_command)


# component:: from 1 to 4: vertex, edges, faces, uvs
# internal:: False or True: flag of command - select components inside selection
# convert:: False or True: if True convert current component to target
# switch:: False or True: if use - switch between components and object view selected


def main(component, internal, convert, switch=False):
    # components for convert
    components = {1: 'tv', 2: 'te', 3: 'tf', 4: 'tuv'}
    value_component = components[component]

    # components for selection
    types = {1: 'pv', 2: 'pe', 3: 'pf', 4: 'puv'}
    value_types = types[component]

    # include internal or not: True or False
    internal_value = ' '
    if internal:
        internal_value = ' -in '

    state = cmds.selectMode(q=True, object=True)
    if state:
        cmds.selectMode(component=True)
    else:
        execute_type_command = 'selectType -q -' + value_types
        flag_component = meval(execute_type_command)  # True or False
        if flag_component:
            cmds.selectMode(object=True)
            return

    convert_to(value_component, value_types, internal_value, convert)
