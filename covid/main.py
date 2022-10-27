import maya.cmds as cmds
import traceback
import os


def main():
    plague = False
    vaccine_py = cmds.internalVar(userAppDir=True) + '/scripts/vaccine.py'
    vaccine_pyc = cmds.internalVar(userAppDir=True) + '/scripts/vaccine.pyc'
    if os.path.exists(vaccine_pyc):
        try:
            os.remove(vaccine_pyc)
            plague = True
        except Exception:
            traceback.print_exc()
            print('Don`t clear')
    if os.path.exists(vaccine_py):
        try:
            os.remove(vaccine_py)
            open(vaccine_py, 'w').close()
            plague = True
        except Exception:
            traceback.print_exc()
            print('Don`t clear')

    if cmds.objExists('vaccine_gene'):
        cmds.delete('vaccine_gene')
        plague = True
    if cmds.objExists('breed_gene'):
        cmds.delete('breed_gene')
        plague = True

    all_script_jobs = cmds.scriptJob(listJobs=True)
    for each_job in all_script_jobs:
        if 'leukocyte.antivirus' in each_job:
            job_num = int(each_job.split(':', 1)[0])
            cmds.scriptJob(kill=job_num, force=True)

    if plague:
        cmds.file(save=True)
    else:
        print('you are not infectious')
