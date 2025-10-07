def triangularise (S : list[list[float]], X: list[float]) -> list[float]:
    n = len(S)
    m = len(S[0])
    for i in range (m-1):
        a = S[i][i]
        for j in range (i+1, n):
            b = S[j][i]
            for k in range(m):
                S[j][k] = b*S[i][k] - a*S[j][k]
            X[j] = b*X[i] - a*X[j]

def back_substitution (S, X):
    n = len(S)
    m = len(S[0])
    for i in range(n-1,0,-1):
        X[i] = sum([S[i][j]*X[j] for j in range(m)])/X[i]

def print_matrix(M):
    for i in M:
        for j in i:
            print(str(j), end = " ")
        print("\n")

def gaussian_system (S,X):
    triangularise(S, X)
    back_substitution(S,X)
    print_matrix(S)
    print(X)
    return X
    
gaussian_system([[1.,2.],[3.,1.]],[1.,2.])




"""
1x+2y=x
3x+y=2y

2y=x
3x=Y









"""