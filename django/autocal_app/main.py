from . import make_rpm,compile
def calculation(expr):
    temp_expr = make_rpm.Method.convert_to_rpn(make_rpm.Method,expr)
    result_expr = compile.cal.deploy(compile.cal,temp_expr)
    return result_expr