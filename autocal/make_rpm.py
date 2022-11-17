class Method:
#   逆ポーランド記法への変換
    def convert_to_rpn(self,expr):
        length = len(expr)
        if length < 2 or expr.isdigit():
            return expr

        if self.__find_brackets(expr) == length-1:
            expr = expr[1:-1]
        
        return self.__find_add_sub(self,expr) or self.__find_mul(self,expr) or expr

        # 不要な括弧の検出
    def __find_brackets(expr):
        deep = 0
        for ct, c in enumerate(expr):
            if c == '(':
                deep += 1
            elif c == ')':
                deep -= 1

            if deep == 0:
                break
        return ct

        # 演算子の検出　＋、ー
    def __find_add_sub(self,expr):
        if len(expr) < 2 or expr.isdigit():
            return None
        result = []
        code = []
        code_ct = 0
        deep = 0
        st = 0
        for ct, c in enumerate(expr):
            deep = self.__deep_process(deep,c)
            if deep == 0:
                if c == '+' or c == '-':
                    result.append(self.convert_to_rpn(self,expr[st:ct]))
                    code.append(c)
                    code_ct += 1
                    if code_ct >= 2:
                        result.append(code[0])
                        code.pop(0)
                        code_ct = 1
                    st = ct + 1
        
        if len(result) < 1:
            return None

        result.append(self.convert_to_rpn(self,expr[st:]))
        result.append(code[-1])
        return result

        # 演算子の検出
    def __find_mul(self,expr):
        if len(expr) < 2 or expr.isdigit():
            return None
        result = []
        code_ct = 0
        deep = 0
        st = 0
        for ct, c in enumerate(expr):
            deep = self.__deep_process(deep,c)
            if deep == 0 and c != '-':
                if c == '*':
                    st = ct + 1

                elif ct >= len(expr)-1:
                    result.append(self.convert_to_rpn(self,expr[st:]))
                    code_ct += 1
                    st = ct + 1

                elif ( c.isdecimal() and expr[ct+1].isdecimal()) == False:
                    result.append(self.convert_to_rpn(self,expr[st:ct+1]))
                    code_ct += 1
                    st = ct + 1
            
                if( code_ct > 1 ):
                    result.append('*')
                    code_ct = 1
        return result

        # 再帰関数の深さ
    def __deep_process(deep,c):
        if c == '(':
            deep += 1
        elif c == ')':
            deep -= 1
        return deep