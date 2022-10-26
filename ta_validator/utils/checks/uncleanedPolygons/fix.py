import maya.cmds as cmds
import maya.mel as mel

def main(*args):

	result = []
	if args:
		print('args', args)

		for i in args:
			result.extend(i)
		print('res', result)
		cmds.select(result)
		mel.eval("Triangulate;")
		cmds.select(d = 1)
		#print 'des'
		# for i in args:
		#	print 'value', i
		#	#result.append(i.split(".")[0])
			# print 'III', i
			# cmds.polyTriangulate(i, ch=0)
		#	#result.append(i)

	#result = list(set(result))
	#print 'result', result

	# if result:
	# 	for i in result:
	# 		cmds.select(i)
	# 		mel.eval("Triangulate;")
	# 		cmds.delete(ch=1)

	# cmds.select(d=1)

	#if result:
	#	for i in result:
	#		cmds.polyTriangulate(i, ch=0)

	return []