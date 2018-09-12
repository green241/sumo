#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    neteditTestFunctions.py
# @author  Pablo Alvarez Lopez
# @date    2016-11-25
# @version $Id$

# Import libraries
from __future__ import print_function
import os
import sys
import subprocess
import autopy
import pyautogui
import time

# define delay before every operation
DELAY_KEY = 0.5 # (0.1)
DELAY_MOUSE = 1
DELAY_QUESTION = 1
DELAY_REFERENCE = 30
DELAY_QUIT = 3
DELAY_UNDOREDO = 1
DELAY_SELECT = 3
DELAY_RECOMPUTE = 4
DELAY_RECOMPUTE_VOLATILE = 5
DELAY_REMOVESELECTION = 5

MoveMouseDelay = 0.2
DelayBeforeDrop = 0.2
DelayAfterDrag = 0.2

NeteditApp = os.environ.get("NETEDIT_BINARY", "netedit")
textTestSandBox = os.environ.get("TEXTTEST_SANDBOX", ".")
referenceImage = os.path.join("imageResources", "reference.png")

#################################################
# interaction functions
#################################################

"""
@brief type escape key
"""


def typeEscape():
    # type ESC key (Sikulix Function)
    autopy.key.tap(autopy.key.Code.ESCAPE, [], DELAY_KEY)


"""
@brief type enter key
"""


def typeEnter():
    # type enter key
    autopy.key.tap(autopy.key.Code.RETURN, [], DELAY_KEY)


"""
@brief type space key
"""


def typeSpace():
    # type space key
    autopy.key.tap(autopy.key.Code.SPACE, [], DELAY_KEY)


"""
@brief type tab key
"""


def typeTab():
    # type tab key (PAGE_DOWN works)
    autopy.key.tap(autopy.key.Code.PAGE_DOWN, [], DELAY_KEY)


"""
@brief type Shift + Tab keys
"""


def typeInvertTab():
    # type invert tab (PAGE_UP works)
    autopy.key.tap(autopy.key.Code.PAGE_UP, [], DELAY_KEY)


"""
@brief type single key
"""


def typeKey(key):
    # type keys
    autopy.key.tap(key, [], DELAY_KEY)


"""
@brief type two keys at the same time (Key2 -> key1)
"""


def typeTwoKeys(key, modifier):
    # type two keys at the same time
    autopy.key.tap(key, modifier, DELAY_KEY)


"""
@brief type three keys at the same time (key2, key3 -> key1)
"""


def typeThreeKeys(key1, key2, key3):
    # wait before every operation
    time.sleep(DELAY_KEY)
    # type three keys at the same time
    autopy.key.toggle(key2, True, [])
    autopy.key.toggle(key3, True, [])
    autopy.key.tap(key1, [])
    autopy.key.toggle(key2, False, [])
    autopy.key.toggle(key3, False, [])


"""
@brief paste value into current text field
"""


def pasteIntoTextField(value, removePreviousContents=True):
    # wait before every operation
    time.sleep(DELAY_KEY)
    # remove previous content
    if(removePreviousContents):
        typeTwoKeys("a", [autopy.key.Modifier.CONTROL])
        time.sleep(0.1)
    # paste string (Sikulix Function)
    autopy.key.type_string(value)


"""
@brief do left click over a position relative to referencePosition (pink square)
"""


def leftClick(referencePosition, positionx, positiony):
    # wait before every operation
    time.sleep(DELAY_MOUSE)
    # obtain clicked position
    clickedPosition = referencePosition.getTarget().offset(positionx, positiony)
    # click respect to offset
    click(clickedPosition)
    print("TestFunctions: Clicked over position", clickedPosition.x, '-', clickedPosition.y)


"""
@brief do left click over a position relative to referencePosition (pink square) while shift key is pressed
"""


def leftClickShift(referencePosition, positionx, positiony):
    # Leave Shift key pressed (Sikulix function)
    keyDown([autopy.key.Modifier.SHIFT])
    # wait before every operation
    time.sleep(DELAY_MOUSE)
    # obtain clicked position
    clickedPosition = referencePosition.getTarget().offset(positionx, positiony)
    # click respect to offset
    click(clickedPosition)
    print("TestFunctions: Clicked with Shift key pressed over position", clickedPosition.x, '-', clickedPosition.y)
    # Release Shift key (Sikulix function)
    keyUp([autopy.key.Modifier.SHIFT])


