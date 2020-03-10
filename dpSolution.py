import sys
import operator

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
    w = base[0]
    l = base[1]
    levelAboveBlocks = []

    for block in allBlocks:
        # check if dimensions of block are smaller than base

        if (block[0] < w and block[1] < l) or (block[0] < l and block[1] < w):
            levelAboveBlocks.append(block)

    return levelAboveBlocks

def maxHeightOfSet(blocks, d):
    heights = []
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
    dOfBases = {}

    for kv in l:
        # if there are no blocks above base, then height of base is it's own height
        if(len(kv['blocksAbove']) == 0):
            dOfBases[kv['base']] = {"blockAbove": (), "height": kv['base'][2]}

        else:
            maxBlockAbove = maxHeightOfSet(kv['blocksAbove'], dOfBases)
            dOfBases[kv['base']] = {"blockAbove": maxBlockAbove[0], "height": kv['base'][2] + maxBlockAbove[1]}


    #maxBase = max(dOfBases.items(), key=operator.itemgetter(1))[0]
    #return {maxBase: dOfBases[maxBase]}
    return dOfBases

def solution(d):
    """
    Takes dynamic table and returns solution in list form
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


def tripToString(trip):
    return str(trip[0]) + " " + str(trip[1]) + " " + str(trip[2]) + " "

def main():
    """
    Can access program through commandline.
    First argument is the name of the inputfile
    Second argument is the name of the output file
    """
    infile = open(sys.argv[1], "r")
    outfile = open(sys.argv[2], "w")

    #infile = open("/Users/jackweber/CS2020/CS140/BlockStacking/infile.txt", "r")
    #outfile = open("/Users/jackweber/CS2020/CS140/BlockStacking/outfile.txt", "w")


    inLines = infile.read().splitlines()
    numBlockTypes = int(inLines.pop(0)) # FIXME: may not need to store this

    for i in range(0, len(inLines)):
        tl = inLines[i].split() # create a temporary list (tl) of the dimensions in the line
        inLines[i] = (int(tl[0]), int(tl[1]), int(tl[2]))

    blocks = allPossibleTuples(inLines)

    # now we want to create a list of key value pairs where keys are bases and values are list of blocks that can be on top of base
    lod = []
    for base in blocks:
        levelAboveBlocks = blocksOnTop(base, blocks)
        lod.append({"base": base, "blocksAbove":levelAboveBlocks})

    # we now sort the list in increasing order of the number of potential blocks directly above base
    lod = sorted(lod, key=lambda i: len(i['blocksAbove']))

    dpt = dpTableGenerator(lod)
    solutionList = solution(dpt)

    outfile.write(str(len(solutionList)) + "\n")
    for block in solutionList:
        outfile.write(tripToString(block) + "\n")


if __name__ == "__main__":
    main()
