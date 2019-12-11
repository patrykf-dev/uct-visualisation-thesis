from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen, get_button
from src.main_application.gui_settings import DisplaySettings
from src.main_application.iteration_progress_widget import IterationProgressWidget
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class MachineVsMachineWindow(QMainWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings):
        super(MachineVsMachineWindow, self).__init__(parent)
        self.display_settings = display_settings
        self.manager = manager
        main_widget = QWidget()
        main_layout = QGridLayout()
        self.iteration_progress_widget = IterationProgressWidget()
        main_layout.addWidget(self.manager.canvas, 0, 0, 2, 1)
        main_layout.addWidget(self.iteration_progress_widget, 0, 1)
        main_layout.addWidget(self.tree_widget, 1, 1)
        self.tree_widget = MonteCarloTreeCanvasWidget(sequences=False)
        main_layout.addWidget(self.tree_widget, 0, 1)
        self.next_move_button = get_button("Make next move")
        self.next_move_button.clicked.connect(self.handle_next_move_button)
        main_layout.addWidget(self.next_move_button, 1, 0)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.manager.on_update_tree += self._handle_iteration_performed

    def _handle_iteration_performed(self, sender, earg):
        self.iteration_progress_widget.layout.progress_bar.setValue(earg * 100)
        if self.display_settings.animate:
            reset_walkers_data(self.manager.mc_manager.tree.root)
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)
        if earg == 1:
            self.tree_widget.layout.canvas.use_root_data(self.manager.mc_manager.tree.root)

    def handle_next_move_button(self, sender):
        self.manager.perform_algorithm_move()

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