"""
@brief do left click over a position relative to referencePosition (pink square) while control key is pressed
"""


def leftClickControl(referencePosition, positionx, positiony):
    # Leave Shift key pressed (Sikulix function)
    keyDown([autopy.key.Modifier.CONTROL])
    # wait before every operation
    time.sleep(DELAY_MOUSE)
    # obtain clicked position
    clickedPosition = referencePosition.getTarget().offset(positionx, positiony)
    # click respect to offset
    click(clickedPosition)
    print("TestFunctions: Clicked with Control key pressed over position", clickedPosition.x, '-', clickedPosition.y)
    # Release Shift key (Sikulix function)
    keyUp([autopy.key.Modifier.CONTROL])


"""
@brief drag and drop from position 1 to position 2
"""


def dragDrop(referencePosition, x1, y1, x2, y2):
    # wait before every operation
    time.sleep(DELAY_KEY)
    drag(referencePosition.getTarget().offset(x1, y1))
    time.sleep(DELAY_MOUSE)
    dropAt(referencePosition.getTarget().offset(x2, y2))

#################################################
# basic functions
#################################################


"""
@brief setup Netedit
"""


def setup(NeteditTests):
    # Open current environment file to obtain path to the Netedit App,
    # textTestSandBox
    envFile = os.path.join(NeteditTests, "currentEnvironment.tmp")
    if os.path.exists(envFile):
        global NeteditApp, textTestSandBox, currentOS
        with open(envFile) as env:
            NeteditApp, sandBox = [l.strip() for l in env.readlines()]
        if os.path.exists(sandBox):
            textTestSandBox = sandBox
        os.remove(envFile)
    # get reference for referencePosition
    global referenceImage
    referenceImage = os.path.join(
        NeteditTests, "imageResources", "reference.png")


"""
@brief open Netedit
"""


def Popen(extraParameters, debugInformation):
    # set the default parameters of Netedit
    NeteditCall = [NeteditApp, '--gui-testing', '--window-pos', '50,50',
                   '--window-size', '700,500', '--no-warnings',
                   '--error-log', os.path.join(textTestSandBox, 'log.txt')]

    # check if debug output information has to be enabled
    if debugInformation:
        NeteditCall += ['--gui-testing-debug']

    # check if an existent net must be loaded
    if os.path.exists(os.path.join(textTestSandBox, "input_net.net.xml")):
        NeteditCall += ['--sumo-net-file',
                        os.path.join(textTestSandBox, "input_net.net.xml")]

    # Check if additionals must be loaded
    if os.path.exists(os.path.join(textTestSandBox, "input_additionals.add.xml")):
        NeteditCall += ['--sumo-additionals-file',
                        os.path.join(textTestSandBox, "input_additionals.add.xml")]

    # Check if shapes must be loaded
    if os.path.exists(os.path.join(textTestSandBox, "input_shapes.add.xml")):
        NeteditCall += ['--sumo-shapes-file',
                        os.path.join(textTestSandBox, "input_shapes.add.xml")]

    # check if a gui settings file has to be load
    if os.path.exists(os.path.join(textTestSandBox, "gui-settings.xml")):
        NeteditCall += ['--gui-settings-file',
                        os.path.join(textTestSandBox, "gui-settings.xml")]

    # set output for net
    NeteditCall += ['--output-file',
                    os.path.join(textTestSandBox, 'net.net.xml')]

    # set output for additionals
    NeteditCall += ['--additionals-output',
                    os.path.join(textTestSandBox, "additionals.xml")]

    # set output for shapes
    NeteditCall += ['--shapes-output',
                    os.path.join(textTestSandBox, "shapes.xml")]

    # add extra parameters
    NeteditCall += extraParameters

    # return a subprocess with Netedit
    return subprocess.Popen(NeteditCall, env=os.environ, stdout=sys.stdout, stderr=sys.stderr)


"""
@brief obtain reference referencePosition (pink square)
"""


