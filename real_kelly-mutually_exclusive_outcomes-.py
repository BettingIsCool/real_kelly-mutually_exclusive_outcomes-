import math
import time
import numpy as np
import scipy.optimize
from scipy.optimize import NonlinearConstraint


def optimize(selections: list, existing_bets: list, bankroll: float):

    start_time = time.time()

    # CREATE A VECTOR OF OUTCOME PROBABILITIES OF SIZE LEN(SELECTIONS)
    probs = [1 / item['odds_fair'] for item in selections]
    print(f'Sum of probabilities add up to {sum(probs)}')

    # ADD WINS AND LOSSES FROM EXISTING BETS
    existing_bets_profits = len(selections) * [0]
    for index_selection, selection in enumerate(selections):
        for existing_bet in existing_bets:
            existing_bets_profits[index_selection] -= existing_bet['stake']
            if existing_bet['name'] == selection['name']:
                existing_bets_profits[index_selection] += existing_bet['stake'] * existing_bet['odds_book']

    def f(stakes):
        """ This function will be called by scipy.optimize.minimize repeatedly to find the global maximum """

        # INITIALIZE END_BANKROLLS AND OBJECTIVE BEFORE EACH OPTIMIZATION STEP
        end_bankrolls, objective = len(selections) * [bankroll - np.sum(stakes)] + np.asarray(existing_bets_profits), 0.00

        # CALCULATE END_BANKROLL FOR EACH SELECTION WITH A 'STAKES' VECTOR OF SIZE LEN(SELECTIONS) AS VARIABLE
        for index_selection, selection in enumerate(selections):

            # ADD WINS & LOSSES
            end_bankrolls[index_selection] += stakes[index_selection] * selection['odds_book']

        # RETURN THE OBJECTIVE AS A SUMPRODUCT OF PROBABILITIES AND END_BANKROLLS - THIS IS THE FUNCTION TO BE MAXIMIZED
        # SEE https://www.pinnacle.com/en/betting-articles/Betting-Strategy/the-real-kelly-criterion/HZKJTFCB3KNYN9CJ
        return -sum([p * e for p, e in zip(probs, np.log(end_bankrolls))])

    def constraint(stakes):
        """ Sum of all stakes must not exceed bankroll """
        return sum(stakes) - min(existing_bets_profits)

    # FIND THE GLOBAL MAXIMUM USING SCIPY'S CONSTRAINED MINIMIZATION
    bounds = list(zip(len(selections) * [0], len(selections) * [bankroll]))
    nlc = NonlinearConstraint(constraint, -np.inf, bankroll)
    res = scipy.optimize.differential_evolution(func=f, bounds=bounds, constraints=(nlc))

    runtime = time.time() - start_time

    # CONSOLE OUTPUT
    print(f"\nOptimization finished. Runtime --- {round(runtime, 3)} seconds ---\n")
    print(f"Objective: {round(res.fun, 5)}")
    print(f"Certainty Equivalent: {round(math.exp(-res.fun), 3)}\n")
    for num, selection in enumerate(selections):
        stake = res.x[num]
        if stake > 1.00:
            print(f"{selections[num]['name']} @{selections[num]['odds_book']} - € {round(stake, 2)}")


selections = list()
selections.append({'name': 'Bayern Munich', 'odds_book': 1.2, 'odds_fair': 1.142})
selections.append({'name': 'Borussia Dortmund', 'odds_book': 7, 'odds_fair': 12.626})
selections.append({'name': 'RB Leipzig', 'odds_book': 10, 'odds_fair': 22.83})
selections.append({'name': 'Borussia Monchengladbach', 'odds_book': 201, 'odds_fair': 1176.471})
selections.append({'name': 'Bayer Leverkusen', 'odds_book': 250, 'odds_fair': 1960.784})
selections.append({'name': 'Schalke 04', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': '1899 Hoffenheim', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'VfL Wolsburg', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'SC Freiburg', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'FC Koln', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'Eintracht Frankfurt', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'Union Berlin', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'Hertha BSC', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'FC Augsburg', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'Mainz 05', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'Fortuna Dusseldorf', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'Werder Bremen', 'odds_book': 1, 'odds_fair': 1000000})
selections.append({'name': 'SC Paderborn', 'odds_book': 1, 'odds_fair': 1000000})

# ADD YOUR EXISTING BETS HERE
existing_bets = list()
existing_bets.append({'name': 'Bayern Munich', 'odds_book': 1.434, 'stake': 120})
existing_bets.append({'name': 'RB Leipzig', 'odds_book': 5, 'stake': 35})

# CALL THE FUNCTION WITH GIVEN BANKROLL
optimize(selections=selections, existing_bets=existing_bets, bankroll=2500.00)




