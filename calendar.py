import colors
from datetime import datetime
from persiantools.jdatetime import JalaliDate

# dorsa modules
import dorsa_datetime
from  dorsa_datetime   import  get_date
from  dorsa_datetime   import  get_time
from  dorsa_datetime   import  get_datetime
from  dorsa_datetime   import  get_days_per_month

#constants
from CONSTANTS import NUMBER_OF_ROWS, NUMBER_OF_DAYS_IN_WEEK, NUMBER_OF_MONTH_IN_A_YEAR


#### turn miladi week to persion week, monday is start of week, in persian calendar saturday is 0
week_transform = {0:2, 1:3, 2:4, 3:5, 4:6, 5:0, 6:1}


class Calendar:
    def __init__(self, persian = True):
        """calendar class (doing all the date related functions of calendar)

        Args:
            persian (bool, optional): is it persian calendar. Defaults to True.
        """

        # flags and variables
        self.persian = persian
        self.selected_date = ''


        # get date of today
        self.what_day_is_today()


        if self.persian:
            # persian months
            self.months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

        else:
            #miladi monthes
            self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        

        # set year, month, day
        self.update_year_month_day(year=self.today_year, month_index=self.today_month, day=self.today_day)

  
    def what_day_is_today(self):
        """find the date of today
        """
        
        # all in string
        today = get_date(persian=self.persian, folder_path=False)
        self.today_day = str(today[8:10])
        self.today_month = int(today[5:7])
        self.today_year = str(today[0:4])
        if self.persian:
            print('today in persian calendar is: ', today)
        else:
            print('today in miladi calendar is: ', today)


    def update_year_month_day(self, year, month_index, day):
        """update day, month and year

        Args:
            year (str): year string
            month_index (int): month index 1<=index<=12
            day (str): day string 1<=day<=31
        """

        # everything is string, except indexes

        # check if input is valid, and then update values

        if (day is not None) and isinstance(int(day), int) and 1<=int(day)<=31:
            self.day = str(day)
        
        if (month_index is not None) and (1 <= month_index <= 12): 
            self.month_index = month_index
            self.month_name = str(self.months[self.month_index - 1])
        
        if (year is not None) and (int(year) >= 0) :
            self.year_name = str(year)


    def check_days_per_month(self):
        """how days are in this month?

        Returns:
            int: number of days in this month
        """
        
        return get_days_per_month(month = self.month_index, persian=self.persian)


    def find_first_day_of_this_month(self):
        """find what day of week is the first day of this month

        Returns:
            int: a number between 0 and 6 showing what day of week is first of this month
            for miladi calendar monday 0
            for persian calendar saturday 0
        """

        if self.persian:
            first_of_this_month = JalaliDate(int(self.year_name), int(self.month_index), 1).to_gregorian().weekday()
            # trun to iraninan calendar, since weekday() has 0 for monday
            return  week_transform[first_of_this_month]
            
        else:
            date = datetime(int(self.year_name), int(self.month_index), 1)
            return date.weekday()


    def check_leap_year(self):
        """is it leap year?

        Returns:
            boolean: is it leap year or not
        """
        if self.persian:
            return self.is_it_a_leap_year_jalali()
        else:
            return self.is_it_a_leap_year_miladi()


    ##### check if it is a leap year jalali
    def is_it_a_leap_year_jalali(self):
        """calculating leap year for persian calendar

        Returns:
            boolean: is it leap year or not
        """
        year = int(self.year_name)
        left_over = (year % 33)
        if (left_over == 1) or (left_over ==5) or (left_over ==9) \
                or (left_over ==13) or (left_over ==18) or (left_over ==22) \
                or (left_over ==26) or (left_over ==30):
            
            return True
        else:
            return False


    ##### check if it is a leap year miladi
    def is_it_a_leap_year_miladi(self):
        """calculating leap year for miladi calendar

        Returns:
            boolean: is it leap year or not
        """
        
        year = int(self.year_name)
        
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False



if __name__ == "__main__":
  
    # persian calendar testing
    print('persian calendar testing: ')
    calendar_obj = Calendar(persian=True)
    print('days per month: ', calendar_obj.check_days_per_month())
    print('is it leap year: ',calendar_obj.check_leap_year())
    print('first day of this month: ',calendar_obj.find_first_day_of_this_month())
    
    # miladi calendar testing
    print('miladi calendar testing: ')
    calendar_obj = Calendar(persian=False)
    print('days per month: ', calendar_obj.check_days_per_month())
    print('is it leap year: ',calendar_obj.check_leap_year())
    print('first day of this month: ',calendar_obj.find_first_day_of_this_month())