def getReferenceMatch(neProcess, waitTime):
    # show information
    print("Finding reference...")
    # get image reference
    reference = autopy.bitmap.Bitmap.open('reference.png')
    # 30 second for search  reference
    for x in range(0, waitTime/2):
        # capture screen and search reference
        pos = autopy.bitmap.capture_screen().find_bitmap(reference)
        # check if pos was found
        if pos:
            # break loop
            print("TestFunctions: 'reference.png' found. Position: %s" % str(pos))
            # check that position is consistent (due scaling)
            if (pos[0] != 288 or pos[1] != 124):
                print("TestFunctions: Position of 'reference.png' isn't consistent. Check that interface scaling " +
                      "is 100% (See #3746)")
            return pos
        # wait two second
        time.sleep(2)
    # reference not found, then kill netedit process
    neProcess.kill()
    # print debug information
    sys.exit("TestFunctions: Killed Netedit process. 'reference.png' not found")


"""
@brief setup and start Netedit
"""


def setupAndStart(testRoot, extraParameters=[], debugInformation=True, searchReference=True, waitTime=DELAY_REFERENCE):
    setup(testRoot)
    # Open Netedit
    NeteditProcess = Popen(extraParameters, debugInformation)
    # atexit.register(quit, NeteditProcess, False, False)
    # print debug information
    print("TestFunctions: Netedit opened successfully")
    # Check if reference must be searched
    if(searchReference):
        # Wait for Netedit reference
        return NeteditProcess, getReferenceMatch(NeteditProcess, waitTime)
    else:
        # print debug information
        print("TestFunctions: 'searchReference' option disabled. Reference isn't searched")
        # Wait 1 second for Netedit process
        time.sleep(2)
        # focus netedit windows clicking over it
        click(Region(200, 200, 10, 10))
        return NeteditProcess, None


"""
@brief rebuild network
"""


def rebuildNetwork():
    typeKey(F5)
    # wait for output
    time.sleep(DELAY_RECOMPUTE)


"""
@brief rebuild network with volatile options
"""


def rebuildNetworkWithVolatileOptions(question=True):
    typeTwoKeys(F5, [autopy.key.Modifier.SHIFT])
    # confirm recompute
    if question is True:
        waitQuestion('y')
        # wait for output
        time.sleep(DELAY_RECOMPUTE_VOLATILE)
    else:
        waitQuestion('n')


"""
@brief clean junction
"""


def cleanJunction():
    typeKey(F6)


"""
@brief join selected junctions
"""


def joinSelectedJunctions():
    typeKey(F7)


"""
@brief select focus on upper element of current frame
"""


def focusOnFrame():
    typeKey(F12)


"""
@brief undo last operation
"""


def undo(referencePosition, number):
    # needed to avoid errors with undo/redo (Provisionally)
    typeKey("i")
    # click over referencePosition
    leftClick(referencePosition, 0, 0)
    for x in range(0, number):
        typeTwoKeys("z", [autopy.key.Modifier.CONTROL])
        time.sleep(DELAY_UNDOREDO)


"""
@brief undo last operation
"""


def redo(referencePosition, number):
    # needed to avoid errors with undo/redo (Provisionally)
    typeKey("i")
    # click over referencePosition
    leftClick(referencePosition, 0, 0)
    for x in range(0, number):
        typeTwoKeys("y", [autopy.key.Modifier.CONTROL])
        time.sleep(DELAY_UNDOREDO)


"""
@brief set Zoom
"""


def setZoom(positionX, positionY, zoomLevel):
    # open edit viewport dialog
    typeKey("v")
    # by default is in "load" button, then go to position X
    for x in range(0, 3):
        typeTab()
    # Paste position X
    pasteIntoTextField(positionX)
    # go to Y
    typeTab()
    # Paste Position Y
    pasteIntoTextField(positionY)
    # go to Z
    typeTab()
    # Paste Zoom Z
    pasteIntoTextField(zoomLevel)
    # press OK Button using shortcut
    typeTwoKeys('o', autopy.key.Code.ALT)


"""
@brief wait question of Netedit and select a yes/no answer
"""


def waitQuestion(answer):
    # wait 0.5 second to question dialog
    time.sleep(DELAY_QUESTION)
    # Answer can be "y" or "n"
    typeTwoKeys(answer, autopy.key.Code.ALT)


"""
@brief quit Netedit quit
"""


