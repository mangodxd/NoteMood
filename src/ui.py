import os, random, math
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QLabel, QComboBox, QMessageBox
from PyQt6.QtGui import QColor, QPainter, QBrush, QKeySequence, QAction
from PyQt6.QtCore import Qt, QTimer, QPointF, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from weather_effects import WeatherEffect

class NoteMood(QWidget):
    def __init__(self, path=None):
        super().__init__()
        self.setWindowTitle("NoteMood")
        self.resize(600, 500)
        self.currentPath = path
        self.unsavedChanges = False
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.currentMusic = None

        self.setupUI()
        self.setupConnections()
        self.setupShortcuts()

        # Autosave
        self.autoSaveTimer = QTimer(self)
        self.autoSaveTimer.timeout.connect(self.autoSave)
        self.autoSaveTimer.start(120000)

    def resizeEvent(self, event):
        self.effectLayer.setGeometry(self.rect())
        super().resizeEvent(event)

    # ----- UI -----
    def setupUI(self):
        self.textArea = QTextEdit()
        self.textArea.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                background-color: rgba(255,255,255,0.85);
                padding: 10px;
                color: #1F2937;
                font-size: 15px;
            }
        """)
        self.textArea.textChanged.connect(self.markUnsaved)

        self.status = QLabel("🌈 Welcome to NoteMood")
        self.status.setStyleSheet("""
            QLabel {
                background-color: rgba(255,255,255,0.6);
                color: #1F2937;
                padding: 4px;
                border-radius: 4px;
            }
        """)
        self.moodBox = QComboBox()
        self.moodBox.addItems(["Sleepy", "Calm", "Relaxed", "Focus", "Creative", "Energetic"])
        self.moodBox.setStyleSheet(f"""
    QComboBox {{
        background-color: rgba(255,255,255,0.85);  /* nền sáng hơn */
        color: #1F2937;  /* chữ đậm */
        border-radius: 6px;
        padding: 4px 8px;
    }}
