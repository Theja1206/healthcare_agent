def calculator(expression: str):
    """
    simple calculator tool for ai agent 
    example: 5+10*2
    """
    try:
       result = eval(expression)
       return f"calculation result: {result}"
    except Exception as e:
        return f"error in calculation: {str(e)}" 
    