def quit(NeteditProcess, openNetNonSavedDialog=False, saveNet=False,
         openAdditionalsNonSavedDialog=False, saveAdditionals=False,
         openShapesNonSavedDialog=False, saveShapes=False):
    # check if Netedit is already closed
    if NeteditProcess.poll() is not None:
        # print debug information
        print("[log] TestFunctions: Netedit already closed")
    else:
        # first move cursor out of magenta square
        autopy.mouse.move(150, 200)

        # quit using hotkey
        typeTwoKeys("q", [autopy.key.Modifier.CONTROL])

        # Check if net must be saved
        if openNetNonSavedDialog:
            # Wait some seconds
            time.sleep(DELAY_QUESTION)
            if saveNet:
                waitQuestion("s")
                # wait for log 
                time.sleep(DELAY_RECOMPUTE)
            else:
                waitQuestion("q")

        # Check if additionals must be saved
        if openAdditionalsNonSavedDialog:
            # Wait some seconds
            time.sleep(DELAY_QUESTION)
            if saveAdditionals:
                waitQuestion("s")
            else:
                waitQuestion("q")

        # Check if additionals must be saved
        if openShapesNonSavedDialog:
            # Wait some seconds
            time.sleep(DELAY_QUESTION)
            if saveShapes:
                waitQuestion("s")
            else:
                waitQuestion("q")

        # wait some seconds
        time.sleep(DELAY_QUIT)
        if NeteditProcess.poll() is not None:
            # print debug information
            print("TestFunctions: Netedit closed successfully")
        else:
            NeteditProcess.kill()
            # print debug information
            print("TestFunctions: Error closing Netedit")


"""
@brief load network as
"""


def openNetworkAs(waitTime=2):
    # open save network as dialog
    typeTwoKeys("o", [autopy.key.Modifier.CONTROL])
    # jump to filename TextField
    typeTwoKeys("f", autopy.key.Code.ALT)
    filename = os.path.join(textTestSandBox, "input_net_loadedmanually.net.xml")
    pasteIntoTextField(filename)
    typeEnter()
    # wait for saving
    time.sleep(waitTime)


"""
@brief save network
"""


def saveNetwork():
    # save network using hotkey
    typeTwoKeys("s", [autopy.key.Modifier.CONTROL])
    # wait for debug
    time.sleep(DELAY_RECOMPUTE)


"""
@brief save network as
"""


def saveNetworkAs(waitTime=2):
    # open save network as dialog
    typeTreeKeys("s", [autopy.key.Modifier.CONTROL], [autopy.key.Modifier.SHIFT])
    # jump to filename TextField
    typeTwoKeys("f", autopy.key.Code.ALT)
    filename = os.path.join(textTestSandBox, "net.net.xml")
    pasteIntoTextField(filename)
    typeEnter()
    # wait for saving
    time.sleep(waitTime)
    # wait for debug
    time.sleep(DELAY_RECOMPUTE)


"""
@brief save additionals
"""


def saveAdditionals():
    # save additionals using hotkey
    typeThreeKeys("d", [autopy.key.Modifier.CONTROL], [autopy.key.Modifier.SHIFT])


"""
@brief save shapes
"""


def saveShapes():
    # save additionals using hotkey
    typeThreeKeys("p", [autopy.key.Modifier.CONTROL], [autopy.key.Modifier.SHIFT])


"""
@brief open and close about dialog
"""


def openAboutDialog(waitingTime=DELAY_QUESTION):
    # type F2 to open about dialog
    typeKey(autopy.key.Code.F2)
    # wait before closing
    time.sleep(waitingTime)
    # press enter to close dialog (Ok must be focused)
    typeSpace()


"""
@brief open configuration using shortcut
"""


def openConfigurationShortcut(waitTime=2):
    # open configuration dialog
    typeThreeKeys("o", [autopy.key.Modifier.CONTROL], [autopy.key.Modifier.SHIFT])
    # jump to filename TextField
    typeTwoKeys("f", autopy.key.Code.ALT)
    filename = os.path.join(textTestSandBox, "input_net.netccfg")
    pasteIntoTextField(filename)
    typeEnter()
    # wait for loading
    time.sleep(waitTime)


"""
@brief save configuration using shortcut
"""


def savePlainXML(waitTime=2):
    # open configuration dialog
    typeTwoKeys("l", [autopy.key.Modifier.CONTROL])
    # jump to filename TextField
    typeTwoKeys("f", autopy.key.Code.ALT)
    filename = os.path.join(textTestSandBox, "net")
    pasteIntoTextField(filename)
    typeEnter()
    # wait for loading
    time.sleep(waitTime)

