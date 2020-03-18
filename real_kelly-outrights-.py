import math
import time
import numpy as np
import scipy.optimize


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

    # INITITAL STAKES ARE 0 AND STAKES MUST BE NON-NEGATIVE
    guess = np.asarray(len(selections) * [0])
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


# ADD YOUR SELECTIONS HERE - MAKE SURE ALL PROBABILITIES (= 1 / 'odds_fair) ADD UP TO 1
selections = list()
selections.append({'name': 'Matsuyama, Hideki', 'odds_book': 4.33, 'odds_fair': 3.86})
selections.append({'name': 'Rahm, Jon', 'odds_book': 12, 'odds_fair': 14})
selections.append({'name': 'English, Harris', 'odds_book': 19, 'odds_fair': 22.9})
selections.append({'name': 'Morikawa, Collin', 'odds_book': 26, 'odds_fair': 23.6})
selections.append({'name': 'Cantlay, Patrick', 'odds_book': 13, 'odds_fair': 23.9})
selections.append({'name': 'Bezuidenhout, Christiaan', 'odds_book': 26, 'odds_fair': 26.8})
selections.append({'name': 'Simpson, Webb', 'odds_book': 26, 'odds_fair': 26.8})
selections.append({'name': 'McIlroy, Rory', 'odds_book': 17, 'odds_fair': 41.6})
selections.append({'name': 'Leishman, Marc', 'odds_book': 23, 'odds_fair': 44.4})
selections.append({'name': 'Schauffele, Xander', 'odds_book': 41, 'odds_fair': 47.8})
selections.append({'name': 'Im, Sungjae', 'odds_book': 41, 'odds_fair': 48.5})
selections.append({'name': 'Hovland, Viktor', 'odds_book': 34, 'odds_fair': 49.1})
selections.append({'name': 'Scott, Adam', 'odds_book': 41, 'odds_fair': 55.6})
selections.append({'name': 'Scheffler, Scottie', 'odds_book': 67, 'odds_fair': 58.1})
selections.append({'name': 'Kim, Si Woo', 'odds_book': 23, 'odds_fair': 72.2})
selections.append({'name': 'Berger, Daniel', 'odds_book': 41, 'odds_fair': 73.1})
selections.append({'name': 'Thomas, Justin', 'odds_book': 51, 'odds_fair': 79.1})
selections.append({'name': 'Sabbatini, Rory', 'odds_book': 101, 'odds_fair': 81.1})
selections.append({'name': 'DeChambeau, Bryson', 'odds_book': 41, 'odds_fair': 82.2})
selections.append({'name': 'Cabrera Bello, Rafa', 'odds_book': 51, 'odds_fair': 86.4})
selections.append({'name': 'Hatton, Tyrrell', 'odds_book': 51, 'odds_fair': 89.1})
selections.append({'name': 'Kuchar, Matt', 'odds_book': 67, 'odds_fair': 94.1})
selections.append({'name': 'Conners, Corey', 'odds_book': 81, 'odds_fair': 106})
selections.append({'name': 'Todd, Brendon', 'odds_book': 81, 'odds_fair': 116})
selections.append({'name': 'An, Byeong Hun', 'odds_book': 81, 'odds_fair': 118})
selections.append({'name': 'Koepka, Brooks', 'odds_book': 41, 'odds_fair': 129})
selections.append({'name': 'Johnson, Dustin', 'odds_book': 41, 'odds_fair': 138})
selections.append({'name': 'Horschel, Billy', 'odds_book': 126, 'odds_fair': 147})
selections.append({'name': 'Long, Adam', 'odds_book': 151, 'odds_fair': 158})
selections.append({'name': 'Hadwin, Adam', 'odds_book': 126, 'odds_fair': 160})
selections.append({'name': 'Poulter, Ian', 'odds_book': 126, 'odds_fair': 165})
selections.append({'name': 'Kokrak, Jason', 'odds_book': 126, 'odds_fair': 184})
selections.append({'name': 'Dahmen, Joel', 'odds_book': 151, 'odds_fair': 189})
selections.append({'name': 'Willett, Danny', 'odds_book': 101, 'odds_fair': 198})
selections.append({'name': 'Moore, Ryan', 'odds_book': 201, 'odds_fair': 201})
selections.append({'name': 'Mitchell, Keith', 'odds_book': 81, 'odds_fair': 207})
selections.append({'name': 'Munoz, Sebastian', 'odds_book': 201, 'odds_fair': 208})
selections.append({'name': 'Dufner, Jason', 'odds_book': 101, 'odds_fair': 214})
selections.append({'name': 'Perez, Victor', 'odds_book': 81, 'odds_fair': 222})
selections.append({'name': 'McDowell, Graeme', 'odds_book': 101, 'odds_fair': 223})
selections.append({'name': 'Laird, Martin', 'odds_book': 201, 'odds_fair': 230})
selections.append({'name': 'Garcia, Sergio', 'odds_book': 101, 'odds_fair': 239})
selections.append({'name': 'Fitzpatrick, Matthew', 'odds_book': 126, 'odds_fair': 243})
selections.append({'name': 'Furyk, Jim', 'odds_book': 301, 'odds_fair': 274})
selections.append({'name': 'Taylor, Vaughn', 'odds_book': 251, 'odds_fair': 276})
selections.append({'name': 'Champ, Cameron', 'odds_book': 101, 'odds_fair': 289})
selections.append({'name': 'Kisner, Kevin', 'odds_book': 251, 'odds_fair': 292})
selections.append({'name': 'Wolff, Matthew', 'odds_book': 101, 'odds_fair': 294})
selections.append({'name': 'Jones, Matt', 'odds_book': 201, 'odds_fair': 313})
selections.append({'name': 'Hoge, Tom', 'odds_book': 251, 'odds_fair': 337})
selections.append({'name': 'Reavie, Chez', 'odds_book': 251, 'odds_fair': 351})
selections.append({'name': 'Aphibarnrat, Kiradech', 'odds_book': 151, 'odds_fair': 351})
selections.append({'name': 'Homa, Max', 'odds_book': 201, 'odds_fair': 352})
selections.append({'name': 'Lashley, Nate', 'odds_book': 151, 'odds_fair': 364})
selections.append({'name': 'Thompson, Michael', 'odds_book': 151, 'odds_fair': 371})
selections.append({'name': 'Vegas, Jhonattan', 'odds_book': 201, 'odds_fair': 372})
selections.append({'name': 'Stanley, Kyle', 'odds_book': 301, 'odds_fair': 392})
selections.append({'name': 'Cauley, Bud', 'odds_book': 251, 'odds_fair': 410})
selections.append({'name': 'Perez, Pat', 'odds_book': 201, 'odds_fair': 414})
selections.append({'name': 'Glover, Lucas', 'odds_book': 201, 'odds_fair': 432})
selections.append({'name': 'Straka, Sepp', 'odds_book': 201, 'odds_fair': 432})
selections.append({'name': 'Hoffman, Charley', 'odds_book': 151, 'odds_fair': 456})
selections.append({'name': 'Poston, J.T.', 'odds_book': 301, 'odds_fair': 530})
selections.append({'name': 'Johnson, Zach', 'odds_book': 301, 'odds_fair': 536})
selections.append({'name': 'List, Luke', 'odds_book': 251, 'odds_fair': 569})
selections.append({'name': 'Harman, Brian', 'odds_book': 301, 'odds_fair': 576})
selections.append({'name': 'Reed, Patrick', 'odds_book': 201, 'odds_fair': 585})
selections.append({'name': 'Stuard, Brian', 'odds_book': 301, 'odds_fair': 602})
selections.append({'name': 'Schenk, Adam', 'odds_book': 401, 'odds_fair': 635})
selections.append({'name': 'Lowry, Shane', 'odds_book': 251, 'odds_fair': 647})
selections.append({'name': 'Walker, Jimmy', 'odds_book': 151, 'odds_fair': 654})
selections.append({'name': 'Landry, Andrew', 'odds_book': 401, 'odds_fair': 670})
selections.append({'name': 'Howell III, Charles', 'odds_book': 201, 'odds_fair': 684})
selections.append({'name': 'Van Rooyen, Erik', 'odds_book': 301, 'odds_fair': 721})
selections.append({'name': 'Lee, Kyoung-Hoon', 'odds_book': 301, 'odds_fair': 729})
selections.append({'name': 'Grace, Branden', 'odds_book': 151, 'odds_fair': 733})
selections.append({'name': 'Burgoon, Bronson', 'odds_book': 501, 'odds_fair': 795})
selections.append({'name': 'Varner III, Harold', 'odds_book': 301, 'odds_fair': 816})
selections.append({'name': 'Watson, Bubba', 'odds_book': 201, 'odds_fair': 899})
selections.append({'name': 'Duncan, Tyler', 'odds_book': 501, 'odds_fair': 920})
selections.append({'name': 'McCarthy, Denny', 'odds_book': 801, 'odds_fair': 940})
selections.append({'name': 'Putnam, Andrew', 'odds_book': 401, 'odds_fair': 966})
selections.append({'name': 'Griffin, Lanto', 'odds_book': 801, 'odds_fair': 1057})
selections.append({'name': 'Ancer, Abraham', 'odds_book': 501, 'odds_fair': 1132})
selections.append({'name': 'Casey, Paul', 'odds_book': 401, 'odds_fair': 1163})
selections.append({'name': 'Woodland, Gary', 'odds_book': 301, 'odds_fair': 1250})
selections.append({'name': 'Stenson, Henrik', 'odds_book': 401, 'odds_fair': 1364})
selections.append({'name': 'Wise, Aaron', 'odds_book': 401, 'odds_fair': 1412})
selections.append({'name': 'Piercy, Scott', 'odds_book': 601, 'odds_fair': 1412})
selections.append({'name': 'Herman, Jim', 'odds_book': 251, 'odds_fair': 1429})
selections.append({'name': 'Frittelli, Dylan', 'odds_book': 401, 'odds_fair': 1446})
selections.append({'name': 'Na, Kevin', 'odds_book': 301, 'odds_fair': 1463})
selections.append({'name': 'Smith, Cameron', 'odds_book': 301, 'odds_fair': 1500})
selections.append({'name': 'Baddeley, Aaron', 'odds_book': 501, 'odds_fair': 1558})
selections.append({'name': 'Palmer, Ryan', 'odds_book': 401, 'odds_fair': 1579})
selections.append({'name': 'Taylor, Nick', 'odds_book': 751, 'odds_fair': 1655})
selections.append({'name': 'Niemann, Joaquin', 'odds_book': 501, 'odds_fair': 2143})
selections.append({'name': 'Snedeker, Brandt', 'odds_book': 501, 'odds_fair': 2182})
selections.append({'name': 'Streelman, Kevin', 'odds_book': 1001, 'odds_fair': 2308})
selections.append({'name': 'Merritt, Troy', 'odds_book': 601, 'odds_fair': 2500})
selections.append({'name': 'Garnett, Brice', 'odds_book': 1001, 'odds_fair': 2581})
selections.append({'name': 'Spaun, J.J.', 'odds_book': 301, 'odds_fair': 2667})
selections.append({'name': 'Kang, Sung', 'odds_book': 501, 'odds_fair': 2667})
selections.append({'name': 'Lee, Danny', 'odds_book': 601, 'odds_fair': 2759})
selections.append({'name': 'Rodgers, Patrick', 'odds_book': 501, 'odds_fair': 3077})
selections.append({'name': 'Gooch, Talor', 'odds_book': 751, 'odds_fair': 3429})
selections.append({'name': 'Knox, Russell', 'odds_book': 601, 'odds_fair': 3478})
selections.append({'name': 'Henley, Russell', 'odds_book': 401, 'odds_fair': 3529})
selections.append({'name': 'Finau, Tony', 'odds_book': 301, 'odds_fair': 3529})
selections.append({'name': 'Burns, Sam', 'odds_book': 751, 'odds_fair': 3636})
selections.append({'name': 'Brown, Scott', 'odds_book': 751, 'odds_fair': 4000})
selections.append({'name': 'Ryder, Sam', 'odds_book': 1501, 'odds_fair': 4211})
selections.append({'name': 'Hughes, Mackenzie', 'odds_book': 401, 'odds_fair': 4364})
selections.append({'name': 'Wiesberger, Bernd', 'odds_book': 401, 'odds_fair': 4364})
selections.append({'name': 'Rose, Justin', 'odds_book': 401, 'odds_fair': 4444})
selections.append({'name': 'Fowler, Rickie', 'odds_book': 601, 'odds_fair': 5000})
selections.append({'name': 'Malnati, Peter', 'odds_book': 401, 'odds_fair': 5000})
selections.append({'name': 'Fleetwood, Tommy', 'odds_book': 1501, 'odds_fair': 6154})
selections.append({'name': 'Day, Jason', 'odds_book': 601, 'odds_fair': 6667})
selections.append({'name': 'Ortiz, Carlos', 'odds_book': 2501, 'odds_fair': 8000})
selections.append({'name': 'Hubbard, Mark', 'odds_book': 801, 'odds_fair': 8276})
selections.append({'name': 'Grillo, Emiliano', 'odds_book': 751, 'odds_fair': 8571})
selections.append({'name': 'Clark, Wyndham', 'odds_book': 601, 'odds_fair': 11538})
selections.append({'name': 'Armour, Ryan', 'odds_book': 2501, 'odds_fair': 20000})
selections.append({'name': 'Spieth, Jordan', 'odds_book': 601, 'odds_fair': 20000})
selections.append({'name': 'Mickelson, Phil', 'odds_book': 751, 'odds_fair': 20000})
selections.append({'name': 'Holmes, J.B.', 'odds_book': 801, 'odds_fair': 20000})
selections.append({'name': 'Janewattananond, Jazz', 'odds_book': 4001, 'odds_fair': 40000})
selections.append({'name': 'Hadley, Chesson', 'odds_book': 601, 'odds_fair': 40000})

# ADD YOUR EXISTING BETS HERE
existing_bets = list()
existing_bets.append({'name': 'English, Harris', 'odds_book': 21, 'stake': 25})
existing_bets.append({'name': 'Morikawa, Collin', 'odds_book': 27, 'stake': 10})

# CALL THE FUNCTION WITH GIVEN BANKROLL
optimize(selections=selections, existing_bets=existing_bets, bankroll=2500.00)


