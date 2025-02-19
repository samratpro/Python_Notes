from PyQt6.QtCore import QObject, pyqtSignal

class data_save_signals(QObject):
    data_saved = pyqtSignal()

# Create a single instance of SharedSignals to share across modules
data_save_signals = data_save_signals()