""")
        self.newBtn = QPushButton("📄 New")
        self.openBtn = QPushButton("📂 Open")
        self.saveBtn = QPushButton("💾 Save")
        self.saveAsBtn = QPushButton("💾 Save As")
        self.musicBtn = QPushButton("🎵 Music")
        self.musicBtn.setCheckable(True)

        topBar = QHBoxLayout()
        moodLabel = QLabel("Mood:")
        moodLabel.setStyleSheet("""
                    QLabel {
                        color: #1F2937;
                    }
                """)
        topBar.addWidget(moodLabel)        
        topBar.addWidget(self.moodBox)
        topBar.addStretch()
        for b in [self.newBtn, self.openBtn, self.saveBtn, self.saveAsBtn, self.musicBtn]:
            topBar.addWidget(b)

        layout = QVBoxLayout(self)
        layout.addLayout(topBar)
        layout.addWidget(self.textArea)
        layout.addWidget(self.status)

        self.effectLayer = WeatherEffect(self)
        self.effectLayer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.effectLayer.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.textArea.raise_()
        self.effectLayer.raise_()

    # ----- Logic -----
    def setupConnections(self):
        self.moodBox.currentTextChanged.connect(self.changeMood)
        self.newBtn.clicked.connect(self.newFile)
        self.openBtn.clicked.connect(self.openFile)
        self.saveBtn.clicked.connect(self.saveFile)
        self.saveAsBtn.clicked.connect(self.saveFileAs)
        self.musicBtn.clicked.connect(self.toggleOrChooseMusic)

    def setupShortcuts(self):
        for key, func in {
            QKeySequence.StandardKey.New: self.newFile,
            QKeySequence.StandardKey.Open: self.openFile,
            QKeySequence.StandardKey.Save: self.saveFile,
        }.items():
            act = QAction(self)
            act.setShortcut(key)
            act.triggered.connect(func)
            self.addAction(act)

    def markUnsaved(self):
        if not self.unsavedChanges:
            self.unsavedChanges = True
            if not self.windowTitle().endswith('*'):
                self.setWindowTitle(self.windowTitle() + '*')

    # ----- File ops -----
    def confirmSave(self):
        if self.unsavedChanges:
            resp = QMessageBox.question(self, "Unsaved Changes", 
                "Do you want to save changes before continuing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if resp == QMessageBox.StandardButton.Yes:
                return self.saveFile()
            elif resp == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def newFile(self):
        if not self.confirmSave():
            return
        self.textArea.clear()
        self.currentPath = None
        self.unsavedChanges = False
        self.setWindowTitle("NoteMood – New Note")

    def openFile(self):
        if not self.confirmSave():
            return
        path, _ = QFileDialog.getOpenFileName(self, "Open Note", "", "Text Files (*.txt)")
        if path:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    self.textArea.setPlainText(f.read())
                self.currentPath = path
                self.setWindowTitle(f"NoteMood – {os.path.basename(path)}")
                self.unsavedChanges = False
                self.status.setText(f"📂 Opened: {os.path.basename(path)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Cannot open file: {e}")

    def saveFile(self):
        if not self.currentPath:
            return self.saveFileAs()
        try:
            with open(self.currentPath, "w", encoding="utf-8") as f:
                f.write(self.textArea.toPlainText())
            self.unsavedChanges = False
            if self.windowTitle().endswith('*'):
                self.setWindowTitle(self.windowTitle().rstrip('*'))
            self.status.setText(f"💾 Saved: {os.path.basename(self.currentPath)}")
            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot save file: {e}")
            return False

    def saveFileAs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Note", "", "Text Files (*.txt)")
        if path:
            if not path.endswith(".txt"):
                path += ".txt"
            self.currentPath = path
            return self.saveFile()
        return False

    def autoSave(self):
        if self.unsavedChanges and self.currentPath:
            self.saveFile()

    # ----- Mood & Style -----
    def changeMood(self, mood):
        theme = {
            "Calm": ("#B5E2FA", "#ffffff", "#1F2937", "cloudy"),
            "Focus": ("#B3EFB6", "#ffffff", "#1F2937", "rain"),
            "Sleepy": ("#B197FC", "#EDE7FF", "#12082B", "snow"),
            "Energetic": ("#FFD166", "#FFF8E1", "#3A2500", "sunny"),
            "Creative": ("#FF9E7D", "#FFE9D6", "#341C00", "sunny"),
            "Relaxed": ("#90E0EF", "#F1FAFB", "#1C2833", "cloudy"),
        }

        bg, textBg, textColor, weather = theme.get(mood, ("#A3CEF1", "#ffffff", "#1F2937", "sunny"))
        self.effectLayer.effect = weather
        self.effectLayer.initParticles()
        self.setStyleSheet(f"background-color: {bg};")
        self.textArea.setStyleSheet(f"""
            QTextEdit {{
                border-radius: 8px;
                background-color: {textBg};
                padding: 10px;
                color: {textColor};
                font-size: 15px;
            }}
        """)
        for btn in [self.newBtn, self.openBtn, self.saveBtn, self.saveAsBtn, self.musicBtn]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255,255,255,0.25);
                    color: {textColor};
                    border-radius: 6px;
                    padding: 5px 10px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255,255,255,0.45);
                }}
            """)
        self.status.setText(f"🎨 Mood: {mood}")

    # ----- Music -----
    def toggleOrChooseMusic(self, checked):
        if checked:
            if not self.currentMusic:
                # Ask user which music to play
                choice = QMessageBox.question(
                    self,
                    "Select Music",
                    "Do you want to listen to app's random music?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if choice == QMessageBox.StandardButton.Yes:
                    self.currentMusic = random.choice([
                        "https://cdn.pixabay.com/audio/2025/04/26/audio_5281b3676b.mp3",
                        "https://cdn.pixabay.com/audio/2023/07/30/audio_e0908e8569.mp3",
                        "https://cdn.pixabay.com/audio/2025/07/25/audio_4bd532f458.mp3",
                        "https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3",
                        "https://cdn.pixabay.com/audio/2025/06/21/audio_ec132b92fb.mp3"
                    ])
                else:
                    path, _ = QFileDialog.getOpenFileName(
                        self, "Choose Music", "", "Audio Files (*.mp3 *.wav *.ogg)"
                    )
                    if path:
                        self.currentMusic = path
                    else:
                        # If user cancels file dialog, uncheck button
                        self.musicBtn.setChecked(False)
                        return
            self.player.setSource(QUrl(self.currentMusic))
            self.player.play()
            self.status.setText("🎶 Music playing...")
        else:
            self.player.pause()
            self.status.setText("🎧 Music paused.")


    # ----- Close Event -----
    def closeEvent(self, event):
        if self.confirmSave():
            event.accept()
        else:
            event.ignore()