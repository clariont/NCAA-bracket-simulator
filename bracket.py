#!/bin/python

import pandas as pd
import sys
import numpy as np
#import matplotlib as plt


# Functions
def getWinner(a, b, rdnum):
    colname='rd'+str(rdnum)+'_fix'
    af = float(a[colname].item())
    bf = float(b[colname].item())
    aff = af/(af+bf)
    bff = bf/(af+bf)
#    print a['team_name'].item(), aff, b['team_name'].item(), bff
    if (aff < bff):
	if (np.random.random() < aff):
	    return a['team_name'].item()
	else:
	    return b['team_name'].item()
    else:
	if (np.random.random() < bff):
	    return b['team_name'].item()
	else:
	    return a['team_name'].item()

# Main

def main():
    df = pd.read_csv("fivethirtyeight_ncaa_forecasts.csv")
    df['rd2_fix'] = df['rd2_win']/df['rd1_win']
    for i in xrange(3,8):
	nl='rd'+str(i)+'_fix'
	nr='rd'+str(i)+'_win'
	nrr='rd'+str(i-1)+'_fix'
	df[nl] = df[nr]/df[nrr]
#    print df.head()

    # Make a game data type that stores the winners, and has a pointer to the next game.
    # East - West -- Midwest - South
    # 1-16 . 8-9 .. 5-12 . 4-13 .... 6-11 . 3-14 .. 7-10 . 2-15
    # 0    . 1   ..  2   .  3   ....  4   .  5   ..  6   .  7
    firsts = [(1, 16), (8, 9), (5, 12), (4, 13), (6, 11), (3, 14), (7, 10), (2, 15) ]
    gg = [ [] for x in xrange(63) ]
    conf = ['East', 'West', 'Midwest', 'South']
    ctr = 0
    print "\nRound of 32:"
    for i in conf:
	print i
	for j in firsts:
	    a = df.loc[(df['team_seed'] == j[0]) & (df['team_region'] == i)]
	    b = df.loc[(df['team_seed'] == j[1]) & (df['team_region'] == i)]
	    gg[ctr].append(getWinner(a,b,2))
	    print "\t", gg[ctr][-1]
	    ctr = ctr + 1

    print "\nSweet 16: "
    for i in xrange(32, 48):
	ic = 2*(i - 32)
	a = df.loc[(df['team_name'] == gg[ic][-1])]
	b = df.loc[(df['team_name'] == gg[ic+1][-1])]
	gg[i].append(getWinner(a,b,3))
	print "\t", gg[i][-1]

    print "\nElite Eight: "
    for i in xrange(48, 56):
	ic = (i-16)+(i-48)
	a = df.loc[(df['team_name'] == gg[ic][-1])]
	b = df.loc[(df['team_name'] == gg[ic+1][-1])]
	gg[i].append(getWinner(a,b,4))
	print "\t", gg[i][-1]

    # Elite 8
    print "\nFinal Four: "
    for i in xrange(56, 60):
	ic = (i-8)+(i-56)
	a = df.loc[(df['team_name'] == gg[ic][-1])]
	b = df.loc[(df['team_name'] == gg[ic+1][-1])]
	gg[i].append(getWinner(a,b,5))
	print "\t", gg[i][-1]

    # Final 4
    print "\nChamps: "
    for i in xrange(60, 62):
	ic = (i-4)+(i-60)
	print "\t",gg[ic][-1], "vs ", gg[ic+1][-1]
	a = df.loc[(df['team_name'] == gg[ic][-1])]
	b = df.loc[(df['team_name'] == gg[ic+1][-1])]
	gg[i].append(getWinner(a,b,6))
	print "\t", gg[i][-1]
    
    # Champs
    print "\nNational Champion: "
    ic = 60
    print "\t",gg[ic][-1], "vs ", gg[ic+1][-1]
    a = df.loc[(df['team_name'] == gg[ic][-1])]
    b = df.loc[(df['team_name'] == gg[ic+1][-1])]
    gg[ic+2].append(getWinner(a,b,7))
    print "\t", gg[ic+2][-1]



if __name__ == "__main__":
    main()


