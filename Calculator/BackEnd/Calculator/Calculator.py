from math import cos, sin, tan, atan, acos, asin, sqrt, pi, e, log10, log


def tokenize(exp):

    tokens = list()
    exp = " " + exp + " "
    prev = " " # prev is used to notify the algorithm when parsing (-) to know whether it is subtraction or a minus sign of a number

    n = len(exp)
    i = -1
    while i < n:
        
        c = exp[i]

        if c == "+" or c == "/" or c == "^" or c == "*" or c == "%": # tokenize +, /, *, %
            tokens.append(c)
            prev = "opr"

        elif c == "(": # tokenize (
            tokens.append(c)
            prev = "("

        elif c == ")": # tokenize )
            tokens.append(c)
            prev = ")"
        
        elif c == "t" or c == "c" and (n - i + 1) >= 3: #tokenize tan or cos
            tokens.append(exp[i:i+3])
            prev = "opr"
            i += 2

        elif c == "s":
            if exp[i+1] == "q" and (n - i + 1) >= 4: # tokenize sqrt
                tokens.append(exp[i:i+4])
                i += 3
            elif (n - i + 1) >= 3: # tokenize sin
                tokens.append(exp[i:i+3])
                i += 2

            prev = "opr"

        elif c == "l":
            if exp[i + 1] == 'n' and (n - i + 1) >= 2: # tokenize ln
                tokens.append(exp[i:i + 2])
                i += 1
            
            elif exp[i + 1] == 'o' and (n - i + 1) >= 3: # tokenize log  (to base 10)
                tokens.append(exp[i:i+3])
                i += 2
            
            prev = "opr"


        elif c == "-": #tokenize - wheter it means subtraction or minus depend on prev
            if prev == "num" or prev == ")":
                tokens.append("-")
                prev = "opr"
                i += 1
                continue 

            j = i + 1; num = "-"
            encs = 1 if i < n - 1 and exp[j] != "e" else 2
            while j < n and (exp[j].isdigit() or exp[j] == "p" or exp[j] == "i" or exp[j] == "e" or exp[j] == "." or (encs == 0  and exp[j] == "-" )):
                if exp[j] == "e": encs -= 1
                num += exp[j]
                j += 1
            tokens.append(num)
            prev = "num"
            i = j - 1
            
        
        elif c.isdigit() or c == "e" or c == "p":

            j = i + 1; num = c
            encs = 1
            while j < n and (exp[j].isdigit() or exp[j] == "p" or exp[j] == "i" or exp[j] == "e" or exp[j] == "." or (encs == 0  and exp[j] == "-" ) ):
                if exp[j] == "e": encs -= 1
                num += exp[j]
                j += 1
            tokens.append(num)
            prev = "num"
            i = j - 1

        i += 1 # update counter

    return tokens
        

def toPostFix(tokens):
    
    post = []; stack = []
    precedence = { # define the presedence of operators
    "(" : -5,
    "+" : 1, "-": 1,
    "*" : 2, "/": 2, "%" : 2,
    "^": 3,
    "cos" : 4, "sin" : 4, "tan" : 4, "atan" : 4, "asin": 4, "acos": 4, "sqrt": 4, "ln": 4, "log": 4}
    

    for tkn in tokens:

        if tkn[0].isdigit() or tkn[0] == '.' or tkn == "pi" or tkn == 'e':

            if tkn[0].isdigit() or tkn[0] == '.': post.append(float (tkn) )
            elif tkn == "pi": post.append(pi)
            elif tkn == "e": post.append(e)



        elif tkn[0] == '-' and len(tkn) > 1:
            
            if tkn[1].isdigit() or tkn[1] == '.': post.append( float (tkn) )
            elif tkn[1] == "p" : post.append(-1 * pi)
            elif tkn[1] == "e" : post.append(-1 * e)

        
        elif tkn == "(":
            stack.append(tkn)

        elif tkn == ")":
            while len(stack) > 0 and stack[len(stack) - 1] != "(":
                post.append(stack.pop())

            stack.pop()


        else:

            if len(stack) == 0:
                stack.append(tkn)
                continue

            while len(stack) > 0 and precedence[stack[len(stack) - 1]] >= precedence[tkn]:
                post.append(stack.pop())

            stack.append(tkn)

    
    while len(stack) > 0:
        post.append(stack.pop())

    return post


def reslolve(post):
    
    unary = {"cos": lambda x: cos(x) , "sin": lambda x: sin(x), "tan": lambda x: tan(x),
            "acos": lambda x: acos(x), "asin": lambda x: asin(x), "atan": lambda x: atan(x), "sqrt": lambda x: sqrt(x),
            "ln": lambda x: log(x), "log": lambda x: log10(x)}

    binary = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y,
             "/": lambda x, y: x / y, "%": lambda x, y: x % y, "^": lambda x, y: x ** y}
    
    i = 0
    while(i < len(post)):
        if isinstance(post[i], float):
            i += 1
         

        elif post[i] in binary.keys(): #evaluate binary operators
            op1 = post[i - 2]; op2 = post[i - 1]
            res = binary[post[i]](op1, op2)
            post[i] = res
            del post[i - 2: i]
            i -= 2


        elif post[i] in unary.keys(): #evalueate unary functions
            op = post[i - 1]
            res = unary[post[i]](op)
            post[i] = res
            del post[i-1]
            i -= 1


    return post[0]
    


def evaluate(exp):
    tokens = tokenize(exp)
    post = toPostFix(tokens)
    result = reslolve(post)
    return result


print(evaluate("15+cos(pi/3)"))