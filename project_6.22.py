import numpy as np

# V = 'GTAGGCTTAAGGTTA'
# W = 'TAGATA'

# V = 'TCGCGGTATGGCATGATAGCGCCCGGAA'
# W = 'TATAAT'

#diavazei tin megali akolouthia V
with open('data1_6.22.txt', 'r') as data1:
    V = data1.read()
    data1.close()
#diavazi tin mikri akolouthia W
with open('data2_6.22.txt', 'r') as data2:
    W = data2.read()
    data1.close()


def Similar(A, B):
    if A == B:
        return 1
    else:
        return -1


def Fit_Sequence(V, W):
    # kostos astoxias
    d = -1
    n = len(W) + 1
    m = len(V) + 1

    S = np.zeros([n, m], dtype='int')
    B = np.zeros([n, m], dtype='int')

    for i in range(n):
        S[i][0] = i * d

    for i in range(1, n):
        for j in range(1, m):
            Match = S[i - 1][j - 1] + Similar(V[j - 1], W[i - 1])
            Delete = S[i - 1][j] + d
            Insert = S[i][j - 1] + d
            S[i][j] = max(Match, Delete, Insert)

            # if Delete >= Match and Delete >= Insert:
            #     B[i][j] = 1
            # elif Insert >= Match:
            #     B[i][j] = 2
            # else:
            #     B[i][j] = 3

            if V[j - 1] == W[i - 1] and Match >= Delete and Match >= Insert:
                B[i][j] = 3
            else:
                if Delete == max(Match, Delete, Insert):
                    B[i][j] = 1
                elif Insert == max(Match, Delete, Insert):
                    B[i][j] = 2
                else:
                    B[i][j] = 3

    return S, B


def Read_B(V, W, S, B):
    d = -1
    AlignmetV = ''
    AlignmetW = ''
    i = len(W)
    j = np.argmax(S[i])
    BestScore = S[i][j]

    while B[i][j] != 0:
        if B[i][j] == 3:
            AlignmetV = V[j - 1] + AlignmetV
            AlignmetW = W[i - 1] + AlignmetW
            i -= 1
            j -= 1
        elif B[i][j] == 1:
            AlignmetV = '-' + AlignmetV
            AlignmetW = W[i - 1] + AlignmetW
            j -= 1
        else:
            AlignmetV = V[j - 1] + AlignmetV
            AlignmetW = '-' + AlignmetW
            j -= 1

    print('The aligment of V is: ')
    print(AlignmetV)
    print('The aligment of W is: ')
    print(AlignmetW)
    print('And the best score is: ' + str(BestScore))


if __name__ == "__main__":
    if len(V)> len(W):
        s, b = Fit_Sequence(V, W)

        # print('to S einai:')
        # print(s)
        # print('to B einai ')
        # print(b)

        Read_B(V, W, s, b)
    else:
        print('invalid data!')