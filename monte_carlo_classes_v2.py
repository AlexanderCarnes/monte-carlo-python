import csv
import random
import matplotlib
import matplotlib.pyplot as plt

class employee_roster(object):
    first_names = []
    last_names = []
    simulation = 0
    def __init__(self):
        self.employee_roster = employee_roster
        self.getNameList()

##    def __iter__(self):
##        return self
##
##    def __next__(self):
##        count = len(self.employee_roster)
##        i = 0
##        while i < count:
##            return self.employee_roster[i]
##            i +=1
        
        
    def build_roster(self,number_of_employees,user_machine_class,uniform_age_distro = True,get_stats = False):
        first_name = ''
        last_name = ''
        employee_roster = []
        
        for i in range(0,number_of_employees):
            rp = random.randint(0,100)*.01
            first_name_int = random.randint(0,len(self.first_names)-1)
            last_name_int = random.randint(0,len(self.last_names)-1)
            thoughtfulness_score = random.randint(0,5)*.01
            buy_back_probability = random.randint(0,100)*.01
            first_name = self.first_names[first_name_int]
            last_name = self.last_names[last_name_int]
            emp_machine = user_machine_class
            
            if uniform_age_distro == False:
                emp_machine.age = random.randint(0,emp_machine.years_to_replace)
            
            emp = employee(first_name,last_name,thoughtfulness_score,buy_back_probability,True,emp_machine)
            if get_stats == True: 
                emp.getEmployeeStats()
            
            employee_roster.append(emp)
            self.employee_roster = employee_roster     
        
    def getNameList(self):
        self.first_names = []
        self.last_names =[]
        with open('Y:/Sense Corp/Documents/Sense Corp Moving To Mac/Python Analysis/Name Spreadhsheet.txt', 'r') as f:
            reader = csv.reader(f, dialect='excel', delimiter='\t')
            next(reader,None)
            for row in reader:
                if row[0] != '':
                    self.first_names.append( row[0])
                if row[1] != '':
                    self.last_names.append( row[1])

    def resetSimulationStats(self):
        for employee in self.employee_roster:
            #Employee Stats 
            employee.resetEmployeeStats()
            #Reset machine stats
            employee.machine.resetStats()
        
    def printRoster(self):
        for emp in self.employee_roster:
            
            mch = emp.machine
            fn = emp.first_name
            ln = emp.last_name
            ts = emp.thoughtfulness
            machine_costs = emp.machine_costs
            mt = emp.machine.machine_type
            es = emp.currently_employed

            c = mch.cost
            ytr = mch.years_to_replace
            rp = mch.replace_probability
            rep = mch.repair_probability
            vp = mch.virus_probability

            print('EMPLOYEE STATS {} {} \nThoughtfulness Score: {}\nMachine Type: {}\nMachine Cost: {}, Is First machine:{}\n'.format(fn,ln,ts,mt.capitalize(),machine_costs,self.machine.first_machine))
            print('MACHINE STATS\nCost: {}\nYears to replace: {}\nReplace Probability: {}\nRepair Probability: {}\nVirus Probability: {}\n------------'.format(c,ytr,rp,rep,vp))

    def runSimulation(self,number_of_months,rebuild_roster=False,uniform_machine_age_distribution = True,uniform_machine_distribution = True,machine = None,buy_back=False,secondary_machine=None):
        months_list = []
        total_cost_per_month = []
        total_cost = 0 
        
        self.resetSimulationStats()
        if machine == None:
            machine = machine_class('Toshiba',750,1.5,0,.1,.15,.05)
            
        if self.rebuild_roster == False and self.simulation == 0:
            self.build_roster(number_of_months,machine,uniform_machine_age_distribution)
        elif rebuild_roster == True and self.simulation > 0:
            self.build_roster(number_of_months,machine,uniform_machine_age_distribution)
        
        
        for month in range(1,number_of_months+1):
            months_list.append(month)
            monthly_sum = 0
            #print("Month Number: {}".format(month))
            for employee in self.employee_roster:
                employee.needsRepair()
                employee.needsReplacing()
                employee.virusAttack()
                employee.machine.age +=1
                #employee.getEmployeeStats()
                #print('Employee machine age, in months: {}, Years to replace: {}, is first machine: {}'.format(employee.machine.age,employee.machine.years_to_replace,employee.machine.first_machine))
               # print('Employee machine age in years: {}, Years to replace/2: {}'.format(employee.machine.age/12,employee.machine.years_to_replace/2))

                if employee.machine.age/12 == employee.machine.years_to_replace:
                   # print('Replaced machine')
                   if uniform_machine_distribution == False and employee.replacements == 0:
                       employee.giveMachine(secondary_machine)
                   else:
                       employee.giveMachine()

                if month % 12 == 0 and ('mac' in employee.machine.machine_type.lower() or 'macbook' in employee.machine.machine_type.lower() or 'mac book' in employee.machine.machine_type.lower()):
                    fee_for_parallels = 99.00
                    sales_tax = .12
                    total_fee = fee_for_parallels + (fee_for_parallels*sales_tax)
                    employee.machine_costs += total_fee

                if buy_back == True and employee.machine_type !='toshiba':
                    if (employee.machine.age/12) >= employee.machine.years_to_replace/2:
                        buy_back_prob = random.randint(0,100)*.01
                        #print ('Buy back probability: {}%, employee buy back probaility: {}%'.format(buy_back_prob*100,employee.buy_back_probability*100))
                        if buy_back_prob <= employee.buy_back_probability:
                            employee.giveMachine()
                            employee.machine_costs -= employee.machine.cost/2
                         #   print('Employee machine cost: {}'.format(employee.machine_costs))

                    
                #employee.getEmployeeStats()  
            monthly_sum += employee.machine_costs
            total_cost_per_month.append(monthly_sum)
        #print(len(total_cost_per_month))
        #print(len(months_list))
        X = months_list
        Y = total_cost_per_month
        if 'toshiba' in self.employee_roster[0].machine.machine_type.lower(): 
            plt.plot(X,Y,label=self.employee_roster[0].machine.machine_type+'_sim_'+str(self.simulation),linestyle='--')
            plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
        else: 
            plt.plot(X,Y,label=self.employee_roster[0].machine.machine_type+'_sim_'+str(self.simulation))
            plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)

        for employee in self.employee_roster:
            total_cost += employee.machine_costs

        self.simulation +=1
        return total_cost
        
                   
