#!python
# Copyright (c) 2014, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of expidesi.
#
# expidesi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# expidesi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iggy.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
import sys
import argparse
from pyasp.asp import *
from __expidesi__ import query, utils, bioquali

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("networkfiles",
                        help="directory of influence graph in SIF format")
    parser.add_argument("experivarfile",
                        help="experimental variables")

    args = parser.parse_args()

    net_dir = args.networkfiles
    exp_string = args.experivarfile

    flist =  os.listdir(net_dir)
    print('\nReading',len(flist),'network from',net_dir,'...',end='\n')
    NETS = TermSet()
    for f in flist :
      net_string= os.path.join(net_dir,f)
      print ('   reading',net_string,'... ',end='')
      net = bioquali.readSIFGraph(net_string)
      NETS = TermSet(NETS.union(net))
      print('done.')


    print('\nReading experimental variables',exp_string, '...',end='')
    mu = bioquali.readProfile(exp_string)
    print('done.')
    #print(mu)


    print('\nCompute best single experiment ...',end='')
    experiments = query.get_best_single_experiments(NETS,mu)
    print('done.')

    if experiments == [] :
      print("no experiment can distinguish the networks.")
      print("add more readouts or more perturbations.")

    else:
      count=0
      for e in experiments :
        count = count+1
        print("best single experiment",count,":")
        utils.print_experiment_table(e)
    
      print('\nCompute best experiment sets ...',end='')
      max_number_experiments = 10
      experiments = query.get_experiments(NETS,mu,max_number_experiments)
      print('done.')

      count=0
      for e in experiments :
        count = count+1
        print("best experiment set",count,":")
        utils.print_experiment_table(e)

    utils.clean_up()



