from PyQt5.QtWidgets import QMainWindow, QGridLayout

from src.main_application.game_window import GameWindow
from src.main_application.gui_settings import DisplaySettings
from src.main_application.iteration_progress_widget import IterationProgressWidget
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class GameVisualizationWindow(GameWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings,
                 main_layout: QGridLayout):
        super(GameVisualizationWindow, self).__init__(parent, manager, main_layout)
        self.display_settings = display_settings
        self.tree_widget = MonteCarloTreeCanvasWidget(sequences=False)
        self.iteration_progress_widget = IterationProgressWidget()
        main_layout.addWidget(self.iteration_progress_widget, 0, 1)
        main_layout.addWidget(self.tree_widget, 1, 1)
        self.manager.mc_manager.iteration_performed += self._handle_iteration_performed

    def _handle_iteration_performed(self, sender, earg):
        self.iteration_progress_widget.layout.progress_bar.setValue(earg * 100)
        if self.display_settings.animate:
            self.manager.mc_manager.tree.root.reset_walkers_data()
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)
        if earg == 1:
            self.manager.mc_manager.tree.root.reset_walkers_data()
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)
