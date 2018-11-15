#! encoding = utf-8

'''
Visualize the number of literatures on various dimers
'''

DB = 'dimer_lit.db'
DEFAULT_LIT_TYPES = ['Microwave', '(sub)mm', 'IR', 'Theory']

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
import mylib


class MainWindow(QtWidgets.QMainWindow):
    '''
        Implements the main window
    '''
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setStyleSheet('font-size: 10pt; font-family: default')

        # Set global window properties
        self.setWindowTitle('Dimer Visualizer')
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)
        self.resize(QtCore.QSize(1600, 900))

        # Connet to database
        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()

        # Set menu bar actions
        entryAction = QtWidgets.QAction('Edit Entry', self)
        entryAction.setShortcuts(['Ctrl+E'])
        entryAction.setStatusTip('Edit literature entry')
        entryAction.triggered.connect(self._show_entryPanel)

        visAction = QtWidgets.QAction('Visualization', self)
        visAction.setStatusTip('Visulize literature counts')
        visAction.triggered.connect(self._show_visPanel)

        # Set menu bar
        self.statusBar()

        menuEntry = self.menuBar().addMenu('&Entry')
        menuEntry.addAction(entryAction)
        menuVis = self.menuBar().addMenu('&Visulization')
        menuVis.addAction(visAction)

        # Set window layout
        self.entryPanel = EntryPanel(self)
        self.visPanel = VisPanel(self)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.entryPanel)
        self.mainLayout.addWidget(self.visPanel)
        self.entryPanel.show()
        self.visPanel.hide()

        # Enable main window
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def _show_entryPanel(self):

        self.visPanel.hide()
        self.entryPanel.show()

    def _show_visPanel(self):

        self.entryPanel.hide()
        self.visPanel.show()

    def closeEvent(self, event):
        q = QtWidgets.QMessageBox.question(self, 'Quit?',
                       'Are you sure to quit?', QtWidgets.QMessageBox.Yes |
                       QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if q == QtWidgets.QMessageBox.Yes:
            self.conn.close()
            self.close()
        else:
            event.ignore()


class EntryPanel(QtWidgets.QWidget):
    ''' Entry edit panel '''

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent

        self.newEntry = NewEntry(self.parent)
        self.searchEntry = SearchEntry(self, self.parent)
        self.editEntry = EditEntry(self, self.parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.newEntry)
        self.mainLayout.addWidget(self.searchEntry)
        self.mainLayout.addWidget(self.editEntry)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.mainLayout)

    def pass_search_result(self, result):
        ''' pass the search result from searchEntry to editEntry '''

        self.editEntry.clear()
        self.editEntry.display(result)


