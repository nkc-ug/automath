class Method:
    def convert_to_rpn(self,expr):
        length = len(expr)
        if length < 2 or expr.isdigit():
            return expr

        if self.find_extra_brackets(expr):
            expr = expr[1:-1]
        
        return self.find_add_sub(self,expr) or self.find_mul(self,expr) or expr

    def find_extra_brackets(expr):
        brackets_deep = 0
        for c in expr[:-1]:
            if c == '(':
                brackets_deep += 1
            elif c == ')':
                brackets_deep -= 1

            if brackets_deep == 0:
                return False
        return True

    def find_add_sub(self,expr):
        if len(expr) < 2 or expr.isdigit():
            return None
        output = []
        code_stack = []
        code_insert_timing = 0  #'*'を挿入するタイミングを管理する
        brackets_deep = 0
        st = 0
        for ct, c in enumerate(expr):
            brackets_deep = self.measure_brackets_deep(brackets_deep,c)
            if brackets_deep > 0:
                continue

            if c == '+' or c == '-':
                output.append(self.convert_to_rpn(self,expr[st:ct]))
                code_stack.append(c)
                code_insert_timing += 1
                if code_insert_timing >= 2:
                    output.append(code_stack[0])
                    code_stack.pop(0)
                    code_insert_timing = 1
                st = ct + 1
        
        if len(output) < 1:
            return None

        output.append(self.convert_to_rpn(self,expr[st:]))
        output.append(code_stack[-1])
        return output

    def find_mul(self,expr):
        if len(expr) < 2 or expr.isdigit():
            return None
        output = []
        code_insert_timing = 0  # ２になると演算子挿入
        deep = 0
        st = 0
        for ct, c in enumerate(expr):
            deep = self.measure_brackets_deep(deep,c)
            if deep == 0 and c != '-':
                if c == '*':
                    st = ct + 1

                elif ct >= len(expr)-1:
                    output.append(self.convert_to_rpn(self,expr[st:]))
                    code_insert_timing += 1
                    st = ct + 1

                elif ( c.isdecimal() and expr[ct+1].isdecimal()) == False:
                    output.append(self.convert_to_rpn(self,expr[st:ct+1]))
                    code_insert_timing += 1
                    st = ct + 1
            
                if( code_insert_timing == 2 ):
                    output.append('*')
                    code_insert_timing = 1
        return output

    def measure_brackets_deep(brackets_deep,c):
        if c == '(':
            brackets_deep += 1
        elif c == ')':
            brackets_deep -= 1
        return brackets_deep

    def convert_list_to_str(self,list):
        array = []
        for cell in list:
            if isinstance(cell, str):
                array.append(cell)
            else:
                array += self.convert_list_to_str(self,cell)

        return array