from typing import List
import os
from pdsutils.realization_utils import _determine_prefix



def check_property(prop: str, expected_val, file_path_list: List[str], correct: bool = True) -> None:
    """checks each the value of property in each file in file_path_list. 
        - If all instances of property match the expected_val,
        the function returns an empty list []
        - If any instances of a property don't match the expected_val,
        the function returns a list of file paths where the property DID NOT match.
        - If the correct parameter is left as True, the property will be edited to match the expected value
        in each instance where it originally differed.

        Args:
            1)  prop (str): the property to be checked and potentially modified. Must be preceded by the $ character
            2)  expected_val (any): the desired value of the given property. Should be a double or int depending on the property
            3)  file_path_list (List[str]): a list of file paths to check for the given property. If the file does not contain
                the property, it is ignored and nothing happens.
            4)  correct (optional, bool): positive by default. If you don't want to correct the property to the expected_val,
                set to False
        
        Returns:
            Void
    """

    for file_path in file_path_list:
        update_property(prop, expected_val, file_path)

def update_property(prop:str, expected_val, file_path: str):
    if not os.path.exists(file_path):
        raise RuntimeError(f"Provided file path does not exist. {file_path}")
    lines = []
    new_lines = []
    prop_exists = False
    change_required = False
    
    # check if the property exists in the provided file
    with open(file_path, "r") as file:
        lines = file.readlines()

        # filter out comment lines

        for line in lines:
            if line.startswith("//"):
                new_lines.append(line);
            else:
                
                line_split = line.split()

                if len(line_split) == 2:
                    prop_name = line_split[0]
                    value = _convert_to_best_type(line_split[1])

                    if prop == prop_name:
                        prop_exists = True
                        change_required = True if value != expected_val else False
                    
                        if change_required:
                            new_lines.append(f"{prop} {expected_val}\n")
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

    
    if not prop_exists:
        print(f"Property {prop} did not exist in {file_path}")
        return

    if not change_required:
        print(f"Property {prop} did exist in {file_path} but it was already set to {expected_val}.")
        return

    # update the property
    print(f"Property {prop} was set to {expected_val} in {file_path}")
    with open(file_path, "w") as file:
        file.writelines(new_lines)



def _convert_to_best_type(value: str):
    """ Attempts to convert the provided string to either an int or a float, whatever works best.
        
        Args:
            1) value (str): the string to be converted to either an int or a float.

        Returns:
            The integer conversion of the provided string if possible, then the float conversion if possible.
            If both conversions fail, the string is returned unchanged.
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value



