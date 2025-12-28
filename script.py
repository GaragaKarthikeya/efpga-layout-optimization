import numpy  as np
import random as rnd
from jinja2 import Environment, FileSystemLoader
import os

#k6_frac_N10_frac_chain_depop50_mem32K_40nm.xml is the base architecture on which we perform the genetic algortihm

##run these after opening the repo
#python3 -m venv .venv
#source .venv/bin/activate
#pip install numpy
#pip install jinja2
#pip install prettytable

class genetic_algorithm():#this is the class that implements the genetic algorithm
    def __init__(self,sol, num_sol, num_gen, cross_prob, mut_prob):
        print("reached genetic algorithm")#sol indicates the solution,num_ind indicates the number of chromosomes
        self.sol=sol
        self.num_sol = num_sol
        self.num_gen = num_gen
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.run_num = 1#indicates the run number
        self.max = 0#indicates the max fitness cost 

    def __del__(self):
        print("delted object of class gen_alg")

    def fitness_function(self,sol):

        gen_object = generate(sol,self.run_num)#this is for running the vtr flow and obtain the fitness
        print("back to script after running vtr on sol" )
        [fit_value,run_num] = gen_object.main()
        self.run_num = run_num
        del gen_object#after this the gen_object need is completed

        if(fit_value > self.max): 
            self.max = fit_value
            self.max = self.max*10000#this punishes the failed archiectures and enables the ones which have passed(fit_val!=1) equally small_number/self.max give same as all fitness_val tend to be small
        if(fit_value == 1):
            fit_value = self.max#for failed ones we give them the self.max becuase they should have 0 prob to get selected
        return fit_value
    
    def initiate(self):#this function initiates the populatuion bag of solutions with rnd_solutions
        population_bag = []
        for i in range(self.num_sol):
            rnd_sol = self.sol.copy()
            population_bag.append(rnd_sol)#appends the same solution self.num_sol times(size of population bag)
        return np.array(population_bag,dtype=object)#returns the population bag as a numpy array
    
    def fit_pop(self,population_bag):
        #res is a dictionary that maintains the fitness_values,fitness_weights,respective solutions of the population
        res = {}
        fit_val_list = []
        sols = []
        for sol in population_bag:
            fit_val_list.append(self.fitness_function(sol))
            sols.append(sol)

        res["fit_val"] = fit_val_list
        min_wgt = [np.max(list(res["fit_val"]))-i for i in list(res["fit_val"])]
        #this process converts fitness_values into weights that the least area*delay ones will have higher fit_wgt
        if(sum(min_wgt) == 0):#if all the solutions have same area*delay then to handle that case
            res["fit_wgt"] = [i/self.max for i in min_wgt]
        else:
            res["fit_wgt"] = [i/sum(min_wgt) for i in min_wgt]

        res["sol"] = np.array(sols)
        #dictionary of solution-->{ fit_val: 
        #                           fit_wgt: 
        #                           sol:[[10],[[12,2,3]....],[[1,2,3]......]],..]}
        return res
    
    def pick(self,population_bag,fit_bag_evals):#this picking favours high fit_wt ones
       
        t = True
        while t:
            rnIndex = rnd.randint(0, len(population_bag)-1)#this is to pick one of the solution out of the population bag
            rnPick = fit_bag_evals["fit_wgt"][rnIndex]
            r = rnd.random()
            if r <= rnPick:
                pickedSol = fit_bag_evals["sol"][rnIndex]
                t = False
        return pickedSol #the solution that is picked is returned
    
    def crossover(self, solA, solB):
        #solA and solB are array of solutions in the population bag
        # offspring = [10,[[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan]],[[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan]]]
        offspring = solA
        # we know that len(solA) = 3
        n = len(solA)    
        
        num_els = np.ceil(n*(rnd.randint(10,90)/100)) #this is to generate a random number between 0 and 3 ,done to pick respective genes from solA
        str_pnt = rnd.randint(0,n-2)
        end_pnt = n if int(str_pnt+num_els) > n else int(str_pnt+num_els)
        blockA = list(solA[str_pnt:end_pnt])#blcokA contains the genes from the solA from the str_pnt to end_pnt
        offspring[str_pnt:end_pnt] = blockA#placing some genes from solA onto the offspring
        for i in range(1,n):
            if list(blockA).count(solB[i]) == 0:#checks if solB[i] gene is present in the partial offspring if no the accepted
                for j in range(1,n):
                    if (offspring[j][0][0] == solA[j][0][0]):#this indicates the preference (if same preference same then same kind)??? so ideally this also checks if the exchange is among the same kind of chip
                        if(len(offspring[j]) == len(solB[i])):    #exchange between bram <-> bram or dsp <-> dsp or clb <->  only since our implementation does not contain their number to be same we can use this logic
                            offspring[j] = solB[i]
                            break
       
        return offspring
    
    def mutation(self,sol):
        n = len(sol) #-->3
        x = [] #this is the list that maintains the x cordinates that have already been taken as a part of mutation
        y = []#this is the list that maintains the y coordinates that have already been taken as a part of the mutaution
        #these are done to ensure that any two blocks wont have the same x or y coordinates from mutation

        for i in range(n):#the first element(i==0) indicates the prority for that particular block type
            if(i == 0):
                if(rnd.random() <= self.mut_prob):
                    sol[i] = rnd.randint(1,10)
            else:
                for j in range(len(sol[i])):
                    for k in range(len(sol[i][j])):
                        if(rnd.random() <= self.mut_prob):
                            if(k == 0):
                                num = rnd.randint(3,20)
                                while x.count(num):
                                    num = rnd.randint(3,20)
                                sol[i][j][k] = num
                                x.append(sol[i][j][k])
                            elif(k == 1):
                                num = rnd.randint(3,20)
                                while y.count(num):
                                    num = rnd.randint(3,20)
                                sol[i][j][k] = num
                                y.append(sol[i][j][k])
        result = sol
        return result       #updates the x and y coordinates and produces the result

    def func(self):#this is the main function
        #initially array of population bags 
        pop_bag = self.initiate()
        g = 0#it is the variable that maintains the generation number for iteration
        t_con = [0 for i in range(0,self.num_gen)]
        for gen in range(self.num_gen):
            #array of dictionaries of results
            #called this function for first time--->self.monitor inc
            pop_bag_fit = self.fit_pop(pop_bag)
            #final solution would be in the form--->-->[10,[[12,2,3]....],[[1,2,3]......]]
            
            best_fit = np.min(pop_bag_fit["fit_val"])
            best_fit_index = pop_bag_fit["fit_val"].index(best_fit)
            best_sol = pop_bag_fit["sol"][best_fit_index]

            if gen == 0:
                #clb
                best_fit_global = best_fit
                best_sol_global = best_sol#since it is the first iteration of generations these variables should be initailsed
            else:
                if best_fit <= best_fit_global:
                    best_fit_global = best_fit
                    best_sol_global = best_sol
            
            new_pop_bag = []

            for i in range(self.num_sol):
                pA = self.pick(pop_bag,pop_bag_fit)
                pB = self.pick(pop_bag,pop_bag_fit)
                new_element = pA

                if rnd.random() <= self.cross_prob:
                    new_element = self.crossover(pA,pB)

                if rnd.random() <= self.mut_prob:
                    new_element = self.mutation(new_element)

                new_pop_bag.append(new_element)

            pop_bag = np.array(new_pop_bag)     #any (self.num_sol which is size of population bag) solutions from the previus generation go into the next generation that depends on the pick,mutate,crossover functions

            # /******since we require the best solution each of the benchmark circuit we should obtain the output for each on seperate file 
            # so in the filename = "benchmark_output.txt" use like this 
            #look into generate class main method for some instructions******/

            print(f"Best fitness: {best_fit_global}")
            print(f"Best solution: {best_sol_global}")
            print("Generation number:"+str(gen))
            filename = "diffeq1_output.txt"
            with open(filename, mode="a+", encoding="utf-8") as message:
                message.write(f"Best fitness: {best_fit_global}\n")
                message.write(f"Best solution: {best_sol_global}\n")
                print(f"... wrote {filename}")
            t_con[g] = best_fit_global#this maintains the best globa solution upto that generation
            check = 0
            if(g >= 14):
                for i in range(g-14,g+1):
                    if(t_con[i] == t_con[g]):
                        check = check+1
                    if(check >= 14):
                        print("breaking condition reached....")
                        return best_fit_global#breaking condition is if previous 15 generations give same fitness or 50 generations complete
            g = g+1#best solution will be at the end of the output.txt file


    
