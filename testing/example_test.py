import pytest
import System
import Student
import User
import Professor
import TA
import Staff


def test_login(gs):
    gs.login('goggins', 'augurrox')
    gs.usr == Professor.Professor('goggins', gs.users, gs.courses)
    

def test_check_password(gs):
    name = "hdjsr7"
    password = "pass1234"
    gs.check_password( name, password)
    name = "saab"
    password = "boomr345"
    gs.check_password( name, password)
    name = "goggins"
    password = "augurrox"
    gs.check_password( name, password)
    name = "cmhbf5"
    password = "bestTA"
    gs.check_password( name, password)
    

def test_change_grade(gs):  ##Correct grade is changed for correct user, but not to correct value??
    ta = TA.TA("cmhbf5",gs.users,gs.courses)
    name = "hdjsr7"
    course = "software_engineering"
    assignment = "assignment1"
    ta.change_grade(name,course,assignment,"80")

    student = Student.Student("hdjsr7", gs.users,gs.courses)
    grades = student.check_grades('software_engineering')

    100 != grades[0][1]


def test_create_assignment(gs):
    gs.login('goggins', 'augurrox')
    gs.usr.create_assignment('assignment6', '04/03/24', 'cloud_computing')
    assert 'assignment6' in gs.usr.all_courses['cloud_computing']['assignments']
    
def test_add_student(gs): ##FAILS 1
    teacher = Professor.Professor("goggins",gs.users,gs.courses)
    teacher.add_student('akend3', 'software_engineering')
    assert 'software_engineering' in gs.users['akend3']['courses']

def test_drop_student(gs): ##FAILS 2
    teacher = Professor.Professor("goggins",gs.users,gs.courses)
    teacher.drop_student('cmhbf5', 'software_engineering')
    assert 'software_engineering' not in gs.users['cmhbf5']['courses']

def test_submit_assignment(gs):
    teacher = Professor.Professor("saab",gs.users,gs.courses)
    student = Student.Student("akend3", gs.users, gs.courses)

    teacher.create_assignment('assignment3', '04/03/24', 'comp_sci')
    student.submit_assignment('comp_sci','assignment3','Done','04/03/24')
    assert gs.users['akend3']['courses']['comp_sci']['assignment3']

def test_check_ontime(gs): ##FAILS 3
    student = Student.Student("hdjsr7", gs.users, gs.courses)
    assert student.check_ontime('1/3/20','1/3/20') == True
    assert student.check_ontime('1/4/20','1/3/20') == False

def test_check_grades(gs): ##FAILS 4
    student = Student.Student("hdjsr7", gs.users, gs.courses)
    assert student.check_grades('software_engineering') == [['assignment1', 0], ['assignment2', 100]]

    student2 = Student.Student("yted91", gs.users, gs.courses) 
    assert student2.check_grades('cloud_computing') == [['assignment1', 100], ['assignment2', 0]]

def test_view_assignments(gs): ##FAILS 5
    student = Student.Student("yted91", gs.users, gs.courses) 
    assignments = [['assignment1', '2/2/20'], ['assignment2', '2/10/20'], ['assignment3', '04/03/24']]
    assert student.view_assignments('cloud_computing') != assignments


def test_correct_grade(gs): ##1##FAILS: Checks to see if grade change results in correct value
    ta = TA.TA("cmhbf5",gs.users,gs.courses)
    name = "hdjsr7"
    course = "cloud_computing"
    assignment = "assignment1"
    ta.change_grade(name,course,assignment,"80")

    student = Student.Student("hdjsr7", gs.users,gs.courses)
    # gs.login('hdjsr7', 'pass1234')
    grades = student.check_grades('cloud_computing')

    80 == grades[0][1]

def test_more_passwords(gs): ##2##FAILS: Checks if password is alphanumeric
    name = "calyam"
    password = "#yeet"
    gs.login(name, password)
    assert password.isalnum()

def test_teacher_classes(gs): ##3##FAULS: Checks that teachers can have only one class
    teacher = Professor.Professor("goggins",gs.users,gs.courses)
    assert len(teacher.courses) == 1

def test_password_len(gs): ##4##FAILS: Checks that password is no longer than 18 characters
    name = "yted91"
    password = "imoutofpasswordnames"
    gs.login(name, password)
    assert len(password) < 18

def test_correct_prof(gs): ##5##FAILS: Only corresponding professors can change grades for students in course
    name = "calyam"
    password = "#yeet"
    gs.login(name, password)
    gs.usr.change_grade('yted91','software_engineering','assignment1',0)
    assert 'software_engineering' in gs.usr.courses




@pytest.fixture
def gs():
    gs = System.System()
    gs.load_data()
    return gs
