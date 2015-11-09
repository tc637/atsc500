import os
import glob, stat
import datetime
import tzlocal  #pip install tzlocal
import pytz
import subprocess

local_tz = tzlocal.get_localzone()
notebooklist=glob.glob('*.ipynb')
pythonlist=glob.glob('./python/*.py')

py_dict={}
nb_dict={}
for the_file in notebooklist:
    head,ext=os.path.splitext(the_file)
    the_date=datetime.datetime.fromtimestamp(os.stat(the_file)[stat.ST_MTIME])
    the_date=local_tz.localize(the_date)
    the_date = the_date.astimezone(pytz.utc)
    nb_dict[head] = the_date

for the_file in pythonlist:
    head,name=os.path.split(the_file)
    head,tail=os.path.splitext(name)
    the_date=datetime.datetime.fromtimestamp(os.stat(the_file)[stat.ST_MTIME])
    the_date=local_tz.localize(the_date)
    the_date = the_date.astimezone(pytz.utc)
    py_dict[head] = the_date


#notebooks not in pythonlist

py_files=set(py_dict.keys())
nb_files=set(nb_dict.keys())

make_py=nb_files - py_files
print('rebuilding {}'.format(make_py))
cmdstring='ipython nbconvert --stdout --to python ../{0:s}.ipynb > python/{0:s}.py'
for the_file in make_py:
    command=cmdstring.format(the_file)
    out=subprocess.getstatusoutput(command)
    print(out)

for the_file in nb_files:
    if nb_dict[the_file] > py_dict[the_file]:
        print('rebuilding {}'.format(the_file))
        command=cmdstring.format(the_file)
        out=subprocess.getstatusoutput(command)
        print(out)

