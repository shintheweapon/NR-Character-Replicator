'''
Function library module for NR Character Replicator
'''

import os
import sys
import pathlib
import time
import fnmatch

from functools import wraps

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui

def strGetFilename(str_path, bool_with_ext=False):
    """
    Get the filename from a path. With or without the extension.

    Parameters
    ----------
    str_path : str
        The path of the file.

    bool_with_ext : boolean
        Whether to include the extension.

        True = include the extension
        False = not include the extension

        Default = False

    Returns
    -------
    str_filename : str
        The filename from the path.
    """

    str_filename = ''

    if bool_with_ext:

        str_filename = os.path.basename(str_path)

    else:

        str_filename = os.path.basename(str_path)

        str_filename = os.path.splitext(str_filename)[0]

    return str_filename


def strGetParPath(str_scr):
    '''
    This function returns the parent path of the given path.

    Parameters
    ----------
    str_scr : str
        The given path.

    Returns
    -------
    str_temp : str
        The parent path of the given path.

    References
    -----------
    https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number

    Examples
    --------
    .. code:: python

        >>> str_par = os.path.join('c:/', 'parent', 'scr')
        >>> str_par
        'c:/parent\\scr'
        >>> strGetParPath(str_par)
        'c:\\parent'
        >>>
    '''

    str_temp = os.path.abspath(os.path.join(str_scr, os.pardir))

    return str_temp


def strLocalTime(str_format):
    """
    Return the system local date and time as a string according to the
    given format.

    Parameters
    ----------
    str_format : str
        Date/Time code format.

        Example: '%Y-%m-%d, %H:%M:%S'

    Returns
    -------
    str_date_time : str
        Formatted system local date time string.
    """

    str_date_time = time.strftime(str_format, time.localtime())

    return str_date_time


def boolPathExists(str_path, bool_dir=False):
    """
    Check whether the path exists or not. Can check both file's and dir's.

    If exists, return True; else, return False.

    Parameters
    ----------
    str_path : str
        The path to check.

    bool_dir : boolean
        Is the path a dir?
        True = it's a dir
        False = it is not a dir

        Default = False

    Returns
    -------
    bool_exists : boolean
        True = path exists
        False = path not found
    """

    if not bool_dir:

        bool_exists = os.path.isfile(str_path)

    else:

        bool_exists = os.path.isdir(str_path)

    return bool_exists


def listGetPathRecursive(str_scr, str_filter):
    '''
    This function walks every sub dir inside the given source dir and
    returns the files' paths that matches the file filter.

    Parameters
    ----------
    str_scr : str
        The given source dir.

    str_filter : str
        The file filter. Need to be in the format of '*.filter'.

    Returns
    -------
    list_paths : list
        The list containing all the file paths found. Or
        and empty list.

    Example
    -------
    .. code:: python

        >>> str_dir = '.../Global variables'
        >>> listGetPathRecursive(str_dir, '*.txt')
        ['.../Global variables\\Strong\\Strong_A_for_PSCAD.txt', '.../Global variables\\Strong\\Strong_B_for_PSCAD.txt']
        >>> listGetPathRecursive(str_dir, '*.add')
        []
        >>> listGetPathRecursive(str_dir, 'txt')
        []
        >>>
    '''

    bool_temp = boolPathExists(str_scr, bool_dir=True)

    if bool_temp:

        list_paths = []

        for root, dirnames, filenames in os.walk(str_scr):

            for filename in fnmatch.filter(filenames, str_filter):

                list_paths.append(os.path.join(root, filename))

        return list_paths

    else:

        print('Source directory not found.')

        return list()


def filename2QLineEdit(func):
    '''
    Decorator for putting filename to a line edit from the
    actually function return.
    '''

    @wraps(func)
    def wrapper(obj, str_lename, *args, **kwargs):
        '''
        Put the function return string into a Qt line edit.
        '''

        str_filename = func(
            obj, str_lename, *args, **kwargs)

        # Pass the filename to QLineEdit
        if str_filename:

            obj_le = getattr(obj, str_lename)

            obj_le.setText(str_filename)

        else:

            pass

    return wrapper


@filename2QLineEdit
def browseDir(
    obj, str_lename, str_title,
    qwidget=None,
    str_dir='', options=QFileDialog.ShowDirsOnly
):
    '''
    This function uses QFileDialog.getSaveFileName to get a
    filename and then use the decorator function
    "filename2QLineEdit()"
    to put the filename into a Qt line edit.

    Parameters
    ----------
    str_lename : str
        The object name of the line edit to put the filename into.

    str_title : str
        The title for the file dialogue window.

    str_filter : str
        File filter.

        Default = 'All Files (*)'

    qwidget : obj
        Parent Qt widget.

        Default = None

    str_dir : str
        Default directory.

        Default = ''

    options : Qt file dialogue options
        Qt file dialogue options.

        Default = QFileDialog.Options()

    Returns
    -------
    filename : str
        The full file path of the selected file.
    '''

    filename = QFileDialog.getExistingDirectory(
        qwidget,
        str_title,
        str_dir,
        options=options
    )

    return filename


def decorateMsgbox(str_type):
    '''
    This is a decorator for different QMessageBox.

    The message box will be executed at end.

    The decorated function should return a QMessageBox object for
    decoration.

    Parameters
    ----------
    str_type : type of the message box, str

        'info' or 'information' = QMessageBox.Information

        'critical' = QMessageBox.Critical

        'warning' = QMessageBox.Warning

        'question' = QMessageBox.Question

        else = QMessageBox.Information

    Returns
    -------
    The inner function.
    '''

    # If this grows much bigger, than may consider aliasing
    dict_map = {'info': QMessageBox.Information,
                'information': QMessageBox.Information,
                'critical': QMessageBox.Critical,
                'warning': QMessageBox.Warning,
                'question': QMessageBox.Question}

    def inner_func(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            msgBox = func(*args, **kwargs)

            box_type = dict_map.get(str_type, QMessageBox.Information)

            msgBox.setIcon(box_type)

            msgBox.exec_()

        return wrapper

    return inner_func


@decorateMsgbox('critical')
def msgError(str_title, str_text):
    '''
    This is a decorated function for making a Critical type QMessageBox.

    Parameters
    ----------
    str_title : str
        The title for the message box.

    str_text : str
        The main text for the message box.

    Returns
    -------
    The message box object to be decorated.
    '''

    msgBox = QMessageBox()

    msgBox.setWindowTitle(str_title)

    msgBox.setText(str_text)

    msgBox.setStandardButtons(QMessageBox.Ok)

    return msgBox


@decorateMsgbox('info')
def msgInfo(str_title, str_text):
    '''
    This is a decorated method for making a Information type QMessageBox.

    Parameters
    ----------
    str_title : str
        The title for the message box.

    str_text : str
        The main text for the message box.

    Returns
    -------
    The message box object to be decorated.
    '''

    msgBox = QMessageBox()

    msgBox.setWindowTitle(str_title)

    msgBox.setText(str_text)

    msgBox.setStandardButtons(QMessageBox.Ok)

    return msgBox