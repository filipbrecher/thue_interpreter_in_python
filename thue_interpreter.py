
import random

class tc:  # text colors
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    NOTICE = '\033[93m'
    FAIL = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def splitRule(line):
    for pos in range(len(line) - 2):
        if line[pos] == ":" and line[pos + 1] == ":" and line[pos + 2] == "=":
            before = line[:pos]
            after = line[pos + 3:]
            return before, after


def setup(fileDirectory, fileName):
    rules = {}
    state = ""

    # save lines
    t = open(fileDirectory + fileName + ".txt", "r", encoding="utf8")
    lines = []
    for line in t:
        lines.append(line.replace("\n", ""))
    t.close()

    # create rules and initial state
    addToState = False
    for line in lines:
        if addToState:
            state += line
        else:
            if "::=" not in line:  # check if it can be a rule
                continue
            before, after = splitRule(line)
            if before == "":  # if it is a rule that replaces "nothing"
                if after == "":  # check if it is the ::= that ends the rules
                    addToState = True
                    continue
                print(tc.FAIL + "ERROR - cannot make a rule that doesn't replace anything")
                print("line =>" + line + "<=" + tc.END)
                quit()
            if before not in rules:  # add to rules
                rules[before] = []
            rules[before].append(after)

    return rules, state


def getStepsInput(stepLimit, totalSteps):
    print("Steps left to termination: " + tc.CYAN + str(stepLimit - totalSteps) + tc.END)
    raiseStepLimit = False
    steps = input("Steps to do: ")
    if len(steps) > 0:
        if steps[0] == "+":
            raiseStepLimit = True
            steps = steps[1:]
    inputIsValid = steps.isdigit()
    while not inputIsValid:
        raiseStepLimit = False
        steps = input("Steps to do" + tc.NOTICE + "(INPUT FAILED - ENTER A DIGIT)" + tc.END + ": ")
        if len(steps) > 0:
            if steps[0] == "+":
                raiseStepLimit = True
                steps = steps[1:]
        inputIsValid = steps.isdigit()
    if raiseStepLimit:
        return True, int(steps)
    else:
        return False, int(steps)


def printStateAndOutput(type, state, output):
    print(type + " state:\n" + tc.GRAY + state + tc.END)
    print(type + " output:\n" + tc.MAGENTA + tc.UNDERLINE + output + tc.END)


def getApplicableRule(ruleList, state):
    random.shuffle(ruleList)
    applicableRule = ""
    for rule in ruleList:
        if rule in state:
            applicableRule = rule
            break
    return applicableRule


def getApplicablePositions(applicableRule, ruleLength, state):
    positions = []
    for pos in range(len(state) - ruleLength + 1):
        if state[pos: pos+ruleLength] == applicableRule:
            positions.append(pos)
    return positions


def applyRule(rules, ruleList, state, output, printProgress, printOnNewOutput):

    # get the first random rule that can be applied
    applicableRule = getApplicableRule(ruleList, state)
    if applicableRule == "":
        return True, state, output
    ruleLength = len(applicableRule)
    endState = random.choice(rules[applicableRule])

    # get all positions where it can be applied
    positions = getApplicablePositions(applicableRule, ruleLength, state)
    position = random.choice(positions)

    stateFormer = state[:position]
    stateLatter = state[position + ruleLength:]

    if printProgress or endState == ":::":  # print state before
        print()
        print(tc.GRAY + stateFormer + tc.BLUE + tc.UNDERLINE + applicableRule + tc.END + tc.GRAY + stateLatter + tc.END)

    if len(endState) > 0:
        if endState[0] == "~":  # is it a printout?
            output += endState[1:]
            if printOnNewOutput:
                if not printProgress:
                    print()
                print("new output:\n" + tc.MAGENTA + output + tc.END)
            endState = ""
        elif endState == ":::":  # takes input?
            endState = input(tc.NOTICE + "Type input: " + tc.END)

    state = stateFormer + endState + stateLatter

    if printProgress:  # print state after
        print(tc.GRAY + stateFormer + tc.GREEN + tc.UNDERLINE + endState + tc.END + tc.GRAY + stateLatter + tc.END)

    return False, state, output


def run(rules, state, printProgress, goBySteps, stepLimit, printOnNewOutput):

    ruleList = [rule for rule in rules]
    totalSteps = 0
    stepsToDo = 0
    output = ""
    doTerminate = False
    while not doTerminate:
        if goBySteps:
            print(tc.WHITE + "---------------" + tc.END)
            printStateAndOutput("current", state, output)

            askMore = True
            while askMore:
                askMore, stepsToDo = getStepsInput(stepLimit, totalSteps)
                if askMore:
                    stepLimit += stepsToDo

            print(tc.WHITE + "================" + tc.END)
        else:
            stepsToDo = 1

        while stepsToDo > 0 and totalSteps <= stepLimit:
            doTerminate, state, output = applyRule(rules, ruleList, state, output, printProgress, printOnNewOutput)

            if doTerminate:  # terminate before adding because we didn't apply any rule
                break
            totalSteps += 1
            stepsToDo -= 1

        if totalSteps > stepLimit and not doTerminate:
            print()
            print(tc.FAIL + "PROGRAM TERMINATED - STEP LIMIT REACHED: " + tc.CYAN + str(stepLimit) + tc.END)
            printStateAndOutput("reached", state, output)
            quit()

    print()
    print(tc.NOTICE + "Program finished" + tc.END)
    print("total steps: " + tc.CYAN + str(totalSteps) + tc.END)
    printStateAndOutput("reached", state, output)


def main():

    fileName = "fileName"  # only reads .txt files - input takes the file name without the .txt suffix
    fileDirectory = "filePath/"  # here write the path to your .txt file
    printProgress = True  # print the state with highlighted string to change and then the state with the change highlighted
    printOnNewOutput = True  # when something gets added to the output, print the output
    goBySteps = True  # if True, you need to input an integer and that many steps will be run, otherwise it will run until rules are exhausted
        # if you want to EXTEND THE STEP LIMIT, type in +n and the stepLimit will be raise by n
    printInitialStateAndRules = False
    stepLimit = 100000  # if the program makes too many steps it terminates automatically

    # TO ADD - more ways the next rule to be applied can be chosen
    # TO ADD - ask if step limit reached and goBySteps is False, if we want to raise the step limit
    # TO ADD - the possibility to check if there is a rule (before) that is a subset of another rule (before) -> it could have random chance which one gets picked

    rules, state = setup(fileDirectory, fileName)  # setup the program
    run(rules, state, printProgress, goBySteps, stepLimit, printOnNewOutput)  # run the program

    if printInitialStateAndRules:
        print()
        print("initial state:\n" + state)
        print("rules list:\n", rules)

    quit()

main()
