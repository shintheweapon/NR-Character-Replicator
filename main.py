'''
An simple app for replicating one NR character's skins to all characters.
'''

import sys
import os
import shutil
import pathlib

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

import lib_func

# Constants for NR characters names
LIST_CHAR_NAME_FOR_COMBOBOX = [
    '复仇者 Revenant',
    '女爵 Duchess',
    '守护者 Guardian',
    '铁眼 Ironeye',
    '无赖 Raider',
    '隐士 Recluse',
    '执行者 Executor',
    '追踪者 Wylder'
]

LIST_CHAR_NAME_CHN = [
    '复仇者',
    '女爵',
    '守护者',
    '铁眼',
    '无赖',
    '隐士',
    '执行者',
    '追踪者'
]

LIST_CHAR_NAME_ENG = [
    'Revenant',
    'Duchess',
    'Guardian',
    'Ironeye',
    'Raider',
    'Recluse',
    'Executor',
    'Wylder'
]

# Constants for NR character IDs
LIST_ID_REVENANT = [
    '5050',
    '5150',
    '5250',
    '5350',
    '5550',
    '5650'
]

LIST_ID_DUCHESS = [
    '5030',
    '5130',
    '5230',
    '5330',
    '5530',
    '5670'
]

LIST_ID_GUARDIAN = [
    '5010',
    '5110',
    '5210',
    '5310',
    '5510',
    '5610'
]

LIST_ID_IRONEYE = [
    '5020',
    '5120',
    '5220',
    '5320',
    '5520',
    '5620'
]

LIST_ID_RAIDER = [
    '5040',
    '5140',
    '5240',
    '5340',
    '5540',
    '5640'
]

LIST_ID_RECLUSE = [
    '5060',
    '5160',
    '5260',
    '5360',
    '5560',
    '5660'
]

LIST_ID_EXECUTOR = [
    '5070',
    '5170',
    '5270',
    '5370',
    '5570',
    '5630'
]

LIST_ID_WYLDER = [
    '5000',
    '5100',
    '5200',
    '5300',
    '5500',
    '5600'
]

LIST_CHAR_ID_ALL = [
    LIST_ID_REVENANT,
    LIST_ID_DUCHESS,
    LIST_ID_GUARDIAN,
    LIST_ID_IRONEYE,
    LIST_ID_RAIDER,
    LIST_ID_RECLUSE,
    LIST_ID_EXECUTOR,
    LIST_ID_WYLDER
]

# Create NR character dictionaries
DICT_CHAR = dict(zip(LIST_CHAR_NAME_FOR_COMBOBOX, LIST_CHAR_ID_ALL))

DICT_CHAR_NAME_CHN = dict(zip(LIST_CHAR_NAME_FOR_COMBOBOX, LIST_CHAR_NAME_CHN))

DICT_CHAR_NAME_ENG = dict(zip(LIST_CHAR_NAME_FOR_COMBOBOX, LIST_CHAR_NAME_ENG))