class NewEntry(QtWidgets.QGroupBox):
    ''' Add a new database entry '''

    def __init__(self, main):
        QtWidgets.QWidget.__init__(self, main)
        self.main = main

        self.setTitle('Add new entries to the database')
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setCheckable(False)

        self.mol1Input = QtWidgets.QLineEdit()
        self.mol2Input = QtWidgets.QLineEdit()
        self.chooseLitType = QtWidgets.QComboBox()
        self.yearInput = QtWidgets.QLineEdit()
        self.bibkeyInput = QtWidgets.QLineEdit()
        self.noteInput = QtWidgets.QLineEdit()
        self.addBtn = QtWidgets.QPushButton('Add')
        self.chooseLitType.addItems(DEFAULT_LIT_TYPES)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.addWidget(QtWidgets.QLabel('Monomer 1'), 0, 0, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Monomer 2'), 0, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Lit type'), 0, 2, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Year'), 0, 3, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Bibkey'), 0, 4, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Brief Note'), 0, 5, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.mol1Input, 1, 0)
        self.mainLayout.addWidget(self.mol2Input, 1, 1)
        self.mainLayout.addWidget(self.chooseLitType, 1, 2)
        self.mainLayout.addWidget(self.yearInput, 1, 3)
        self.mainLayout.addWidget(self.bibkeyInput, 1, 4)
        self.mainLayout.addWidget(self.noteInput, 1, 5)
        self.mainLayout.addWidget(self.addBtn, 1, 6)

        self.setLayout(self.mainLayout)

        self.addBtn.clicked.connect(self._insert_entry)

    def _insert_entry(self):
        ''' insert new entry into the database '''

        entry = self._get_input()

        if entry:
            # write entry into database
            self.main.cursor.execute("INSERT INTO lit (mol1, mol2, lit_type, year, bibkey, note) VALUES (?,?,?,?,?,?)", entry)
            self.main.conn.commit()
        else:
            pass

    def _get_input(self):
        ''' retrieve input. Return:
        (mol1, mol2, lit_type, year, bibkey, note) if valid
        False if not valid
        '''

        mol1 = self.mol1Input.text()
        mol2 = self.mol2Input.text()
        lit_type = self.chooseLitType.currentText()
        year = self.yearInput.text()
        bibkey = self.bibkeyInput.text()
        note = self.noteInput.text()

        valid = True

        if mol1:
            self.mol1Input.setStyleSheet('color: black')
        else:
            self.mol1Input.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        if mol2:
            self.mol2Input.setStyleSheet('color: black')
        else:
            self.mol2Input.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        try:
            int(year)
            self.yearInput.setStyleSheet('color: black')
        except ValueError:
            self.yearInput.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        if bibkey:
            self.bibkeyInput.setStyleSheet('color: black')
        else:
            self.bibkeyInput.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        if valid:
            if self._check_duplicates(mol1, mol2, year, bibkey):
                msg = MsgWarning(self, 'Duplicates!', 'A duplicated copy of this input already exists in the database. Please change your input.')
                msg.exec_()
                return False
            else:
                return (mol1, mol2, lit_type, year, bibkey, note)
        else:
            return False

    def _check_duplicates(self, mol1, mol2, year, bibkey):
        ''' check whether the input entry is duplicated '''

        r = self.main.cursor.execute("SELECT bibkey FROM lit WHERE mol1 = (?) AND mol2 = (?) AND year = (?) AND bibkey = (?)", (mol1, mol2, year, bibkey))

        return bool(r.fetchall())


