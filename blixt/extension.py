from javax.swing import JButton
from javax.swing import JComboBox
from javax.swing import JLabel
from javax.swing import JPanel
from javax.swing import JTextField
from javax.swing import SpringLayout
from javax.swing import BoxLayout
from javax.swing.event import ChangeListener
from java.awt.event import ActionListener
from java.awt.event import KeyListener
from java.awt.event import KeyEvent
from javax.swing import DefaultComboBoxModel
from javax.swing.border import TitledBorder
from java.awt import Color
from org.openpnp.model import Placement


class ChangeListenerWrapper(ChangeListener):

    def __init__(self):
        self._changed_handler = None

    def set_changed_handler(self, handler):
        self._changed_handler = handler

    def stateChanged(self, e):
        if self._changed_handler:
            self._changed_handler(e)


class ActionListenerWrapper(ActionListener):

    def __init__(self):
        self._action_performed_handler = None

    def set_action_performed_handler(self, handler):
        self._action_performed_handler = handler

    def actionPerformed(self, e):
        if self._action_performed_handler:
            self._action_performed_handler(e)


class KeyListenerWrapper(KeyListener):

    def __init__(self):
        self._key_pressed_handler = None
        self._key_released_handler = None
        self._key_typed_handler = None

    def keyPressed(self, e):
        if self._key_pressed_handler:
            self._key_pressed_handler(e)

    def keyReleased(self, e):
        if self._key_released_handler:
            self._key_released_handler(e)

    def keyTyped(self, e):
        if self._key_typed_handler:
            self._key_typed_handler(e)

    def set_pressed_handler(self, handler):
        self._key_pressed_handler = handler

    def set_released_handler(self, handler):
        self._key_released_handler = handler

    def set_typed_handler(self, handler):
        self._key_typed_handler = handler


class AutoComboBox(JComboBox):

    def __init__(self):
        super(AutoComboBox, self).__init__()
        self.setEditable(True)
        self._txtField = self.getEditor().getEditorComponent()
        key_listener = KeyListenerWrapper()
        key_listener.set_released_handler(self._key_released)
        self._txtField.addKeyListener(key_listener)
        action_listener = ActionListenerWrapper()
        action_listener.set_action_performed_handler(self._action_performed)
        self.addActionListener(action_listener)
        self._text_changed_callback = None
        self._validate_callback = None
        self._masked_keys = [
            KeyEvent.VK_UP, KeyEvent.VK_DOWN, KeyEvent.VK_ENTER, KeyEvent.VK_RIGHT,
            KeyEvent.VK_SHIFT, KeyEvent.VK_ALT, KeyEvent.VK_CONTROL
        ]

    def set_text_changed_callback(self, callback):
        self._text_changed_callback = callback

    def set_validate_callback(self, callback):
        self._validate_callback = callback

    def set_model_ex(self, model):
        current_text = self._txtField.getText()
        current_cur_pos = self._txtField.getCaretPosition()
        self.setSelectedIndex(-1)
        self.setModel(model)
        self._txtField.setText(current_text)
        self._txtField.setCaretPosition(current_cur_pos)
        if self.getModel().getSize() > 0:
            self.setPopupVisible(True)
        else:
            self.setPopupVisible(False)

    def _key_released(self, e):
        if e.getKeyCode() not in self._masked_keys:
            if self._text_changed_callback:
                self._text_changed_callback(self._txtField.getText())

        if e.getKeyCode() == KeyEvent.VK_ENTER:
            if (self.getModel().getSize() > 0 and self.getSelectedIndex() < 0 and
                    self._txtField.getText() != ""):
                self.setSelectedIndex(0)

        if self._validate_callback:
            self._validate_callback(self._txtField.getText())

    def _action_performed(self, e):
        if self._validate_callback:
            self._validate_callback(self._txtField.getText())


