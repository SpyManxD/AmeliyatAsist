# /path/to/project/ui.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QComboBox, QFileDialog, QDateTimeEdit, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
from database_manager import DatabaseManager
from styles import STYLESHEET

class AmeliyatYonetimSistemiUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager('ameliyat_yonetim.db')
        self.database.initialize_db()
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components."""
        self.setWindowTitle("Ameliyat Yönetim Sistemi")
        self.setGeometry(300, 300, 1200, 700)
        self.setWindowIcon(QIcon('Logo.png'))
        self.setStyleSheet(STYLESHEET)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # UI elements setup
        self.setup_ui_elements(layout)

        self.show()

    def setup_ui_elements(self, layout):
        """Sets up UI elements and layouts."""
        # Tarih ve Saat
        layout.addWidget(QLabel("Tarih ve Saat:"))
        self.tarih_saat_edit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.tarih_saat_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        layout.addWidget(self.tarih_saat_edit)

        # Hasta Adı Soyadı
        layout.addWidget(QLabel("Hasta Adı Soyadı:"))
        self.hasta_adi_soyadi_entry = QLineEdit(self)
        layout.addWidget(self.hasta_adi_soyadi_entry)

        # Ameliyat Tanısı
        layout.addWidget(QLabel("Ameliyat Tanısı:"))
        self.ameliyat_tanisi_entry = QLineEdit(self)
        layout.addWidget(self.ameliyat_tanisi_entry)

        # Firma
        layout.addWidget(QLabel("Firma:"))
        self.firma_combobox = QComboBox(self)
        self.firma_combobox.addItems(["Firma A", "Firma B", "Firma C"])
        layout.addWidget(self.firma_combobox)

        # Teknisyen
        layout.addWidget(QLabel("Teknisyen:"))
        self.teknisyen_adi_entry = QLineEdit(self)
        layout.addWidget(self.teknisyen_adi_entry)

        # Malzeme Markası
        layout.addWidget(QLabel("Malzeme Markası:"))
        self.malzeme_markasi_entry = QLineEdit(self)
        layout.addWidget(self.malzeme_markasi_entry)

        # Gerekli Malzeme
        layout.addWidget(QLabel("Gerekli Malzeme:"))
        self.gerekli_malzeme_entry = QLineEdit(self)
        layout.addWidget(self.gerekli_malzeme_entry)

        # Ekle Butonu
        self.ekle_btn = QPushButton("Ekle", self)
        self.ekle_btn.clicked.connect(self.on_add_ameliyat)
        layout.addWidget(self.ekle_btn)

        # Listele Butonu
        self.listele_btn = QPushButton("Ameliyatları Listele", self)
        self.listele_btn.clicked.connect(self.on_list_ameliyatlar)
        layout.addWidget(self.listele_btn)

        # Excel'e Aktar Butonu
        self.excel_btn = QPushButton("Excel'e Aktar", self)
        self.excel_btn.clicked.connect(self.on_export_to_excel)
        layout.addWidget(self.excel_btn)

        # Ameliyatlar Tablosu
        self.setup_ameliyatlar_table(layout)

    def setup_ameliyatlar_table(self, layout):
        """Sets up the table widget for displaying surgeries."""
        self.ameliyatlar_tablo = QTableWidget(0, 8, self)
        self.ameliyatlar_tablo.setHorizontalHeaderLabels(
            ["ID", "Tarih", "Hasta Adı Soyadı", "Ameliyat Tanısı", "Firma", "Teknisyen", "Malzeme Markası",
             "Gerekli Malzeme"])
        self.ameliyatlar_tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.ameliyatlar_tablo)
        # Surgery Status
        layout.addWidget(QLabel("Durum:"))
        self.durum_combobox = QComboBox(self)
        self.durum_combobox.addItems(["Completed", "Incomplete", "Canceled", "Postponed"])
        layout.addWidget(self.durum_combobox)

        # Reason for Cancellation or Postponement
        layout.addWidget(QLabel("Sebep:"))
        self.sebep_entry = QLineEdit(self)
        layout.addWidget(self.sebep_entry)

        # New Date for Postponed Surgery
        layout.addWidget(QLabel("Yeni Tarih:"))
        self.yeni_tarih_edit = QDateTimeEdit(self)
        self.yeni_tarih_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        layout.addWidget(self.yeni_tarih_edit)

    def on_add_ameliyat(self):
        """Handles the add operation."""
        # Collecting data from UI elements
        tarih_saat = self.tarih_saat_edit.dateTime().toString("yyyy-MM-dd HH:mm")
        hasta_adi_soyadi = self.hasta_adi_soyadi_entry.text()
        ameliyat_tanisi = self.ameliyat_tanisi_entry.text()
        firma = self.firma_combobox.currentText()
        teknisyen = self.teknisyen_adi_entry.text()
        malzeme_markasi = self.malzeme_markasi_entry.text()
        gerekli_malzeme = self.gerekli_malzeme_entry.text()


        # Validate inputs
        if not all([hasta_adi_soyadi, ameliyat_tanisi, firma, teknisyen, malzeme_markasi, gerekli_malzeme]):
            QMessageBox.warning(self, "Eksik Bilgi", "Tüm alanlar doldurulmalıdır.")
            return

        # Insert into database
        try:
            self.database.insert_ameliyat(
                (tarih_saat, hasta_adi_soyadi, ameliyat_tanisi, firma, teknisyen, malzeme_markasi, gerekli_malzeme, ""))
            QMessageBox.information(self, "Başarılı", "Ameliyat başarıyla eklendi.")
            self.on_list_ameliyatlar()  # Refresh the list
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı işlemi sırasında bir hata oluştu: {str(e)}")

    def on_list_ameliyatlar(self):
        """Fetches and displays all surgery records in the table."""
        try:
            records = self.database.fetch_all_ameliyatlar()
            self.ameliyatlar_tablo.setRowCount(0)  # Clear existing rows
            for row_number, record in enumerate(records):
                self.ameliyatlar_tablo.insertRow(row_number)
                for column_number, data in enumerate(record):
                    item = QTableWidgetItem(str(data))
                    self.ameliyatlar_tablo.setItem(row_number, column_number, item)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ameliyatlar listelenirken bir hata oluştu: {str(e)}")

    def on_export_to_excel(self):
        """Exports surgery records to an Excel file."""
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Excel'e Aktar", "", "Excel Files (*.xlsx)",
                                                      options=options)
            if fileName:
                import pandas as pd

                # Fetch records from the database
                records = self.database.fetch_all_ameliyatlar()

                # Ensure the columns list matches the data structure from your database
                columns = ["ID", "Tarih", "Hasta Adı Soyadı", "Ameliyat Tanısı", "Firma", "Teknisyen",
                           "Malzeme Markası", "Gerekli Malzeme", "Fatura Dosyası"]
                df = pd.DataFrame(records, columns=columns)

                # Export to Excel
                df.to_excel(fileName, index=False)
                QMessageBox.information(self, "Başarılı", "Ameliyat kayıtları başarıyla Excel dosyasına aktarıldı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel'e aktarılırken bir hata oluştu: {str(e)}")

    def update_status_style(self):
        status = self.durum_combobox.currentText()
        if status == "Completed":
            self.durum_combobox.setStyleSheet("background-color: green; color: white;")
        elif status == "Canceled":
            self.durum_combobox.setStyleSheet("background-color: red; color: white;")
        elif status == "Postponed":
            self.durum_combobox.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.durum_combobox.setStyleSheet("")

        self.durum_combobox.currentIndexChanged.connect(lambda: self.update_status_style())
