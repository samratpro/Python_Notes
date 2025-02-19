from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from sqlalchemy.exc import SQLAlchemyError
from features.data_save_signals import data_save_signals
from sqlalchemy.orm import sessionmaker, declarative_base
from ui.settings_ui import Ui_settingsPage
from models import *
import csv
import os
import zipfile
from datetime import datetime
from sqlalchemy import Date, Integer, Float, Boolean, create_engine
from time import sleep


class settingsPage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setup_database()  # First setup database
        self.ui = Ui_settingsPage()
        self.ui.setupUi(self)
        self.setup_ui()


    def setup_database(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///business.db') 
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    def setup_ui(self):
        session = self.Session()
        setting = session.query(SettingModel).first()

        user = session.query(UserModel).filter(UserModel.username==self.username).one()
        self.ui.username.setText(user.username)
        self.ui.username.setDisabled(True)
        self.ui.downloadProgress.setVisible(False)
        self.ui.restoreprogressBar.setVisible(False)

        self.passEcho = True
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ui.password.setText(user.password)
        self.ui.viewPassword.clicked.connect(self.passEchoBool)

        self.ui.commission.setText(str(setting.commission))
        self.ui.dhol.setText(str(setting.dhol))

        session.close()
        session = self.Session()
        try:
            setting = session.query(SettingModel).first()
            if setting:
                self.ui.username.setText(user.username)
                self.ui.password.setText(user.password)
                self.ui.commission.setText(str(setting.commission))
                self.ui.dhol.setText(str(setting.dhol))
                self.ui.fontSelect.setCurrentText(setting.font)
            else:
                QtWidgets.QMessageBox.warning(None, "Error", f"Settings Not Founded")
        except SQLAlchemyError as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Database error : {e}")
        finally:
            session.close()
        self.ui.updateBtn.clicked.connect(self.update_setting)

        self.ui.downloadBtn.clicked.connect(self.download_backup)
        self.ui.selectFileBtn.clicked.connect(self.select_file)
        self.ui.restoreBtn.clicked.connect(self.restore_backup)

    def passEchoBool(self):
        if self.passEcho == True:
            self.ui.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.passEcho = False
        else:
            self.ui.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.passEcho = True


    def update_setting(self):
        username = self.ui.username.text().strip()
        password = self.ui.password.text().strip()
        commision = self.ui.commission.text().strip()
        dhol = self.ui.dhol.text().strip()
        font = self.ui.fontSelect.currentText().strip()

        # Check if any field is empty
        if not username or not commision or not dhol or not password or not font:
            QtWidgets.QMessageBox.warning(None, "Error", f"No field can't empty")
            return

        # Validate commission
        try:
            commission_value = float(commision)
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Error", f"কমিশন (শতাংশ) একটি সঠিক সংখ্যা প্রদান করুন")
            return

        # Validate dhol
        try:
            dhol_value = int(dhol)
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Error", f"ঢল (গ্রাম) একটি সঠিক সংখ্যা প্রদান করুন")
            return

        # Update the setting
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            setting = session.query(SettingModel).first()
            user = session.query(UserModel).filter(UserModel.username==username).one_or_none()
            if setting is None:
                QtWidgets.QMessageBox.warning(None, "Error", f"No settings founded")
                return
            if user is None:
                QtWidgets.QMessageBox.warning(None, "Error", f"Username not founded")
                return

            setting.commission = commission_value
            setting.dhol = dhol_value
            setting.font = font
            user.username = username
            user.password = password
            session.commit()
        except SQLAlchemyError as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Happend a problem to update settings: {e}")
            session.rollback()
        finally:
            session.close()
        QtWidgets.QMessageBox.information(None, "Success", f"Settings has been updated")
        data_save_signals.data_saved.emit()


    # backup *****************
    def download_backup(self):
        # Generate a default filename with the current date and time
        default_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"

        # Open a file dialog for selecting the destination with the default filename
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Backup", default_filename, "ZIP Files (*.zip)"
        )

        if file_path:  # Proceed if the user selects a file
            try:
                # Show the progress bar
                self.ui.downloadProgress.setVisible(True)
                self.ui.downloadProgress.setValue(0)

                # List of models to back up
                models = [SellerProfileModel, SellingModel, BuyerProfileModel, BuyingModel,
                          DealerModel, LoanModel, CostModel, SettingModel, UserModel, FinalAccounting]

                # Create a persistent directory for CSV files
                temp_dir = os.path.join(os.getcwd(), "temp_backup")
                os.makedirs(temp_dir, exist_ok=True)

                # Create a ZIP file
                with zipfile.ZipFile(file_path, 'w') as zipf:
                    total_models = len(models)
                    for i, model in enumerate(models):
                        # Create a CSV file in the persistent directory
                        csv_filename = os.path.join(temp_dir,
                                                    f"{model.__tablename__}_{datetime.now().strftime('%Y-%m-%d')}.csv")

                        # Backup the table to CSV (skip if no data)
                        try:
                            self.backup_table_to_csv(model, csv_filename)

                            # Add the CSV file to the ZIP archive only if it was created
                            if os.path.exists(csv_filename):
                                zipf.write(csv_filename, os.path.basename(csv_filename))
                                print(f"Added {csv_filename} to ZIP archive.")
                            else:
                                print(f"Skipped {model.__tablename__} (no data).")
                        except Exception as e:
                            print(f"Error processing {model.__tablename__}: {e}")

                        # Update the progress bar
                        progress = int((i + 1) / total_models * 100)
                        self.ui.downloadProgress.setValue(progress)
                        sleep(1)

                # Hide the progress bar after completion
                self.ui.downloadProgress.setVisible(False)

                # Show a success message
                QtWidgets.QMessageBox.information(self, "Backup", "Backup completed successfully!")
            except Exception as e:
                # Handle errors during backup
                QtWidgets.QMessageBox.critical(self, "Backup Error", f"An error occurred: {str(e)}")
                self.ui.downloadProgress.setVisible(False)
            finally:
                # Clean up the temporary directory after the process
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, file))
                    os.rmdir(temp_dir)

    def backup_table_to_csv(self, model, file_path):
        """Backup a table to a CSV file."""
        try:
            data = session.query(model).all()
            if not data:
                print(f"No data found for {model.__tablename__}. Skipping...")
                return  # Skip empty tables

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow([column.name for column in model.__table__.columns])
                # Write data rows
                for row in data:
                    writer.writerow([getattr(row, column.name) for column in model.__table__.columns])
            print(f"Successfully backed up {model.__tablename__} to {file_path}")
        except Exception as e:
            print(f"Error backing up {model.__tablename__}: {e}")
            raise

    def select_file(self):
        # Open file dialog to select a file (show both CSV and ZIP files)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Backup File", "", "Backup Files (*.csv *.zip)"
        )
        if file_path:
            self.ui.fileChosenLabel.setText(file_path)




    def restore_backup(self):
        # Get file path from the label
        file_path = self.ui.fileChosenLabel.text()
        if not os.path.isfile(file_path):
            QtWidgets.QMessageBox.warning(self, "Restore", "Invalid file selected!")
            return

        try:
            # Show the progress bar
            self.ui.restoreprogressBar.setVisible(True)
            self.ui.restoreprogressBar.setValue(0)

            # Extract the ZIP file
            with zipfile.ZipFile(file_path, 'r') as zipf:
                file_list = zipf.namelist()
                total_files = len(file_list)

                for i, filename in enumerate(file_list):
                    if filename.endswith('.csv'):
                        # Extract the CSV file
                        zipf.extract(filename)

                        # Extract the table name correctly
                        # Example: seller_profile_model_2025-01-26.csv -> seller_profile_model
                        table_name = "_".join(filename.split("_")[:-1])  # Remove the date part

                        model_mapping = {
                            "seller_profile_model": SellerProfileModel,
                            "selling_model": SellingModel,
                            "buyer_profile_model": BuyerProfileModel,
                            "buying_model": BuyingModel,
                            "dealer_model": DealerModel,
                            "loan_model": LoanModel,
                            "cost_model": CostModel,
                            "setting_model": SettingModel,
                            "user_model": UserModel,
                            "final_accounting": FinalAccounting,
                        }

                        model = model_mapping.get(table_name)
                        if not model:
                            QtWidgets.QMessageBox.warning(self, "Restore",
                                                          f"Unknown table in the backup file: {table_name}!")
                            continue

                        # Restore the table from the CSV file
                        self.restore_table_from_csv(model, filename)
                        os.remove(filename)  # Remove the temporary CSV file

                        # Update the progress bar
                        progress = int((i + 1) / total_files * 100)
                        self.ui.restoreprogressBar.setValue(progress)
                        sleep(1)

            # Hide the progress bar after completion
            self.ui.restoreprogressBar.setVisible(False)
            self.ui.fileChosenLabel.setText(":  No File Chosen...")

            # Show a success message
            QtWidgets.QMessageBox.information(self, "Restore", "Restore completed successfully!")
        except Exception as e:
            # Handle errors during restore
            QtWidgets.QMessageBox.critical(self, "Restore Error", f"An error occurred: {str(e)}")
            self.ui.restoreprogressBar.setVisible(False)
        data_save_signals.data_saved.emit()

    def restore_table_from_csv(self, model, file_path):
        """Restore a table from a CSV file."""
        with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            columns = next(reader)  # Read header

            for row in reader:
                data = {}
                for column, value in zip(columns, row):
                    # Get the column type
                    column_type = model.__table__.columns[column].type

                    # Convert the value based on the column type
                    if isinstance(column_type, Date):
                        # Convert to Python date object
                        data[column] = datetime.strptime(value, "%Y-%m-%d").date()
                    elif isinstance(column_type, Integer):
                        # Convert to integer
                        data[column] = int(value)
                    elif isinstance(column_type, Float):
                        # Convert to float
                        data[column] = float(value)
                    elif isinstance(column_type, Boolean):
                        # Convert to boolean
                        data[column] = value.lower() == "true"
                    else:
                        # Keep the value as is (e.g., String)
                        data[column] = value

                # Create an instance of the model and merge it into the session
                instance = model(**data)
                session.merge(instance)  # Use merge to avoid duplicates

            # Commit the session to save changes
            session.commit()

