#from PyQt4.QtCore import *
#from PyQt4.QtWidgets import *
from PyQt4.QtGui import  *

from fcn import *
import binascii


class FCNGui(QWidget):
    protocol = 6
    host_protocol = 'TCP'
    msg_type = 0

    def get_var(self):
        class ImportVariables:
            srcip = str(self.source_ip_edit.text())
            destip = str(self.destination_ip_edit.text())
            seq_no = int(self.seq_no_edit.text())
            srcport = int(self.source_port_edit.text())
            destport = int(self.destination_port_edit.text())
            prototype = self.protocol
            msgtype = self.msg_type #int(self.msg_type_edit.text())
            timeoutval = int(self.timeout_val_edit.text())
            export = str(self.export_name_edit.text())
            mclass = str(self.class_name_edit.text())
            prio = int(self.priority_edit.text())
            HOST = str(self.host_ip_edit.text())
            PORT = int(self.host_port_edit.text())
            PROTO = self.host_protocol #str(self.host_protocol_edit.text())
            a_flg = 0
        return ImportVariables

    def __init__(self, parent=None):
        super(FCNGui, self).__init__(parent)
        # Initial
        self.rap = {}

        # Title
        title = 'Fake Classifier Node'

        # Create Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 1024, 300)
        self.setWindowTitle(title)
        self.show()

        self.header_ui()
        self.match_ui()
        self.message_type_dropdown()
        self.send_button.clicked.connect(self.send_message_handler)

    def header_ui(self):
        tuple_label = QLabel('Match 5-tuple Parameters')
        self.grid.addWidget(tuple_label, 0, 0)

        setting_label = QLabel('Settings')
        self.grid.addWidget(setting_label, 0, 2)

        host_label = QLabel('Host Settings')
        self.grid.addWidget(host_label, 0, 4)

    def message_type_dropdown(self):
        msg_type_dropdown = QComboBox(self)
        self.grid.addWidget(msg_type_dropdown, 2, 3)
        msg_type_dropdown.addItems(["Add",
                                    "Delete Matching",
                                    "Delete All IP"])
        msg_type_dropdown.activated[str].connect(self.msg_type_dropdown_active)

    def match_ui(self):
        # 1st Column Labels
        source_ip_label = QLabel('Source IP')
        destination_ip_label = QLabel('Destination IP')
        source_port_label = QLabel('Source Port')
        destination_port_label = QLabel('Destination Port')
        protocol_label = QLabel('Protocol')

        # 2nd Column Labels
        seq_no_label = QLabel('Sequence Number')
        msg_type_label = QLabel('Message Type')
        timeout_val_label = QLabel('Timeout Value')
        export_name_label = QLabel('Export Name')
        class_name_label = QLabel('Class Name')
        priority_label = QLabel('Priority')

        # 3rd Column Labels
        host_ip_label = QLabel('Host IP')
        host_port_label = QLabel('Host Port')
        host_protocol_label = QLabel('Host Protocol')

        # 2nd Column edit boxs
        self.source_ip_edit = QLineEdit()
        self.destination_ip_edit = QLineEdit()
        self.source_port_edit = QLineEdit()
        self.destination_port_edit = QLineEdit()

        # Dropdown for protocol
        protocol_dropdown = QComboBox(self)
        protocol_dropdown.addItem("TCP")
        protocol_dropdown.addItem("UDP")
        protocol_dropdown.addItem("ICMP")
        protocol_dropdown.activated[str].connect(self.protocol_dropdown_active)


        # Add Tuple Widgets
        self.grid.addWidget(source_ip_label, 1, 0)
        self.grid.addWidget(self.source_ip_edit, 1, 1)

        self.grid.addWidget(destination_ip_label, 2, 0)
        self.grid.addWidget(self.destination_ip_edit, 2, 1)

        self.grid.addWidget(source_port_label, 3, 0)
        self.grid.addWidget(self.source_port_edit, 3, 1)

        self.grid.addWidget(destination_port_label, 4, 0)
        self.grid.addWidget(self.destination_port_edit, 4, 1)

        self.grid.addWidget(protocol_label, 5, 0)
        self.grid.addWidget(protocol_dropdown, 5, 1)

        self.source_port_edit.setDisabled(False)
        self.destination_port_edit.setDisabled(False)

        # Settings Widgets
        self.seq_no_edit = QLineEdit()
        #self.msg_type_edit = QLineEdit()
        self.timeout_val_edit = QLineEdit()
        self.export_name_edit = QLineEdit()
        self.class_name_edit = QLineEdit()
        self.priority_edit = QLineEdit()

        # Add Settings Widgets
        self.grid.addWidget(self.seq_no_edit, 1, 3)
        #self.grid.addWidget(self.msg_type_edit, 2, 3)
        self.grid.addWidget(self.timeout_val_edit, 3, 3)
        self.grid.addWidget(self.export_name_edit, 4, 3)
        self.grid.addWidget(self.class_name_edit, 5, 3)
        self.grid.addWidget(self.priority_edit, 6, 3)

        # Add Settings Widgets Labels
        self.grid.addWidget(seq_no_label, 1, 2)
        self.grid.addWidget(msg_type_label, 2, 2)
        self.grid.addWidget(timeout_val_label, 3, 2)
        self.grid.addWidget(export_name_label, 4, 2)
        self.grid.addWidget(class_name_label, 5, 2)
        self.grid.addWidget(priority_label, 6, 2)

        # Host Widgets
        self.host_ip_edit = QLineEdit()
        self.host_port_edit = QLineEdit()
        host_protocol_dropdown = QComboBox(self)
        host_protocol_dropdown.addItem("TCP")
        host_protocol_dropdown.addItem("UDP")
        host_protocol_dropdown.activated[str].connect(self.host_protocol_active)

        # Add Host Widgets
        self.grid.addWidget(self.host_ip_edit, 1, 5)
        self.grid.addWidget(self.host_port_edit, 2, 5)
        self.grid.addWidget(host_protocol_dropdown, 3, 5)
        # Add Host Widgets Label
        self.grid.addWidget(host_ip_label, 1, 4)
        self.grid.addWidget(host_port_label, 2, 4)
        self.grid.addWidget(host_protocol_label, 3, 4)

        # Send Button
        self.send_button = QPushButton("Send", self)
        self.grid.addWidget(self.send_button, 7, 6)
        self.send_button.setEnabled(True)

    def protocol_dropdown_active(self, text):
        if text == 'TCP':
            self.protocol = 6
            self.source_port_edit.setDisabled(False)
            self.destination_port_edit.setDisabled(False)
        elif text == 'UDP':
            self.protocol = 17
            self.source_port_edit.setDisabled(False)
            self.destination_port_edit.setDisabled(False)
        elif text == 'ICMP':
            self.protocol = 1
            self.source_port_edit.setDisabled(True)
            self.destination_port_edit.setDisabled(True)
        else:
            self.protocol = 0

    def host_protocol_active(self, text):
        if text == 'TCP':
            self.host_protocol = 'TCP'
        elif text == 'UDP':
            self.host_protocol = 'UDP'

    def msg_type_dropdown_active(self, text):
        if text == 'Add':
            self.msg_type = 0
        elif text == 'Delete Matching':
            self.msg_type = 1
        elif text == 'Delete All IP':
            self.msg_type = 2

    def send_message_handler(self):
        name = self.source_ip_edit.text()
        if name == '':
            QMessageBox.information(self, 'Empty Field', "Need Input.")
            return
        else:
            # Get Inputs
            inputs = self.get_var()

            fake = FCN.__new__(FCN)
            # Convert to byte hex
            print(inputs.srcip)
            c_msg = fake.create_msg_payload(cli_inputs=inputs)
            c_temp = fake.create_template(payload_len=len(c_msg))
            c_header = fake.create_header(cli_inputs=inputs,
                                          payload_len=len(c_msg),
                                          template_len=len(c_temp))
            message = binascii.a2b_hex(c_header + c_temp +c_msg)
            fake.send_message(message, inputs)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = FCNGui()
    screen.show()

    sys.exit(app.exec_())