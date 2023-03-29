termdays = []
import itertools

from datetime import datetime, date

def isTermLine(sLine):
    sLine = sLine.strip().strip("/n")
    bTerm = " until " in sLine
    #print("sLine", sLine, "bTerm", bTerm)
    return bTerm 


assert isTermLine("\n") == False
assert isTermLine("School term dates 2022-23\n") == False
assert isTermLine("   Thursday 1 September 2022 until Friday 21 October 2022\n") == True
assert isTermLine("   24 to 28 October 2022\n") == False
assert isTermLine("School calendar 2022-23 (PDF, 136.7KB)\n") == False
assert isTermLine("    Monday 4 September 2023 until Friday 20 October 2023\n") == True
assert isTermLine("    1 April 2024 (Easter Monday)\n") == False
assert isTermLine("    Monday 4 November until Friday 20 December 2024\n") == True

def getTermBoundaries(sLine):
    sLine = sLine.strip().strip("/n")
    aParts = sLine.split(" until ")
    sStart = aParts[0]
    sEnd   = aParts[1]
    dEnd   = datetime.strptime(sEnd,   "%A %d %B %Y").date()
    
    try :
        dStart = datetime.strptime(sStart, "%A %d %B %Y").date()
    except :
        sStart = sStart + " "+ str(dEnd.year)
        dStart = datetime.strptime(sStart, "%A %d %B %Y").date()
    
    return dStart, dEnd
    
assert getTermBoundaries("    Monday 4 November until Tuesday 5 November 2024\n") == (date.fromisoformat('2024-11-04'), date.fromisoformat('2024-11-05'))

def getTermDates(sLine):
    dStart, dEnd = getTermBoundaries(sLine)
    aDates = []#dStart, dEnd]
    iStart = dStart.toordinal()
    iEnd   = dEnd.toordinal()
    for iDate in range(iStart, iEnd+1):
        dDate = date.fromordinal(iDate)
        #print("dDate", dDate, dDate.weekday())
        if dDate.weekday() < 5:
            aDates.append(dDate)
    #print(aDates)
    return aDates

assert getTermDates("    Monday 4 November until Tuesday 5 November 2024\n") == [date.fromisoformat('2024-11-04'), date.fromisoformat('2024-11-05')]
assert getTermDates("    Monday 4 November until Wednesday 6 November 2024\n") == [
    date.fromisoformat('2024-11-04'),
    date.fromisoformat('2024-11-05'),
    date.fromisoformat('2024-11-06')]
assert len(getTermDates("    Friday 1 November until Monday 4 November 2024\n")) == 2

def getTermDatesFromFile(filename):
    with open(filename) as f:
        termlines = list(filter(isTermLine, f.readlines()))
        terms = map(getTermDates, termlines)
        termdates = list(itertools.chain(*terms))
        return termdates
    
print(getTermDatesFromFile("term_dates.txt"))

class weekCalc():
    def __init__(self) -> None:
        pass