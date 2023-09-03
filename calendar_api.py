from CONSTANTS import NUMBER_OF_ROWS, NUMBER_OF_DAYS_IN_WEEK, NUMBER_OF_MONTH_IN_A_YEAR



import calendar
class calendarAPI:
    def __init__(self, calendar_ui = None, persian = True):
        """API class for calendar

        Args:
            calendar_ui (ui file, optional): ui file. Defaults to None.
            persian (bool, optional): is it persian calendar. Defaults to True.
        """
        
        # ui object
        self.calendar_ui = calendar_ui

        # persian calendar flag
        self.persian = persian

        #calendar object
        self.calendar_obj = calendar.Calendar(persian=self.persian)

        # previous btn
        self.calendar_ui.button_connector(self.calendar_ui.pushButton_prev, self.go_prev_month)

        # forward btn
        self.calendar_ui.button_connector(self.calendar_ui.pushButton_next, self.go_next_month)

        # close btn
        self.calendar_ui.button_connector(self.calendar_ui.close_btn, self.close_app)

        # ok btn
        self.calendar_ui.button_connector(self.calendar_ui.ok_btn, self.return_selected_date)

        # cancle btn
        self.calendar_ui.button_connector(self.calendar_ui.cancle_btn, self.close_app)

        # go to today btn
        self.calendar_ui.button_connector(self.calendar_ui.btn_go_to_today, self.show_selected_date)

    
    def return_selected_date(self):
        """prints the selected date
        """
        print(self.calendar_ui.label_selected_date.text())
        self.close_app() 
    
    
    def show_selected_date(self):
        """makes string of selected date and sets it on a label in ui

        if you need the date in any other format, you should change here
        """
        
        # which btn has called the function?
        btn = self.calendar_ui.sender()

        # is it go to today btn?
        if btn.objectName() != 'btn_go_to_today':
            
            # one of day btns, get its text
            day = btn.text()
            self.calendar_obj.update_year_month_day(year=None, month_index=None, day = day)
        
        else:

            # go to today btn is clicked, go to today
            self.calendar_obj.what_day_is_today()

            # update date variables
            self.calendar_obj.update_year_month_day(year=str(self.calendar_obj.today_year), month_index=self.calendar_obj.today_month, day = self.calendar_obj.today_day)
            
            # update ui
            self.calendar_ui.update_ui()
        

        # show the selected date
        if (self.calendar_obj.year_name is not None) and (self.calendar_obj.month_index is not None) and (self.calendar_obj.day is not None):

            #string of selected date (if you need the date in other formats, change here)
            self.selected_date = self.calendar_obj.year_name +"/" + str(self.calendar_obj.month_index) + "/" + str(self.calendar_obj.day)
            self.calendar_ui.label_selected_date.setText(self.selected_date)
            # self.close_app() 
        else:
            self.calendar_ui.label_selected_date.setText('')
            self.selected_date = ''
            # self.close_app()



    def close_app(self):
        """this function closes the app
        """

        # close app window and exit the program
        self.calendar_ui.close()     
        

    def go_prev_month(self):
        """going back one month
        """
        
        # going back one month
        if self.calendar_obj.month_index > 1:    #if it is not the first month of year
            
            # go back one month
            month_index = self.calendar_obj.month_index - 1
            # update month and year variables 
            self.calendar_obj.update_year_month_day(year = None, month_index=month_index, day=None)
            #update ui
            self.calendar_ui.update_ui()

        else: # if it is first month of year, we should go back one year
            
            #go back one year, to last month
            year_name = str(int(self.calendar_obj.year_name) - 1)
            
            # update month and year variables 
            self.calendar_obj.update_year_month_day(year = year_name, month_index=NUMBER_OF_MONTH_IN_A_YEAR, day=None)
            
            # update ui
            self.calendar_ui.update_ui()

   
    def go_next_month(self):
        """going forward one month
        """

        # going forward one month
        if self.calendar_obj.month_index < NUMBER_OF_MONTH_IN_A_YEAR:
            
            # if it is not the last month of year, go forward
            month_index = self.calendar_obj.month_index + 1

            # update date variables
            self.calendar_obj.update_year_month_day(year=None, month_index=month_index, day = None)

            # update ui on the new month
            self.calendar_ui.update_ui()
        
        else: # if it is last month, go to first month of next year
            year_name = str(int(self.calendar_obj.year_name) + 1)

            #update date variables
            self.calendar_obj.update_year_month_day(year = year_name, month_index = 1, day = None)

            #update ui for new month data
            self.calendar_ui.update_ui()

        