/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2006-2021 German Aerospace Center (DLR) and others.
// This program and the accompanying materials are made available under the
// terms of the Eclipse Public License 2.0 which is available at
// https://www.eclipse.org/legal/epl-2.0/
// This Source Code may also be made available under the following Secondary
// Licenses when the conditions for such availability set forth in the Eclipse
// Public License 2.0 are satisfied: GNU General Public License, version 2
// or later which is available at
// https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
// SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
/****************************************************************************/
/// @file    FXUndoList2.h
/// @author  Pablo Alvarez Lopez
/// @date    Sep 2021
///
//
/****************************************************************************/
#pragma once
#include <config.h>

#include <utils/foxtools/fxheader.h>


/**
 * Base class for undoable commands.  Each undo records all the
 * information necessary to undo as well as redo a given operation.
 * Since commands are derived from FXObject, subclassed commands can
 * both send and receive messages (like ID_GETINTVALUE, for example).
 */
class FXCommand2 : public FXObject {
    FXDECLARE_ABSTRACT(FXCommand2)

public:
    // @name declare friend class
    friend class FXUndoList2;
    friend class FXCommandGroup2;

    /**
     * Undo this command; this should save the
     * information for a subsequent redo.
     */
    virtual void undo() = 0;

    /**
     * Redo this command; this should save the
     * information for a subsequent undo.
     */
    virtual void redo() = 0;

    /**
     * Return the size of the information in the undo record.
     * The undo list may be trimmed to limit memory usage to
     * a certain limit.  The value returned should include
     * the size of the command record itself as well as any
     * data linked from it.
     */
    virtual FXuint size() const;

    /**
     * Name of the undo command to be shown on a button;
     * for example, "Undo Delete".
     */
    virtual FXString undoName() const;

    /**
     * Name of the redo command to be shown on a button;
     * for example, "Redo Delete".
     */
    virtual FXString redoName() const;

    /**
     * Return TRUE if this command can be merged with previous undo
     * commands.  This is useful to combine e.g. multiple consecutive
     * single-character text changes into a single block change.
     * The default implementation returns FALSE.
     */
    virtual bool canMerge() const;

    /**
     * Called by the undo system to try and merge the new incoming command
     * with this command; should return TRUE if merging was possible.
     * The default implementation returns FALSE.
     */
    virtual bool mergeWith(FXCommand2* command);

    /// Delete undo command
    virtual ~FXCommand2(){}

protected:
    /// @brief FOX need this
    FXCommand2();

private:
    // @brief next command
    FXCommand2 *next;

    /// @brief invalidate assignment operator
    FXCommand2(const FXCommand2&);
    
    /// @brief invalidate assignment operator
    FXCommand2 &operator=(const FXCommand2&) = delete;
};


/**
* Group of undoable commands.  A group may comprise multiple
* individual actions which together undo (or redo) a larger
* operation.  Even larger operations may be built by nesting
* multiple undo groups.
*/
class FXCommandGroup2 : public FXCommand2 {
    FXDECLARE(FXCommandGroup2)

public:
    // @name declare friend class
    friend class FXUndoList2;

    /// Construct initially empty undo command group
    FXCommandGroup2(const std::string &description);

    /// @brief get description
    const std::string& getDescription();

    /// @brief get undo Name
    FXString undoName() const;

    /// @brief get redo name
    FXString redoName() const;

    /// Return TRUE if empty
    bool empty();

    /// Undo whole command group
    virtual void undo();

    /// Redo whole command group
    virtual void redo();

    /// Return the size of the command group
    virtual FXuint size() const;

    /// Delete undo command and sub-commands
    virtual ~FXCommandGroup2();

protected:
    /// @brief FOX need this
    FXCommandGroup2();

private:
    /// @brief undo list command
    FXCommand2* undoList;

    /// @brief redo list command
    FXCommand2* redoList;

    /// @brief group
    FXCommandGroup2* group;        
    