#################################################
# Create nodes and edges
#################################################


"""
@brief Change to create edge mode
"""


def createEdgeMode():
    typeKey("e")


"""
@brief Cancel current created edge (used in chain mode)
"""


def cancelEdge():
    # type ESC to cancel current edge
    typeEscape()


"""
@brief Change chain option
"""


def changeChainOption():
    # cancel current created edge
    cancelEdge()
    # jump to chain
    for x in range(0, 3):
        typeInvertTab()
    # change chain mode
    typeSpace()


"""
@brief Change two-way mode
"""


def changeTwoWayOption():
    # cancel current created edge
    cancelEdge()
    # jump to two way
    for x in range(0, 2):
        typeInvertTab()
    # change two way mode
    typeSpace()

#################################################
# Inspect mode
#################################################


"""
@brief go to inspect mode
"""


def inspectMode():
    typeKey("i")


"""
@brief modify attribute of type int/float/string
"""


def modifyAttribute(attributeNumber, value):
    # focus current frame
    focusOnFrame()
    # jump to attribute
    for x in range(0, attributeNumber + 1):
        typeTab()
    # paste the new value
    pasteIntoTextField(value)
    # type Enter to commit change
    typeEnter()


"""
@brief modify boolean attribute
"""


def modifyBoolAttribute(attributeNumber):
    # focus current frame
    focusOnFrame()
    # jump to attribute
    for x in range(0, attributeNumber + 1):
        typeTab()
    # type SPACE to change value
    typeSpace()

#################################################
# Move mode
#################################################


"""
@brief set move mode
"""


def moveMode():
    typeKey("m")


"""
@brief move element
"""


def moveElement(referencePosition, startX, startY, endX, endY):
    # change mouse move delay
    Settings.MoveMouseDelay = 0.5
    # move element
    dragDrop(referencePosition, startX, startY, endX, endY)
    # set back mouse move delay
    Settings.MoveMouseDelay = 0.2

#################################################
# crossings
#################################################


"""
@brief Change to crossing mode
"""


def crossingMode():
    typeKey("r")


"""
@brief create crossing
"""


def createCrossing():
    # focus current frame
    focusOnFrame()
    # jump to create crossing button
    for x in range(0, 7):
        typeTab()
    # type space to create crossing
    typeSpace()


"""
@brief change default int/real/string crossing default value
"""


def modifyCrossingDefaultValue(numtabs, value):
    # focus current frame
    focusOnFrame()
    # jump to value
    for x in range(0, numtabs + 1):
        typeTab()
    # paste the new value
    pasteIntoTextField(value)
    # type enter to save change
    typeEnter()


"""
@brief change default boolean crossing default value
"""


def modifyCrossingDefaultBoolValue(numtabs):
    # focus current frame
    focusOnFrame()
    # jump to value
    for x in range(0, numtabs + 1):
        typeTab()
    # type space to change value
    typeSpace()


"""
@brief clear crossing
"""


def crossingClearEdges(useSelectedEdges=False, thereIsSelectedEdges=False):
    # focus current frame
    focusOnFrame()
    if(useSelectedEdges and thereIsSelectedEdges):
        # jump to clear button
        for x in range(0, 1):
            typeTab()
    else:
        # jump to clear button
        for x in range(0, 1):
            typeTab()
    # type space to activate button
    typeSpace()


"""
@brief invert crossing
"""


def crossingInvertEdges(useSelectedEdges=False, thereIsSelectedEdges=False):
    # focus current frame
    focusOnFrame()
    if(useSelectedEdges and thereIsSelectedEdges):
        # jump to clear button
        for x in range(0, 1):
            typeTab()
    else:
        # jump to clear button
        for x in range(0, 2):
            typeTab()
    # type space to activate button
    typeSpace()


#################################################
# crossings
#################################################


"""
@brief Change to crossing mode
"""


def connectionMode():
    typeKey("c")

    
"""
@brief show connections (Note: Inspector mode has to be enabled)
"""


def toogleShowConnectionsInspectorMode():
    # focus current frame
    focusOnFrame()
    # go to check box
    typeInvertTab()
    # type space to toogle checkbox
    typeSpace()
    # focus frame again
    typeTab()
    

    
"""
@brief Change to crossing mode
"""


