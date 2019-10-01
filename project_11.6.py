import math

obs = ('1', '1', '2', '1', '2', '2')

states = ('D1', 'D2','END')

alpha_beta = ('1', '2', '3')

start_prob = {'D1': 0.5, 'D2': 0.5,'END': 0}

trans_prob = {
   'D1': {'D1': 0.5, 'D2': 0.25,'END': 0.25},
   'D2': {'D1': 0.25, 'D2': 0.5,'END': 0.25},
   'END':{'D1': 0, 'D2': 0,'END': 0}
   }

emit_prob = {
   'D1': {'1': 0.5, '2': 0.25, '3': 0.25},
   'D2': {'1': 0.25, '2': 0.5, '3': 0.25},
   'END': {'1': 0, '2': 0, '3': 0},
   }


def logarithm_convertion(Dict2D,firstD,secondD):
    for i in firstD:
        for j in secondD:
            if Dict2D[i][j] == 0:
                Dict2D[i][j] = -float('Inf')
            else:
               Dict2D[i][j] = math.log2(Dict2D[i][j])
    return Dict2D


def viterbi(obs, states, ab, start_p, trans_p, emit_p):
    #ftiaxnei mia lista pou periexei ena adio dict
    #se auti tin lista tha apothikeuete i megisti pithanotita metavasis kai ekpompis simvolou
    S = [{}]

    # ipologizoume apo poia katastasi tha ekpemthei to proto simvolo
    for st in states:
        if start_p[st] == 0:
            S[0][st] = {'prob': - float('Inf'), 'prev': None}
        else:
            S[0][st] = {'prob': math.log2(start_p[st]) + emit_p[st][obs[0]], 'prev': None}
    # gia ta ipolipa simvola
    for inp in range(1,len(obs)):
        S.append({})
        for st in states:
            #vriskei tin megisti pithanotita metavasis sto trexon state apo to proigoumeno
            max_tr_prob = max(S[inp - 1][prev_st]["prob"] + trans_p[prev_st][st] for prev_st in states)
            #afou vrike tin pithanotita metavasis
            #psaxnei na vrei poio itan to proigoumeno state mesa apo ta states
            for prev_st in states:
                if S[inp - 1][prev_st]["prob"] + trans_p[prev_st][st] == max_tr_prob:
                    #ipologizei tin sinoliki pithanotita(ekpompis kai metavasis)
                    max_prob = max_tr_prob + emit_p[st][obs[inp]]
                    #kai ta apothikeuei sto dictionary
                    S[inp][st] = {"prob": max_prob, "prev": prev_st}
                    break
    #prosthetoume to final state stin e3odo
    S.append({})
    for st in states:
        if st == 'END':
            max_tr_prob = max(S[len(obs)-1][prev_st]["prob"] + trans_p[prev_st][st] for prev_st in states)
            # afou vrike tin pithanotita metavasis
            # psaxnei na vrei poio itan to proigoumeno state mesa apo ta states
            for prev_st in states:
                if S[len(obs)-1][prev_st]["prob"] + trans_p[prev_st][st] == max_tr_prob:
                    S[len(obs)][st] = {"prob": max_tr_prob, "prev": prev_st}
                    break
        else:
            tr_prob = - float('Inf')
            S[len(obs)][st] = {'prob': tr_prob, 'prev': None}

    for line in dptable(S):
        print(line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in S[-1].values())
    previous = None
    # Get most probable state and its backtrack

    for st, data in S[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    print(opt)
    print(previous)
    # Follow the backtrack till the first observation
    for t in range(len(S) - 2, -1, -1):
        opt.insert(0, S[t + 1][previous]["prev"])
        previous = S[t + 1][previous]["prev"]
    #prosthiki tis arxikis katastasis start
    opt.insert(0,'START')
    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)


def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