class SearchEntry(QtWidgets.QGroupBox):
    ''' Search existing entry & edit it '''

    def __init__(self, parent, main):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.main = main

        self.setTitle('Search database')
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setCheckable(False)

        self.searchBtn = QtWidgets.QPushButton('Search')
        self.sortOption = QtWidgets.QComboBox()
        self.sortOption.addItems(['Mol', 'Year', 'Lit Type'])
        self.mol1Search = QtWidgets.QLineEdit()
        self.mol2Search = QtWidgets.QLineEdit()
        self.yearStart = QtWidgets.QLineEdit()
        self.yearEnd = QtWidgets.QLineEdit()
        self.chooseLitType = QtWidgets.QWidget()
        self.chooseLitOptions = []

        chooseLitLayout = QtWidgets.QHBoxLayout()
        for item in DEFAULT_LIT_TYPES:
            self.chooseLitOptions.append(QtWidgets.QCheckBox())
            chooseLitLayout.addWidget(self.chooseLitOptions[-1])
            chooseLitLayout.addWidget(QtWidgets.QLabel(item + '  '))
        self.chooseLitType.setLayout(chooseLitLayout)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.addWidget(QtWidgets.QLabel('Monomer 1'), 0, 0, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Monomer 2'), 0, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Year'), 0, 2, 1, 3, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Lit Type'), 0, 5, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.mol1Search, 1, 0)
        self.mainLayout.addWidget(self.mol2Search, 1, 1)
        self.mainLayout.addWidget(self.yearStart, 1, 2)
        self.mainLayout.addWidget(QtWidgets.QLabel('to'), 1, 3)
        self.mainLayout.addWidget(self.yearEnd, 1, 4)
        self.mainLayout.addWidget(self.chooseLitType, 1, 5)
        self.mainLayout.addWidget(self.searchBtn, 1, 6)

        self.setLayout(self.mainLayout)

        self.searchBtn.clicked.connect(self._search_entry)

    def _search_entry(self):
        ''' search entry & return results to self.parent Panel '''

        search_opts = self._get_search_option()
        if not search_opts:  # if input value error, do nothing
            pass
        else:
            sql_str, sql_arg = mylib.gen_search_sql_str(search_opts)
            if sql_arg:
                if isinstance(sql_arg, list):
                    r = self.main.cursor.execute(sql_str, sql_arg)
                else:
                    r = self.main.cursor.execute(sql_str, [sql_arg])
            else:
                r = self.main.cursor.execute(sql_str)

            self.parent.pass_search_result(r.fetchall())


    def _get_search_option(self):
        ''' retrieve search option '''

        mol1 = self.mol1Search.text()
        mol2 = self.mol2Search.text()
        yr_start_text = self.yearStart.text()
        yr_end_text = self.yearEnd.text()
        checked_lit_types = []
        for i in range(len(DEFAULT_LIT_TYPES)):
            if self.chooseLitOptions[i].isChecked():
                checked_lit_types.append(DEFAULT_LIT_TYPES[i])
            else:
                pass
        try:
            yr_start = int(yr_start_text)
            self.yearStart.setStyleSheet('color: black')
        except ValueError:
            self.yearStart.setStyleSheet('border: 1px solid #FF9933')
            yr_start = None
        try:
            yr_end = int(yr_end_text)
            self.yearEnd.setStyleSheet('color: black')
        except ValueError:
            self.yearEnd.setStyleSheet('border: 1px solid #FF9933')
            yr_end = None

        if yr_start and yr_end and yr_start > yr_end:   # swap number
            yr_start, yr_end = yr_end, yr_start
        else:
            pass

        return (mol1, mol2, yr_start, yr_end, checked_lit_types)


class EditEntry(QtWidgets.QGroupBox):
    ''' Display search result & enable edits to the entries '''

    def __init__(self, parent, main):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.main = main

        self.setTitle('Search results')
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setCheckable(False)

        self.entryList = []

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.addWidget(QtWidgets.QLabel('Monomer 1'), 0, 0, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Monomer 2'), 0, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Lit type'), 0, 2, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Year'), 0, 3, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Bibkey'), 0, 4, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(QtWidgets.QLabel('Brief Note'), 0, 5, QtCore.Qt.AlignHCenter)

        # make the trick to put in a scroll bar
        mainWidget = QtWidgets.QWidget()
        mainArea = QtWidgets.QScrollArea()
        mainArea.setWidgetResizable(True)
        mainArea.setWidget(mainWidget)
        mainWidget.setLayout(self.mainLayout)

        widgetLayout = QtWidgets.QVBoxLayout()
        widgetLayout.addWidget(mainWidget)
        self.setLayout(widgetLayout)

    def display(self, result):
        ''' display result. Arguments
        result -- [(pid, mol1, mol2, lit_type, year, bibkey, note), ...]
        '''

        # create EntryRow objects
        for item in result:
            row = result.index(item)
            entryRow = EditEntryRow(self.main, item[1:], item[0])
            self.entryList.append(entryRow)
            self.mainLayout.addWidget(entryRow.mol1Input, row+1, 0)
            self.mainLayout.addWidget(entryRow.mol2Input, row+1, 1)
            self.mainLayout.addWidget(entryRow.chooseLitType, row+1, 2)
            self.mainLayout.addWidget(entryRow.yearInput, row+1, 3)
            self.mainLayout.addWidget(entryRow.bibkeyInput, row+1, 4)
            self.mainLayout.addWidget(entryRow.noteInput, row+1, 5)
            self.mainLayout.addWidget(entryRow.editBtn, row+1, 6)

    def clear(self):
        ''' clear elements and remove from the layout '''

        while self.entryList:
            entryRow = self.entryList.pop()
            entryRow.mol1Input.deleteLater()
            entryRow.mol2Input.deleteLater()
            entryRow.chooseLitType.deleteLater()
            entryRow.yearInput.deleteLater()
            entryRow.bibkeyInput.deleteLater()
            entryRow.noteInput.deleteLater()
            entryRow.editBtn.deleteLater()


