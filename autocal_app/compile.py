class Item:     #項の中身(名前、項)
    def __init__(self,item):
        self.number = 1
        if item[0] == '-':
            self.number = -1
            item = item[1:]

        if item.isdecimal():
            self.number *= int(item)
            self.literal_expr = ''

        elif item.isalpha():
            self.literal_expr = item

        else:
            borderline = 0
            for ct,partition in enumerate(item):
                if partition.isdecimal() == False:
                    borderline = ct    #正規表現で左側の数字の文字列の長さを検出して格納する
                    break
            self.literal_expr = "".join(sorted(( item[borderline:] )))
            self.number *= int(item[:borderline])
            
class expr_list:
    def __init__(self,expr):
        if expr == '':
            self.expr_compose = []
            return

        expr_devided = expr[0] + expr[1:].replace('+','/').replace('-','/-')#演算子ごとに'/'を付けるが先頭の'-'には'/'を付けない
        self.expr_compose = [Item]*(expr_devided.count('/')+1)
        for ct,splited in enumerate(expr_devided.split('/')):
            self.expr_compose[ct] = Item(splited)

    def arrange(self):
        output = ''
        for expr_partition in self.expr_compose:
            if expr_partition.number == 0:
                continue
            elif expr_partition.number == 1:
                add_compose = expr_partition.literal_expr
            elif expr_partition.number == -1:
                add_compose = '-' + expr_partition.literal_expr
            else:
                add_compose = str( expr_partition.number ) + expr_partition.literal_expr
            
            if add_compose == '-':   #文字が何もなくて定数が-1だった時への対処
                add_compose = '-1'

            elif add_compose[0] != '-' and len(output) > 0:
                add_compose = '+' + add_compose
            output += add_compose

        return output

class cal:
    def compile(self,exper):
        if isinstance(exper,str) or len(exper) == 0:
            return exper
        output = []
        for partition in exper:
            if  isinstance(partition,list):
                output.append(self.compile(self,partition))

            elif partition == '+'or partition == '-':
                output[-2] = self.__add_sub_cal(self,output[-2],output[-1],partition)
                output.pop(-1)

            elif partition == '*':
                output[-2] = self.__mul_cal(self,output[-2],output[-1])
                output.pop(-1)

            else:
                output.append(partition)

        return output[0]

    def __mul_cal(self,former,latter):
        output= ''
        F_formura = expr_list(former)
        L_formura = expr_list(latter)
        output = expr_list('')
        for F_expr_part in F_formura.expr_compose:
            for L_expr_part in L_formura.expr_compose:
                number = str( F_expr_part.number * L_expr_part.number )
                literal_expr = "".join(sorted(( F_expr_part.literal_expr + L_expr_part.literal_expr )))
                if number == '1':
                    number = ''
                elif number == '-1' and literal_expr != '':
                    number = '-'
                output.expr_compose.append( Item( number + literal_expr ))

        return self.__cleaner(output.arrange())

    def __add_sub_cal(self,former,latter,code):
        if latter[0] != '-':
            latter = '+' + latter

        if code == '+':
            output = former + latter

        else:
            output = former + latter.replace('+','/').replace('-','+').replace('/','-')

        return self.__cleaner(output)

    def __cleaner(expr):
        unclean_list = expr_list(expr)
        cleaned_list = expr_list('')
        for nuclean_list_part in unclean_list.expr_compose:
            identical_compose = None
            for clean_list_part in cleaned_list.expr_compose:
                if clean_list_part.literal_expr == nuclean_list_part.literal_expr:
                    clean_list_part.number += nuclean_list_part.number
                    identical_compose = 'exited'
                    break
            if identical_compose == None:
                cleaned_list.expr_compose.append(nuclean_list_part)

        return cleaned_list.arrange()