Analysis of NBA Game Using Python

Purposals:

As a NBA fan, I like to watch NBA games and predict the result of every game. Therefore, this project will use the previous statistics of NBA games to judge the combat effectiveness of each team and predict the results of a game. Based on the NBA regular season and playoff statistics from 2017 to 2018, I will forecast the results of each game currently under way in 2018-2019.

Rules:

1） In this eproject, I will use the statistical data from Basketball Reference.com. In all the tables summarized from 2017-2018, I will mainly use the following three data tables:

·   Team Per Game Stats

·   Opponent Per Game Stats

·   Miscellaneous Stats

2）I will use each team's results of past game and Elo score to judge the winning probability of each team. Assuming that the current grades of A and B are RA and RB, the expected winning rate of A to B is:

EA=1/(1+10^(RA-RB)/400)

3） If team A's real score SA(winning 1 point, drawing 0.5 points, losing 0 points) is different from his expectation of winning rate, then his grade score should be adjusted according to the following formula:

RA(new)=RA(old)+K(SA-RA(old))

4） The K value will also be adjusted according to the different grades of SA.

·   ≥2400\ge2400≥2400，K=16

·   2100~2400 分，K=24

·   ≤2100\le2100≤2100，K=32
