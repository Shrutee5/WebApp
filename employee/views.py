from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
import calendar
from django.db.models import Sum
from datetime import timedelta
import csv
from django.db.models import Q
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def HomePage(request):
    return render(request, 'index.html')


def register(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        ei = request.POST['emailid']
        pwd = request.POST['pwd1']
        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=ei, password=pwd)
            EmployeeDetail.objects.create(user=user,empcode=ec)
            error = "no"
        except:
            error = "yes"
    return render(request,'registration.html',locals())

def employeeLogin(request):
    error = ""

    if request.method == "POST":
        u = request.POST['emailid']
        pwd = request.POST['password']
        user = authenticate(username=u, password=pwd)
        if user is not None :
            login(request, user)
            error = "no"
        else:
            error = "yes"
    return render(request, 'employeeLogin.html', locals())

def employeeHome(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    emp = EmployeeDetail.objects.get(user=request.user)
    return render(request, 'employeeHome.html',locals())


def viewProfile(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    if not employee.pfno:
        employee.pfno = "Not Applicable"
    if not employee.uan:
        employee.uan = "Not Applicable"
    if not employee.esicip:
        employee.esicip = "Not Applicable"
    return render(request, 'viewProfile.html', locals())

def Logout(request):
    logout(request)
    return redirect('HomePage')


def adminLogin(request):
    return render(request, 'adminLogin.html')

def empChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    error = ""
    user = request.user
    if request.method == "POST":
        cp = request.POST['currentpwd']
        newp = request.POST['newpwd']
        try:
            if user.check_password(cp):
                user.set_password(newp)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    
    return render(request, 'employeeChangePwd.html',locals())

def adminLogin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_superuser:
                login(request,user)
                error = "no"
            else :
                error = "yes"
        except:
            error = "yes"
        
    return render(request, 'adminLogin.html', locals())


def adminHome(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    return render(request, 'adminHome.html')


def adminChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    error = ""
    user = request.user
    if request.method == "POST":
        cp = request.POST['currentpwd']
        newp = request.POST['newpwd']
        try:
            if user.check_password(cp):
                user.set_password(newp)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    
    return render(request, 'adminChangePwd.html',locals())


def allEmployeeDetails(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    employee = EmployeeDetail.objects.all()
    return render(request, 'allEmployeeDetails.html',locals())


def attendanceReport(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    emp = Attend.objects.all()
    cnt = emp.count()
    print(cnt)
    return render(request, 'allEmpAttendance.html',{'emp':emp,'cnt':cnt})

def viewEmployeeAttendance(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    emp1 = Attendance.objects.filter(employee = request.user)
    cnt = emp1.count()
    emp = Attendance.objects.get(employee = request.user)
    return render(request, 'viewEmployeeAttendance.html',locals())

'''
def applyForLeave(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    error = ""
    u = request.user
    emp = EmployeeDetail.objects.get(user=u)
    if request.method == "POST":
        lT = request.POST['leaveType']
        sD = request.POST['startDate']
        eD = request.POST['endDate']
        r = request.POST['reason']
        try:
            employee = ApplyForLeave.objects.create(user=u, leave_type = lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
            employee.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'applyForLeave.html',{'emp':emp,'error':error})
'''
def approveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()
    return redirect('viewLeaveApplication')

def disapproveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()
    return redirect('viewLeaveApplication')

def viewLeaveApplication(request):
    user = request.user
    # Get the specific leave application if application_id is provided

    managed_leave_apps = ApplyForLeave.objects.filter(man=user).order_by('-start_date')
    context = {
        'managed_leave_apps':managed_leave_apps,
    }

    return render(request, 'viewLeaveApplication.html', context)


def viewEmpLeaveApplication(request):
    user = request.user
    employee = ApplyForLeave.objects.filter(user=user).order_by('-start_date')
    return render(request, 'viewEmpLeaveApplication.html',locals())



def markAttend(request):
    man = 0
    if not request.user.is_authenticated:
        return redirect('empLogin')
    user = request.user
    attendance_date = date.today()
    flag = 0
    if attendance_date.weekday() == 6:
        flag=1
    attendance = Attend.objects.filter(user=user, date = attendance_date).first()
    if attendance :
        pass
    else:
        attendance = Attend.objects.create(user=user, date=attendance_date, is_present=0)
    emp = EmployeeDetail.objects.get(user=user)
    employee_attendance = []
    absent_count = 0
    present_count = 0
    on_leave_count = 0
    attendance_status = 0 if attendance is None else attendance.is_present
    if attendance_status == 0:
        absent_count +=1
    elif attendance_status == 1:
        present_count+=1
    elif attendance_status == 2:
        on_leave_count+=1
    employee_attendance.append({
        'employee':emp,
        'attendance':attendance_status
    })
    if emp.designation == "Manager":
        man = 1
        emps = EmployeeDetail.objects.filter(manage=user.username)
                # Create a list to store the is_present status of employees
        
        
        for e in emps:
            attendance_record = Attend.objects.filter(user=e.user, date=attendance_date).first()
            attendance_status = 0 if attendance_record is None else attendance_record.is_present
            if attendance_record:
                if attendance_record.is_present == 1:
                    present_count += 1
                elif attendance_record.is_present == 2:
                    on_leave_count += 1
            if attendance_record is None :
                absent_count +=1
    
            employee_attendance.append({
        'employee': e,
        'attendance': attendance_status
    })
        #print(employee_attendance)
        #print(absent_count)
        #print(on_leave_count)
        #print(present_count)
    else:
        man = 0
        pass
    return render(request,'markAttend.html',locals())

def updateAttendanceSummary(request):
    try:
        attendance_data = AttendanceSummary.objects.get(user=request.user)
        cnt = 1
    except:
        attendance_data = AttendanceSummary.objects.filter(user=request.user)
        cnt = 2
    return render(request, 'attendSummary.html',locals())

def markA(request):
    attendM = Attend.objects.get(user=request.user, date=str(date.today()))
    dat = date.today()
    # Get the selected month and year from the attendance_date
    selected_month = dat.month
    selected_year = dat.year

    # Update or create the attendance summary
    summary, created = AttendanceSummary.objects.get_or_create(
        user=request.user,
        month=selected_month,
        year=selected_year,
    )
    attendM.is_present = 1
    summary.days_present +=1
    summary.days_total = calendar.monthrange(selected_year, selected_month)[1]
    # Get the calendar for the specified year and month
    cal = calendar.monthcalendar(selected_year, selected_month)
    # Count the number of Sundays (which are represented by weekday 6)
    sundays = sum(1 for week in cal if week[calendar.SUNDAY] != 0)
    summary.sundays = sundays
    attendM.save()
    summary.save()
    return redirect('markAttend')

# to see attendance report of particular user
def viewAttendance(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    user = request.user
    attendance_data = AttendanceSummary.objects.filter(user=user)
    return render(request, 'viewAttendance.html',locals())

# to see attendance report of all the users
def viewAttendanceReport(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    attendance_data = AttendanceSummary.objects.all()
    cnt = attendance_data.count()
    return render(request, 'viewAttendanceReport.html', locals())


def paySlip(request):
    emp = EmployeeDetail.objects.get(user=request.user)
    return render(request, 'paySlip.html', locals())


def generateSlip(request):
    user = request.user
    if request.method == 'POST':
        selected_month = int(request.POST.get('month'))
        selected_year = int(request.POST.get('year'))

        # Get the calendar for the specified month and year
        cal = calendar.monthcalendar(selected_year, selected_month)

        saturdays = 0
        sundays = 0

        for week in cal:
            # Saturday is represented by index 5 and Sunday by index 6 in the week
            saturdays += 1 if week[calendar.SATURDAY] != 0 else 0
            sundays += 1 if week[calendar.SUNDAY] != 0 else 0

        # Query the attendance records for the employee for the selected month
        # Assuming the field 'is_present' indicates the employee's presence on that day
        print(saturdays, sundays)
    return render(request, 'generateSlip.html',locals())


def addEmpDetails(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    error = ""
    if request.method == "POST":
        ei = request.POST['emailid']
        dept = request.POST['empDep']
        des = request.POST['empDes']
        cont = request.POST['empContact']
        doj = request.POST['jdate']
        gend = request.POST['gender']
        man = request.POST['manager']
        dobb = request.POST['db']
        an = request.POST['adharno']
        pfn = request.POST['pf']
        un = request.POST['uann']
        eip = request.POST['esic']
        bn = request.POST['bname']
        acn = request.POST['acno']
        ic = request.POST['ifscno']
        etype = request.POST['employeeType']
        leaveD = request.POST['ldate']
        stat = request.POST['status']
        cname = request.POST['company']
        user = User.objects.get(username=ei)
        employee = EmployeeDetail.objects.get(user=user)
        employee.empdept = dept
        employee.designation =des
        employee.contact = cont
        employee.gender = gend
        employee.manage = man
        employee.adhar = an
        employee.pfno = pfn
        employee.uan = un
        employee.esicip = eip
        employee.bank = bn
        employee.ifsc = ic
        employee.accountno = acn
        employee.emptype = etype
        employee.status = stat
        employee.company_name = cname
        employee.joiningDate = doj
        if dobb :
            employee.dob = dobb
        if dobb == '' :
            employee.dob = None
        if leaveD:
            employee.leavingDate = leaveD
        if leaveD == '' :
            employee.leavingDate = None
        if des == "Manager":
            user.is_staff = 1
            user.save()
        try:
            employee.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'addEmpDetails.html', locals())


#not using this function
def approveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()
    return redirect('viewLeaveApplication')

#not using this function
def disapproveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()
    return redirect('viewLeaveApplication')

def approveLeave2(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()

    # Mark the attendance for the approved leave
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    if leave.leave_type == 'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            attendSummary.paid_leave += 1
            attendance.save()
            attendSummary.save()
        attendSummary.biMOB = attendSummary.biMOB - len(date_range)
        
        
        
    if start_date.month == end_date.month and leave.leave_type != 'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            if leave.leave_type != "Optional Holiday" :
                attendSummary.paid_leave += 1
            else :
                attendSummary.unpaid_leave +=1
            attendance.save()
            attendSummary.save()
    if start_date.month != end_date.month and leave.leave_type != 'Bi-monthly Offs':
        attendSummary1, created1 = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year,
                                                                 days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        print(attendSummary1)
        attendSummary2, created2 = AttendanceSummary.objects.get_or_create(user=user, month=end_date.month, year=end_date.year,
                                                                days_total = calendar.monthrange(end_date.year, end_date.month)[1])
        for date in date_range:
            if date.month == start_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary1.paid_leave +=1
                else:
                    attendSummary1.unpaid_leave +=1
                attendance.save()
                attendSummary1.save()
            if date.month == end_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary2.paid_leave +=1
                else:
                    attendSummary2.unpaid_leave +=1
                attendance.save()
                attendSummary2.save()

    return redirect('viewLeaveApplication')

def disapproveLeave2(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()

    # Mark the attendance for the disapproved leave as 0
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    emp = EmployeeDetail.objects.get(user=user)
    if leave.leave_type == "Earned Leave":
        emp.earnedLeaveB += len(date_range)
        emp.save()
    elif leave.leave_type == "Sick Leave":
        emp.sickLeaveB += len(date_range)
        emp.save()
    elif leave.leave_type == "Freedom From Covid Leave":
        emp.ffcB += len(date_range)
        emp.save()
    elif leave.leave_type == "Maternity Leave":
        emp.maternityLB += len(date_range)
        emp.save()
    elif leave.leave_type == "Optional Holiday (OH)":
        emp.oH2B += len(date_range)
        emp.save()
    elif leave.leave_type == "Optional Holiday":
        emp.oHB += len(date_range)
        emp.save()
    elif leave.leave_type ==  'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year)
        attendSummary.biMOB += len(date_range)
        attendSummary.save()
    
    for date in date_range:
        attendance, created = Attend.objects.get_or_create(user=user, date=date)
        attendance.is_present = 0
        attendance.save()

    return redirect('viewLeaveApplication')

'''
def applyForLeave2(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    
    error = ""
    u = request.user
    emp = EmployeeDetail.objects.get(user=u)
    dat = date.today()
    attendSummary, created = AttendanceSummary.objects.get_or_create(user=u, month = dat.month, year = dat.year,
                                                                        days_total = calendar.monthrange(dat.year, dat.month)[1])

    if request.method == "POST":
        lT = request.POST['leaveType']
        sD = request.POST['startDate']
        eD = request.POST['endDate']
        r = request.POST['reason']
        # Convert the start_date and end_date strings to datetime objects
        start_date = datetime.strptime(sD, '%Y-%m-%d')
        end_date = datetime.strptime(eD, '%Y-%m-%d')
        # Get all the dates between start_date and end_date, excluding Sundays
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
        print(len(date_range))
        if lT == 'Sick Leave':
            balanceD = emp.sickLeaveB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                emp.sickLeaveB = balanceD
                emp.save()
                error = "no"
        elif lT == 'Earned Leave':
            balanceD = emp.earnedLeaveB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                emp.earnedLeaveB = balanceD
                emp.save()
                error = "no"
        elif lT == 'Freedom From Covid Leave':
            balanceD = emp.ffcB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                emp.ffcB = balanceD
                emp.save()
                error = "no"
        elif lT == 'Maternity Leave':
            balanceD = emp.maternityLB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                emp.maternityLB = balanceD
                emp.save()
                error = "no"
        elif lT == 'Optional Holiday (OH)':
            balanceD = emp.oH2B
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                emp.oH2B = balanceD
                emp.save()
                error = "no"
        elif lT == 'Optional Holiday':
            balanceD = emp.oHB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                emp.oHB = balanceD
                emp.save()
                error = "no"
        elif lT == 'Bi-monthly Offs':
            if start_date.month == end_date.month:
                balanceD = attendSummary.biMOB
                if len(date_range) > balanceD:
                    error = "yes"
                if len(date_range) <= balanceD:
                    employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                    balanceD -= len(date_range)
                    attendSummary.biMOB = balanceD
                    attendSummary.save()
                    error = "no"


    return render(request, 'applyForLeave.html', locals())
'''



def staffSalary(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = StaffSalary.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.salary_csv.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)

    return render(request,'StaffSalary.html',locals())

def update_fields(request):
    if request.method == 'POST':
        empcode = request.POST.get('0')  # Get the empcode from the hidden input
        print(empcode)
        employee_detail_instance = EmployeeDetail.objects.get(empcode=empcode)
        staff,created = StaffSalary.objects.get_or_create(empcode=employee_detail_instance)

        # Update the fields based on the form data
        staff.basic = request.POST.get('1')  # Use proper indexes for other fields
        staff.hra = request.POST.get('2')
        staff.specialAll = request.POST.get('3')
        staff.grossS = request.POST.get('4')
        staff.syear = request.POST.get('5')
        staff.save()

        return redirect('staffSalary')  # Redirect back to the salary page





def employee_salary_detail(request):
    try:
        employee_detail = EmployeeDetail.objects.get(user=request.user)
        staff_salary = StaffSalary.objects.get(empcode=employee_detail)
    except (EmployeeDetail.DoesNotExist, StaffSalary.DoesNotExist):
        employee_detail = None
        staff_salary = None


    return render(request, 'employee_salary_detail.html', locals())

def OpenIncentive(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = Incentive.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.inc_file.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)
    # Process CSV data and apply calculations
    for row in csv_data:
        reds_per = int(row[4])
        inc1=0
        if reds_per <= 20 :
            inc1 = 5
        elif reds_per > 20 and reds_per <= 30 :
            inc1 = 4
        elif reds_per > 30 and reds_per <= 40 :
            inc1 = 3
        elif reds_per > 40 :
            inc1 = 2
        
        # Replace the inc1 value in the corresponding row
        row[6] = str(inc1)  # Assuming inc1 column is at index 5
        row[7] = str(f"{int(row[6])*int(row[2]):.2f}")
        #print(row[6])

        nps = int(row[8].strip('%'))
        inc2=0
        if nps <= 50 :
            inc2 = 2
        elif nps >50 and nps <= 60:
            inc2 = 3
        elif nps >60 and nps <= 70:
            inc2 = 4
        elif nps > 70 :
            inc2 = 5
        
        row[9] = str(inc2)
        row[10] = str(f"{int(row[9])*int(row[2]):.2f}")
        qrs = int(row[11].strip('%'))
        inc3=0
        if qrs <= 60 :
            inc3 = 2
        elif qrs > 60 and qrs <= 70:
            inc3 = 3
        elif qrs > 70 and qrs <= 80 :
            inc3 = 4
        elif qrs > 80 :
            inc3 = 5
        
        row[12] = str(inc3)
        row[13] = str(f"{int(row[12])*int(row[2]):.2f}")
        row[14] = str(int(row[6])+ int(row[9]) + int(row[12]))
        row[15] = str(f"{float(row[7]) + float(row[10]) + float(row[13]):.2f}")
        row[17] = str(f"{int(row[16])*2*int(row[14]):.2f}")
        row[19] = str(f"{round(int(row[18])*0.25*int(row[14])):.2f}")
        #print(row[18])
        row[21] = str(f"{float(row[15])+ float(row[17]) + float((row[19])):.2f}")
        #print(row[20])
        if row[22] != '':
            row[23] = str(f"{float(row[21]) + float(row[22]):.2f}")
        else:
            row[23] = str(f"{float(row[21]):.2f}")
        row[24] = str(f"{round(float(row[23])*0.1):.2f}")
        row[25] = str(f"{float(row[23]) - float(row[24]):.2f}")



    context = {
        'csv_data': csv_data,
        'column_names': column_names,
    }

    return render(request, 'Incentive.html', context)

def OpenDoctorIncentive(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = DoctorIncentive.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.inc_file.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)
    selected_month = ''
    selected_year = ''
    column_names.append('Month')
    column_names.append('Year')
    month_dict = {'':'','1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', 
                  '10':'October', '11':'November', '12':'December'}
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
    for row in csv_data:
        row.append(month_dict[selected_month])
        row.append(selected_year)
        reds_per = int(row[4].strip('%'))
        inc1=0
        if reds_per <= 20 :
            inc1 = 30
        elif reds_per > 20 and reds_per <= 30 :
            inc1 = 24
        elif reds_per > 30 and reds_per <= 40 :
            inc1 = 18
        elif reds_per > 40 :
            inc1 = 12
        
        # Replace the inc1 value in the corresponding row
        row[5] = str(inc1)  # Assuming inc1 column is at index 5
        row[6] = str(f"{int(row[5])*int(row[1]):.2f}")
        nps = int(row[7].strip('%'))
        inc2=0
        if nps <= 50 :
            inc2 = 12
        elif nps >50 and nps <= 60:
            inc2 = 18
        elif nps >60 and nps <= 70:
            inc2 = 24
        elif nps > 70 :
            inc2 = 30
        
        row[8] = str(inc2)
        row[9] = str(f"{int(row[8])*int(row[1]):.2f}")

        qrs = int(row[10].strip('%'))
        inc3=0
        if qrs <= 60 :
            inc3 = 12
        elif qrs > 60 and qrs <= 70:
            inc3 = 18
        elif qrs > 70 and qrs <= 80 :
            inc3 = 24
        elif qrs > 80 :
            inc3 = 30
        
        row[11] = str(inc3)
        row[12] = str(f"{int(row[11])*int(row[1]):.2f}")
        row[13] = str(int(row[5])+ int(row[8]) + int(row[11]))
        row[14] = str(f"{float(row[6]) + float(row[9]) + float(row[12]):.2f}")
        row[16] = str(f"{round(int(row[13])*0.25*int(row[15])):.2f}")
        row[17] = str(f"{float(row[14]) + float(row[16]):.2f}")
        if row[18] != '':
            row[19] = str(f"{float(row[17]) + float(row[18]):.2f}")
        else:
            row[19] = str(f"{float(row[17]):.2f}")
        row[20] = str(f"{round(float(row[19])*0.1):.2f}")
        row[21] = str(f"{float(row[19]) - float(row[20]):.2f}")


    return render(request, 'doctorIncentive.html', locals())

def OpenDietIncentive(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = DietIncentive.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.diet_file.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)
# Update csv_data with selected_month and selected_year
    for row in csv_data:
        reds_per = int(row[5].strip('%'))
        inc1=0
        if reds_per <= 20 :
            inc1 = 10
        elif reds_per > 20 and reds_per <= 30 :
            inc1 = 8
        elif reds_per > 30 and reds_per <= 40 :
            inc1 = 6
        elif reds_per > 40 :
            inc1 = 4
        # Replace the inc1 value in the corresponding row
        row[6] = str(inc1)  # Assuming inc1 column is at index 5
        row[7] = str(f"{int(row[6])*int(row[2]):.2f}")
        nps = int(row[8].strip('%'))
        inc2=0
        if nps <= 50 :
            inc2 = 4
        elif nps >50 and nps <= 60:
            inc2 = 6
        elif nps >60 and nps <= 70:
            inc2 = 8
        elif nps > 70 :
            inc2 = 10
        
        row[9] = str(inc2)
        row[10] = str(f"{int(row[9])*int(row[2]):.2f}")

        qrs = int(row[11].strip('%'))
        inc3=0
        if qrs <= 60 :
            inc3 = 4
        elif qrs > 60 and qrs <= 70:
            inc3 = 6
        elif qrs > 70 and qrs <= 80 :
            inc3 = 8
        elif qrs > 80 :
            inc3 = 10
        
        row[12] = str(inc3)
        row[13] = str(f"{int(row[12])*int(row[2]):.2f}")
        row[14] = str(int(row[6])+ int(row[9]) + int(row[12]))
        row[15] = str(f"{float(row[7]) + float(row[10]) + float(row[13]):.2f}")
        row[17] = str(f"{round(int(row[16])*2*int(14)):.2f}")
        row[19] = str(f"{round(int(row[18])*0.25*int(row[14])):.2f}")
        row[21] = str(f"{float(row[15]) + float(row[17]) + float(row[19]):.2f}")
        row[22] = str(f"{round(float(row[21])*0.1):.2f}")
        row[23] = str(f"{float(row[21]) - float(row[22]):.2f}")


    return render(request, 'dietIncentive.html', locals())


def salaryCalculation1(request):
    selected_month1 = 'August'
    selected_year = 2023
    month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    selected_month = month_dict[selected_month1]
    # Retrieve StaffSalary and AttendanceSummary data for the selected month and year
    staff_data = StaffSalary.objects.select_related('empcode__user', 'empcode').filter(syear=selected_year).all()
    attendance_data = AttendanceSummary.objects.select_related('user').filter(month=selected_month, year=selected_year)

    # Create a dictionary to store attendance data by user ID
    attendance_dict = {attendance.user_id: attendance for attendance in attendance_data}

    # Combine data for the same employees
    combined_data = []
    for staff in staff_data:
        user_id = staff.empcode.user_id
        if user_id in attendance_dict:
            attendance = attendance_dict[user_id]
            combined_data.append((staff, attendance))
    return render(request, 'salaryCalculation.html',locals())


def update_doctor_fields(request):
    return redirect('update_doctor_fields')


def update_exercise_field(request):
    if request.method == 'POST':
        empcode = request.POST.get('0')  # Get the empcode from the hidden input
        print(empcode)
        employee_detail_instance = EmployeeDetail.objects.get(empcode=empcode)
        month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        selected_month = request.POST.get('26')
        selected_month = month_dict[selected_month]
        print(selected_month)
        selected_year = request.POST.get('27')
        staff,created = Incentive.objects.get_or_create(empcode=employee_detail_instance, imonth=selected_month, iyear=selected_year)
        staff.totAllottedPart = request.POST.get('2')
        staff.totalPartWI0 = request.POST.get('3')
        staff.totalPatientsInred = request.POST.get('4')
        staff.redsPer = request.POST.get('5')
        staff.inc1 = request.POST.get('6')
        staff.amt1 = request.POST.get('7')
        staff.nps = request.POST.get('8')
        staff.inc2 = request.POST.get('9')
        staff.amt2 = request.POST.get('10')
        staff.qrs = request.POST.get('11')
        staff.inc3 = request.POST.get('12')
        staff.amt3 = request.POST.get('13')
        staff.totalEffortInc = request.POST.get('14')
        staff.totalEffortIncPayout = request.POST.get('15')
        staff.vipParticipants = request.POST.get('16')
        staff.amtVipParticipants = request.POST.get('17')
        staff.intPartiAll = request.POST.get('18')
        staff.addPayIntParti = request.POST.get('19')
        amtIntPart1 = request.POST.get('20')
        if amtIntPart1:
            staff.amtIntPart = amtIntPart1
        else:
            staff.amtIntPart = 0.00
        staff.totalFinalPayout = request.POST.get('21')
        trp1 = request.POST.get('22')
        if trp1:
            staff.trp = trp1
        else:
            staff.trp = 0.00
        staff.addTotalFinalPayout = request.POST.get('23')
        staff.lessTDS = request.POST.get('24')
        staff.netPayout = request.POST.get('25')
        staff.save()
    return redirect('incentive')

def salaryCalculation(request):
    selected_month1 = 'August'
    selected_year = 2023
    month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    selected_month = month_dict[selected_month1]
    # Retrieve StaffSalary and AttendanceSummary data for the selected month and year
    staff_data = StaffSalary.objects.filter(syear=selected_year).all()
    return render(request, 'salaryCalculation.html',locals())

def add_salary_calculation(request):
    if request.method == 'POST':
        empcode = request.POST.get('empcode')
        #print(empcode)
        selected_month = request.POST.get('selected_month')
        #print(selected_month)
        selected_year = request.POST.get('selected_year')
        #print(selected_year)
        others_earning = request.POST.get('others')
        #print(others_earning)
        other_ded = request.POST.get('others_deduction')
        #print(other_ded)
        if others_earning :
            others_earning = float(others_earning)
        else :
            others_earning = 0.0
        if other_ded :
            other_ded = float(other_ded)
        else :
            other_ded = 0.0
        staff = StaffSalary.objects.get(empcode=empcode, syear= selected_year) ###########
        month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        selected_month = month_dict[selected_month]
        attendanceS= AttendanceSummary.objects.get(user=staff.empcode.user, month=selected_month, year=selected_year)
        total_days = attendanceS.days_present + attendanceS.paid_leave
        #print(total_days)
        bas_a = float(round((staff.basic * total_days)/attendanceS.days_total))
        #print(bas_a)
        hra_a_t = float(round((staff.hra * total_days)/attendanceS.days_total))
        #print(hra_a_t)
        spe_All_a = float(round((staff.specialAll * total_days)/attendanceS.days_total))
        #print(spe_All_a)
        gross_earn = bas_a + hra_a_t + spe_All_a + others_earning
        #print(gross_earn)
        pf_ded =float(round(min(staff.basic, 15000)*0.12))
        #print(pf_ded)
        esic_ded = 0.0
        if staff.grossS <= 21000:
            esic_ded = float(round(0.0075*gross_earn))
        #print(esic_ded)
        prof_tax = 0.0
        if staff.empcode.gender == 'Male':
            if selected_month == 2:
                prof_tax = float(300)
            elif gross_earn < float(7500):
                prof_tax = 0.0
            elif gross_earn >= float(7500) and gross_earn < float(10000):
                prof_tax = float(175)
            elif gross_earn >= 10000 :
                prof_tax = float(200)
        elif staff.empcode.gender == 'Female':
            if selected_month == 2:
                prof_tax = float(300)
            elif gross_earn < float(25000):
                prof_tax = 0.0
            elif gross_earn >= float(25000):
                prof_tax = float(200)
        #print(prof_tax)
        gross_ded = pf_ded + esic_ded + prof_tax + other_ded
        #print(gross_ded)
        net_sal = gross_earn - gross_ded
        #print(net_sal)
        salaryCal, created = SalaryCalculation.objects.get_or_create(
            staff_salary=staff,
            month=selected_month,
            year=selected_year,
        )
        salaryCal.paid_days = total_days + attendanceS.sundays
        salaryCal.basic_a = bas_a
        salaryCal.hra_a = hra_a_t
        salaryCal.specialAll_a = spe_All_a
        salaryCal.grossS_a = gross_earn
        salaryCal.others = others_earning
        salaryCal.pf_deduction = pf_ded
        salaryCal.esic_deduction = esic_ded
        salaryCal.other_deduction = other_ded
        salaryCal.gross_deduction = gross_ded
        salaryCal.netSalary = net_sal
        salaryCal.save()

    return redirect('salaryCalculation')


def viewExcerciseIncentive1(request):
    exerInc = ExcerciseInce1.objects.filter(month='August', year=2023)
    for emp in exerInc:
        reds = int(emp.calling_reds.strip('%'))
        if reds < 20 :
            emp.incentive_1 = 5
        elif reds >= 20 and reds < 30:
            emp.incentive_1 = 4
        elif reds >= 30 and reds < 40:
            emp.incentive_1 = 3
        elif reds >= 40:
            emp.incentive_1 = 2
        emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
        nps = int(emp.nps_percent.strip('%'))
        if nps < 50 :
            emp.incentive_2 = 2
        elif nps >= 50 and nps < 60 :
            emp.incentive_2 = 3
        elif nps >= 60 and nps < 70 :
            emp.incentive_2 = 4
        elif nps >= 70 :
            emp.incentive_2 = 5
        emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
        qrs = int(emp.qrs_percent.strip('%'))
        if qrs < 60 :
            emp.incentive_3 = 2
        elif qrs >= 60 and qrs < 70 :
            emp.incentive_3 = 3
        elif qrs >= 70 and qrs < 80 :
            emp.incentive_3 = 4
        elif qrs >= 70 :
            emp.incentive_3 = 5
        emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
        emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
        emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
        emp.amount_vip_participant = float(emp.total_effort_incentive * 2 * emp.vip_participants)
        emp.add_pay_for_international_participant = float(round(emp.international_participant_alloted * 0.25 * emp.total_effort_incentive))
        emp.total_effort_incentive_payout = emp.total_effort_payout + emp.amount_vip_participant + emp.add_pay_for_international_participant
        emp.final_effort_incentive_payout = emp.total_effort_incentive_payout + emp.trp
        emp.less_tds = float(round(emp.final_effort_incentive_payout * 0.1))
        emp.net_payout = emp.final_effort_incentive_payout - emp.less_tds
    return render(request, 'viewExcerciseIncentive.html',locals())

def viewExcerciseIncentive(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        exerInc = ExcerciseInce1.objects.filter(month=selected_month, year=selected_year)
        #print("Hello")
        #inc = exerInc[0].incentive_1
        for emp in exerInc:
            inc = emp.incentive_1
            #print(inc)
            if inc == 0 :
                #print("hi")
                reds = int(emp.calling_reds.strip('%'))
                if reds < 20 :
                    emp.incentive_1 = 5
                elif reds >= 20 and reds < 30:
                    emp.incentive_1 = 4
                elif reds >= 30 and reds < 40:
                    emp.incentive_1 = 3
                elif reds >= 40:
                    emp.incentive_1 = 2
                emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
                nps = int(emp.nps_percent.strip('%'))
                if nps < 50 :
                    emp.incentive_2 = 2
                elif nps >= 50 and nps < 60 :
                    emp.incentive_2 = 3
                elif nps >= 60 and nps < 70 :
                    emp.incentive_2 = 4
                elif nps >= 70 :
                    emp.incentive_2 = 5
                emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
                qrs = int(emp.qrs_percent.strip('%'))
                if qrs < 60 :
                    emp.incentive_3 = 2
                elif qrs >= 60 and qrs < 70 :
                    emp.incentive_3 = 3
                elif qrs >= 70 and qrs < 80 :
                    emp.incentive_3 = 4
                elif qrs >= 80 :
                    emp.incentive_3 = 5
                emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
                emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
                emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
                emp.amount_vip_participant = float(emp.total_effort_incentive * 2 * emp.vip_participants)
                emp.add_pay_for_international_participant = float(round(emp.international_participant_alloted * 0.25 * emp.total_effort_incentive))
                emp.total_effort_incentive_payout = emp.total_effort_payout + emp.amount_vip_participant + emp.add_pay_for_international_participant
                emp.final_effort_incentive_payout = emp.total_effort_incentive_payout + emp.trp
                emp.less_tds = float(round(emp.final_effort_incentive_payout * 0.1))
                emp.net_payout = emp.final_effort_incentive_payout - emp.less_tds
                emp.save()
            else :
                #print("Hello")
                pass
    return render(request, 'viewExcerciseIncentive.html',locals())

def viewDoctorIncentive(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        doctInc = DoctorInce1.objects.filter(month=selected_month, year=selected_year)
        #print("Hello")
        #inc = exerInc[0].incentive_1
        for emp in doctInc:
            inc = emp.incentive_1
            #print(inc)
            if inc == 0 :
                #print("hi")
                reds = int(emp.calling_reds.strip('%'))
                if reds < 20 :
                    emp.incentive_1 = 30
                elif reds >= 20 and reds < 30:
                    emp.incentive_1 = 24
                elif reds >= 30 and reds < 40:
                    emp.incentive_1 = 18
                elif reds >= 40:
                    emp.incentive_1 = 12
                emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
                nps = int(emp.nps_percent.strip('%'))
                if nps < 50 :
                    emp.incentive_2 = 12
                elif nps >= 50 and nps < 60 :
                    emp.incentive_2 = 18
                elif nps >= 60 and nps < 70 :
                    emp.incentive_2 = 24
                elif nps >= 70 :
                    emp.incentive_2 = 30
                emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
                qrs = int(emp.qrs_percent.strip('%'))
                if qrs < 60 :
                    emp.incentive_3 = 12
                elif qrs >= 60 and qrs < 70 :
                    emp.incentive_3 = 18
                elif qrs >= 70 and qrs < 80 :
                    emp.incentive_3 = 24
                elif qrs >= 80 :
                    emp.incentive_3 = 30
                emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
                emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
                emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
                emp.add_pay_for_international_participant = float(round(emp.total_effort_incentive * 0.25 * emp.international_participant_alloted))
                emp.total_effort_incentive_payout = emp.total_effort_payout + emp.add_pay_for_international_participant
                emp.final_effort_incentive_payout = emp.total_effort_incentive_payout + emp.trp
                emp.less_tds = float(round(emp.final_effort_incentive_payout * 0.1))
                emp.net_payout = emp.final_effort_incentive_payout - emp.less_tds
                emp.save()
            else :
                #print("Hello")
                pass
    return render(request, 'viewDoctorIncentive.html', locals())


def viewDietIncentive(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        diInc = DietInce1.objects.filter(month=selected_month, year=selected_year)
        #print("Hello")
        #inc = exerInc[0].incentive_1
        for emp in diInc:
            inc = emp.incentive_1
            #print(inc)
            if inc == 0 :
                #print("hi")
                reds = int(emp.calling_reds.strip('%'))
                if reds < 20 :
                    emp.incentive_1 = 10
                elif reds >= 20 and reds < 30:
                    emp.incentive_1 = 8
                elif reds >= 30 and reds < 40:
                    emp.incentive_1 = 6
                elif reds >= 40:
                    emp.incentive_1 = 4
                emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
                nps = int(emp.nps_percent.strip('%'))
                if nps < 50 :
                    emp.incentive_2 = 4
                elif nps >= 50 and nps < 60 :
                    emp.incentive_2 = 6
                elif nps >= 60 and nps < 70 :
                    emp.incentive_2 = 8
                elif nps >= 70 :
                    emp.incentive_2 = 10
                emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
                qrs = int(emp.qrs_percent.strip('%'))
                if qrs < 60 :
                    emp.incentive_3 = 4
                elif qrs >= 60 and qrs < 70 :
                    emp.incentive_3 = 6
                elif qrs >= 70 and qrs < 80 :
                    emp.incentive_3 = 8
                elif qrs >= 80 :
                    emp.incentive_3 = 10
                emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
                emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
                emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
                emp.amount_vip_participant = float(emp.vip_patients * 2 * emp.total_effort_incentive)
                emp.add_pay_for_international_participant = float(round(emp.international_participant_alloted * 0.25 * emp.total_effort_incentive))
                emp.total_effort_incentive_payout = emp.total_effort_payout + emp.amount_vip_participant + emp.add_pay_for_international_participant
                emp.less_tds = float(round(emp.total_effort_incentive_payout * 0.1))
                emp.net_payout = emp.total_effort_incentive_payout - emp.less_tds
                emp.save()
            else:
                pass
    return render(request, 'viewDietIncentive.html', locals())

'''
def professionalSalaryCalculation(request):
    error = 0
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
            
        
        salary_structure_exists = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year).exists()
        if salary_structure_exists :
            
            salary = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year)
            month_numbers = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}           
            # First, filter employees based on empType
            professional_employees = EmployeeDetail.objects.filter(emptype='Professional')
            # Get the User objects for professional employees
            professional_users = professional_employees.values_list('user', flat=True)

            # Then, filter AttendanceSummary objects for the selected month and year, related to professional employees
            attendSum = AttendanceSummary.objects.filter(
            user__in=professional_users,
            month=month_numbers[selected_month],
            year=selected_year
            )
            # After filtering the AttendanceSummary objects, retrieve the empcode for each employee
            employee_codes = EmployeeDetail.objects.filter(user__in=professional_users).values('user', 'empcode')
            # Create a dictionary to map user IDs to empcodes
            employee_code_map = {entry['user']: entry['empcode'] for entry in employee_codes}
            # Create a list of dictionaries containing the necessary information for rendering in the template
            attendSum_data = [
            {
            'employee_name': f"{emp.user.first_name} {emp.user.last_name}",
            'employee_code': employee_code_map[emp.user.id],
            'selected_month': selected_month,
            'selected_year': selected_year,
            'days_present': emp.days_present,
            'days_total': emp.days_total,
            }
            for emp in attendSum
            ]
            context = {
            'attendSum_data': attendSum_data,
            }
            
            error = 0
        else :
            error = 1

    return render(request, 'professionalSalaryCalculation.html', locals())
'''

def add_professional_salary_calculation(request):
    print("Hello")
    selected_month = request.POST.get('month')
    selected_year = request.POST.get('year')
    #return redirect('professionalSalaryCalculation')
    # Redirect to professionalSalaryCalculation with selected month and year as URL parameters
    return HttpResponseRedirect(reverse('professionalSalaryCalculation') + f'?month={selected_month}&year={selected_year}')


def getMonthnYear(request):
    error = 0
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
            
        
        salary_structure_exists = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year).exists()
        if salary_structure_exists :
            error = 0
        else:
            error = 1
        # Redirect to professionalSalaryCalculation with selected month and year as URL parameters
        return redirect(reverse('professionalSalaryCalculation') + f'?month={selected_month}&year={selected_year}')
    return render(request,'getMonthnYear.html',locals())

def professionalSalaryCalculation(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    s_year = 0
    e_year = 0
    print(selected_month)
    print(selected_year)
    # Check if there is a salary structure for the selected period
    # Construct the conditions for checking if the selected month and year are within the range
    if selected_month in ['January', 'February', 'March'] :
        e_year = int(selected_year)
        s_year = int(selected_year) -1
        
    elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
        s_year = int(selected_year)
        e_year = int(selected_year) + 1
    salary = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year)
    month_numbers = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}           
    # First, filter employees based on empType        
    professional_employees = EmployeeDetail.objects.filter(emptype='Professional')
    # Get the User objects for professional employees
    professional_users = professional_employees.values_list('user', flat=True)

    # Then, filter AttendanceSummary objects for the selected month and year, related to professional employees
    attendSum = AttendanceSummary.objects.filter(
    user__in=professional_users,
    month=month_numbers[selected_month],
    year=selected_year
    )
    # After filtering the AttendanceSummary objects, retrieve the empcode for each employee
    employee_codes = EmployeeDetail.objects.filter(user__in=professional_users).values('user', 'empcode')
    # Create a dictionary to map user IDs to empcodes
    employee_code_map = {entry['user']: entry['empcode'] for entry in employee_codes}
    # Create a list of dictionaries containing the necessary information for rendering in the template
    attendSum_data = [
    {
            'employee_name': f"{emp.user.first_name} {emp.user.last_name}",
            'employee_code': employee_code_map[emp.user.id],
            'selected_month': selected_month,
            'selected_year': selected_year,
            'days_present': emp.days_present,
            'days_total': emp.days_total,
    }
    for emp in attendSum
    ]
    context = {
            'attendSum_data': attendSum_data,
            }
    
    return render(request, 'professionalSalaryCalculation.html',context)

def applyForLeave(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    
    error = ""
    u = request.user
    emp = EmployeeDetail.objects.get(user=u)
    dat = datetime.now().today()
    #print(yearLeaveObj)
    attendSummary, created = AttendanceSummary.objects.get_or_create(user=u, month = dat.month, year = dat.year,
                                                                        days_total = calendar.monthrange(dat.year, dat.month)[1])
    today_month = dat.month
    today_year = dat.year
    print(today_month)
    print(today_year)
    s_year = 0
    e_year = 0
    if today_month in [1, 2, 3] :
        e_year = today_month
        s_year = today_year -1
    elif today_month in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
        s_year = today_year
        e_year = today_year + 1
    yearLeaveObj3, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year, end_year = e_year)

    if request.method == "POST":
        lT = request.POST['leaveType']
        sD = request.POST['startDate']
        eD = request.POST['endDate']
        r = request.POST['reason']
        # Convert the start_date and end_date strings to datetime objects
        start_date = datetime.strptime(sD, '%Y-%m-%d')
        end_date = datetime.strptime(eD, '%Y-%m-%d')
        # Get all the dates between start_date and end_date, excluding Sundays
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
        today_month1 = start_date.month
        today_year1 = start_date.year
        print(today_month1)
        print(today_year1)
        s_year1 = 0
        e_year1 = 0
        if today_month1 in [1, 2, 3] :
            e_year1 = today_year1
            s_year1 = today_year1 -1
            print(s_year1)
            print(e_year1)
        elif today_month1 in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
            s_year1 = today_year1
            e_year1 = today_year1 + 1
            print(s_year1)
            print(e_year1)
        
        today_month2 = end_date.month
        today_year2 = end_date.year
        print(today_month2)
        print(today_year2)
        s_year2 = 0
        e_year2 = 0
        if today_month2 in [1, 2, 3] :
            e_year2 = today_year2
            s_year2 = today_year2 -1
            print(s_year2)
            print(e_year2)
        elif today_month2 in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
            s_year2 = today_year2
            e_year2 = today_year2 + 1
            print(s_year2)
            print(e_year2)
        
        if s_year1 == s_year2 and e_year1 == e_year2 and lT == 'Sick Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            balanceD = yearLeaveObj.sickLeaveB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.sickLeaveB = balanceD
                yearLeaveObj.save()
                error = "no"
        # if case is like 30-March-2024 to 4-April-2024
        elif s_year1 != s_year2 and e_year1 != e_year2 and lT == 'Sick Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
            balanceD1 = yearLeaveObj1.sickLeaveB
            balanceD2 = yearLeaveObj2.sickLeaveB
            print(balanceD1)
            print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.sickLeaveB -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.sickLeaveB -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif s_year1 == s_year2 and e_year1 == e_year2 and lT == 'Earned Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            balanceD = yearLeaveObj.earnedLeaveB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.earnedLeaveB = balanceD
                yearLeaveObj.save()
                error = "no"
        # if case is like 30-March-2024 to 4-April-2024
        elif s_year1 != s_year2 and e_year1 != e_year2 and lT == 'Earned Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
            balanceD1 = yearLeaveObj1.earnedLeaveB
            balanceD2 = yearLeaveObj2.earnedLeaveB
            print(balanceD1)
            print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.earnedLeaveB -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.earnedLeaveB -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif s_year1 == s_year2 and e_year1 == e_year2 and lT == 'Freedom From Covid Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            balanceD = yearLeaveObj.ffcB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.ffcB = balanceD
                yearLeaveObj.save()
                error = "no"
        # if case is like 30-March-2024 to 4-April-2024
        elif s_year1 != s_year2 and e_year1 != e_year2 and lT == 'Freedom From Covid Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
            balanceD1 = yearLeaveObj1.ffcB
            balanceD2 = yearLeaveObj2.ffcB
            print(balanceD1)
            print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.ffcB -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.ffcB -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif s_year1 == s_year2 and e_year1 == e_year2 and lT == 'Maternity Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            balanceD = yearLeaveObj.maternityLB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.maternityLB = balanceD
                yearLeaveObj.save()
                error = "no"
        elif s_year1 != s_year2 and e_year1 != e_year2 and lT == 'Maternity Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
            balanceD1 = yearLeaveObj1.maternityLB
            balanceD2 = yearLeaveObj2.maternityLB
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
                months_between = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
                print("Months between : ",months_between)
                unique_months = set((date.year, date.month, calendar.monthrange(date.year, date.month)[1]) for date in date_range)
                unique_months = list(unique_months)
                print(unique_months)
                first_month_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
                last_month_days = end_date.day
                print(first_month_days)
                print(last_month_days)
                sorted_unique_months = sorted(unique_months, key=lambda date: (date[0], date[1]))
                subset = [[year, month, last_day] for year, month, last_day in sorted_unique_months]
                print(subset)
                subset[0][2]  = first_month_days
                list_len = len(subset)
                subset[list_len-1][2] = last_month_days
                print(subset[0][2])
                print(subset[list_len-1][2])
                print(subset)
                print("Sorted unique months:")
                days1 = 0 # for prev year
                days2 = 0 # for new year
                for i in range(len(subset)):
                    if subset[i][1] in [1,2,3]:
                        days1 += subset[i][2]
                    elif subset[i][1] in [4,5,6,7,8,9,10,11,12]:
                        days2 += subset[i][2]
                yearLeaveObj1.maternityLB -= days1
                yearLeaveObj2.maternityLB -= days2
                yearLeaveObj1.save()
                yearLeaveObj2.save()
                print(yearLeaveObj2.maternityLB)
                error = "no"
                
            
        elif s_year1 == s_year2 and e_year1 == e_year2 and lT == 'Optional Holiday (OH)':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            balanceD = yearLeaveObj.oH2B
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.oH2B = balanceD
                yearLeaveObj.save()
                error = "no"
                
        # if case is like 30-March-2024 to 4-April-2024
        elif s_year1 != s_year2 and e_year1 != e_year2 and lT == 'Optional Holiday (OH)':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
            balanceD1 = yearLeaveObj1.oH2B
            balanceD2 = yearLeaveObj2.oH2B
            print(balanceD1)
            print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.oH2B -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.oH2B -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif  lT == 'Bi-monthly Offs':
            if start_date.month == end_date.month:
                balanceD = attendSummary.biMOB
                if len(date_range) > balanceD:
                    error = "yes"
                if len(date_range) <= balanceD:
                    employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                    balanceD -= len(date_range)
                    attendSummary.biMOB = balanceD
                    attendSummary.save()
                    error = "no"
        elif start_date.month == end_date.month and lT == 'Bi-monthly Offs':
            attendSum, created = AttendanceSummary.objects.get_or_create(user=u, month = start_date.month, year = start_date.year,
                                                                        days_total = calendar.monthrange(start_date.year, start_date.month)[1])
            balanceD = attendSum.biMOB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                attendSum.biMOB = balanceD
                attendSum.save()
                error = "no"
        
        elif start_date.month != end_date.month and lT == 'Bi-monthly Offs':
            attendSum1, created1 = AttendanceSummary.objects.get_or_create(user=u, month = start_date.month, year = start_date.year,
                                                                        days_total = calendar.monthrange(start_date.year, start_date.month)[1])
            attendSum2, created2 = AttendanceSummary.objects.get_or_create(user=u, month = end_date.month, year = end_date.year,
                                                                        days_total = calendar.monthrange(end_date.year, end_date.month)[1])
            balanceD1 = attendSum1.biMOB
            balanceD2 = attendSum2.biMOB
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month:
                        attendSum1.biMOB -= 1
                        attendSum1.save()
                    elif date.month == end_date.month:
                        attendSum2.biMOB -= 1
                        attendSum2.save()
                error = "no"

    return render(request, 'applyForLeave.html', locals())


def approveLeave3(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()

    # Mark the attendance for the approved leave
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    today_month1 = start_date.month
    today_year1 = start_date.year
    print(today_month1)
    print(today_year1)
    s_year1 = 0
    e_year1 = 0
    if today_month1 in [1, 2, 3] :
        e_year1 = today_year1
        s_year1 = today_year1 -1
        print(s_year1)
        print(e_year1)
    elif today_month1 in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
        s_year1 = today_year1
        e_year1 = today_year1 + 1
        print(s_year1)
        print(e_year1)
        
    today_month2 = end_date.month
    today_year2 = end_date.year
    print(today_month2)
    print(today_year2)
    s_year2 = 0
    e_year2 = 0
    if today_month2 in [1, 2, 3] :
        e_year2 = today_year2
        s_year2 = today_year2 -1
        print(s_year2)
        print(e_year2)
    elif today_month2 in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
        s_year2 = today_year2
        e_year2 = today_year2 + 1
        print(s_year2)
        print(e_year2)
    # Get all the dates between start_date and end_date, excluding Sundays
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
    if leave.leave_type == 'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            attendSummary.paid_leave += 1
            attendance.save()
            attendSummary.save()
        attendSummary.biMOB = attendSummary.biMOB - len(date_range)
        
        
        
    if start_date.month == end_date.month and leave.leave_type != 'Bi-monthly Offs' and leave.leave_type != 'Maternity Leave':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            if leave.leave_type != "Optional Holiday" :
                attendSummary.paid_leave += 1
            else :
                attendSummary.unpaid_leave +=1
            attendance.save()
            attendSummary.save()
    if start_date.month != end_date.month and leave.leave_type != 'Bi-monthly Offs' and leave.leave_type != 'Maternity Leave':
        attendSummary1, created1 = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year,
                                                                 days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        print(attendSummary1)
        attendSummary2, created2 = AttendanceSummary.objects.get_or_create(user=user, month=end_date.month, year=end_date.year,
                                                                days_total = calendar.monthrange(end_date.year, end_date.month)[1])
        for date in date_range:
            if date.month == start_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary1.paid_leave +=1
                else:
                    attendSummary1.unpaid_leave +=1
                attendance.save()
                attendSummary1.save()
            if date.month == end_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary2.paid_leave +=1
                else:
                    attendSummary2.unpaid_leave +=1
                attendance.save()
                attendSummary2.save()
    if leave.leave_type == 'Maternity Leave':
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        months_between = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
        print("Months between : ",months_between)
        unique_months = set((date.year, date.month, calendar.monthrange(date.year, date.month)[1]) for date in date_range)
        unique_months = list(unique_months)
        first_month_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
        last_month_days = end_date.day
        print(first_month_days)
        print(last_month_days)
        sorted_unique_months = sorted(unique_months, key=lambda date: (date[0], date[1]))
        subset = [[year, month, last_day] for year, month, last_day in sorted_unique_months]
        print(subset)
        subset[0][2]  = first_month_days
        list_len = len(subset)
        subset[list_len-1][2] = last_month_days
        print(subset[0][2])
        print(subset[list_len-1][2])
        print(subset)
        print("Sorted unique months:")
        for year, month, last_day in subset:
            print(year, calendar.month_name[month], last_day)
        
        for i in range(len(subset)):
            attendSum, created = AttendanceSummary.objects.get_or_create(user=user, month=subset[i][1], year=subset[i][0],
                                                                 days_total = subset[i][2])
            attendSum.paid_leave += subset[i][2]
            attendSum.save()
    
        

    return redirect('viewLeaveApplication')

def disapproveLeave3(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()

    # Mark the attendance for the disapproved leave as 0
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    today_month1 = start_date.month
    today_year1 = start_date.year
    s_year1 = 0
    e_year1 = 0
    if today_month1 in [1, 2, 3] :
        e_year1 = today_year1
        s_year1 = today_year1 -1
    elif today_month1 in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
        s_year1 = today_year1
        e_year1 = today_year1 + 1
    print(s_year1)
    print(e_year1)
        
    today_month2 = end_date.month
    today_year2 = end_date.year
    s_year2 = 0
    e_year2 = 0
    if today_month2 in [1, 2, 3] :
        e_year2 = today_year2
        s_year2 = today_year2 -1
    elif today_month2 in [4, 5, 6, 7, 8, 9, 10, 11, 12] :
        s_year2 = today_year2
        e_year2 = today_year2 + 1
    print(s_year2)
    print(e_year2)
    # Get all the dates between start_date and end_date, excluding Sundays
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
    print(date_range)
    emp = EmployeeDetail.objects.get(user=user)
    if s_year1 == s_year2 and e_year1 == e_year2 and leave.leave_type == "Earned Leave":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearlyLeave.earnedLeaveB += len(date_range)
        yearlyLeave.save()
    elif s_year1 != s_year2 and e_year1 != e_year2 and leave.leave_type == 'Earned Leave':
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.earnedLeaveB += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.earnedLeaveB += 1
                yearLeaveObj2.save()
    elif s_year1 == s_year2 and e_year1 == e_year2 and leave.leave_type == "Sick Leave":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearlyLeave.sickLeaveB += len(date_range)
        yearlyLeave.save()
    elif s_year1 != s_year2 and e_year1 != e_year2 and leave.leave_type == "Sick Leave":
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.sickLeaveB += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.sickLeaveB += 1
                yearLeaveObj2.save()
    elif s_year1 == s_year2 and e_year1 == e_year2 and leave.leave_type == "Freedom From Covid Leave":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearlyLeave.ffcB += len(date_range)
        yearlyLeave.save()
    elif s_year1 != s_year2 and e_year1 != e_year2 and leave.leave_type == "Freedom From Covid Leave":
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.ffcB += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.ffcB += 1
                yearLeaveObj2.save()
    if s_year1 == s_year2 and e_year1 == e_year2 and leave.leave_type == "Maternity Leave":
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearlyLeave.maternityLB += len(date_range)
        yearlyLeave.save()
    if s_year1 != s_year2 and e_year1 != e_year2 and leave.leave_type == "Maternity Leave":
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
        unique_months = set((date.year, date.month, calendar.monthrange(date.year, date.month)[1]) for date in date_range)
        unique_months = list(unique_months)
        first_month_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
        last_month_days = end_date.day
        print(first_month_days)
        print(last_month_days)
        sorted_unique_months = sorted(unique_months, key=lambda date: (date[0], date[1]))
        subset = [[year, month, last_day] for year, month, last_day in sorted_unique_months]
        print(subset)
        subset[0][2]  = first_month_days
        list_len = len(subset)
        subset[list_len-1][2] = last_month_days
        print(subset[0][2])
        print(subset[list_len-1][2])
        print(subset)
        days1 = 0 # for prev year
        days2 = 0 # for new year
        for i in range(len(subset)):
            if subset[i][1] in [1,2,3]:
                days1 += subset[i][2]
            elif subset[i][1] in [4,5,6,7,8,9,10,11,12]:
                days2 += subset[i][2]
        yearLeaveObj1.maternityLB += days1
        yearLeaveObj2.maternityLB += days2
        yearLeaveObj1.save()
        yearLeaveObj2.save()
        
    elif s_year1 == s_year2 and e_year1 == e_year2 and leave.leave_type == "Optional Holiday (OH)":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearlyLeave.oH2B += len(date_range)
        yearlyLeave.save()
    elif s_year1 != s_year2 and e_year1 != e_year2 and leave.leave_type == "Optional Holiday (OH)":
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year1, end_year = e_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =4, end_month = 3 ,start_year = s_year2, end_year = e_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.oH2B += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.oH2B += 1
                yearLeaveObj2.save()
    elif start_date.month == end_date.month and leave.leave_type ==  'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        attendSummary.biMOB += len(date_range)
        attendSummary.save()
    elif start_date.month != end_date.month and leave.leave_type ==  'Bi-monthly Offs':
        attendSum1, created1 = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                        days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        attendSum2, created2 = AttendanceSummary.objects.get_or_create(user=user, month = end_date.month, year = end_date.year,
                                                                        days_total = calendar.monthrange(end_date.year, end_date.month)[1])
        for date in date_range:
            if date.month == start_date.month:
                attendSum1.biMOB += 1
                attendSum1.save()
            if date.month  == end_date.month:
                attendSum1.biMOB += 1
                attendSum2.save()
    for date in date_range:
        attendance, created = Attend.objects.get_or_create(user=user, date=date)
        attendance.is_present = 0
        attendance.save()

    return redirect('viewLeaveApplication')



