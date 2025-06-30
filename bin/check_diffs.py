# compare diffs between .svg files

import os
import sys
import glob
import subprocess

if (len(sys.argv) < 3):
  usage_str = "Usage: %s <dir1> <dir2>" % (sys.argv[0])
  print(usage_str)
  print("e.g.:  python check_diffs.py . ~/git/studio_dev/bin")
  exit(1)
else:
   dir1 = sys.argv[1]
   dir2 = sys.argv[2]

py_files = ['studio.py','biwt_dev.py','config_tab.py','microenv_tab.py','cell_def_tab.py','user_params_tab.py','rules_tab.py','ics_tab.py','populate_tree_cell_defs.py','run_tab.py','vis_base.py', 'vis_tab.py','vis_tab_ecm.py','settings.py','studio_classes.py','vis3D_tab.py']
if len(py_files) == 0:
    print("No py files found in ",dir1)
    exit(1)
for filename in py_files:
   print("------ ",filename)
   f = os.path.basename(filename)
   f1 = os.path.join(dir1,f)
   f2 = os.path.join(dir2,f)
   cmd =  ["diff", f1, f2]
   #  print("Running: ", " ".join(cmd))
   res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = res.communicate()
   if res.returncode > 1:
      print("Error running diff")
      print(err)
      print(out)
      exit(1)
   vstr = out.splitlines()
   print(vstr)
#    if len(vstr) == 0 or (len(vstr) == 4 and vstr[1].startswith(b"<    0 days") and vstr[3].startswith(b">    0 days")):
#       print(filename, ": OK")
#    else:
#       print(filename, ": ERR")
#       print(out)
#       print(err)
#       exit(1)
exit(0)