class EditEntryRow(QtWidgets.QWidget):
    ''' A row of entry record to edit.
        entry = (mol1, mol2, lit_type, year, bibkey, note)
    '''

    def __init__(self, main, entry, pid):
        QtWidgets.QWidget.__init__(self, main)
        self.main = main
        self.pid = pid      # entry pid in the database

        self.editBtn = QtWidgets.QPushButton('Edit')
        self.mol1Input = QtWidgets.QLineEdit()
        self.mol2Input = QtWidgets.QLineEdit()
        self.chooseLitType = QtWidgets.QComboBox()
        self.yearInput = QtWidgets.QLineEdit()
        self.bibkeyInput = QtWidgets.QLineEdit()
        self.noteInput = QtWidgets.QLineEdit()

        # by default disable edit of the entry
        self._set_read_only(entry)

        self.editBtn.clicked.connect(self._edit_entry)

    def _set_read_only(self, entry):
        ''' set default values & read only '''

        (mol1, mol2, lit_type, year, bibkey, note) = entry

        # clear lit_type QComboBox items
        self.chooseLitType.clear()

        # set values
        self.mol1Input.setText(mol1)
        self.mol2Input.setText(mol2)
        self.chooseLitType.addItems([lit_type])
        self.chooseLitType.setCurrentText(lit_type)
        self.yearInput.setText(str(year))
        self.bibkeyInput.setText(bibkey)
        self.noteInput.setText(note)

        # set text color
        self.mol1Input.setStyleSheet('background-color: #EEEEEE')
        self.mol2Input.setStyleSheet('background-color: #EEEEEE')
        self.yearInput.setStyleSheet('background-color: #EEEEEE')
        self.bibkeyInput.setStyleSheet('background-color: #EEEEEE')
        self.noteInput.setStyleSheet('background-color: #EEEEEE')

        # set read only
        self.mol1Input.setReadOnly(True)
        self.mol2Input.setReadOnly(True)
        self.yearInput.setReadOnly(True)
        self.bibkeyInput.setReadOnly(True)
        self.noteInput.setReadOnly(True)

    def _set_editable(self):
        ''' set entry editable '''

        # set lit_type Combobox
        _this_lit_type = self.chooseLitType.currentText()
        # clear lit_type QComboBox items
        self.chooseLitType.clear()
        self.chooseLitType.addItems(DEFAULT_LIT_TYPES)
        self.chooseLitType.setCurrentText(_this_lit_type)

        # set color
        self.mol1Input.setStyleSheet('color: black')
        self.mol2Input.setStyleSheet('color: black')
        self.yearInput.setStyleSheet('color: black')
        self.bibkeyInput.setStyleSheet('color: black')
        self.noteInput.setStyleSheet('color: black')

        # set editable
        self.mol1Input.setReadOnly(False)
        self.mol2Input.setReadOnly(False)
        self.yearInput.setReadOnly(False)
        self.bibkeyInput.setReadOnly(False)
        self.noteInput.setReadOnly(False)

    def _edit_entry(self):
        ''' enable edit to the entry '''

        # check the button status
        if self.editBtn.text() == 'Edit':
            self._set_editable()
            self.editBtn.setText('Update')
        else:
            entry = self._get_input()
            if entry:   # if input is valid
                # unpack entry
                entry_and_pid = list(entry)
                entry_and_pid.append(self.pid)
                # update database
                self.main.cursor.execute("UPDATE lit SET mol1 = (?), mol2 = (?), lit_type = (?), year = (?), bibkey = (?), note = (?) WHERE id = (?)", entry_and_pid)
                self.main.conn.commit()
                self._set_read_only(entry)
                self.editBtn.setText('Edit')
            else:
                pass


    def _get_input(self):
        ''' retrieve input. Return:
        (mol1, mol2, lit_type, year, bibkey, note, pid) if valid
        False if not valid
        '''

        mol1 = self.mol1Input.text()
        mol2 = self.mol2Input.text()
        lit_type = self.chooseLitType.currentText()
        year = self.yearInput.text()
        bibkey = self.bibkeyInput.text()
        note = self.noteInput.text()

        valid = True

        if mol1:
            self.mol1Input.setStyleSheet('color: black')
        else:
            self.mol1Input.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        if mol2:
            self.mol2Input.setStyleSheet('color: black')
        else:
            self.mol2Input.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        try:
            int(year)
            self.yearInput.setStyleSheet('color: black')
        except ValueError:
            self.yearInput.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        if bibkey:
            self.bibkeyInput.setStyleSheet('color: black')
        else:
            self.bibkeyInput.setStyleSheet('border: 1px solid #D63333')
            valid *= False

        if valid:
            if self._check_duplicates(mol1, mol2, year, bibkey, note):
                msg = MsgWarning(self, 'Duplicates!', 'A duplicated copy of this input already exists in the database. Please change your input.')
                msg.exec_()
                return False
            else:
                return (mol1, mol2, lit_type, year, bibkey, note)
        else:
            return False

    def _check_duplicates(self, mol1, mol2, year, bibkey, note):
        ''' check whether the input entry is duplicated '''

        r = self.main.cursor.execute("SELECT bibkey FROM lit WHERE mol1 = (?) AND mol2 = (?) AND year = (?) AND bibkey = (?) AND note = (?)", (mol1, mol2, year, bibkey, note))

        return bool(r.fetchall())