def kBestViterbi(obs, states, ab, start_p, trans_p, emit_p):
    kBestS = [{}]
    for st in states:
        if start_p[st] == 0:
            pr_list = [- float('Inf')]
            kBestS[0][st] = {'prob': pr_list, 'prev': None}
        else:
            pr_list = [math.log2(start_p[st]) + emit_p[st][obs[0]]]
            kBestS[0][st] = {'prob': pr_list, 'prev': None}
    # gia ta ipolipa simvola
    for inp in range(1, len(obs)):
        kBestS.append({})
        for st in states:
            tr_pr = []
            prev = []
            for prev_st in states:
                tr_prob = max(kBestS[inp - 1][prev_st]["prob"]) + trans_p[prev_st][st] + emit_p[st][obs[inp]]
                tr_pr.append(tr_prob)
                prev.append(prev_st)
            kBestS[inp][st] = {'prob': tr_pr, 'prev':prev}
    #termatiki katastasi
    kBestS.append({})
    for st in states:
        if st == 'END':
            tr_pr = []
            prev = []
            for prev_st in states:
                tr_prob = max(kBestS[len(obs)-1][prev_st]["prob"]) + trans_p[prev_st][st]
                tr_pr.append(tr_prob)
                prev.append(prev_st)
            kBestS[len(obs)][st] = {'prob': tr_pr, 'prev': prev}
        else:
            pr_list = [- float('Inf')]
            kBestS[len(obs)][st] = {'prob': pr_list, 'prev': None}

    #Euresi ton K best paths
    #gia na vroume ta K best paths prepei na elen3oume 2 periptosis:
    #an stin katastasi END emfanizete i megisti pithanotita me parapano apo enan progonous
    opt = [[]]
    opt[0].append('END')
    max_prob = max(kBestS[len(obs)]['END']['prob'])
    previous = None
    counter = 0
    for i in range(len(states)):
        #anazitisi tou previous
        if max_prob == kBestS[len(obs)]['END']['prob'][i] and counter == 0:
            previous = kBestS[len(obs)]['END']['prev'][i]
            #afou vrei tin teliki katastasi enos path me megisti pithanotita
            #kanei backtrack sto sigkekrimeno path
            # gia tin euresi olon ton best path tha xrisimopoiithei anadromi
            FindBestPath(kBestS, len(obs), len(states), opt, previous, counter)
            counter = counter + 1
        elif max_prob == kBestS[len(obs)]['END']['prob'][i] and counter != 0:
            opt.append(list(opt[counter-1]))
            previous = kBestS[len(obs)]['END']['prev'][i]
            FindBestPath(kBestS, len(obs), len(states), opt, previous, counter)
            counter = counter + 1
        else:
            pass
    #prosthetoume se kathe veltisto path tin arxiki katastasi start!
    print('The number of best paths is:' + str(len(opt)))
    for i in range(len(opt)):
        opt[i].insert(0 , 'START')
        print('Best path ' + str(i+1)+ ' is:')
        print(opt[i])

def FindBestPath(kBestS, inpLen, stagesLen, opt, previous, counter):
    opt[counter].insert(0, previous)
    for inp in range(inpLen -1, 0, -1):
        #opt[counter].insert(0,previous)
        #evresi tou kenouriou max_prob
        max_prob = max(kBestS[inp][previous]['prob'])
        # gia na vroume to kenourio previous
        # veiskoume tin tin megisti pithanotita na einai se auti tin katastasi
        # an emfanizete parapano apo mia fora kanoume anadromi
        count = 0
        new_previous = None
        for i in range(stagesLen):
            if max_prob == kBestS[inp][previous]['prob'][i] and count == 0:
                new_previous = kBestS[inp][previous]['prev'][i]
                count = count +1
            elif max_prob == kBestS[inp][previous]['prob'][i] and count != 0:
                opt.append(list(opt[counter]))
                temp_previous = kBestS[inp][previous]['prev'][i]
                FindBestPath(kBestS, inp, len(states), opt, temp_previous, count)
                count = count + 1
            else:
                pass
        previous = new_previous
        opt[counter].insert(0, previous)
if __name__ == "__main__":
    #logarithmizoume ta trans_p kai emit_p
    trans_p = logarithm_convertion(trans_prob, states, states)
    emit_p = logarithm_convertion(emit_prob, states, alpha_beta)
    inp = input('For Viterbi Algorithm press "1", In order to get the K best paths press "2", Press others to exit. ')
    while inp == '1' or inp == '2':
        if inp == '1':
            viterbi(obs,
                    states,
                    alpha_beta,
                    start_prob,
                    trans_prob,
                    emit_prob)

        else:
            kBestViterbi(obs,
                         states,
                         alpha_beta,
                         start_prob,
                         trans_prob,
                         emit_prob)

        inp = input('For Viterbi Algorithm press "1", In order to get the K best paths press "2", Press others to exit. ')
