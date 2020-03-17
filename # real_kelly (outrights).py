import math
import time
import scipy.optimize
from numpy import asarray
from numpy import log as ln


def optimize(selections: list, bankroll: float):

    start_time = time.time()

    # CREATE A VECTOR OF OUTCOME PROBABILITIES OF SIZE LEN(SELECTIONS)
    probs = [1 / item['odds_fair'] for item in selections]
    print(f'Sum of probabilities add up to {sum(probs)}')

    def f(stakes):
        """ This function will be called by scipy.optimize.minimize repeatedly to find the global maximum """

        # INITIALIZE END_BANKROLLS AND OBJECTIVE BEFORE EACH OPTIMIZATION STEP
        end_bankrolls, objective = len(selections) * [bankroll], 0.00

        # CALCULATE END_BANKROLL FOR EACH SELECTION WITH A 'STAKES' VECTOR OF SIZE LEN(SELECTIONS) AS VARIABLE
        for index_selection, selection in enumerate(selections):

            # ADD ALL WINS TO END_BANKROLL
            end_bankrolls[index_selection] += stakes[index_selection] * (selection['odds_book'] - 1)

            # DEDUCT ALL LOSSES TO END_BANKROLL
            for index_end_bankroll, end_bankroll in enumerate(end_bankrolls):
                if index_end_bankroll != index_selection:
                    end_bankrolls[index_end_bankroll] -= stakes[index_selection]

            # ADD WINS AND LOSSES FROM EXISTING BETS
            for existing_bet in existing_bets:
                if existing_bet['name'] == selection['name']:
                    end_bankrolls[index_selection] += existing_bet['stake'] * (existing_bet['odds_book'] - 1)
                else:
                    end_bankrolls[index_selection] -= existing_bet['stake']

        # RETURN THE OBJECTIVE AS A SUMPRODUCT OF PROBABILITIES AND END_BANKROLLS - THIS IS THE FUNCTION TO BE MAXIMIZED
        # SEE https://www.pinnacle.com/en/betting-articles/Betting-Strategy/the-real-kelly-criterion/HZKJTFCB3KNYN9CJ
        return -sum([p * e for p, e in zip(probs, ln(end_bankrolls))])

    # INITITAL STAKES ARE 0 AND STAKES MUST BE NON-NEGATIVE
    guess = asarray(len(selections) * [0])
    bounds = list(zip(len(selections) * [0], len(selections) * [None]))

    # FIND THE GLOBAL MAXIMUM USING SCIPY'S CONSTRAINED MINIMIZATION
    # FOR ALTERNATIVE ALGORITHMS SEE https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    res = scipy.optimize.minimize(fun=f, x0=guess, method='L-BFGS-B', bounds=bounds, options={'maxiter': 1000000})

    runtime = time.time() - start_time

    # CONSOLE OUTPUT
    print(f"\nOptimization finished. Runtime --- {round(runtime, 3)} seconds ---\n")
    print(f"Objective: {round(res.fun, 5)}")
    print(f"Certainty Equivalent: {round(math.exp(-res.fun), 3)}\n")
    for num, selection in enumerate(selections):
        stake = res.x[num]
        if stake > 0.00:
            print(f"{selections[num]['name']} @{selections[num]['odds_book']} - € {round(stake, 2)}")


