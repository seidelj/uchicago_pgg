q_first = {
    'q1': ["Today's experiment is divided in 4 periods. Each period is composed by 8 rounds", 'True'],
    'q2': ["Only 1 of the 4 periods is randomly selected for payments.", "True"],
    'q3': ["Your final earnings are the sum of your earnings in each of the 8 rounds that constitute the randomly selected period", "True"],
    'q4': ['In each period you will make your decisions with a different group of participants.', "True"],
    'q5': ["In each round, you choose how to invest 10 tokens between an Individual Account and a Group Account.", "True"],
    'q6': ["If in a given round the true return rate of the Group Account is for example, 0.55, you and each group member will earn 0.55 tokens for each token invested in the Group Account, no matter who invested it.", "True"],
}

private_2 = {

    'q1': ["Your signal this round is equal to 0.45", "True"],
    'q2': ["Each other group member receieves a private signal", "True"],
    'q3': ["There is only one true value of the return rate in each round, and your earnings from the Group Account depend only on that value (not on your signal)", "True"],
    'q4': ["According to your signal, which values can be the true return rate in this example?", "3"],
    'table': [
        [21, .35, .45, .55],
        [24, 0, 0, 0],
        [23, 0, 0, 0],
        [22, 0, 0, 0],
    ]

}

private_3 = {

    'q1': ["Your signal this round is equal to 0.95", "True"],
    'q2': ["According to your signal, which values can be the true return rate in this example?", "2"],
    'table': [
        [21, .85, .95, 1.05],
        [24, 0, 0, 0],
        [23, 0, 0, 0],
        [22, 0, 0, 0],
    ]
}

exact_2 = {
    'q1': ["The value of the return rate of the Group Account in this round is 0.75.", "True"],
    'table': [
        [45, 0, .75, 0],
        [47, 0, .75, 0],
        [48, 0, .75, 0],
        [46, 0, .75, 0],
    ],
}

exact_3 = {
    'q1': ["The value of the return rate of the Group Account in this round in 0.45.", "True"],
    'table': [
        [45, 0, .45, 0],
        [47, 0, .45, 0],
        [48, 0, .45, 0],
        [46, 0, .45, 0],
    ],
}

public_2 = {
    'q1': ["Your signal in this round is equal to 1.15", "True"],
    'q2': ["The signal of the participant with ID 7 is 0.95 in this round.", "True"],
    'q3': ["There is only one true value of the return rate in each round, and your earnings from the Group Account depend only on that value (not on your signal).", "True"],
    'q4': ["According to your signal and the signal of all other group members, what value(s) can the true return rate be in this example?", "3"],
    "table": [
        [5, 1.05, 1.15, 1.25],
        [7, .85, .95, 1.05],
        [6, 1.05, 1.15, 1.25],
        [8, 1.05, 1.15, 1.25],
    ]  
}

public_3 = {
    'q1': ["Your signal in this round is equal to 1.05", "True"],
    'q2': ["The signal of participant with ID 8 is 1.15 in this round.", "True"],
    'q3': ["According to your signal and the signals of all other groups members, what value(s) can the true return rate be in this example?", "2"],
    "table": [
        [5, .95, 1.05, 1.15],
        [7, 1.05, 1.15, 1.25],
        [6, .95, 1.05, 1.15],
        [8, 1.05, 1.15, 1.25],
    ]
}

private_wide_2 = {
    'q1': ["Your signal this round is equal to 0.45", "True"],
    'q2': ["Each other group member receieves a private signal", "True"],
    'q3': ["There is only one true value of the return rate in each round, and your earnings from the Group Account depend only on that value (not on your signal)", "True"],
    'q4': ["According to your signal, which values can be the true return rate in this example?", "3"],
    'table': [
        [21, .25, .45, .65],
        [24, 0, 0, 0],
        [23, 0, 0, 0],
        [22, 0, 0, 0],
    ]
}

private_wide_3 = {
    'q1': ["Your signal this round is equal to 0.95", "True"],
    'q2': ["According to your signal, which values can be the true return rate in this example?", "2"],
    'table': [
        [21, .75, .95, 1.15],
        [24, 0, 0, 0],
        [23, 0, 0, 0],
        [22, 0, 0, 0],
    ]
}

public_wide_2 = {
    'q1': ["Your signal in this round is equal to 1.05", "True"],
    'q2': ["The signal of the participant with ID 7 is 0.95 in this round.", "True"],
    'q3': ["There is only one true value of the return rate in each round, and your earnings from the Group Account depend only on that value (not on your signal).", "True"],
    'q4': ["According to your signal and the signal of all other group members, what value(s) can the true return rate be in this example?", "3"],
    "table": [
        [5, .85, 1.05, 1.25],
        [7, .75, .95, 1.15],
        [6, .65, .85, 1.05],
        [8, .85, 1.05, 1.25],
    ]
}

public_wide_3 = {
    'q1': ["Your signal in this round is equal to .45", "True"],
    'q2': ["The signal of participant with ID 8 is .45 in this round.", "True"],
    'q3': ["According to your signal and the signals of all other groups members, what value(s) can the true return rate be in this example?", "2"],
    "table": [
        [5, .25, .45, .65],
        [7, .15, .35, .55],
        [6, .35, .55, .75],
        [8, .25, .45, .65],
    ]
}


dict_of_dicts = {
    'q_first' : q_first,
    'private_2': private_2,
    'private_3': private_3,
    'exact_2': exact_2,
    'exact_3': exact_3,
    'public_2': public_2,
    'public_3': public_3,
    'private_wide_2': private_wide_2,
    'private_wide_3': private_wide_3,
    'public_wide_2': public_wide_2,
    'public_wide_3': public_wide_3,
}


