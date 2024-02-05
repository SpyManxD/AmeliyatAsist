STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #F5F5F5;
    }
    QLabel, QLineEdit, QComboBox, QDateTimeEdit, QPushButton {
        font: 14px Arial;
        margin-bottom: 10px;
    }
    QLineEdit, QComboBox, QDateTimeEdit {
        padding: 8px;
        border: 1px solid #D3D3D3;
        border-radius: 5px;
    }
    QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
        border-color: #4CAF50; 
    }
    QPushButton {
        color: white;
        background-color: #4CAF50;
        padding: 12px 18px;
        border: none;
        border-radius: 5px;
        margin-top: 10px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QTableWidget {
        border: 1px solid #D3D3D3;
        border-radius: 5px;
        selection-background-color: #C0C0C0;
    }
    QTableWidget::item {
        padding: 8px;
        border-color: #F0F0F0; 
    }
    QHeaderView::section {
        background-color: #E0E0E0;
        padding: 8px;
        border: 1px solid #F0F0F0;
    }
    /* Custom Styles for Status */
    .Completed { background-color: green; color: white; }
    .Canceled { background-color: red; color: white; }
    .Postponed { background-color: yellow; color: black; }
"""