selections = list()
selections.append({'name': 'Michael van Gerwen', 'odds_book': 2.59, 'odds_fair': 5.95})
selections.append({'name': 'Peter Wright', 'odds_book': 5.5, 'odds_fair': 7.363})
selections.append({'name': 'Ian White', 'odds_book': 25, 'odds_fair': 7.9})
selections.append({'name': 'Gerwyn Price', 'odds_book': 7, 'odds_fair': 7.979})
selections.append({'name': 'Glen Durrant', 'odds_book': 20, 'odds_fair': 20.117})
selections.append({'name': 'Krzysztof Ratajski', 'odds_book': 25, 'odds_fair': 21.768})
selections.append({'name': 'Mensur Suljovic', 'odds_book': 40, 'odds_fair': 24.649})
selections.append({'name': 'Nathan Aspinall', 'odds_book': 15, 'odds_fair': 25.006})
selections.append({'name': 'Jonny Clayton', 'odds_book': 64.51, 'odds_fair': 40.371})
selections.append({'name': 'Rob Cross', 'odds_book': 13.6, 'odds_fair': 40.634})
selections.append({'name': 'Michael Smith', 'odds_book': 19.84, 'odds_fair': 43.745})
selections.append({'name': 'Gabriel Clemens', 'odds_book': 50, 'odds_fair': 46.232})
selections.append({'name': 'Jeffrey de Zwaan', 'odds_book': 40, 'odds_fair': 47.985})
selections.append({'name': 'James Wade', 'odds_book': 35, 'odds_fair': 78.125})
selections.append({'name': 'Joe Cullen', 'odds_book': 65.51, 'odds_fair': 81.433})
selections.append({'name': 'Jamie Hughes', 'odds_book': 80, 'odds_fair': 81.566})
selections.append({'name': 'Danny Noppert', 'odds_book': 66.53, 'odds_fair': 83.403})
selections.append({'name': 'Jermaine Wattimena', 'odds_book': 70, 'odds_fair': 94.607})
selections.append({'name': 'Kim Huybrechts', 'odds_book': 127.32, 'odds_fair': 99.108})
selections.append({'name': 'Steve Lennon', 'odds_book': 85.25, 'odds_fair': 101.937})
selections.append({'name': 'Justin Pipe', 'odds_book': 161.56, 'odds_fair': 128.535})
selections.append({'name': 'Mervyn King', 'odds_book': 120.32, 'odds_fair': 139.665})
selections.append({'name': 'Luke Humphries', 'odds_book': 80, 'odds_fair': 154.083})
selections.append({'name': 'Steve West', 'odds_book': 128.33, 'odds_fair': 158.228})
selections.append({'name': 'Steve Beaton', 'odds_book': 131.98, 'odds_fair': 159.236})
selections.append({'name': 'Stephen Bunting', 'odds_book': 80, 'odds_fair': 180.832})
selections.append({'name': 'Kai Fan Leung', 'odds_book': 130.99, 'odds_fair': 185.529})
selections.append({'name': 'Ron Meulenkamp', 'odds_book': 167.5, 'odds_fair': 187.266})
selections.append({'name': 'Ryan Searle', 'odds_book': 100, 'odds_fair': 207.9})
selections.append({'name': 'Dimitri van den Bergh', 'odds_book': 54.67, 'odds_fair': 215.517})
selections.append({'name': 'Damon Heta', 'odds_book': 102.61, 'odds_fair': 256.41})
selections.append({'name': 'Andy Boulton', 'odds_book': 219.31, 'odds_fair': 304.878})
selections.append({'name': 'Dirk van Duijvenbode', 'odds_book': 236.37, 'odds_fair': 324.675})
selections.append({'name': 'Luke Woodhouse', 'odds_book': 143.89, 'odds_fair': 862.069})
selections.append({'name': 'Rowby John Rodriguez', 'odds_book': 242.22, 'odds_fair': 1428.571})
selections.append({'name': 'Martijn Kleermaker', 'odds_book': 196.07, 'odds_fair': 1612.903})
selections.append({'name': 'Andy Hamilton', 'odds_book': 204.35, 'odds_fair': 3225.806})
selections.append({'name': 'Mike de Decker', 'odds_book': 234.9, 'odds_fair': 4166.667})
selections.append({'name': 'Callan Rydz', 'odds_book': 199.15, 'odds_fair': 4166.667})
selections.append({'name': 'Derk Telnekes', 'odds_book': 192, 'odds_fair': 7142.857})
selections.append({'name': 'Darren Penhall', 'odds_book': 296.43, 'odds_fair': 16666.667})

existing_bets = list()
existing_bets.append({'name': 'Michael van Gerwen', 'odds_book': 2.85, 'stake': 22})
existing_bets.append({'name': 'Ian White', 'odds_book': 29, 'stake': 50})

optimize(selections=selections, bankroll=2500.00)


