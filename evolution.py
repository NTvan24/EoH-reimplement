import re
import time
from prompt import GetPrompts
from llm import LLMAPI
class Evolution():

    def __init__(self, **kwargs):

        # set prompt interface
        prompts = GetPrompts()
        self.prompt_task         = prompts.get_task()
        self.prompt_func_name    = prompts.get_func_name()
        self.prompt_func_inputs  = prompts.get_func_inputs()
        self.prompt_func_outputs = prompts.get_func_outputs()
        self.prompt_inout_inf    = prompts.get_inout_inf()
        self.prompt_other_inf    = prompts.get_other_inf()
        if len(self.prompt_func_inputs) > 1:
            self.joined_inputs = ", ".join("'" + s + "'" for s in self.prompt_func_inputs)
        else:
            self.joined_inputs = "'" + self.prompt_func_inputs[0] + "'"

        if len(self.prompt_func_outputs) > 1:
            self.joined_outputs = ", ".join("'" + s + "'" for s in self.prompt_func_outputs)
        else:
            self.joined_outputs = "'" + self.prompt_func_outputs[0] + "'"

        # set LLMs
        self.interface_llm = LLMAPI()
    

    import re

    def get_alg_and_code(self, prompt):
        response = self.interface_llm.get_reponse(prompt)

        algorithm = re.findall(r"\{(.*)\}", response, re.DOTALL)
        if len(algorithm) == 0:
            if 'python' in response:
                algorithm = re.findall(r'^.*?(?=python)', response,re.DOTALL)
            elif 'import' in response:
                algorithm = re.findall(r'^.*?(?=import)', response,re.DOTALL)
            else:
                algorithm = re.findall(r'^.*?(?=def)', response,re.DOTALL)

        code = re.findall(r"import.*return", response, re.DOTALL)
        if len(code) == 0:
            code = re.findall(r"def.*return", response, re.DOTALL)

        n_retry = 1
        while (len(algorithm) == 0 or len(code) == 0):
            if self.debug_mode:
                print("Error: algorithm or code not identified, wait 1 seconds and retrying ... ")

            response = self.interface_llm.get_reponse(prompt)

            algorithm = re.findall(r"\{(.*)\}", response, re.DOTALL)
            if len(algorithm) == 0:
                if 'python' in response:
                    algorithm = re.findall(r'^.*?(?=python)', response,re.DOTALL)
                elif 'import' in response:
                    algorithm = re.findall(r'^.*?(?=import)', response,re.DOTALL)
                else:
                    algorithm = re.findall(r'^.*?(?=def)', response,re.DOTALL)

            code = re.findall(r"import.*return", response, re.DOTALL)
            if len(code) == 0:
                code = re.findall(r"def.*return", response, re.DOTALL)
                
            if n_retry > 3:
                break
            n_retry +=1

        algorithm = algorithm[0]
        code = code[0] 

        code_all = code+" "+", ".join(s for s in self.prompt_func_outputs) 


        return [code_all, algorithm]

    def i1(self):
        """
        Operator Init
        Returns:
            [code_all, algorithm]
        """
        prompt_content = self.prompt_task+"\n"\
"First, describe your new algorithm and main steps in one sentence. \
The description must be inside a brace. Next, implement it in Python as a function named \
"+self.prompt_func_name +". This function should accept "+str(len(self.prompt_func_inputs))+" input(s): "\
+self.joined_inputs+". The function should return "+str(len(self.prompt_func_outputs))+" output(s): "\
+self.joined_outputs+". "+self.prompt_inout_inf+" "\
+self.prompt_other_inf+"\n"+"Do not give additional explanations."

        
        [code_all, algorithm] = self.get_alg_and_code(prompt_content)
        return [code_all, algorithm]

    
    def e1(self,parents):
        """
        Toán tử e1, tạo ra 1 heurictics mới hoàn toàn từ cha mẹ
        Returns:
            [code_all, algorithm]
        """

        prompt_indiv = ""
        for i in range(len(parents)):
            prompt_indiv=prompt_indiv+"No."+str(i+1) +" algorithm and the corresponding code are: \n" + parents[i]['algorithm']+"\n" +parents[i]['code']+"\n"
        prompt_content = self.prompt_task+"\n"\
