"""
Danny Tamkin and Jack Weber
CS140 PSET 11
The program uses dynamic programming to solve the block stacking problem
"""
import sys

def allPossibleTuples(listOfTrips):
    """
    :param listOfTrips: list of tuples with 3 elements
    :return: list of all possible tuple combinations
    """
    allTrips = []

    for trip in listOfTrips:
        allTrips.append(trip)
        allTrips.append((trip[1], trip[2], trip[0]))
        allTrips.append((trip[2], trip[0], trip[1]))

    return allTrips


def blocksOnTop(base, allBlocks):
    """
    Takes a given base and a list of all possible blocks and returns a list of all the potential blocks that could
    go above the base
    :param base: tuple with three ints each representing a dimension of the base block of interest
    :param allBlocks: list of tuples representing all of the blocks that can be made from the blocktypes
    :return: lost of tuples representing the blocks that could fit on top of base.
    """
    w = base[0]
    l = base[1]
    levelAboveBlocks = []

    for block in allBlocks:
        # check if dimensions of block are smaller than base

        if (block[0] < w and block[1] < l) or (block[0] < l and block[1] < w):
            levelAboveBlocks.append(block)

    return levelAboveBlocks


def maxHeightOfSet(blocks, d):
    """
    Uses the dynamic table to return a tuple representing the max height of a set of blocks
    :param blocks: list of tuples where each tuple contains 3 ints representing the dimensions of a block
    :param d: dynamic table (partially) generated in dpTableGenerator
    :return:
    """
    maxHeight = 0
    maxBlock = ()
    for block in blocks:
        if d[block]['height'] > maxHeight:
            maxHeight =  d[block]['height']
            maxBlock = block

    return (maxBlock, maxHeight)


def dpTableGenerator(l):
    """
    Generates a dp table that enables us to solve the problem
    :param l:
    :return: dp table
        key: tuple that represents block that represents base of stack
        value: dictionary with the following kv pairs
            blockAbove: tuple of the block directly above base that results in largest height
            height: height of the max stack with the given block as the base.
    """
    dt = {}

    # iterate through all posible bases
    for kv in l:
        # if there are no blocks above base, then height of base is it's own height
        if(len(kv['blocksAbove']) == 0):
            dt[kv['base']] = {"blockAbove": (), "height": kv['base'][2]}

        else:
            maxBlockAbove = maxHeightOfSet(kv['blocksAbove'], dt)
            dt[kv['base']] = {"blockAbove": maxBlockAbove[0], "height": kv['base'][2] + maxBlockAbove[1]}

    return dt


def optimalStack(d):
    """
    Takes dynamic table and returns solution (optimal stack) in list form
    :param d: dynamic table generated in dpTableGenerator
    :return: list of tuples representing the maximum possible stack of blocks. First item is base of stack.
    """
    # find key with the maximum associated height
    maxHeight = 0
    maxBase = ()
    for k in d.keys():
        if (d[k]['height'] > maxHeight):
            maxHeight = d[k]['height']
            maxBase = k

    # now construct list where each item represents a block. First item is the base
    solutionList = [maxBase]
    currBlock = maxBase

    while len(d[currBlock]['blockAbove']) > 0:
        solutionList.append(d[currBlock]['blockAbove'])
        currBlock = d[currBlock]['blockAbove']

    print("The tallest tower has " + str(len(solutionList)) + " blocks and a height of " + str(maxHeight))

    return solutionList


def levelOneTwo(blockTypes):
    """
    creates a list of dictionaries that represents all possibilities for the first and second level of the stack.
    First level includes all possible bases and all possible blocks that can go directly above base
    :param blockTypes: list of tuples representing the block types
    :return: a list of dictionaries with the following kv pairs
        base: tuple representing a possible base
        blocksAbove: list of tuples representing all possible blocks that can go on top of base.
    """

    """
    first lets create a list of all possible bases. For the purposes of this program, a block type (a,b,c) can be
    three possible bases, determined by the height: (a,b,c), (b,c,a), and (c,a,b)
    """
    blocks = allPossibleTuples(blockTypes)

    # now we want to create a list of key value pairs where keys are bases and values are list of blocks that can be on top of base
    lod = []
    for base in blocks:
        levelAboveBlocks = blocksOnTop(base, blocks)
        lod.append({"base": base, "blocksAbove":levelAboveBlocks})

    return lod


def tripToString(trip):
    return str(trip[0]) + " " + str(trip[1]) + " " + str(trip[2]) + " "


def main():
    """
    Can access program through commandline.
    First argument is the name of the inputfile
    Second argument is the name of the output file
    """
    #infile = open(sys.argv[1], "r")
    #outfile = open(sys.argv[2], "w")

    infile = open("/Users/jackweber/CS2020/CS140/BlockStacking/infile.txt", "r")
    outfile = open("/Users/jackweber/CS2020/CS140/BlockStacking/outfile.txt", "w")

    # stores lines in file in variable as list of strings where each item represents a line
    inLines = infile.read().splitlines()
    inLines.pop(0)  # removes the first line which represents the number of block types.

    """
    Now, each item in inLines is a string. We iterate through inLines to convert each line into a tuple of 3 ints
    representing the dimensions of the block types
    """
    for i in range(0, len(inLines)):
        tl = inLines[i].split()  # create a temporary list (tl) of the dimensions in the line
        inLines[i] = (int(tl[0]), int(tl[1]), int(tl[2]))

    """
    We have a list of tuples where each tuple represents a block type. Let's now figure out all of the possible ways
    to build the first two levels of the stack. The first level is the base. The second level is the base and whatever
    blocks can go ontop of the base. We create a list of dictionaries to represent the first two levels.
    """
    first_two_levels = levelOneTwo(inLines)

    # we now sort the list in increasing order of the number of potential blocks directly above base
    first_two_levels = sorted(first_two_levels, key=lambda i: len(i['blocksAbove']))

    """
    here, we generate a dynamic table where each possible base is stored with the max height it can achieve as well
    as the block that goes directly above it to achieve this optimal height
    """
    dpt = dpTableGenerator(first_two_levels)

    # we use the dynamic table to generate a list representing the optimal stack
    tallestStack = optimalStack(dpt)

    outfile.write(str(len(tallestStack)) + "\n")
    for block in tallestStack:
        outfile.write(tripToString(block) + "\n")


if __name__ == "__main__":
    main()