class employee(object):
    replacements = 0
    virus_attacks = 0
    repairs = 0
    machine_costs = 0
    
    def __init__(self,first_name,last_name,thoughtfulness,buy_back_probability,currently_employed,machine=None):
        self.first_name = first_name
        self.last_name = last_name
        self.machine = machine
        self.thoughtfulness = thoughtfulness
        self.currently_employed = currently_employed
        self.buy_back_probability = buy_back_probability
        

    def getName(self):
        return self.first_name + self.last_name
    def getMachineType(self):
        return self.machine_type
    def getEmploymentStatus(self):
        return self.currently_employed
    def getMachineType(self):
        return self.machine.machine_type
    
    def giveMachine(self,new_machine=None):
        self.replacements +=1
        self.machine.age = 0
        self.machine.first_machine = False
        if new_machine == None: 
            self.machine_costs += self.machine.cost
            #print('After being replaced, the machine age is: {}'.format(self.machine.age) )
        else:
            self.machine_costs = new_machine.cost
        return self.machine

    def needsRepair(self):
        repair_roll = random.randint(0,1000)*.001
        repair_cost = 0
       # print('Repair Roll: {}%'.format(repair_roll*100))
        #print('Probability employee will need repair:{}%'.format((self.machine.repair_probability + self.thoughtfulness)*100))
        
        if repair_roll <= (self.machine.repair_probability + self.thoughtfulness):
            #print('Needs repairs')
            repair_cost = random.uniform(.01*self.machine.cost,.49*self.machine.cost)
            self.machine_costs += repair_cost
            self.repairs += 1
            self.machine.repairs +=1
            self.machine.machine_costs += repair_cost
            #print('Repair Cost: {}'.format(repair_cost))

    def needsReplacing(self,new_machine=None):
        replacement_roll = random.randint(0,1000)*.001
        if replacement_roll <= self.machine.replace_probability:
           # print('Needs replacing')
           if new_machine == None:
                self.machine.machine_costs += self.machine.cost
                self.giveMachine()
           else:
                self.giveMachine(new_machine)
            
    def virusAttack(self,new_machine=None):
        virus_roll = random.randint(0,1000)*.001
        virus_cost = 0
        
        if virus_roll <= self.machine.virus_probability:
            virus_cost = random.uniform(0,self.machine.cost)
            self.virus_attacks += 1
            self.machine.virus_attacks +=1
            self.machine.machine_costs += virus_cost
           # print('VIURS ATTACK!')
            if virus_cost >= self.machine.cost*.8:
                if new_machine == None:
                    self.giveMachine()
                else:
                    self.giveMachine(new_machine)
             #   print("Virus took this one")
            else:
                self.machine_costs +=  virus_cost
            #print('Virus Cost: {}'.format(virus_cost))

    def resetEmployeeStats(self):
       self.repairs = 0
       self.replacements = 0
       self.virus_attacks = 0
       self.machine_costs = 0     
        
    
    def getEmployeeStats(self):
        replacements = self.replacements
        machine_cost = self.machine_costs
        print('{} {} : Number of replacements: {},Number of repairs: {},Number of Virus Attacks: {}, Total Machine Cost: {}, Age of Machine: {}'.format(self.first_name,self.last_name,self.replacements,self.repairs,self.virus_attacks,self.machine_costs,self.machine.age))

class machine_class(object):
    repairs = 0
    virus_attacks = 0
    machine_costs = 0
    def __init__(self,machine_type,cost,years_to_replace,age,replace_probability,repair_probability,virus_probability,first_machine=False):
        self.machine_type = machine_type
        self.cost = cost
        self.years_to_replace = years_to_replace
        self.age = age
        self.replace_probability = replace_probability
        self.repair_probability = repair_probability
        self.virus_probability = virus_probability
        self.first_machine = first_machine 

    def resetStats(self):
        self.repairs =0
        self.virus_attacks =0
        self.machine_costs =  0
        self.first_machine = True
            
     