"I have "+str(len(parents))+" existing algorithms with their codes as follows: \n"\
+prompt_indiv+\
"Please help me create a new algorithm that has a totally different form from the given ones. \n"\
"First, describe your new algorithm and main steps in one sentence. \
The description must be inside a brace. Next, implement it in Python as a function named \
"+self.prompt_func_name +". This function should accept "+str(len(self.prompt_func_inputs))+" input(s): "\
+self.joined_inputs+". The function should return "+str(len(self.prompt_func_outputs))+" output(s): "\
+self.joined_outputs+". "+self.prompt_inout_inf+" "\
+self.prompt_other_inf+"\n"+"Do not give additional explanations."
        
        [code_all, algorithm] = self.get_alg_and_code(prompt_content)
        return [code_all, algorithm]
    
    def e2(self,parents):
        """
        Toán tử e2, tạo ra 1 heurictics mới lấy cảm hứng từ cha mẹ
        Returns:
            [code_all, algorithm]
        """

        prompt_indiv = ""
        for i in range(len(parents)):
            prompt_indiv=prompt_indiv+"No."+str(i+1) +" algorithm and the corresponding code are: \n" + parents[i]['algorithm']+"\n" +parents[i]['code']+"\n"

        prompt_content = self.prompt_task+"\n"\
"I have "+str(len(parents))+" existing algorithms with their codes as follows: \n"\
+prompt_indiv+\
"Please help me create a new algorithm that has a totally different form from the given ones but can be motivated from them. \n"\
"Firstly, identify the common backbone idea in the provided algorithms. Secondly, based on the backbone idea describe your new algorithm in one sentence. \
The description must be inside a brace. Thirdly, implement it in Python as a function named \
"+self.prompt_func_name +". This function should accept "+str(len(self.prompt_func_inputs))+" input(s): "\
+self.joined_inputs+". The function should return "+str(len(self.prompt_func_outputs))+" output(s): "\
+self.joined_outputs+". "+self.prompt_inout_inf+" "\
+self.prompt_other_inf+"\n"+"Do not give additional explanations."
      
        [code_all, algorithm] = self.get_alg_and_code(prompt_content)
        return [code_all, algorithm]

    def m1(self,parents):
        """
        Toán tử đột biến m1, tạo ra 1 heurictics mới bằng cách modified 1 thuật toán cũ.
        Returns:
            [code_all, algorithm]
        """
        prompt_content = self.prompt_task+"\n"\
"I have one algorithm with its code as follows. \
Algorithm description: "+parents['algorithm']+"\n\
Code:\n\
"+parents['code']+"\n\
Please assist me in creating a new algorithm that has a different form but can be a modified version of the algorithm provided. \n"\
"First, describe your new algorithm and main steps in one sentence. \
The description must be inside a brace. Next, implement it in Python as a function named \
"+self.prompt_func_name +". This function should accept "+str(len(self.prompt_func_inputs))+" input(s): "\
+self.joined_inputs+". The function should return "+str(len(self.prompt_func_outputs))+" output(s): "\
+self.joined_outputs+". "+self.prompt_inout_inf+" "\
+self.prompt_other_inf+"\n"+"Do not give additional explanations."
      
        [code_all, algorithm] = self.get_alg_and_code(prompt_content)
        return [code_all, algorithm]
    
    def m2(self,parents):
        """
        Toán tử đột biến m2, tạo ra 1 heurictics mới bằng cách sửa parameter 1 thuật toán cũ.
        Returns:
            [code_all, algorithm]
        """
        prompt_content = self.prompt_task+"\n"\
"I have one algorithm with its code as follows. \
Algorithm description: "+parents['algorithm']+"\n\
Code:\n\
"+parents['code']+"\n\
Please identify the main algorithm parameters and assist me in creating a new algorithm that has a different parameter settings of the score function provided. \n"\
"First, describe your new algorithm and main steps in one sentence. \
The description must be inside a brace. Next, implement it in Python as a function named \
"+self.prompt_func_name +". This function should accept "+str(len(self.prompt_func_inputs))+" input(s): "\
+self.joined_inputs+". The function should return "+str(len(self.prompt_func_outputs))+" output(s): "\
+self.joined_outputs+". "+self.prompt_inout_inf+" "\
+self.prompt_other_inf+"\n"+"Do not give additional explanations."
      
        [code_all, algorithm] = self.get_alg_and_code(prompt_content)
        return [code_all, algorithm]
    
    def m3(self,parents):
        """
        Toán tử đột biến m3, tạo ra 1 heurictics mới bằng cách đơn giản hóa thuật toán cho trước
        Returns:
            [code_all, algorithm]
        """
        prompt_content = "First, you need to identify the main components in the function below. \
Next, analyze whether any of these components can be overfit to the in-distribution instances. \
Then, based on your analysis, simplify the components to enhance the generalization to potential out-of-distribution instances. \
Finally, provide the revised code, keeping the function name, inputs, and outputs unchanged. \n"+parents['code']+"\n"\
+self.prompt_inout_inf+"\n"+"Do not give additional explanations."
      
        [code_all, algorithm] = self.get_alg_and_code(prompt_content)
        return [code_all, algorithm]
