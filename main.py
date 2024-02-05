# /path/to/project/main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui import AmeliyatYonetimSistemiUI


def main():
    """Main function to start the application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Optional: set style to Fusion for a modern look

    main_window = AmeliyatYonetimSistemiUI()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
