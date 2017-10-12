import csv
import random

class employee_roster(object):
    first_names = []
    last_names = []
    
    def __init__(self,employee_roster):
        self.employee_roster = employee_roster
        self.getNameList()
        
    def build_roster(self,machine_type,number_of_employees):
        first_name = ''
        last_name = ''
        employee_roster = []
        
        for i in range(0,number_of_employees):
            
            first_name_int = random.randint(0,len(self.first_names)-1)
            last_name_int = random.randint(0,len(self.last_names)-1)
            thoughtfulness_score = random.randint(0,5)*.01
            first_name = self.first_names[first_name_int]
            last_name = self.last_names[last_name_int]
            emp = employee(first_name,last_name,machine_type,thoughtfulness_score,True)
            print(emp.first_name)
            employee_roster.append(emp)
            self.employee_roster = employee_roster
            
        
    def getNameList(self):
        self.first_names = []
        self.last_names =[]
        with open('F:/Sense Corp/Documents/Sense Corp Moving To Mac/Python Analysis/Name Spreadhsheet.txt', 'r') as f:
            reader = csv.reader(f, dialect='excel', delimiter='\t')
            next(reader,None)
            for row in reader:
                if row[0] != '':
                    self.first_names.append( row[0])
                if row[1] != '':
                    self.last_names.append( row[1])

    def printRoster(self):
        for i in range(0,len(self.employee_roster)):
            emp = self.employee_roster[i]
            mch = emp.machine
            fn = emp.first_name
            ln = emp.last_name
            ts = emp.thoughtfulness
            mt = emp.machine_type
            es = emp.currently_employed

            c = mch.cost
            ytr = mch.years_to_replace
            rp = mch.replace_probability
            rep = mch.repair_probability
            vp = mch.virus_probability

            print('EMPLOYEE STATS {} {} \nThoughtfulness Score: {}\nMachine Type: {}\nEmployment Status: {}\n'.format(fn,ln,ts,mt.capitalize(),es))
            print('MACHINE STATS\nCost: {}\nYears to replace: {}\nReplace Probability: {}\nRepair Probability: {}\nVirus Probability: {}\n------------'.format(c,ytr,rp,rep,vp))
                    
class employee(object):
    replacements = 0
    machine_costs = 0
    def __init__(self,first_name,last_name,machine_type,thoughtfulness,currently_employed):
        self.first_name = first_name
        self.last_name = last_name
        self.machine_type = machine_type
        self.machine = self.giveMachine()
        self.thoughtfulness = thoughtfulness
        self.currently_employed = currently_employed

    def getName(self):
        return self.first_name + self.last_name
    def getMachineType(self):
        return self.machine_type
    def getEmploymentStatus(self):
        return self.currently_employed
    def getMachineType(self):
        return self.machine.machine_type
    
    def giveMachine(self):
        rp = random.randint(0,100)*.01
        
        if self.machine_type.lower() == 'toshiba':
            return  machine_class('Toshiba',500,18/12,1,rp,.1,.05)
        else:
            return machine_class('MacBook Pro',2995,6,1,rp,.02,.05)
        

class machine_class(object):
    def __init__(self,machine_type,cost,years_to_replace,machine_age,replace_probability,repair_probability,virus_probability):
        self.machine_type = machine_type
        self.cost = cost
        self.years_to_replace = years_to_replace
        self.machine_age = machine_age
        self.replace_probability = replace_probability
        self.repair_probability = repair_probability
        self.virus_probability = virus_probability

    def needsRepair(self,thoughtfulness_score):
        repair_roll = random.randint(0,100)*.01
        repair_cost = 0
        if repair_roll <= (self.repair_probability + thoughtfulness_score):
            repair_cost = 100 #Units of USD
        return repair_cost

    def needsRelacing(self):
        replacement_roll = random.randint(0,100)*.01
        if replacement_roll <=self.replace_probability:
            return self.cost,1
        else:
            return 0,0

    def virusAttack(self):
        virus_roll = random.randint(0,100)*.01
        virus_cost = 0
        replacement = 0
        if virus_roll<= virus_probability:
            virus_cost = random.randint(0,self.cost)
            if virus_cost >= self.cost*.8:
                replacement = 1
        return virus_cost,replacement
            
     



x = employee_roster([])
x.build_roster('toshiba',1)
x.printRoster()

number_of_year = 10
number_of_months = 12*10




