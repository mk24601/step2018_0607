def readNumber(line, index):

    number = 0

    flag = 0

    keta = 1

    while index < len(line) and (line[index].isdigit() or line[index] == '.'):

        if line[index] == '.':

            flag = 1

        else:

            number = number * 10 + int(line[index])

            if flag == 1:

                keta *= 0.1

        index += 1

    token = {'type': 'NUMBER', 'number': number * keta}

    return token, index


def readPlus(line, index):

    token = {'type': 'PLUS'}

    return token, index + 1


def readMinus(line, index):

    token = {'type': 'MINUS'}

    return token, index + 1


def readMultip(line, index):

    token = {'type': 'MULTIP'}

    return token, index + 1


def readDevision(line, index):

    token = {'type': 'DEVISION'}

    return token, index + 1


def readLeftPar(line, index): # 左かっこを読み込む

    token = {'type': 'LEFT'}

    return token, index + 1


def readRightPar(line, index): # 右かっこを読み込む

    token = {'type': 'RIGHT'}

    return token, index + 1


def tokenize(line):

    tokens = []

    index = 0

    while index < len(line):

        if line[index].isdigit():

            (token, index) = readNumber(line, index)

        elif line[index] == '+':

            (token, index) = readPlus(line, index)

        elif line[index] == '-':

            (token, index) = readMinus(line, index)

        elif line[index] == '*':

            (token, index) = readMultip(line, index)

        elif line[index] == '/':

            (token, index) = readDevision(line, index)

        elif line[index] == '(':

            (token, index) = readLeftPar(line, index)

        elif line[index] == ')':

            (token, index) = readRightPar(line, index)
        else:

            print('Invalid character found: ' + line[index])

            exit(1)

        tokens.append(token)

    return tokens


def evalParenthesis(tokens): # かっこを処理する関数
    indexLeft = 1
    while indexLeft < len(tokens):
        counter = 0 #counterは左かっこを見つけたら++1,右かっこを見つけたら--1される．
        if tokens[indexLeft]['type'] == 'LEFT': #ここで見つかった左かっこのペアが見つかるまで，↓のwhileループはずっと続く．
            indexRight = indexLeft + 1
            while True:
                if tokens[indexRight]['type'] == 'LEFT':
                    counter += 1
                elif tokens[indexRight]['type'] == 'RIGHT':
                    if counter == 0: #counter = 0のときに右かっこがみつかったら，その右かっこが探していた「ペア」．
                        break
                    else:
                        counter -=1
                indexRight +=1
            tokens[indexLeft]['number'] = evaluate(tokens[indexLeft+1:indexRight]) #indexLeft ~ indexRight間のトークンをevaluate()へ
            tokens[indexLeft]['type'] = 'NUMBER'
            for i in range(indexRight - indexLeft):
                tokens.pop(indexLeft+1)
        indexLeft+=1

def evaluateMD(tokens): # ×÷を処理する関数
    index = 1

    while index < len(tokens):

        if tokens[index]['type'] == 'MULTIP': # 掛け算だった場合

            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER' : # ×の前後がそれぞれ数字か確認
                tokens[index - 1]['number'] = tokens[index - 1]['number'] * tokens[index + 1]['number'] # 3 * 2 の場合，もともと「3」が入っていたトークンに演算結果(6)を代入する
                tokens.pop(index) # 「*」「2」が入っていたトークンを削除
                tokens.pop(index)
                index -= 1

            else:

                print('Invalid syntax')

        elif tokens[index]['type'] == 'DEVISION': # 割り算だった場合

            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER' : # ÷の前後がそれぞれ数字か確認
                tokens[index - 1]['number'] = tokens[index - 1]['number'] / tokens[index + 1]['number'] # 6 / 2 の場合，もともと「6」が入っていたトークンに演算結果(3)を代入する
                tokens.pop(index) # 「/」「2」が入っていたトークンを削除
                tokens.pop(index)
                index -= 1

            else:

                print('Invalid syntax')

        index += 1

def evaluatePM(tokens): # ＋−を処理する関数
    answer = 0
    index = 1

    while index < len(tokens):

        if tokens[index]['type'] == 'NUMBER':

            if tokens[index - 1]['type'] == 'PLUS':

                answer += tokens[index]['number']

            elif tokens[index - 1]['type'] == 'MINUS':

                answer -= tokens[index]['number']

            else:

                print('Invalid syntax')

        index += 1

    return answer


def evaluate(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    evalParenthesis(tokens) # かっこを処理する関数
    evaluateMD(tokens) # ×÷を処理する関数
    answer = evaluatePM(tokens) # ＋−を処理する関数

    return answer


def test(line, expectedAnswer):

    tokens = tokenize(line)

    actualAnswer = evaluate(tokens)

    if abs(actualAnswer - expectedAnswer) < 1e-8:

        print("PASS! (%s = %f)" % (line, expectedAnswer))

    else:

        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))







# Add more tests to this function :)

def runTest():

    print("==== Test started! ====")

    test("1",1) # 数字単品

    test("1+2", 3) # 二項の足し算

    test("1.0+2.1-3", 0.1) # 多項の足し算

    test("2*3", 6) # 二項の掛け算

    test("1*2*3*4*5", 120) # 多項の掛け算

    test("4/2",2) # 二項の割り算

    test("120/5/4/3", 2) # 多項の割り算

    test("2+6/2*7-3",20) # + - * / 四種類の混じった計算

    test("(2+6)/2*(7-3)",16) # かっこの入った計算

    test("2*((4+6)/5)",4) # 二重かっこの入った計算

    test("((6+(2+3*2)/2))+(3+4/2)*(6+10)/((2*1)-1)",90) # 三重以上のかっこを含む複雑な問題

    print("==== Test finished! ====\n")

runTest()




while True:

    print('> ')

    line = input()

    tokens = tokenize(line)

    answer = evaluate(tokens)

    print("answer = %f\n" % answer)