class generate():#this class takes in the solution and the run_number and based on that gives the output from the vtr run
    def __init__(self,sol,run_num):
        print("reached genration script")
        self.clb_priority = sol[0] 
        self.dsps = sol[1]
        self.mems = sol[2]
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.template = self.environment.get_template("k6_frac_N10_frac_chain_depop50_mem32K_40nm.xml")
        self.run_num = run_num

    def __del__(self):
        print("deleted gen script object")

    def main(self):
        filename = "my_arch.xml"
        content = self.template.render(
            clb_priority=self.clb_priority,
            dsps=self.dsps,
            mems=self.mems
        )#this content variable is what are the positions of the dsps and the brams that we place in  the base architecture of k6_frac_N10_frac_chain_depop50_mem32K_40nm.xml
        with open('/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/arch/timing/'+filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"... wrote {filename}")
        #this is to run the vtr flow and obtain the result

        '''
        /*******inorder to obtain the result of the benchmark circuit that we want we should change the file 
        vtr-verilog-to-routing/vtr_flow/vtr_reg_basic/basic_timing/config/config.txt in such a way that 
        the variables [ arch_list_add=my_arch.xml , circuit_list_add=benchmark.v ] should be assigned like this 
        benchmark deontes whatever benchmark we choose ex: diffeq1.v,reygentop.v,spree.v
        '''

        status = os.system('/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/scripts/run_vtr_task.py regression_tests/vtr_reg_basic/basic_timing')
        print("ran vtr-flow--sucessfully")
        #extraction script

        if(status == 0):#this section obtains the area,delay from the results with the help of the class extraction_script
            if(self.run_num < 10):
                print("reading from run00"+str(self.run_num))
                ext_object = extract("/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing/run00"+str(self.run_num)+"/parse_results.txt") #-->add file name
            elif(self.run_num >= 10 and self.run_num < 100):
                print("reading from run0"+str(self.run_num))
                ext_object = extract("/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing/run0"+str(self.run_num)+"/parse_results.txt") #-->add file name
            else:
                print("reading from run"+str(self.run_num))
                ext_object = extract("/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing/run"+str(self.run_num)+"/parse_results.txt") #-->add file name
            ad_prod = ext_object.main()
            print("test-no.:"+str(self.run_num))
            print("area x delay:"+str(ad_prod))
            del ext_object
            return [ad_prod,self.run_num+1]
        else:
            return False
        
