# Author Patelbb
# Date 03/22/2021
# Compablity : Python3

# SYNOPSIS - An application to rotate the PBM and produce pbm file.

# PYTHON BUILT IN IMPORTS
import os
import sys
import logging as logger
from datetime import datetime
from argparse import ArgumentParser

logger.basicConfig(level=logger.ERROR)

# Utilities
def curr_date_time():
    """
    curr_date_time [ A func for current date and time.]

    Returns:
        [`str`]: [Current Datetime]
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_file(path):
    """
    read_file [ A func. to read the PBM file.]

    Args:
        path ([`str`]): [path to file]

    Raises:
        Exception: [Raise exception if file not found]

    Returns:
        [`str`]: [str object from read file.]
    """

    try:
        if (path.endswith(".pbm")):
            buffer = open(path, "r")
            return buffer.read()
        else:
            log_error("File must have a pbm extenstion!")
    except OSError as e:
        log_error("Couldn't open file to read !" + str(e))


def write_file(export_path, matrix):
    """
    write_file [ A func to write the PBM file.]

    Args:
        export_path ([`str`]): [Path where file would be written.]
        matrix ([`list`]): [rotated PBM matrix]

    Raises:
        e: [description]
    """

    try:
        with open(export_path, "w+") as file:
            file.write("P1")
            file.write("\n# " + os.path.basename(export_path))
            file.write("\n{0} {1}".format(len(matrix), len(matrix[0])))
            for m in matrix: # O (n)
                file.write( "\n" + " ".join(m))
    except OSError as e:
        log_error("Couldn't open file to write !" + str(e))


def log_error(msg):
    """
    log_error [Log an error for user.]

    Args:
        msg ([`str`]): [Error message]

    """

    logger.error(curr_date_time() + ' : ' + msg)
    sys.exit(0)

# CORE Func.
def validate_file(buffered_data):
    """
    validate_file [ A func to validate the pbm file content to meet the pbm requirement ]

    Args:
        buffered_data ([`str``]): [string data]
    """

    split_line_list = buffered_data.split("\n")
    file_length = len(split_line_list)

    if file_length <= 1:
        log_error("File not in pbm format !")
    else:
        for i in range(0, file_length - 1): # O (n)
            if (i == 0 and "P1" not in split_line_list[i]):
                log_error("File type not matching P1, Please use P1 PBM file !")
            elif (i > 0 and "P1" not in split_line_list[i] and split_line_list[i][0].isalpha()):
                log_error("File Sytanx issue ! Please refer to PBM syntax ! A comment must have '#'.")
            elif (i > 0  and split_line_list[i][0].isdecimal() and len(split_line_list[i]) > 70):
                log_error("PBM P1 type file format issue, Line character limit must be less than or equal to 70 including white space.")


def clockwise(matrix, degree):
    """
    clockwise [Roate matrix clockwise]

    Args:
        matrix ([`list`]): [List of PBM ascii]
        degree ([`int`]): [Degree of rotation]
    """

    if 90 == degree:
        rotated_matrix = list(zip(*reversed(matrix))) # O(n * m)
        return [list(element) for element in rotated_matrix] # O (n)
    elif 180 == degree:
        return clockwise(clockwise(matrix, 90), 90) # 2
    elif 270 == degree:
        return clockwise(clockwise(matrix, 90), 180) # 3
    elif 360 or 0 == degree:
        return matrix  # 1


def counterclockwise(matrix, degree):
    """
    counterclockwise [Roate matrix counterclockwise]

    Args:
        matrix ([`list`]): [List of PBM ascii]
        degree ([`int`]): [Degree of rotation]
    """

    if -90 == degree:
        rotated_matrix = list(zip(*reversed(matrix))) # O ( n * m)
        return [list(element)[::-1] for element in rotated_matrix][::-1] # O (n)
    elif -180 == degree:
        return counterclockwise(counterclockwise(matrix, -90), -90) # 2
    elif -270 == degree:
        return counterclockwise(counterclockwise(matrix, -90), -180) # 3
    elif -360 == degree:
        return matrix # 1


def rotoate_pbm(buffered_data, degree):
    """
    rotoate_pbm [A func to parse matrix from PBM and rotate pbm to certain degree]

    Args:
        buffered_data ([type]): [description]
        degree ([type]): [description]

    Returns:
        [type]: [description]
    """    

    split_line_list = buffered_data.split("\n")
    file_length = len(split_line_list)
    matrix_row_column = list()
    matrix = list()
    rotated_pbm = list()

    for i in range(0, file_length): # O (n)
        if (split_line_list[i][0].startswith("0") or split_line_list[i][0].startswith("1")):
            matrix.append(split_line_list[i].split(" "))

    if (len(matrix) == 0):
        log_error("There should be exactly one image in file.")

    matrix_row_column.append(len(matrix))
    matrix_row_column.append(len(matrix[0]))

    if (degree >= 0):
        rotated_pbm = clockwise(matrix, degree)
    elif (degree < 0):
        rotated_pbm = counterclockwise(matrix, degree)


    return rotated_pbm

if __name__ == "__main__":

    degree_choices = [ d for d in range(0, 361, 90)]
    degree_choices = degree_choices + [ -d for d in degree_choices[1:]]

    args = ArgumentParser(description="An application to rotate the PBM(Portable Bit Map) to certian degree angle.")
    args.add_argument("--path", dest="path", type=str, required=True, help="An absolute path with pbm filename to read file.")
    args.add_argument("--export_path", dest="export_path", type=str, required=True, help="An absolute path with pbm filename to write file to.")
    args.add_argument("--degree", dest="degree", type=int, choices=degree_choices, required=True, help="Select degree from avaliable choices.\n\
                                                                                                        Use positive integer to clockwise and \
                                                                                                        negative integer value for counterclockwise.\
                                                                                                        NOTICE: SQUARE image only allowed to be rotated to\
                                                                                                        90 degree subsequent angle.")

    parser = args.parse_args()

    buffered_data = read_file(parser.path)
    validate_file(buffered_data)
    rotated_pbm = rotoate_pbm(buffered_data, parser.degree)
    write_file(parser.export_path, rotated_pbm)
    buffered_data = read_file(parser.export_path)
    validate_file(buffered_data)

#EOF