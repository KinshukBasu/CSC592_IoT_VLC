def generateChecksum(datachunk):
    dat = int(datachunk,2)
    return 137^dat
