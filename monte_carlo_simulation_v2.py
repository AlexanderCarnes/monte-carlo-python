from monte_carlo_classes_v2 import *

my_test_roster = employee_roster()
test_machine = machine_class('IBM',100,1,0,.1,.01,.1,True)
my_test_roster.build_roster(2,test_machine,get_stats=True)
