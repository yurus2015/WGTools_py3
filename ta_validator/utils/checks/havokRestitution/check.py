import maya.cmds as cmds
checkLabel = "Find Restitution Value"


def main():
	print('<< ' + checkLabel.upper() + ' >>')
	return_list = []

	nodes = cmds.ls(type = 'hkNodeRigidBody')
	if nodes:
		for node in nodes:
			restitution = cmds.getAttr(node + '.restitution')
			if restitution != 0.0:
				tmp = []
				tmp.append(node + ': ' + str(restitution))
				tmp.append(node)
				return_list.append(tmp)

	return return_list