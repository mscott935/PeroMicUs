# Pandas table adapted from https://stackoverflow.com/a/44605011

from PyQt5 import QtCore
import pandas as pd

class OutputTableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.dataTable = None
        self.headers = None

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.dataTable.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.dataTable.columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i, j = index.row(), index.column()
            return str(self.dataTable.iloc[i,j])
        else:
            return QtCore.QVariant()

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.dataTable.columns[section]
            else:
                return str(self.dataTable.index[section])
        return QtCore.QVariant()

    def loadData(self, filename):
        try:
            df = pd.read_csv(filename)
            self.dataTable = df
            self.headers = df.columns
        except:
            print(f"Unable to read {filename}!")
            self.dataTable = None
            self.headers = None

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def getData(self):
        return self.dataTable

    def getHeaders(self):
        return self.headers

    def save(self, outputFilename):
        try:
            pd.to_csv(outputFilename, index=False)
        except:
            print(f"Could not write to {outputFilename}.")