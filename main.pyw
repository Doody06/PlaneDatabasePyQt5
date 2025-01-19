import os
from dotenv import load_dotenv
from planedb import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
from PyQt5.QtGui import QIcon
from error_dialog import Ui_Dialog
from welcomedialog import Ui_Form
import requests
from py2exe import freeze


class mainwindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.plane_dict = []
        self.z = 0
        self.setWindowIcon(QIcon("planedb_icon.png"))
        self.title = "Doody's Plane Database"
        self.setWindowTitle(self.title)

    def comboBoxValue(self):
        return self.comboBox.currentText()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.next_plane)
        self.pushButton.clicked.connect(self.prev_plane)
        self.pushButton_3.clicked.connect(self.search)
        self.xy_label.setText(f"0 / 0")
        self.setWindowIcon(QIcon("Sukhoi.jpg"))
        self.comboBox.currentTextChanged.connect(self.pholder_text_set)

    def prev_plane(self):
        if self.z != 0:
            self.z += -1
            self.next = False
            self.display_result()
        else:
            pass

    def next_plane(self):
        if self.z + 1 != len(self.plane_dict):
            self.z += 1
            self.next = True
            self.display_result()
        else:
            pass

    def access_API(self, api_url):
        try:
            load_dotenv("SECRET.env")
            API_KEY = os.getenv("API_KEY")
            respond = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        except Exception as e:  # need to find excat exception that occurs when no internet
            print(e)
            dialog = ErrorDialog()
            dialog.internet_error()
            dialog.exec_()
            return
        return respond

    def display_result(self):
        if len(self.plane_dict) == 0:
            dialog = ErrorDialog()
            dialog.not_found_error()
            dialog.exec_()
        else:
            try:
                if self.plane_dict:
                    current_plane = self.plane_dict[self.z]
                    self.xy_label.setText(f"{self.z + 1} / {len(self.plane_dict)}")
                    attribute_list = []

                    for x in current_plane.values():
                        attribute_list.append(x)
                    self.man_label.setText(current_plane["manufacturer"])
                    self.model_label.setText(current_plane["model"])
                    self.engine_label.setText(current_plane["engine_type"])
                    self.speed_label.setText(current_plane["max_speed_knots"])
                    self.ceiling_label.setText(current_plane["ceiling_ft"])
                    self.weight_label.setText(current_plane["gross_weight_lbs"])
                    self.length_label.setText(current_plane["length_ft"])
                    self.height_label.setText(current_plane["height_ft"])
                    self.wing_label.setText(current_plane["wing_span_ft"])
                    self.range_label.setText(current_plane["range_nautical_miles"])
            except KeyError as e:
                self.plane_dict[self.z][e.args[0]] = "API error, value not found"

    def pholder_text_set(self):  # To set placeholder text in line edits based on option chosen in combo box
        comboboxtext = self.comboBoxValue()
        if comboboxtext == "Manufacturer / Model":
            self.lineEdit.setPlaceholderText("Manufacturer")
            self.lineEdit_2.setPlaceholderText("Model")
        elif comboboxtext == "Min / Max range":
            self.lineEdit.setPlaceholderText("Minimum range")
            self.lineEdit_2.setPlaceholderText("Maximum range")
        elif comboboxtext == "Min / Max length":
            self.lineEdit.setPlaceholderText("Minimum length")
            self.lineEdit_2.setPlaceholderText("Maximum length")
        elif comboboxtext == "Min / Max height":
            self.lineEdit.setPlaceholderText("Minimum height")
            self.lineEdit_2.setPlaceholderText("Maximum height")
        elif comboboxtext == "Min / Max wing span":
            self.lineEdit.setPlaceholderText("Minimum wing span")
            self.lineEdit_2.setPlaceholderText("Maximum wing span")

    def search(self):
        self.z = 0
        search_criteria = self.comboBoxValue()
        x = str(self.lineEdit.text())
        y = str(self.lineEdit_2.text())
        if x == "" or y == "":
            dialog = ErrorDialog()
            dialog.not_found_error()
            dialog.exec()
            return
        if search_criteria != "Manufacturer / Model":
            try:
                x = float(x)
                y = float(y)
            except ValueError:
                dialog = ErrorDialog()
                dialog.not_found_error()
                dialog.exec_()
        try:
            if search_criteria == "Manufacturer / Model":
                api_url = 'https://api.api-ninjas.com/v1/aircraft?manufacturer={}&model={}&limit={}'.format(x, y, 30)
            elif search_criteria == "Min / Max range":
                api_url = 'https://api.api-ninjas.com/v1/aircraft?min_range={}&max_range={}&limit={}'.format(x, y, 30)
            elif search_criteria == "Min / Max length":
                api_url = 'https://api.api-ninjas.com/v1/aircraft?min_length={}&max_length={}&limit={}'.format(x, y, 30)
            elif search_criteria == "Min / Max height":
                api_url = 'https://api.api-ninjas.com/v1/aircraft?min_height={}&max_height={}&limit={}'.format(x, y, 30)
            elif search_criteria == "Min / Max wing span":
                api_url = 'https://api.api-ninjas.com/v1/aircraft?min_wingspan={}&max_wingspan={}&limit={}'.format(x, y,
                                                                                                                   30)
        except:
            print("no internet")
        self.response = self.access_API(api_url)
        if self.response == None:
            print("self.response == None go to line 102")
        else:
            print(self.response)
            self.plane_dict = self.response.json()
            self.display_result()


class ErrorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()  # Correctly initialize Ui_Dialog
        self.ui.setupUi(self)
        self.ui.CloseDialogButton.clicked.connect(self.close_dialog)

    def close_dialog(self):
        self.close()

    def internet_error(self):
        self.ui.ErrorDialogLabel.setText("Error! check your internet connection and retry")

    def not_found_error(self):
        self.ui.ErrorDialogLabel.setText("Error! There are no planes with these characteristics in the database")


class WelcomeWindow(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_app)

    def open_app(self):
        MainWindow.show()
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("planedb_icon.png"))
    MainWindow = QMainWindow()
    ui = mainwindow()
    ui.setupUi(MainWindow)
    ui.initUI()
    welcomewindow = WelcomeWindow()
    welcomewindow.show()
    # MainWindow.show()
    sys.exit(app.exec_())