class VisPanel(QtWidgets.QWidget):
    ''' Visualization widget  '''

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent

        # choose which literature type to display
        self.chooseLitType = QtWidgets.QComboBox()
        self.chooseLitType.addItems(DEFAULT_LIT_TYPES)
        self.refreshBtn = QtWidgets.QPushButton('Refresh DB')
        self.detailInfo = QtWidgets.QLineEdit('')
        self.detailInfo.setReadOnly(True)
        self.detailInfo.setStyleSheet('background: transparent; border: 0px')

        self.infoBar = QtWidgets.QWidget()
        infoLayout = QtWidgets.QGridLayout()
        infoLayout.setAlignment(QtCore.Qt.AlignLeft)
        infoLayout.addWidget(self.chooseLitType, 0, 0)
        infoLayout.addWidget(self.refreshBtn, 1, 0)
        infoLayout.addWidget(QtWidgets.QLabel("Details: "), 0, 1, 2, 1)
        infoLayout.addWidget(self.detailInfo, 0, 2, 2, 1)
        self.infoBar.setLayout(infoLayout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.addWidget(self.infoBar)
        # Cache layout because there are only a few lit types.
        # One may wanna switch between lit types, but I don't need
        # to re-generate the grid over and over again.
        self._create_mol_grid(DEFAULT_LIT_TYPES)
        self.setLayout(self.mainLayout)

        self.chooseLitType.currentTextChanged.connect(self._show_grid)
        self.refreshBtn.clicked.connect(self._refresh)

    def _create_mol_grid(self, lit_types):
        ''' create & cache molecule grids '''

        # create empty cache & lower triangular dictionary
        self.cache = {}
        self.mol_list = []
        self.mol_detail = {}

        for lit_type in lit_types:
            self._read_db_mol(lit_type)
            if self.mol_list:
                n = len(self.mol_list)
                for i in range(n):
                    for j in range(n):
                        self.mol_detail[(lit_type, i, j)] = ('', 0)
                self._read_db_detail(lit_type)

                self.cache[lit_type] = QtWidgets.QTableWidget(n, n)
                self.cache[lit_type].setSortingEnabled(False)
                self.cache[lit_type].setHorizontalHeaderLabels(self.mol_list)
                self.cache[lit_type].setVerticalHeaderLabels(self.mol_list)
                self.cache[lit_type].setShowGrid(True)
                self.cache[lit_type].cellClicked.connect(self._show_detail)

                # fill in cells (lower triangular matrix)
                for i in range(n):
                    for j in range(i+1):
                        k = self.mol_detail[(lit_type, i, j)][1]
                        item = QtWidgets.QTableWidgetItem(str(k))
                        item.setFlags(QtCore.Qt.ItemIsSelectable)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.cache[lit_type].setItem(i, j, item)
            else:
                self.cache[lit_type] = QtWidgets.QLabel('No records')
            self.cache[lit_type].hide()
            self.mainLayout.addWidget(self.cache[lit_type])

        self.cache[self.chooseLitType.currentText()].show()


    def _show_grid(self, lit_type):
        ''' Display grid of molecules '''

        for item in DEFAULT_LIT_TYPES:
            self.cache[item].hide()
        self.cache[lit_type].show()

    def _show_detail(self, row, col):
        ''' Display details of the selected cell at row, col '''

        current_lit_type = self.chooseLitType.currentText()
        info_str = self.mol_detail[(current_lit_type, row, col)][0]
        self.detailInfo.setText(info_str)

    def _read_db_mol(self, lit_type):
        ''' read registered molecules from database. '''

        r = self.parent.cursor.execute("SELECT DISTINCT mol FROM (SELECT mol1 AS mol FROM lit WHERE lit_type = ? UNION SELECT mol2 AS mol FROM lit WHERE lit_type = ?)t", (lit_type, lit_type))

        self.mol_list = []
        for row in r.fetchall():
            for x in row:
                self.mol_list.append(x)
        self.mol_list.sort()

    def _read_db_detail(self, lit_type):
        ''' read item details from database for the selected lit_typeself.
        Reform it to a (i, j):"bibkey: note" dictionary item,
        where (i, j) is the table cell index, i >= j

        Arguments
        lit_type -- str from DEFAULT_LIT_TYPES

        Returns
        (detail_txt str, k int) -> self.mol_detail[(lit_type, i, j)]
        k is the number of records
        '''

        r = self.parent.cursor.execute("SELECT mol1, mol2, bibkey, note FROM lit WHERE lit_type = ?", (lit_type,))

        for row in r.fetchall():
            (mol1, mol2, bibkey, note) = row
            i = self.mol_list.index(mol1)
            j = self.mol_list.index(mol2)
            if i < j:
                i, j = j, i
            else:
                pass
            # update values in self.mol_detail
            k = self.mol_detail[(lit_type, i, j)][1]
            _this_str = self.mol_detail[(lit_type, i, j)][0]
            if k == 0:
                _this_str += "{:s}: {:s}".format(bibkey, note)
            else:
                _this_str += "\n{:s}: {:s}".format(bibkey, note)
            k += 1
            self.mol_detail[(lit_type, i, j)] = (_this_str, k)


    def _refresh(self):
        ''' refresh database '''

        # clear previous widgets
        keys = list(self.cache.keys())
        for key in keys:
            _t = self.cache.pop(key)
            _t.deleteLater()

        self._create_mol_grid(DEFAULT_LIT_TYPES)


class MsgWarning(QtWidgets.QMessageBox):
    ''' Warning message box '''

    def __init__(self, parent, title_text, moretext=''):
        QtWidgets.QWidget.__init__(self, parent)

        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.addButton(QtWidgets.QMessageBox.Ok)
        self.setWindowTitle(title_text)
        self.setText(moretext)


def create_db(db_name):
    ''' Create database '''
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lit
                (id INTEGER PRIMARY KEY AUTOINCREMENT, mol1 TEXT NOT NULL, mol2 TEXT NOT NULL, lit_type TEXT NOT NULL, year INT NOT NULL, bibkey TEXT NOT NULL, note TEXT)
                ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':

    create_db(DB)

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
