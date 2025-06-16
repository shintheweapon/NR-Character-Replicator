import sys
import os
import shutil
import pathlib

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from functools import wraps

import lib_func


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


LIST_CODE_REVENANT = [
    '5050',
    '5150',
    '5250',
    '5350',
    '5550',
    '5650'
]

LIST_CODE_DUCHESS = [
    '5030',
    '5130',
    '5230',
    '5330',
    '5530',
    '5670'
]

LIST_CODE_GUARDIAN = [
    '5010',
    '5110',
    '5210',
    '5310',
    '5510',
    '5610'
]

LIST_CODE_IRONEYE = [
    '5020',
    '5120',
    '5220',
    '5320',
    '5520',
    '5620'
]

LIST_CODE_RAIDER = [
    '5040',
    '5140',
    '5240',
    '5340',
    '5540',
    '5640'
]

LIST_CODE_RECLUSE = [
    '5060',
    '5160',
    '5260',
    '5360',
    '5560',
    '5660'
]

LIST_CODE_EXECUTOR = [
    '5070',
    '5170',
    '5270',
    '5370',
    '5570',
    '5630'
]

LIST_CODE_WYLDER = [
    '5000',
    '5100',
    '5200',
    '5300',
    '5500',
    '5600'
]

LIST_CHAR_CODE_ALL = [
    LIST_CODE_REVENANT,
    LIST_CODE_DUCHESS,
    LIST_CODE_GUARDIAN,
    LIST_CODE_IRONEYE,
    LIST_CODE_RAIDER,
    LIST_CODE_RECLUSE,
    LIST_CODE_EXECUTOR,
    LIST_CODE_WYLDER
]

DICT_CHAR = dict(zip(LIST_CHAR_NAME_FOR_COMBOBOX, LIST_CHAR_CODE_ALL))

DICT_CHAR_NAME_CHN = dict(zip(LIST_CHAR_NAME_FOR_COMBOBOX, LIST_CHAR_NAME_CHN))

DICT_CHAR_NAME_ENG = dict(zip(LIST_CHAR_NAME_FOR_COMBOBOX, LIST_CHAR_NAME_ENG))

class Ui(QtWidgets.QMainWindow):

    def __init__(self, str_path_file_ui):

        super(Ui, self).__init__()

        uic.loadUi(str_path_file_ui, self)

        self.cBox_base_char.addItems(LIST_CHAR_NAME_FOR_COMBOBOX)

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
                str_title='Please select the output folder for the renamed files. 请选择输出文件夹'
            )
        )

        self.btn_rename.clicked.connect(self.rename)

        self.show()


    def listNewFilename(
            self,
            list_str_filepath_old,
            list_char_code_old, list_char_code_new,
            str_char_new, str_path_dir_output
        ):

        list_new_filename = []

        str_temp = ''

        for i in list_str_filepath_old:

            for j, k in zip(list_char_code_old, list_char_code_new):

                if j in i:

                    str_temp = i.replace(j, k)

                    str_temp = lib_func.strGetFilename(str_temp, True)

                    str_temp = os.path.join(
                        str_path_dir_output, str_char_new, 'parts', str_temp
                        )

                    list_new_filename.append(str_temp)

        return list_new_filename


    def makeNewCharFile(self, list_str_path_file_char_old, list_str_path_file_char_new):

        str_temp = list_str_path_file_char_new[0]

        str_temp = lib_func.strGetParPath(str_temp)

        path_dir_char_new = pathlib.Path(str_temp)

        path_dir_char_new.mkdir(parents=True, exist_ok=True)

        for i, j in zip(list_str_path_file_char_old, list_str_path_file_char_new):

            # shutil.copyfile(i, j)
            shutil.copy2(i, j)

            str_temp = 'Renaming 重命名中: ' + i + ' -> ' + j

            print(str_temp)


    def printLog(self, str_msg):
        '''
        Print messages to the GUI console.
        '''

        str_temp = ''

        str_temp = self.te_console.toPlainText()

        str_temp += (
            lib_func.strLocalTime('%Y-%m-%d, %H:%M:%S') + ':' + str_msg + '\n'
        )

        self.te_console.setText(str_temp)

        # auto scroll to end
        self.te_console.moveCursor(QtGui.QTextCursor.End)

        QApplication.sendPostedEvents()


    def rename(self):

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

        str_base_character = self.cBox_base_char.currentText()

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
            'Renaming! Please do not close the program!'
            + '正在重命名！请勿关闭程序！'
            )

        for key in DICT_CHAR:

            list_str_path_char_new = []

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
