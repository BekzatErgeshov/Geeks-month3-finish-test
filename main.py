import sys
from PyQt6.QtWidgets import QApplication
from database.db import init_db, get_session
from ui.main_window import MainWindow


def main() -> None:
    init_db()
    session = get_session()

    app = QApplication(sys.argv)
    window = MainWindow(session)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
