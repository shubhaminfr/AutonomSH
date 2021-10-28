import os

# So this file is just to restart the entire block
# Like system restore
# Interesting thing done with centaur savedfiles as some of them are deleted after each step

os.system("rm TestHole.igs")
os.system("rm Centaur/TestHole.igs")
os.system("rm -r opt.*")
os.system("rm -r geom_script_*")

os.chdir("./Centaur")
os.system("rm -r opt*")
os.system("cp savedfiles/* .")

os.system("ls ../.")

os.chdir("../interpMesh/.")
os.system("rm interp* hip-warning* opt*")