class PlacementsPanel(JPanel):

    FIELD_WIDTH = 320

    def __init__(self, openpnp_vars):
        super(PlacementsPanel, self).__init__()
        self.openpnp_vars = openpnp_vars
        self.setBorder(TitledBorder("Placements"))
        self.setLayout(BoxLayout(self, BoxLayout.PAGE_AXIS))

        content_panel = JPanel()
        spring_layout = SpringLayout()
        content_panel.setLayout(spring_layout)
        self.add(content_panel)

        lbl_board = JLabel("Board")
        spring_layout.putConstraint(SpringLayout.NORTH, lbl_board, 10, SpringLayout.NORTH, self)
        spring_layout.putConstraint(SpringLayout.WEST, lbl_board, 10, SpringLayout.WEST, self)
        content_panel.add(lbl_board)

        self.txt_board = JTextField()
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.txt_board, 0,
                                    SpringLayout.VERTICAL_CENTER, lbl_board)
        spring_layout.putConstraint(SpringLayout.WEST, self.txt_board, 80, SpringLayout.EAST,
                                    lbl_board)
        spring_layout.putConstraint(SpringLayout.EAST, self.txt_board, PlacementsPanel.FIELD_WIDTH,
                                    SpringLayout.WEST, self.txt_board)
        self.txt_board.setEnabled(False)
        content_panel.add(self.txt_board)

        self.pnl_board_status = JPanel()
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.pnl_board_status, 0,
                                    SpringLayout.VERTICAL_CENTER, self.txt_board)
        spring_layout.putConstraint(SpringLayout.WEST, self.pnl_board_status, 0, SpringLayout.EAST,
                                    self.txt_board)
        spring_layout.putConstraint(SpringLayout.EAST, self.pnl_board_status, 4, SpringLayout.WEST,
                                    self.pnl_board_status)
        spring_layout.putConstraint(SpringLayout.NORTH, self.pnl_board_status, 0,
                                    SpringLayout.NORTH, self.txt_board)
        spring_layout.putConstraint(SpringLayout.SOUTH, self.pnl_board_status, 0,
                                    SpringLayout.SOUTH, self.txt_board)
        content_panel.add(self.pnl_board_status)

        lbl_ids = JLabel("IDs")
        spring_layout.putConstraint(SpringLayout.NORTH, lbl_ids, 15, SpringLayout.SOUTH, lbl_board)
        spring_layout.putConstraint(SpringLayout.WEST, lbl_ids, 0, SpringLayout.WEST, lbl_board)
        content_panel.add(lbl_ids)

        self.txt_ids = JTextField()
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.txt_ids, 0,
                                    SpringLayout.VERTICAL_CENTER, lbl_ids)
        spring_layout.putConstraint(SpringLayout.WEST, self.txt_ids, 0, SpringLayout.WEST,
                                    self.txt_board)
        spring_layout.putConstraint(SpringLayout.EAST, self.txt_ids, PlacementsPanel.FIELD_WIDTH,
                                    SpringLayout.WEST, self.txt_ids)
        txt_id_key_listener = KeyListenerWrapper()
        txt_id_key_listener.set_released_handler(self._on_txt_id_key_released)
        self.txt_ids.addKeyListener(txt_id_key_listener)
        content_panel.add(self.txt_ids)

        self.pnl_ids_status = JPanel()
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.pnl_ids_status, 0,
                                    SpringLayout.VERTICAL_CENTER, self.txt_ids)
        spring_layout.putConstraint(SpringLayout.WEST, self.pnl_ids_status, 0, SpringLayout.EAST,
                                    self.txt_ids)
        spring_layout.putConstraint(SpringLayout.EAST, self.pnl_ids_status, 4, SpringLayout.WEST,
                                    self.pnl_board_status)
        spring_layout.putConstraint(SpringLayout.NORTH, self.pnl_ids_status, 0, SpringLayout.NORTH,
                                    self.txt_ids)
        spring_layout.putConstraint(SpringLayout.SOUTH, self.pnl_ids_status, 0, SpringLayout.SOUTH,
                                    self.txt_ids)
        content_panel.add(self.pnl_ids_status)

        lbl_enabled = JLabel("Enabled")
        spring_layout.putConstraint(SpringLayout.NORTH, lbl_enabled, 15, SpringLayout.SOUTH,
                                    lbl_ids)
        spring_layout.putConstraint(SpringLayout.WEST, lbl_enabled, 0, SpringLayout.WEST, lbl_ids)
        content_panel.add(lbl_enabled)

        self.cmb_enabled = JComboBox()
        self.cmb_enabled.setModel(DefaultComboBoxModel(["", "True", "False"]))
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.cmb_enabled, 0,
                                    SpringLayout.VERTICAL_CENTER, lbl_enabled)
        spring_layout.putConstraint(SpringLayout.WEST, self.cmb_enabled, 0, SpringLayout.WEST,
                                    self.txt_ids)
        content_panel.add(self.cmb_enabled)

        lbl_part = JLabel("Part")
        spring_layout.putConstraint(SpringLayout.NORTH, lbl_part, 15, SpringLayout.SOUTH,
                                    lbl_enabled)
        spring_layout.putConstraint(SpringLayout.WEST, lbl_part, 0, SpringLayout.WEST, lbl_ids)
        content_panel.add(lbl_part)

        self.cmb_part = AutoComboBox()
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.cmb_part, 0,
                                    SpringLayout.VERTICAL_CENTER, lbl_part)
        spring_layout.putConstraint(SpringLayout.WEST, self.cmb_part, 0, SpringLayout.WEST,
                                    self.cmb_enabled)
        spring_layout.putConstraint(SpringLayout.EAST, self.cmb_part, PlacementsPanel.FIELD_WIDTH,
                                    SpringLayout.WEST, self.cmb_part)
        self.cmb_part.set_text_changed_callback(self._on_cmb_part_text_changed)
        self.cmb_part.set_validate_callback(self._on_cmb_part_validate)
        content_panel.add(self.cmb_part)

        self.pnl_part_status = JPanel()
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.pnl_part_status, 0,
                                    SpringLayout.VERTICAL_CENTER, self.cmb_part)
        spring_layout.putConstraint(SpringLayout.WEST, self.pnl_part_status, 0, SpringLayout.EAST,
                                    self.cmb_part)
        spring_layout.putConstraint(SpringLayout.EAST, self.pnl_part_status, 4, SpringLayout.WEST,
                                    self.pnl_part_status)
        spring_layout.putConstraint(SpringLayout.NORTH, self.pnl_part_status, 0, SpringLayout.NORTH,
                                    self.cmb_part)
        spring_layout.putConstraint(SpringLayout.SOUTH, self.pnl_part_status, 0, SpringLayout.SOUTH,
                                    self.cmb_part)
        content_panel.add(self.pnl_part_status)

        lbl_type = JLabel("Type")
        spring_layout.putConstraint(SpringLayout.NORTH, lbl_type, 15, SpringLayout.SOUTH, lbl_part)
        spring_layout.putConstraint(SpringLayout.WEST, lbl_type, 0, SpringLayout.WEST, lbl_part)
        content_panel.add(lbl_type)

        self.cmb_type = JComboBox()
        self.cmb_type.setModel(DefaultComboBoxModel(["", "Placement", "Fiducial"]))
        spring_layout.putConstraint(SpringLayout.VERTICAL_CENTER, self.cmb_type, 0,
                                    SpringLayout.VERTICAL_CENTER, lbl_type)
        spring_layout.putConstraint(SpringLayout.WEST, self.cmb_type, 0, SpringLayout.WEST,
                                    self.cmb_part)
        content_panel.add(self.cmb_type)

        self.btn_apply = JButton("Apply")
        spring_layout.putConstraint(SpringLayout.WEST, self.btn_apply, 0, SpringLayout.WEST,
                                    self.cmb_type)
        spring_layout.putConstraint(SpringLayout.NORTH, self.btn_apply, 20, SpringLayout.SOUTH,
                                    lbl_type)
        btn_apply_action_listener = ActionListenerWrapper()
        btn_apply_action_listener.set_action_performed_handler(self._on_apply_btn_action)
        self.btn_apply.addActionListener(btn_apply_action_listener)
        content_panel.add(self.btn_apply)

        self.board_name = None
        self.all_placements = {}
        self.selected_placements = {}
        self.invalid_placements = {}
        self.all_parts = {}
        self.field_validation_status = {}

    def _on_cmb_part_text_changed(self, text):

        def filter_fn(val):
            return text.strip().upper() in val.upper()

        if text.strip().upper() == "":
            return
        filtered_parts = filter(filter_fn, self.all_parts.keys())
        self.cmb_part.set_model_ex(DefaultComboBoxModel(filtered_parts))

    def _on_cmb_part_validate(self, text):
        self._update_part_status()

    def _on_txt_id_key_released(self, e):
        self.invalid_placements = {}
        self.selected_placements = {}

        for placement_id in self.txt_ids.getText().strip().split(","):
            placement_id = placement_id.strip().upper()
            if placement_id == "":
                continue

            if placement_id in self.all_placements:
                self.selected_placements[placement_id] = self.all_placements[placement_id]
            else:
                self.invalid_placements[placement_id] = []

        self._update_selected_ids_status()

    def _on_apply_btn_action(self, e):
        self._apply_settings()
        self._clear_fields()

    def _update_board_status(self):
        if self.board_name:
            self.txt_board.setToolTipText("Selected board")
            self.txt_board.setText(self.board_name)
            self.pnl_board_status.setBackground(None)
            self.field_validation_status['board'] = True
        else:
            self.txt_board.setToolTipText("Invalid board selection")
            self.txt_board.setText(None)
            self.pnl_board_status.setBackground(Color.red)
            self.field_validation_status['board'] = False
        self._update_apply_btn_status()

    def _update_selected_ids_status(self):
        if len(self.invalid_placements) > 0:
            ids = [p for p in self.invalid_placements]
            self.txt_ids.setToolTipText("IDs not found: %s" % (', '.join(ids)))
            self.pnl_ids_status.setBackground(Color.red)
            self.field_validation_status['ids'] = False
        else:
            self.txt_ids.setToolTipText(None)
            self.pnl_ids_status.setBackground(None)
            self.field_validation_status['ids'] = True
        self._update_apply_btn_status()

    def _update_part_status(self):
        part_id = self.cmb_part.getEditor().getEditorComponent().getText().strip()
        if part_id in self.all_parts or part_id == "":
            self.cmb_part.setToolTipText("Selected part")
            self.pnl_part_status.setBackground(None)
            self.field_validation_status['part'] = True
        else:
            self.cmb_part.setToolTipText("Invalid part")
            self.pnl_part_status.setBackground(Color.red)
            self.field_validation_status['part'] = False
        self._update_apply_btn_status()

    def _update_apply_btn_status(self):
        if all(item is True for item in self.field_validation_status.values()):
            self.btn_apply.setEnabled(True)
        else:
            self.btn_apply.setEnabled(False)

    def _apply_settings(self):
        if len(self.selected_placements) == 0:
            return False

        enabled = str(self.cmb_enabled.getSelectedItem())
        if enabled == "True":
            placement_enabled = True
        elif enabled == "False":
            placement_enabled = False
        else:
            placement_enabled = None

        part_id = str(self.cmb_part.getSelectedItem())
        if part_id in self.all_parts:
            part = self.all_parts[part_id]
        else:
            part = None

        part_type_str = str(self.cmb_type.getSelectedItem())
        if part_type_str == "Placement":
            part_type = Placement.Type.Placement
        elif part_type_str == "Fiducial":
            part_type = Placement.Type.Fiducial
        else:
            part_type = None

        for placements in self.selected_placements.values():
            for placement in placements:
                if placement_enabled is not None:
                    placement.setEnabled(placement_enabled)

                if part:
                    placement.setPart(part)

                if part_type:
                    placement.setType(part_type)

        return True

    def _clear_fields(self):
        self.txt_ids.setText("")
        self.cmb_enabled.setSelectedIndex(-1)
        self.cmb_part.setSelectedIndex(-1)
        self.cmb_type.setSelectedIndex(-1)
        self.txt_ids.grabFocus()

    def _fetch_placements(self):
        board_name = None
        valid_board = True
        self.all_placements = {}
        for location in self.openpnp_vars['gui'].getJobTab().getSelections():
            board = location.getBoard()
            if not board_name:
                board_name = board.getName()

            if board_name != board.getName():
                valid_board = False

            for placement in board.getPlacements():
                self.all_placements.setdefault(placement.getId().upper(), []).append(placement)

        if valid_board:
            self.board_name = board_name
        else:
            self.board_name = None

    def _fetch_parts(self):
        self.all_parts = {}
        for part in self.openpnp_vars['config'].getParts():
            self.all_parts[part.getId()] = part

    def refresh(self):
        self._fetch_placements()
        self._fetch_parts()
        self._update_board_status()
        self._update_selected_ids_status()


def init(openpnp_vars):
    tabbed_pane = openpnp_vars['gui'].getTabs()

    parent_panel = JPanel()
    parent_panel.setLayout(BoxLayout(parent_panel, BoxLayout.PAGE_AXIS))
    tabbed_pane.add("Quick Settings", parent_panel)

    placements_panel = PlacementsPanel(openpnp_vars)
    parent_panel.add(placements_panel)

    def on_tab_changed(e):
        if e.source.getSelectedComponent() == parent_panel:
            placements_panel.refresh()

    tab_change_listener = ChangeListenerWrapper()
    tab_change_listener.set_changed_handler(on_tab_changed)
    tabbed_pane.addChangeListener(tab_change_listener)

    print("Blixt extension initialised")
