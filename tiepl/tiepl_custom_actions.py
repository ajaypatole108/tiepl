import frappe
from frappe.utils import getdate, add_days, date_diff, cstr
from datetime import datetime, timedelta, date
from frappe.desk import query_report

# @frappe.whitelist()
# def disable_employee_attendance(employee):

#     # with open('disable_attendance.log','a') as f:
#     #     f.write(str(employee))
#     #     f.write("\n")

#     today = getdate()

#     number_of_working_days_to_check = 2

#     employee = employee

#     two_working_days_ago = get_working_day_before(today, number_of_working_days_to_check)
#     # print("two_working_days_ago: ",two_working_days_ago)

#     attendance_not_marked = frappe.db.sql(
#                                             f"""
#                                                 SELECT e.name
#                                                 FROM `tabEmployee` e
#                                                 WHERE e.name NOT IN (
#                                                     SELECT a.employee
#                                                     FROM `tabAttendance` a
#                                                     WHERE a.attendance_date BETWEEN '{two_working_days_ago}' AND '{today}'
#                                                 )
#                                                 AND e.employee = '{employee}'
#                                                 AND e.status = 'Active'
#                                             """,as_dict=True
#                                         )
#     # print(attendance_not_marked)

#     if attendance_not_marked:
#         # doc.set("save_disabled", 1)
#         return 0
#         # frappe.throw(cstr('Attendance requests cannot be saved because attendance has not been marked for the last {} working days (excluding holidays and weekends).'.format(number_of_working_days_to_check)))

# def get_working_day_before(date, days):
#     # Calculate working days (excluding weekends and holidays) before a given date
#     working_days_before = 0
#     while working_days_before < days:
#         date -= timedelta(days=1)
#         print("date: ",date)
#         if is_working_day(date):
#             working_days_before += 1
#     return date

# def is_working_day(date):
#     # This example considers weekends (Sunday) as non-working days
#     # print("date.weekday() : ",date.weekday())
#     # print()
#     if date.weekday() >= 6:  #6 = Sunday
#         return False
#     return True



@frappe.whitelist()
def disable_employee_attendance(employee):

    today = str(getdate())
    # today = str(date.fromisoformat('2023-11-15'))

    number_of_working_days_to_check = 2

    employee = employee

    # logging - 1
    with open('Attendance_Request.log','a') as f:
                f.write('-------------------------'+ str(today) + '-----------------------------')
                f.write('\n')
                f.write(str(employee))
                f.write('\n')

    two_working_days_ago = get_working_day_before(date.fromisoformat(today), number_of_working_days_to_check)

    attendance_not_marked = frappe.db.sql(
                                            f"""
                                                SELECT e.name
                                                FROM `tabEmployee` e
                                                WHERE e.name NOT IN (
                                                    SELECT a.employee
                                                    FROM `tabAttendance` a
                                                    WHERE a.attendance_date BETWEEN '{two_working_days_ago}' AND '{date.fromisoformat(today)}'
                                                )
                                                AND e.employee = '{employee}'
                                                AND e.status = 'Active'
                                            """,as_dict=True
                                        )
    print('attendance_not_marked: ',attendance_not_marked)

    # logging - 2
    with open('Attendance_Request.log','a') as f:
                f.write('attendance_not_marked: '+ str(attendance_not_marked))
                f.write('\n\n')

    if len(attendance_not_marked) != 0:
        with open('Attendance_Request.log','a') as f:
                f.write('return: 0')
                f.write('\n\n')
        return 0

def get_working_day_before(date, days):
    working_days_before = 0
    while working_days_before < days:
        date -= timedelta(days=1)

        if is_working_day(date):
            # logging -3
            with open('Attendance_Request.log','a') as f:
                f.write('Working Days: '+ str(date))
                f.write('\n')
            print('working Day: ',date)
            working_days_before += 1
    return date


# This code is for testing from console
@frappe.whitelist()
def is_working_day(date):
    # db_name = '_f4b2b25149ddf8b5'
    # db_host = 'custom_host'
    # db_user = 'custom_user'
    # db_password = 'adminpass'

    # frappe.connect(db_name=db_name)
    # frappe.connect(site='tiepl.dhupargroup.com')

    year = date.year
    holiday_list = frappe.db.sql(f"""
                                    SELECT holiday_date from `tabHoliday`
                                    WHERE parent = {year}
                                    ORDER BY idx
                                """,as_list=1)
    print(holiday_list)
    with open('Attendance_Request.log','a') as f:
        f.write('Holiday List: '+ str(holiday_list))
        f.write('\n')

    list = []
    for i in holiday_list:
        list.append(i[0].strftime('%Y-%m-%d'))

    if str(date) in list:
        return False
    return True









def get_holiday_list():
    # frappe.init(db_name='_f4b2b25149ddf8b5')
    # frappe.connect(db_name='_f4b2b25149ddf8b5')
    
    year = date.fromisoformat('2023-11-21').year
    print(year)
    # Fetch holiday records from the database using SQL
    holiday_list1 = frappe.db.sql(f"""
                                SELECT holiday_date
                                FROM `tabHoliday`
                                WHERE parent = '{year}'
                                ORDER BY idx
                            """,as_list=True)
    return holiday_list1,len(holiday_list1)