def saveConnectionEdit():
    # focus current frame
    focusOnFrame()
    # go to OK button
    for x in range(0, 3):
        typeTab()
    # type space to press button
    typeSpace()
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief Change to crossing mode
"""


def saveConnectionEdit():
    # focus current frame
    focusOnFrame()
    #go to cancel button
    for x in range(0, 2):
        typeTab()
    # type space to press button
    typeSpace()
    # wait for gl debug
    time.sleep(DELAY_SELECT)
    
    
#################################################
# additionals
#################################################


"""
@brief change to additional mode
"""


def additionalMode():
    typeKey('a')


"""
@brief change additional
"""


def changeAdditional(additional):
    # focus current frame
    focusOnFrame()
    # go to first editable element of frame
    typeTab()
    # paste the new value
    pasteIntoTextField(additional)
    # type enter to save change
    typeEnter()


"""
@brief modify default int/double/string value of an additional
"""


def modifyAdditionalDefaultValue(numTabs, length):
    # focus current frame
    focusOnFrame()
    # go to length TextField
    for x in range(0, numTabs + 1):
        typeTab()
    # paste new length
    pasteIntoTextField(length)
    # type enter to save new length
    typeEnter()


"""
@brief modify default boolean value of an additional
"""


def modifyAdditionalDefaultBoolValue(numTabs):
    # focus current frame
    focusOnFrame()
    # place cursor in check Box position
    for x in range(numTabs + 1):
        typeTab()
    # Change current value
    typeSpace()


"""
@brief modify number of stopping place lines
"""


def modifyStoppingPlaceLines(numTabs, numLines):
    # focus current frame
    focusOnFrame()
    # go to add line
    for x in range(0, numTabs + 1):
        typeTab()
    # add lines using space
    for x in range(0, numLines):
        typeSpace()


"""
@brief fill lines to stopping places
"""


def fillStoppingPlaceLines(numTabs, numLines):
    # focus current frame
    focusOnFrame()
    # place cursor in the first line
    for x in range(0, numTabs + 1):
        typeTab()
    # fill lines
    for x in range(0, numLines):
        # paste line and number
        pasteIntoTextField("Line" + str(x))
        # go to next field
        typeTab()


"""
@brief select child of additional
"""


def selectAdditionalChild(numTabs, childNumber):
    # focus current frame
    focusOnFrame()
    # place cursor in the list of childs
    for x in range(0, numTabs + 1):
        typeTab()
    # select child
    for x in range(0, childNumber):
        typeKey(Key.DOWN)
    typeSpace()
    # use TAB to select additional child
    typeTab()


"""
@brief fix stoppingPlaces
"""


def fixStoppingPlace(solution):
    # select bullet depending of solution
    if (solution == "saveInvalids"):
        for x in range(0, 3):
            typeInvertTab()
        typeSpace()
        # go back and press accept
        for x in range(0, 3):
            typeTab()
        typeSpace()
    elif (solution == "fixPositions"):
        for x in range(0, 2):
            typeInvertTab()
        typeSpace()
        # go back and press accept
        for x in range(0, 2):
            typeTab()
        typeSpace()
    elif (solution == "selectInvalids"):
        typeInvertTab()
        typeSpace()
        # go back and press accept
        typeTab()
        typeSpace()
    elif (solution == "activateFriendlyPos"):
        # default option, then press accept
        typeSpace()
    else:
        # press cancel
        typeTab()
        typeSpace()

#################################################
# delete
#################################################


"""
@brief Change to delete mode
"""


def deleteMode():
    typeKey("d")


"""
@brief delete using SUPR key
"""


def deleteUsingSuprKey():
    typeKey(Key.DELETE)
    # wait for GL Debug
    time.sleep(DELAY_REMOVESELECTION)


"""
@brief Enable or disable 'automatically delete Additionals'
"""


def changeAutomaticallyDeleteAdditionals(referencePosition):
    # select delete mode again to set mode
    deleteMode()
    # use TAB to go to check box
    typeTab()
    # type SPACE to change value
    typeSpace()


"""
@brief close warning about automatically delete additionals
"""


def waitAutomaticallyDeleteAdditionalsWarning():
    # wait 0.5 second to question dialog
    time.sleep(DELAY_QUESTION)
    # press enter to close dialog
    typeEnter()

#################################################
# select mode
#################################################


"""
@brief Change to select mode
"""


def selectMode():
    typeKey("s")


"""
@brief abort current selection
"""


def abortSelection():
    # type ESC to abort current selection
    typeEscape()


"""
@brief toogle select edges
"""


def toogleSelectEdges():
    focusOnFrame()
    # jump to toogle edge
    for x in range(0, 3):
        typeInvertTab()
    typeSpace()
    # Focus on frame again
    focusOnFrame()


"""
@brief toogle show connections (in select mode)
"""


def toogleShowConnections():
    focusOnFrame()
    # jump to toogle edge
    for x in range(0, 2):
        typeInvertTab()
    typeSpace()
    # Focus on frame again
    focusOnFrame()


"""
@brief lock selection by glType
"""


def lockSelection(glType):
    # focus current frame
    focusOnFrame()
    # go to selected glType
    for x in range(0, glType):
        typeTab()
    # type enter to save change
    typeSpace()


"""
@brief select elements with default frame values
"""


def selectDefault():
    # focus current frame
    focusOnFrame()
    for x in range(0, 19):
        typeTab()
    # type enter to select it
    typeEnter()
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief save selection
"""


