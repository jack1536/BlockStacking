"""
Danny Tamkin and Jack Weber
A program that compares two out files- one that is known and the other that is unknown
"""

import sys

def fileToListTups(file):
    """
    Converts file to a list of tuples
    :param file: input file
    :return: list of tuples of 3 integers
    """
    inLines = file.read().splitlines()
    inLines.pop(0)  # removes the first line which represents the number of block types.

    """
    Now, each item in inLines is a string. We iterate through inLines to convert each line into a tuple of 3 ints
    representing the dimensions of the block types
    """
    for i in range(0, len(inLines)):
        tl = inLines[i].split()  # create a temporary list (tl) of the dimensions in the line
        inLines[i] = (int(tl[0]),  int(tl[1]), int(tl[2]))

    return inLines

def main():
    """
    Can access program through commandline.
    First and second arguments are the names of the output
    files to compare.
    """
    out1 = open(sys.argv[1], "r")
    out2 = open(sys.argv[2], "r")

    out1 = fileToListTups(out1)
    out2 = fileToListTups(out2)

    for i in range(0, len(out1)):
        w_x_h_1 = out1[i][0]*out1[i][1]
        w_x_h_2 = out2[i][0] * out2[i][1]
        if(w_x_h_1 != w_x_h_2) or (out1[i][2] != out2[i][2]):
            print("the two outfiles are not equal. Error in line " + str(i+2))
            print(out1[i])
            print(out2[i])
            return False

    print("the two outfiles are equal")
    return True

if __name__ == "__main__":
    main()