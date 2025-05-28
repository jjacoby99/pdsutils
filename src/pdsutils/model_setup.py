from pdsutils.Vector6 import Vector6
from pdsutils.file_reader import read_position_state
from pdsutils.file_utils import extract_suffix
import os

def duplicate(folder_path: str, 
               rb_name: str, 
               n: int, 
               incr: Vector6):
    """
    Duplicates a rigid body named "rb_name" in the folder_path n times based
    on the provided incr list. 
    The contents of the .ini file pertaining to the base rigid body are read for the
    base rb, then written into new .ini files for each of the n new copies.

    Copies will read trailing numbers from the provided rb_name, then increment

    @Params
        folder_path (str) : root folder containing PST project. 
        rb_name (str)     : name of rigid body to be copied. Assumed to already exist in PST project.
        n (int)           : number of copies to create
        incr (Vector6)  : rule to follow when copying. Describes the translation and rotation of one 
                            rigid body to the next. incr = {dx, dy, dz, drx, dry, drz}

    @Returns
        void
    """
    ini_path = os.path.join(folder_path, rb_name + ".ini")
    dat_path = os.path.join(folder_path, rb_name + ".dat")
    sim_path = os.path.join(folder_path, "sim.ini")

    if not os.path.exists(ini_path):
        raise FileNotFoundError(f"Provided folder does not contain an ini file for {rb_name}.")

    if not os.path.exists(dat_path):
        raise FileNotFoundError(f"Provided folder does not contain a dat file for {rb_name}")

    if not os.path.exists(sim_path):
        raise FileNotFoundError(f"Provided folder does not contain a sim.ini file.")

    with open(ini_path, "r") as base, \
         open(os.path.join(folder_path, "sim.ini"), "a") as sim, \
         open(dat_path, "r") as dat:

        base_ini = base.readlines()
        base_dat = dat.readlines()

        try:
            base_position = Vector6.from_iter(read_position_state(base_dat))
        except ValueError as e:
            raise ValueError(f"Error reading state position: {str(e)}")
       
        try:
            start_num = extract_suffix(rb_name) + 1
        except ValueError as e:
            start_num = 1

        end_num = start_num + n
        for rb_id in range(start_num, end_num):
            # write to the sim file
            sim.write(f"$DObjects RigidBody Walkway{rb_id}\n")

            # write the ini file for the new dObject
            name = f"Walkway{rb_id}"
            with open(os.path.join(folder_path, name + ".ini"), "w") as new_ini:
                new_ini.writelines(base_ini)

            # calculate the state of the nth rb
            n = rb_id - start_num
            cur = base_position + (n+1) * incr

            state = f"<state>\n0\n0\n0\n0\n0\n0\n{cur.x}\n{cur.y}\n{cur.z}\n{cur.rx}\n{cur.ry}\n{cur.rz}\n</state>"
            # write the .dat file for the new dObject
            with open(os.path.join(folder_path, name + ".dat"), "w") as new_dat:
                new_dat.writelines(state)