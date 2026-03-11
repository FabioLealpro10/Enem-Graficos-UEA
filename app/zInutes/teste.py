


from time import sleep



def giro_1(qdt):

    # 1 
    # 2 2
    # 3 3 3
    # 4 4 4 4
    # 5 5 5 5 5

    for i in range(1, qdt+1):
        print(f'* '*i)




def giro_2(qdt):
    # 1 1 1 1 1
    # 2 2 2 2 
    # 3 3 3 
    # 4 4
    # 5
    for i in range(1, qdt+1):
        print(f'* '*((qdt+1) -i))

def giro_3(qdt):

    #   1 1 1 1 1
    #     2 2 2 2
    #       3 3 3
    #         4 4
    #           5
    for i in range(qdt):
        print('  '*(i+1),' *'*(qdt - i))



def giro_4(qdt):
    #         1
    #       2 2
    #     3 3 3
    #   4 4 4 4
    # 5 5 5 5 5
    for i in range(1, qdt+1):
        print(("  "*(qdt - i))+'*', end=' ')
        for e in range(1, i):
             print('*',end=' ')
        print()


    




def limpar(v=100):
    print('\n'*v)



def rum(qdt):
    while True:
        limpar()
        giro_1(qdt)
        sleep(1)
        limpar()
        giro_2(qdt)
        sleep(1)
        limpar()
        giro_3(qdt)
        sleep(1)
        limpar()
        giro_4(qdt)
        sleep(1)

#rum(70)

# def f2():

#     print('Olá mundo'if (x>0)else)


    