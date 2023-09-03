# ui files
calendar_ui_file = './calender.ui'

# imports
import sys
import os
from PySide6.QtUiTools import QUiLoader
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
from functools import partial

# calendar module
import calendar
from calendar_api import calendarAPI

from CONSTANTS import NUMBER_OF_ROWS, NUMBER_OF_DAYS_IN_WEEK, NUMBER_OF_MONTH_IN_A_YEAR
from styleSheets import stylesheet_for_today, stylesheet_for_today_en, stylesheet_for_btns, stylesheet_for_btns_en, stylesheet_for_lbls_en, stylesheet_for_title_en




class calenderUi(QtWidgets.QMainWindow):
    def __init__(self, persian = True, ui_file = None):
        """UI class for calendar, generate Qt UI for calendar

        Args:
            persian (bool, optional): is it persian calendar. Defaults to True.
            ui_file (qt ui file, optional): ui file desiged in qt designer. Defaults to None.
        """
          
        
        super(calenderUi, self).__init__()
        
        uic.loadUi(ui_file, self)
        
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))

        # persian or miladi
        self.persian= persian

        if not self.persian:
            # not persian calendar, update headers of weekdays
            self.update_header_weekdays()
            
            # change calendar language and fonts
            self.update_font_and_language()
            

        # api
        self.calendar_api = calendarAPI(calendar_ui=self, persian=self.persian)
        
        # ui window position
        self.pos_ = self.pos()
        self._old_pos = None

        # make necessory changes to ui
        self.update_ui()

    
    
    @staticmethod
    def button_connector( btn: QtWidgets.QPushButton, func):
        """Connects a PyQt Button clicked event into a function

        Args:
            btn (QtWidgets.QPushButton): PyQt button object
            func (_type_): function that execute when event happend
        """
        btn.clicked.connect(partial( func ))

    

    def mousePressEvent(self, event):
        """mouse press event for moving window

        Args:
            event (_type_): mouse press
        """
        # accept event only on top and side bars and on top bar
        if event.button() == QtCore.Qt.LeftButton and not self.isMaximized() and event.pos().y()<=self.header.height():
            self._old_pos = event.globalPos()
    
    
    def mouseReleaseEvent(self, event):
        """mouse release event for stop moving window

        Args:
            event (_type_): mouse release
        """
        if event.button() == QtCore.Qt.LeftButton:
            self._old_pos = None
    

    def mouseMoveEvent(self, event):
        """mouse move event for moving window

        Args:
            event (_type_): mouse left click drag
        """
        if self._old_pos is None:
            return
        delta = QtCore.QPoint(event.globalPos() - self._old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._old_pos = event.globalPos()


    def update_header_weekdays(self):
        """update week days when milladi calendar is loaded
        """
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in range(NUMBER_OF_DAYS_IN_WEEK):
            exec("self.label_weekday_%s.setText(weekdays[i])" %(i))
            exec("self.label_weekday_%s.setStyleSheet(stylesheet_for_lbls_en)" %(i))
            


    def update_font_and_language(self):
        """update texts and stylesheets for btns and labels in ui when miladi calendar is built
        """
        
        # change layout direction
        self.btn_grid.setLayoutDirection(QtCore.Qt.RightToLeft)

        # update label texts and stylesheets
        self.calendar_name_label.setText('Calendar')
        self.calendar_name_label.setStyleSheet(stylesheet_for_title_en)
        self.btn_go_to_today.setText('Go To Today')
        self.btn_go_to_today.setStyleSheet(stylesheet_for_lbls_en)
        self.cancle_btn.setText('Cancle')
        self.cancle_btn.setStyleSheet(stylesheet_for_lbls_en)
        self.ok_btn.setText('Ok')
        self.ok_btn.setStyleSheet(stylesheet_for_lbls_en)
        self.label_selected_date_name.setText('Selected Date:')
        self.label_selected_date_name.setStyleSheet(stylesheet_for_lbls_en)
        self.label_selected_date.setStyleSheet(stylesheet_for_lbls_en)
        


    def update_ui(self):
        
        """update the whole UI, btns and labels
        """
        #check number of days in month
        self.number_days_in_this_month = self.calendar_api.calendar_obj.check_days_per_month()

        # date buttons
        self.make_day_btns()
        
        #update month and year labels in ui
        self.year_label.setText(self.calendar_api.calendar_obj.year_name)
        self.month_label.setText(self.calendar_api.calendar_obj.month_name)
        
        if not self.persian:
            self.year_label.setStyleSheet(stylesheet_for_title_en)
            self.month_label.setStyleSheet(stylesheet_for_title_en)

    
    def make_day_btns(self):
        """make day btns for the selected month
        """


        # what day is the first day of month?
        self.first_of_this_month = self.calendar_api.calendar_obj.find_first_day_of_this_month()
        
        number_of_days_in_this_month = self.calendar_api.calendar_obj.check_days_per_month()
        
        month_days_counter = 1

        # connect btns to their function
        self.connect_btns_to_func()

        # go through rows
        for i in range(NUMBER_OF_ROWS):
            
            #go through days in week
            for j in range(NUMBER_OF_DAYS_IN_WEEK):

                if month_days_counter <= number_of_days_in_this_month:

                    if i==0: # in fisrt week of month, find the first day of month

                        if self.first_of_this_month > j : # disable btns before first day of month
                            self.disable_and_disappear_btn(i,j)
                            
                        else: #from starting day of month , enable and number the btns
                            self.enable_and_appear_btn(i, j, month_days_counter)
                            month_days_counter = month_days_counter + 1

                    else: # enable btns in the remaining weeks of that month, 
                        self.enable_and_appear_btn(i, j, month_days_counter)
                        month_days_counter = month_days_counter + 1

                else: # days of month are finished, disable the rest of the btns
                    self.disable_and_disappear_btn(i, j)

    
    def is_it_today_btn(self, row_position, column_position, number):
        """check if this is the btn showing today

        Args:
            row_position (int): position in row of weeks in y=ui
            column_position (int): position in weeks (columns)
            number (int): the date in the month
        """

        # is this btn today's date?
        if number == int(self.calendar_api.calendar_obj.today_day) and \
                            self.calendar_api.calendar_obj.month_index==self.calendar_api.calendar_obj.today_month and\
                         str(self.calendar_api.calendar_obj.year_name)==str(self.calendar_api.calendar_obj.today_year):
            # if it is, set a stylesheet on it
            if self.persian:
                exec("self.btn_%s%s.setStyleSheet('%s')" %(row_position,column_position, stylesheet_for_today))
            else:
                exec("self.btn_%s%s.setStyleSheet('%s')" %(row_position,column_position, stylesheet_for_today_en))

    
    def connect_btns_to_func(self):

        """connect date btns to showing the date function
        """

        # connect all date btns to a function that returens the date of that btn
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_DAYS_IN_WEEK):
                exec('self.btn_%s%s.clicked.connect(self.calendar_api.show_selected_date)' %(i,j))


    def enable_and_appear_btn(self, row_position, column_position, number):
        """enables and sets style on day btns

        Args:
            row_position (int): position in row of weeks in y=ui
            column_position (int): position in weeks (columns)
            number (int): the date in the month
        """
        
        exec('self.btn_%s%s.setText(str(number))' %(row_position,column_position))
        exec('self.btn_%s%s.setEnabled(True)' %(row_position,column_position))
        if self.persian:
            exec("self.btn_%s%s.setStyleSheet(stylesheet_for_btns)" %(row_position,column_position))
        else:
            exec("self.btn_%s%s.setStyleSheet(stylesheet_for_btns_en)" %(row_position,column_position))

        # check if it is today btn and set its stylesheet
        self.is_it_today_btn(row_position, column_position, number)


    def disable_and_disappear_btn(self, row_position, column_position):
        """disables and disappears btns in ui that are not used for this month

        Args:
            row_position (int): position in row of weeks in y=ui
            column_position (int): position in weeks (columns)
        """
        exec('self.btn_%s%s.setText(str(''))' %(row_position,column_position))
        exec('self.btn_%s%s.setEnabled(False)' %(row_position,column_position))
        exec('self.btn_%s%s.setStyleSheet(\'border:None; background-color:None;\')' %(row_position,column_position))


    def show_message(self, label_name=None, text='', level=0, clearable=True):
        """this function is used to show input message in message label,
         also there is a message level determining the color of label, and a timer to clear meesage after a while

        Args:
            label_name (str, optional): name of label. Defaults to None.
            text (str, optional): desired text. Defaults to ''.
            level (int, optional): level of importance of error or warning. Defaults to 0.
            clearable (bool, optional): does this massage disappear after a while. Defaults to True.
        """

        level = 1 if level<0 or level>2 else level

        # convert label name to pyqt object if is string
        label_name = self.msg_label if label_name is None else label_name
        label = eval('self.%s' % (label_name)) if isinstance(label_name, str) else label_name

        try:
            # set message
            if text != '':
                if level == 0:
                    label.setText(text)
                    label.setStyleSheet('padding-left: 10px; padding-right: 10px; background: %s; color:white;' % (colors.SUCCESS_GREEN))
                #
                if level == 1:
                    label.setText(text)
                    label.setStyleSheet('padding-left: 10px; padding-right: 10px; background: %s; color:white;' % (colors.WARNING_YELLOW))
                #
                if level == 2:
                    label.setText(text)
                    label.setStyleSheet('padding-left: 10px; padding-right: 10px; background: %s; color:white;' % (colors.FAILED_RED))

                # timer to clear the message
                if clearable:
                    QtCore.QTimer.singleShot(5000, lambda: self.show_message(label_name=label_name))

            # clear the message after timeout
            else:
                label.setText('')
                label.setStyleSheet('')
        
        except Exception as e:
            print(e)
            return




if __name__ == "__main__":
    
    # # persian calendar
    # app = QtWidgets.QApplication(sys.argv)
    # win = calenderUi(persian=True, ui_file=calendar_ui_file)
    # win.show()
    # sys.exit(app.exec())

    # miladi calendar
    app = QtWidgets.QApplication(sys.argv)
    win = calenderUi(persian=False, ui_file=calendar_ui_file)
    win.show()
    sys.exit(app.exec())