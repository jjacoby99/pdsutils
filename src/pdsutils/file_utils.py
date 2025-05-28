from pdsutils.realization_utils import _determine_prefix
import re

def generate_file_list(base_folder_path: str, file_name: str, cases: int, reals: int):
    """Generates a list of files from each realization based on a base folder and a provided file name.
    For instance, if the provided file name is env.ini, the function will return a list of all instances of files with that
    name from case01, Realization001 to case0cases to Realization00reals
    """
    
    real_prefix = _determine_prefix("Realization", reals) 
    file_list = []
    for case_num in range(1, cases + 1):
        case_prefix = _determine_prefix("Case", case_num)
        case_folder_path = base_folder_path + "\\" + case_prefix + str(case_num)
        for real_num in range(1, reals + 1):
            file_list.append(case_folder_path + "\\" + real_prefix + str(real_num) + "\\" + file_name)
    
    return file_list

def extract_suffix(name: str) -> int:
    """
    Searches the given string for a numeric suffix. If one does not exist, a ValueError is thrown.
    If a numeric suffic is found, it is converted to an int and returned.

    @params
        name (str): string to check for suffix

    @returns
        int
    """
        m = re.search(r"(\d+)$", name)
        if not m:
            raise ValueError(f"Couldn't parse numeric suffix from '{name}'")
        return int(m.group(1))