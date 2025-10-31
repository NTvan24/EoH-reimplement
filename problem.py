import sys
import types
import numpy as np
import warnings
from gen_instances import GetData

class TSPCONST():
    def __init__(self) -> None:
        self.problem_size = 10
        self.neighbor_size = np.minimum(20,self.problem_size)
        self.n_instance = 2  

        #Gen instances for TSP
        getData = GetData(self.n_instance, self.problem_size)
        self.instance_data = getData.generate_instances()

        #self.prompts = GetPrompts()

    def get_instance_data(self):
        return self.instance_data
    
    def tour_cost(self,instance, solution, problem_size):
        """
        Tính chi phí cho 1 solution
        Returns:
            cost
        """
        cost = 0
        for j in range(problem_size - 1):
            cost += np.linalg.norm(instance[int(solution[j])] - instance[int(solution[j + 1])])
        cost += np.linalg.norm(instance[int(solution[-1])] - instance[int(solution[0])])
        return cost
    
    def generate_neighborhood_matrix(self,instance, problem_size):
        """
        Tạo ma trận xếp thứ tự những đỉnh từ gần đến xa
        Returns:
            Array n x n, với hàng i là danh sách các đỉnh từ gần đến xa so với i
        """
        instance = np.array(instance)
        
        neighborhood_matrix = np.zeros((problem_size, problem_size), dtype=int)

        for i in range(problem_size):
            distances = np.linalg.norm(instance[i] - instance, axis=1)
            sorted_indices = np.argsort(distances)  # sort indices based on distances
            neighborhood_matrix[i] = sorted_indices

        return neighborhood_matrix
    
    def greedy(self,heurictics):
        """
        Đánh giá heurictics bằng greedy, trả về trung bình fitness trên tất cả các instance
        Returns:
            Trung bình fitness
        """
        all_cost = np.ones(self.n_instance)
        for index, (instance, distance_matrix) in enumerate(self.instance_data):
            neighborhood_matrix = self.generate_neighborhood_matrix(instance,len(instance))
            curr_node= 0
            end_node= 0
            route = np.zeros(self.problem_size)
            for i in range(1,len(instance)-1):
                near_nodes  = neighborhood_matrix[curr_node][1:] # Lấy 1: vì cái đầu tiên luôn là chính nó
                mask = ~np.isin(near_nodes,route[:i]) 
                unvisited_near_nodes = near_nodes[mask]
                unvisited_near_nodes = unvisited_near_nodes[:np.minimum(self.neighbor_size,unvisited_near_nodes.size)] #Lấy tối đa neighbor_size hàng xóm thôi
                
                next_node = heurictics.select_next_node(curr_node, end_node, unvisited_near_nodes, distance_matrix) 

                if next_node in route:
                    print("heurictics wrong")
                    return None
                current_node = next_node

                route[i] = current_node
            
            mask = ~np.isin(np.arange(self.problem_size),route[:self.problem_size-1])

            last_node = np.arange(self.problem_size)[mask]
            curr_node = last_node[0]
            route[self.problem_size-1] = curr_node

            cost = self.tour_cost(instance,route,self.problem_size)
            all_cost[index]=cost
        
        average_cost = np.average(all_cost)
        return average_cost
    
    def evaluate(self, code_string):
        """
        Import code_string thành 1 hàm, chạy hàm greedy với hàm đó
        Returns:
            Trung bình fitness của hàm heurictics
        """
        
        try:
            # Suppress warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Create a new module object
                heuristic_module = types.ModuleType("heuristic_module")
                
                # Execute the code string in the new module's namespace
                exec(code_string, heuristic_module.__dict__)

                # Add the module to sys.modules so it can be imported
                sys.modules[heuristic_module.__name__] = heuristic_module

                # Now you can use the module as you would any other
                fitness = self.greedy(heuristic_module)

                
                return fitness
        except Exception as e:
            
            print("Error bla:", str(e))
            print(code_string)
            return None


        
        