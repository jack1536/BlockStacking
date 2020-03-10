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


def maxHeight(l):
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

def main():
    """
    Can access program through commandline.
    First argument is the name of the inputfile
    Second argument is the name of the output file
    """
    #infile = open(sys.argv[1], "r")
    #outfile = open(sys.argv[2], "w")

    infile = open("/Users/jackweber/CS2020/CS140/BlockStacking/infile.txt", "r")
    print(infile)

    inLines = infile.read().splitlines()
    numBlockTypes = int(inLines.pop(0))

    for i in range(0, len(inLines)):
        tl = inLines[i].split() # create a temporary list (tl) of the dimensions in the line
        inLines[i] = (int(tl[0]), int(tl[1]), int(tl[2]))

    blocks = allPossibleTuples(inLines)

    #print(blocksOnTop((4, 4, 4),[(1, 10, 4)]))


    # now we want to create a list of key value pairs where keys are bases and values are list of blocks that can be on top of base
    lod = []
    for base in blocks:
        levelAboveBlocks = blocksOnTop(base, blocks)
        lod.append({"base": base, "blocksAbove":levelAboveBlocks})

    # we now sort the list in increasing order of the number of potential blocks directly above base
    lod = sorted(lod, key=lambda i: len(i['blocksAbove']))
    for kv in lod:
        print(kv)

    print(maxHeight(lod))

    #sortedKeyList = sorted(d.keys(), key=)


    """
    # writes length of longest non-decreasing subsequence
    outfile.write(str(1+tup[1]-tup[0]) + "\n")

    # writes day on which subsequence begins
    outfile.write(str(1+tup[0]) + "\n")

    # writes lines giving the price of the stock on days in subsequence
    for i in range(tup[0],tup[1]+1):
        outfile.write(arr[i] + "\n")
    """

if __name__ == "__main__":
    main()
