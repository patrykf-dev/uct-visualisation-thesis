from PyQt5.QtWidgets import QMainWindow, QGridLayout, QMessageBox

from src.main_application.GUI_utils import show_dialog
from src.main_application.enums import Game
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
        self.tree_widget = MonteCarloTreeCanvasWidget(sequences=False, display_settings=display_settings)
        self.iteration_progress_widget = IterationProgressWidget()
        main_layout.addWidget(self.iteration_progress_widget, 0, 1)
        main_layout.addWidget(self.tree_widget, 1, 1)
        self.manager.mc_manager.iteration_performed += self._handle_iteration_performed

    def _handle_start_over_button(self):
        answer = show_dialog("Do you want to restart the game?")
        if answer == QMessageBox.Ok:
            game_window_properties = {"game": self.manager.game, "game_mode": self.manager.game_mode,
                                      "settings": self.manager.mc_manager.settings,
                                      "display_settings": self.display_settings}
            self.on_close_request.fire(self, earg=game_window_properties)
            self.close()

    def _handle_iteration_performed(self, sender, earg):
        self.iteration_progress_widget.layout.progress_bar.setValue(earg * 100)
        if self.display_settings.animate:
            self.manager.mc_manager.tree.reset_vis_data()
            self.tree_widget.layout.canvas.use_tree_data(self.manager.mc_manager.tree)
            self.tree_widget.layout.fill_tree_details_panel_info(self.manager.mc_manager.tree.data.vertices_count)
        if earg == 1:
            self.manager.mc_manager.tree.reset_vis_data()
            self.tree_widget.layout.canvas.use_tree_data(self.manager.mc_manager.tree)
            self.tree_widget.layout.fill_tree_details_panel_info(self.manager.mc_manager.tree.data.vertices_count)