# Main window class
class Ui(QtWidgets.QMainWindow):

    def __init__(self, str_path_file_ui):
        '''
        Initialisation, takes a Qt Designer UI file to initialise the
        app window.

        Parameters
        ----------
        str_path_file_ui : str
            Full path of the UI file.

        Returns
        -------
        None.
        '''

        super(Ui, self).__init__()

        # Load UI file
        uic.loadUi(str_path_file_ui, self)

        # Load NR character list to the dropdown
        self.cBox_base_char.addItems(LIST_CHAR_NAME_FOR_COMBOBOX)

        # Button connections
        self.btn_browse_dir_base_chr.clicked.connect(
            lambda: lib_func.browseDir(
                self,
                str_lename='le_path_dir_base_char',
                str_title='Where is the base character''s file folder? 请选择母板角色的文件夹'
            )
        )

        self.btn_browse_dir_output.clicked.connect(
            lambda: lib_func.browseDir(
                self,
                str_lename='le_dir_output',
                str_title='Please select the output folder for the replicated files. 请选择输出文件夹'
            )
        )

        self.btn_rename.clicked.connect(self.replicate)

        self.show()


    def listNewFilename(
            self,
            list_str_filepath_old,
            list_char_ID_old, list_char_ID_new,
            str_char_new, str_path_dir_output
        ):
        '''
        This method creates the new file paths for all NR characters.

        It does not actually create the files.

        Parameters
        ----------
        list_str_filepath_old : list
            A list containing all the paths for the base character files.

        list_char_ID_old : list
            A list containing the skin IDs for the base character.

        list_char_ID_new : list
            A list containing the skin IDs for the new character.

        str_char_new: str
            Name of the new character. Will form part of the new paths.

        str_path_dir_output: str
            The output folder path.

        Returns
        -------
        list_new_filename : list
            A list containing the new file paths for the new files to be
            created.
        '''

        list_new_filename = []

        str_temp = ''

        # Replace NR character IDs in file paths and add the new file
        # paths to a list
        for i in list_str_filepath_old:

            for j, k in zip(list_char_ID_old, list_char_ID_new):

                if j in i:

                    str_temp = i.replace(j, k)

                    str_temp = lib_func.strGetFilename(str_temp, True)

                    str_temp = os.path.join(
                        str_path_dir_output, str_char_new, 'parts', str_temp
                        )

                    list_new_filename.append(str_temp)

        return list_new_filename


    def makeNewCharFile(
            self,
            list_str_path_file_char_old, list_str_path_file_char_new
        ):
        '''
        This method creates the new character files.

        Parameters
        ----------
        list_str_path_file_char_old : list
            A list containing all the file paths for the base character.

        list_str_path_file_char_new : list
            A list containing all the file paths for the new characters.

        Returns
        -------
        None
        '''

        # Get a new character file path
        str_temp = list_str_path_file_char_new[0]

        # Get parent path
        str_temp = lib_func.strGetParPath(str_temp)

        # Create the new folder for the new character files
        path_dir_char_new = pathlib.Path(str_temp)

        path_dir_char_new.mkdir(parents=True, exist_ok=True)

        # Carry out the replication
        for i, j in zip(list_str_path_file_char_old, list_str_path_file_char_new):

            # Copy file
            shutil.copy2(i, j)

            str_temp = 'Replicating 克隆中: ' + i + ' -> ' + j

            print(str_temp)


    def printLog(self, str_msg):
        '''
        This method prints messages to the GUI console.

        Parameters
        ----------
        str_msg : str
            Message to be printed to the GUI console.

        Returns
        -------
        None
        '''

        str_temp = ''

        str_temp = self.te_console.toPlainText()

        str_temp += (
            lib_func.strLocalTime('%Y-%m-%d, %H:%M:%S') + ':' + str_msg + '\n'
        )

        self.te_console.setText(str_temp)

        # Auto scroll to end
        self.te_console.moveCursor(QtGui.QTextCursor.End)

        QApplication.sendPostedEvents()


    def replicate(self):
        '''
        Main method that carries out the replication.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        # Check whether the path for the base character exist or not
        str_path_dir_base_char = self.le_path_dir_base_char.text()

        bool_path_base_char = lib_func.boolPathExists(str_path_dir_base_char, True)

        if bool_path_base_char:

            pass

        else:

            self.printLog(
                'Cannot find the folder for the base character! '
                + '找不到模板角色的文件夹！'
                )

            lib_func.msgError(
                'Base character folder not found!',
                'Cannot find the folder for the base character!\n' +
                '找不到模板角色的文件夹！'
            )

            return

        # Check whether the path for the output folder exist or not
        str_path_dir_output = self.le_dir_output.text()

        bool_path_dir_output = lib_func.boolPathExists(str_path_dir_output, True)

        if bool_path_dir_output:

            pass

        else:

            self.printLog('Cannot find the output folder! 找不到输出文件夹！')

            lib_func.msgError(
                'Output folder not found!',
                'Cannot find the output folder!\n' +
                '找不到输出文件夹！'
            )

            return

        # Get the selected base character
        str_base_character = self.cBox_base_char.currentText()

        # Walk through all the subfolders to find all DCX files
        list_str_path_file_char_old = lib_func.listGetPathRecursive(
            str_path_dir_base_char, '*.dcx'
        )

        # Exit if no DCX found
        if not list_str_path_file_char_old:

            self.printLog('No DCX file is found! 没有找到任何DCX文件！')

            lib_func.msgError(
                'ERROR',
                'No DCX file is found! 没有找到任何DCX文件！'
                )

            return

        else:

            self.printLog('The following DCX files are found 已找到以下的DCX文件\n' +
                      '\n'.join(list_str_path_file_char_old)
                      )

        self.printLog(
            'Replicating! Please do not close the program!'
            + '正在克隆！请勿关闭程序！'
            )

        # The actual replication
        for key in DICT_CHAR:

            list_str_path_char_new = []

            # Check output folder names in Chinese or English by
            # checking the two radio buttons
            if self.rd_btn_output_dir_chn.isChecked():

                list_str_path_char_new = self.listNewFilename(
                    list_str_path_file_char_old,
                    DICT_CHAR[str_base_character], DICT_CHAR[key],
                    DICT_CHAR_NAME_CHN[key], str_path_dir_output
                )

            else:

                list_str_path_char_new = self.listNewFilename(
                    list_str_path_file_char_old,
                    DICT_CHAR[str_base_character], DICT_CHAR[key],
                    DICT_CHAR_NAME_ENG[key], str_path_dir_output
                )

            # Empty list if base character not matched
            if not list_str_path_char_new:

                self.printLog('Base character not matched! 模板角色不正确！')

                lib_func.msgError(
                    'ERROR',
                    'Base character not matched! 模板角色不正确！'
                    )

                return

            else:

                self.makeNewCharFile(
                    list_str_path_file_char_old, list_str_path_char_new
                    )

                # Update the progress bar
                progress = list(DICT_CHAR.keys()).index(key) + 1

                progress = progress / len(DICT_CHAR) * 100

                self.progressBar.setValue(int(progress))

        self.printLog('Done! 已完成！')

        lib_func.msgInfo('Done', 'Done! 已完成！')



if __name__ == "__main__":

    str_path_cwd = os.path.realpath(__file__)

    str_path_cwd = lib_func.strGetParPath(str_path_cwd)

    ui_file_name = os.path.join(str_path_cwd, 'gui_NRCharReplicate.ui')

    app = QtWidgets.QApplication(sys.argv)

    window = Ui(ui_file_name)

    app.exec_()
