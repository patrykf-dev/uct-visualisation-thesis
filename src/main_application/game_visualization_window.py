from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen, get_button, get_non_resizable_label
from src.main_application.gui_settings import DisplaySettings
from src.main_application.iteration_progress_widget import IterationProgressWidget
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class GameVisualizationWindow(QMainWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings,
                 main_layout: QGridLayout):
        super(GameVisualizationWindow, self).__init__(parent)
        self.display_settings = display_settings
        self.manager = manager
        main_widget = QWidget()
        self.tree_widget = MonteCarloTreeCanvasWidget(sequences=False)
        self.iteration_progress_widget = IterationProgressWidget()
        self._create_game_layout()
        main_layout.addWidget(self.game_widget, 0, 0, 2, 1)
        main_layout.addWidget(self.iteration_progress_widget, 0, 1)
        main_layout.addWidget(self.tree_widget, 1, 1)
        self.manager.mc_manager.iteration_performed += self._handle_iteration_performed
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _create_game_layout(self):
        game_layout = QGridLayout()
        self.game_widget = QWidget()
        self.game_widget.setLayout(game_layout)
        self.start_over_button = get_button("Start over")
        self.start_over_button.clicked.connect(self.handle_start_over_button)
        self.game_status_label = get_non_resizable_label("Game status: ")
        game_layout.addWidget(self.manager.canvas, 0, 0)
        game_layout.addWidget(self.game_status_label, 1, 0)
        game_layout.addWidget(self.start_over_button, 2, 0)

    def _handle_iteration_performed(self, sender, earg):
        self.iteration_progress_widget.layout.progress_bar.setValue(earg * 100)
        if self.display_settings.animate:
            self.manager.mc_manager.tree.root.reset_walkers_data()
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)
        if earg == 1:
            self.manager.mc_manager.tree.root.reset_walkers_data()
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)

    def handle_start_over_button(self):
        print("Starting over")

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