class extract():#this class is used for the extraction of the results from the vtr_flow our requirements are the area and the delay respectively
    def __init__(self,filename):
        print("reached extraction script")
        self.my_file = open(filename,"r+")
        self.my_file.seek(0)

    def __del__(self):
        print("deleted extraction script object")

    def main(self):
        cont = self.my_file.readlines()
        headings = cont[0]
        values = cont[1]
        hwords = []
        vwords = []

        j = ''
        for i in headings:
            if(i !='\t'):
                j = j+i
            if(i =='\t'):
                hwords.append(j)
                j = ''
        j = ''
        for i in values:
            if(i !='\t'):
                j = j+i
            if(i =='\t'):
                vwords.append(j)
                j = ''

        area = -1
        delay = 0
        for i in range(0,len(hwords)):
            if(hwords[i] == 'logic_block_area_total'):
                area = float(vwords[i])
                print(area)
            if(hwords[i] == 'crit_path_total_sta_time'):
                delay = float(vwords[i])
                print(delay)
        self.my_file.close()
        print(len(hwords))
        print(len(vwords))
        return area*delay


if __name__ == "__main__":
    #this initial solution works for the vtr tool benchmarks, for the koios benchmarks we need to change the initial solution as the dsp,bram chip numbers required for them are more
    
    initial_sol = [10,[[6,1,20], [8,1,20], [9,1,20], [10,1,20], [11,1,20], [12,1,20], [13,1,20], [14,1,20]],[[2, 1, 20], [3, 1, 20], [4, 1, 20], [5, 1, 20], [6, 1, 20]]] #this is a random initial solution
    num_run_num = 5
    num_gen = 50
    cross_prob = 0.87
    mut_prob = 0.7
    ga_object = genetic_algorithm(initial_sol,num_run_num,num_gen,cross_prob,mut_prob)
    fitness_value = ga_object.func()
    del ga_object
