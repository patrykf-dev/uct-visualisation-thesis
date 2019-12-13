from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen
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
        main_layout.addWidget(self.manager.canvas, 0, 0, 2, 1)
        main_layout.addWidget(self.iteration_progress_widget, 0, 1)
        main_layout.addWidget(self.tree_widget, 1, 1)
        self.manager.mc_manager.iteration_performed += self._handle_iteration_performed
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _handle_iteration_performed(self, sender, earg):
        self.iteration_progress_widget.layout.progress_bar.setValue(earg * 100)
        if self.display_settings.animate:
            self.manager.mc_manager.tree.root.reset_walkers_data()
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)
        if earg == 1:
            self.manager.mc_manager.tree.root.reset_walkers_data()
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
