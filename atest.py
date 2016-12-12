# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
import random, time
from decimal import *
# </standard imports>



class Constants:
	name_in_url = 'public_goods'
	players_per_group = 4
	num_rounds = 32
	rounds_per_game = 8
	starting_rounds = [
		1, rounds_per_game+1,
		rounds_per_game*2+1, rounds_per_game*3+1]

	#"""Amount allocated to each player"""
	template_endowment = 10
	efficiency_factor = 2
	efficiency_floats = [
        .05, .15, .25, .35,
        .45, .55, .65, .75,
        .85, .95, 1.05,
        1.15, 1.25,
	]

	getcontext().prec = 28

	efficiency_factors =[Decimal(x).quantize(Decimal('.01')) for x in efficiency_floats]

	fMPCRS = [.25, .55, .95]

	MPCRS = [Decimal(x).quantize(Decimal('.01')) for x in fMPCRS]

	# order of MPCR values 3 = Varied round
	orders = [
        [2, 1, 3, 0],
        [0, 3, 1, 2],
        [2, 3, 0, 1],
        [3, 1, 0, 2],
        [1, 0, 2, 3],
        [3, 2, 1, 0],
	]


	mpcrOrders = []
	for o in orders:
		od = {}
		for x in range(4):
			mpcr = MPCRS[o[x]] if o[x] != 3 else "varied"
			od[starting_rounds[x]] = mpcr
		mpcrOrders.append(od)

print Constants.mpcrOrders
