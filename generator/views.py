from django.shortcuts import render
#from datetime import datetime
import datetime
import calendar
from openpyxl import load_workbook
from czech_holidays import holidays


# Create your views here.
def index(request):
    days_in_month = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)
    days_list = range(1, days_in_month[1] + 1)
    if request.method == 'POST':
        cruncher(dict(request.POST))


    return render(request, 'generator/index.html', {'days_list':days_list})


def cruncher(data_dict):
    """main function to create AIS"""

    #načte šablonu a aktivní list
    wb = load_workbook('generator/AIS_master.xlsx')
    ws = wb.active

    #vstupní data
    data = data_dict['date']
    data_clone = data

    #iteruje vstupními daty, modifikuje hodnotu dne po noční službě na "z_or_n1_next"
    for day_num, day in enumerate(data_clone):
        if day in ["z", "n1"] and day_num != len(data_clone):
            data_clone[day_num-1] = "z_or_n1_next"
    data = data_clone

    day_obj_list = []

    class Day():
        """objekt reprezentující každý den v měsící"""
        def __init__(self, day_num, occupation):
            self.day_num = day_num + 1 #number of the day in the month.
            self.occupation = occupation    #ev. "služba" at given day -d1,d2,d3,z,n1

            #today = datetime.date()
            self.date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, self.day_num)
            self.den_v_tydnu = self.date.weekday()
            self.svatek = self.date in holidays
            self.vikend = self.den_v_tydnu > 5
            self.post_night_shift = False

            self.nan_pd = [" 07:00", "15:30", "11:30", "12:00",  8]


        def populator(self, ais_workbook_ws):
            """funkce, která podle charakteristik objektu vyplňuje šablonu AIS"""

            def basic_iterator():
                #to_iter = ["C", "D", "E", "F", "J"]
                for column_num in range(len(to_iter)):
                    sel_cell = to_iter[column_num] + str(20 + self.day_num)
                    ais_workbook_ws[sel_cell] = day_obj.nan_pd[column_num]
                    pass

            if self.occupation in ["d1", "d2"]:
                if self.vikend and not self.svatek:
                    self.input = [" 07:00", "19:00", 12, 12, 12]
                    to_iter = ["C", "D","J", "R", "T"]
                elif self.svatek and not self.vikend:
                    self.input = [" 07:00", "19:00", 12, 12, 12]
                    to_iter = ["C", "D", "J", "O", "U"]
                elif self.vikend and self.svatek:
                    self.input = [" 07:00", "19:00", 12, 12, 12, 12]
                    to_iter = ["C", "D", "J", "R", "T", "U"]
                else:
                    self.input = [" 07:00", "19:00", "11:30", "12:00", 11.5, 3.5]
                    to_iter = ["C", "D", "E", "F", "J", "O"]
            elif self.occupation == "d3":
                if self.svatek and self.vikend:
                    self.input = [" 07:00", "19:00", 4, 4, 4, 4]
                    to_iter = ["C", "D", "J", "R", "T", "U"]
                elif self.svatek and not self.vikend:
                    self.input = [" 07:00", "19:00", 4, 4, 4]
                    to_iter = ["C", "D", "J", "O", "U"]
                else:
                    self.input = [" 07:00", "11:00", 4, 4, 4]
                    to_iter = ["C", "D", "J", "R", "T"]

            elif self.occupation in ["z", "n1"]:


    for x in data:
        day_obj_list.append(Day(data.index(x), x))

    #print(day_obj_list[0].day_num, day_obj_list[0].occupation)

    to_iter = ["C","D","E","F","J"]
    start_row = 21

    for day_obj in day_obj_list:
        print("first for")
        for column_num in range(len(to_iter)):
            print("second for")
            xxx = to_iter[column_num]+str(start_row)
            print("xxx: %s" %xxx)
            ws[xxx] = day_obj.nan_pd[column_num]
        start_row += 1

    wb.save("sample.xlsx")