def saveSelection():
    focusOnFrame()
    # jump to save
    for x in range(0, 24):
        typeTab()
    typeSpace()
    # jump to filename TextField
    typeTwoKeys("f", autopy.key.Code.ALT)
    filename = os.path.join(textTestSandBox, "selection.txt")
    pasteIntoTextField(filename)
    typeEnter()


"""
@brief save selection
"""


def loadSelection():
    focusOnFrame()
    # jump to save
    for x in range(0, 25):
        typeTab()
    typeSpace()
    # jump to filename TextField
    typeTwoKeys("f", autopy.key.Code.ALT)
    filename = os.path.join(textTestSandBox, "selection.txt")
    pasteIntoTextField(filename)
    typeEnter()
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief select items
"""


def selectItems(elementClass, elementType, attribute, value):
    # focus current frame
    focusOnFrame()
    # jump to elementClass
    for x in range(0, 13):
        typeTab()
    # paste the new elementClass
    pasteIntoTextField(elementClass)
    # jump to element
    for x in range(0, 2):
        typeTab()
    # paste the new elementType
    pasteIntoTextField(elementType)
    # jump to attribute
    for x in range(0, 2):
        typeTab()
    # paste the new attribute
    pasteIntoTextField(attribute)
    # jump to value
    for x in range(0, 2):
        typeTab()
    # paste the new value
    pasteIntoTextField(value)
    # type enter to select it
    typeEnter()
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief delete selected items
"""


def deleteSelectedItems():
    typeKey(Key.DELETE)
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief set modification mode "add"
"""


def modificationModeAdd():
    # focus current frame
    focusOnFrame()
    # jump to mode "add"
    for x in range(0, 9):
        typeTab()
    # select it
    typeSpace()


"""
@brief set modification mode "remove"
"""


def modificationModeRemove():
    # focus current frame
    focusOnFrame()
    # jump to mode "remove"
    for x in range(0, 10):
        typeTab()
    # select it
    typeSpace()


"""
@brief set modification mode "keep"
"""


def modificationModeKeep():
    # focus current frame
    focusOnFrame()
    # jump to mode "keep"
    for x in range(0, 11):
        typeTab()
    # select it
    typeSpace()


"""
@brief set modification mode "replace"
"""


def modificationModeReplace():
    # focus current frame
    focusOnFrame()
    # jump to mode "replace"
    for x in range(0, 12):
        typeTab()
    # select it
    typeSpace()


"""
@brief select using an rectangle
"""


def selectionRectangle(referencePosition, startX, startY, endX, endY):
    # Leave Shift key pressed (Sikulix function)
    keyDown([autopy.key.Modifier.SHIFT])
    # change mouse move delay
    Settings.MoveMouseDelay = 0.5
    # move element
    dragDrop(referencePosition, startX, startY, endX, endY)
    # set back mouse move delay
    Settings.MoveMouseDelay = 0.2
    # Release Shift key (Sikulix function)
    keyUp([autopy.key.Modifier.SHIFT])
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief clear selection
"""