    /// @brief description of command
    const std::string myDescription;

    /// @brief invalidate copy constructor
    FXCommandGroup2(const FXCommandGroup2&);
    
    /// @brief invalidate assignment operator
    FXCommandGroup2 &operator=(const FXCommandGroup2&) = delete;
};


/// @brief The Undo List class manages a list of undoable commands.
class FXUndoList2 : public FXCommandGroup2 {
    FXDECLARE(FXUndoList2)

public:
    enum{
        ID_CLEAR=FXWindow::ID_LAST,
        ID_REVERT,
        ID_UNDO,
        ID_REDO,
        ID_UNDO_ALL,
        ID_REDO_ALL,
        ID_UNDO_COUNT,
        ID_REDO_COUNT,
        ID_LAST
    };

    /// Make new empty undo list, initially unmarked.
    FXUndoList2();

    /**
     * Cut the redo list.
     * This is automatically invoked when a new undo command is added.
     */
    void cut();

    /**
     * Add new command, executing it if desired. The new command will be merged
     * with the previous command if merge is TRUE and we're not at a marked position
     * and the commands are mergeable.  Otherwise the new command will be appended
     * after the last undo command in the currently active undo group.
     * If the new command is successfully merged, it will be deleted.  Furthermore,
     * all redo commands will be deleted since it is no longer possible to redo
     * from this point.
     */
    void add(FXCommand2* command,bool doit=false,bool merge=true);

    /**
     * Begin undo command sub-group. This begins a new group of commands that
     * are treated as a single command.  Must eventually be followed by a
     * matching end() after recording the sub-commands.  The new sub-group
     * will be appended to its parent group's undo list when end() is called.
     */
    void begin(FXCommandGroup2 *command);

    /**
     * End undo command sub-group.  If the sub-group is still empty, it will
     * be deleted; otherwise, the sub-group will be added as a new command
     * into parent group.
     * A matching begin() must have been called previously.
     */
    void end();

    /**
     * Abort the current command sub-group being compiled.  All commands
     * already added to the sub-groups undo list will be discarded.
     * Intermediate command groups will be left intact.
     */
    void abort();

    /// Undo last command. This will move the command to the redo list.
    virtual void undo();

    /// Redo next command. This will move the command back to the undo list.
    virtual void redo();

    /// Undo all commands
    void undoAll();

    /// Redo all commands
    void redoAll();

    /// Can we undo more commands
    bool canUndo() const;

    /// Can we redo more commands
    bool canRedo() const;

    /**
     * Return TRUE if currently inside undo or redo operation; this
     * is useful to avoid generating another undo command while inside
     * an undo operation.
     */
    bool busy() const;

    /// Current top level undo command
    FXCommand2* current() const;

    /**
     * Return name of the first undo command available; if no
     * undo command available this will return the empty string.
     */
    virtual FXString undoName() const;

    /**
     * Return name of the first redo command available; if no
     * Redo command available this will return the empty string.
     */
    virtual FXString redoName() const;

    /**
     * Clear list, and unmark all states.
     * All undo and redo information will be destroyed.
     */
    void clear();

    long onCmdUndo(FXObject*,FXSelector,void*);
    long onUpdUndo(FXObject*,FXSelector,void*);
    long onCmdRedo(FXObject*,FXSelector,void*);
    long onUpdRedo(FXObject*,FXSelector,void*);
    long onCmdClear(FXObject*,FXSelector,void*);
    long onUpdClear(FXObject*,FXSelector,void*);
    long onCmdUndoAll(FXObject*,FXSelector,void*);
    long onCmdRedoAll(FXObject*,FXSelector,void*);

private:
    /// @brief  Currently busy with undo or redo
    bool myWorking;       

    /// @brief invalidate copy constructor
    FXUndoList2(const FXUndoList2&);

    /// @brief invalidate assignment operator
    FXUndoList2 &operator=(const FXUndoList2&) = delete;
};
