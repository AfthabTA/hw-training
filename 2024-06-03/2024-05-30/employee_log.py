import datetime
import json
import pymongo




class EmployeeTaskLog:

    client = pymongo.MongoClient('localhost', 27017)
    db = client["employee"]
    db_collection = db['employee_collection']

    main_task_list = []
    task = {None}

    def employee_login(self):

        self.employee_name = input("Enter Name :")
        self.employee_id = int(input("Enter employee id :")) 
        self.login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def employee_task(self): 

        self.task_title = input("Enter task title :")
        self.task_description = input("Enter task description :")
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.task={
            "task_title":self.task_title,
            "task_description":self.task_description,
            "start_time":self.start_time,
            "end_time":None,
            "task_success":False,
        }
        employee.interface()

    def task_status(self):

        self.end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.task["end_time"] = self.end_time
        self.task["task_success"] = True
        self.main_task_list.append(self.task)
        self.task = {None}
        employee.interface()

    def log_out(self):

        self.logout_time =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        employee.json_out()

    def json_out(self):

        employee_log = {
            "emp_name":self.employee_name,
            "emp_id":self.employee_id,
            "login_time":self.login_time,
            "logout_time":self.logout_time,
            "tasks":self.main_task_list,

        }
        file_name = datetime.date.today().strftime("%Y-%m-%d")+'_'+self.employee_name+".json"
        print(file_name)
        with open(file_name, 'w') as json_file:
            json.dump(employee_log, json_file, indent=4)
        print(self.main_task_list) 
        self.db_collection.insert_one(employee_log)   
   

    def interface(self):
        print("\n1. Start task \n2. End task \n3. Log out")
        selector = int(input("Enter your choice :"))

        if selector == 1:
            if self.task == {None}:
                employee.employee_task()
            else :
                print("* Finish the previous task to start new task *")
                employee.interface()
        elif selector == 2:
            employee.task_status()
        elif selector == 3:  
            employee.log_out()
        else:
            print('Invalid input!!!')      

employee = EmployeeTaskLog()
print('Employee Login')
employee.employee_login()
employee.interface()