def selectionClear(previouslyInserted=False):
    # focus current frame
    focusOnFrame()
    for x in range(0, 22):
        typeTab()
    # type space to select clear option
    typeSpace()
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief invert selection
"""


def selectionInvert():
    # focus current frame
    focusOnFrame()
    for x in range(0, 23):
        typeTab()
    # type space to select invert operation
    typeSpace()
    # wait for gl debug
    time.sleep(DELAY_SELECT)


"""
@brief Toggle select edges and lanes
"""


def selectionToogleEdges():
    # focus current frame
    focusOnFrame()
    # go to check box "select edges"
    for x in range(0, 2):
        typeInvertTab()
    # type space to enable or disable edge selection
    typeSpace()

#################################################
# traffic light
#################################################


"""
@brief Change to traffic light mode
"""


def selectTLSMode():
    typeKey("t")


"""
@brief Create TLS in the current selected Junction
"""


def createTLS():
    # focus current frame
    focusOnFrame()
    # type tab 3 times to jump to create TLS button
    for x in range(0, 3):
        typeTab()
    # create TLS
    typeSpace()

#################################################
# shapes
#################################################


"""
@brief change to shape mode
"""


def shapeMode():
    typeKey('p')


"""
@brief change shape
"""


def changeShape(shape):
    # focus current frame
    focusOnFrame()
    # go to first editable element of frame
    typeTab()
    # paste the new value
    pasteIntoTextField(shape)
    # type enter to save change
    typeEnter()


"""
@brief Create squared Polygon in position with a certain size
"""


def createSquaredPoly(referencePosition, positionx, positiony, size, close):
    # focus current frame
    focusOnFrame()
    # start draw
    typeEnter()
    # create polygon
    leftClick(referencePosition, positionx, positiony)
    leftClick(referencePosition, positionx, positiony - (size / 2))
    leftClick(referencePosition, positionx - (size / 2), positiony - (size / 2))
    leftClick(referencePosition, positionx - (size / 2), positiony)
    # check if polygon has to be closed
    if (close is True):
        leftClick(referencePosition, positionx, positiony)
    # finish draw
    typeEnter()


"""
@brief Create rectangle Polygon in position with a certain size
"""


def createRectangledPoly(referencePosition, positionx, positiony, sizex, sizey, close):
    # focus current frame
    focusOnFrame()
    # start draw
    typeEnter()
    # create polygon
    leftClick(referencePosition, positionx, positiony)
    leftClick(referencePosition, positionx, positiony - (sizey / 2))
    leftClick(referencePosition, positionx - (sizex / 2), positiony - (sizey / 2))
    leftClick(referencePosition, positionx - (sizex / 2), positiony)
    # check if polygon has to be closed
    if (close is True):
        leftClick(referencePosition, positionx, positiony)
    # finish draw
    typeEnter()


"""
@brief Create line Polygon in position with a certain size
"""


def createLinePoly(referencePosition, positionx, positiony, sizex, sizey, close):
    # focus current frame
    focusOnFrame()
    # start draw
    typeEnter()
    # create polygon
    leftClick(referencePosition, positionx, positiony)
    leftClick(referencePosition, positionx - (sizex / 2), positiony - (sizey / 2))
    # check if polygon has to be closed
    if (close is True):
        leftClick(referencePosition, positionx, positiony)
    # finish draw
    typeEnter()


"""
@brief modify default int/double/string value of an shape
"""


def modifyShapeDefaultValue(numTabs, value):
    # focus current frame
    focusOnFrame()
    # go to length TextField
    for x in range(0, numTabs + 1):
        typeTab()
    # paste new value
    pasteIntoTextField(value)
    # type enter to save new value
    typeEnter()


"""
@brief modify default color using dialog
"""


def changeColorUsingDialog(numTabs, color):
    # focus current frame
    focusOnFrame()
    # go to length TextField
    for x in range(0, numTabs + 1):
        typeTab()
    typeSpace()
    # go to list of colors TextField
    for x in range(2):
        typeInvertTab()
    # select color
    for x in range(1 + color):
        typeKey(Key.DOWN)
    # go to accept button and press it
    typeTab()
    typeSpace()


"""
@brief modify default boolean value of an shape
"""


def modifyShapeDefaultBoolValue(numTabs):
    # focus current frame
    focusOnFrame()
    # place cursor in check Box position
    for x in range(numTabs + 1):
        typeTab()
    # Change current value
    typeSpace()
