
coh_decreasing = [['Day','Cash On Hand'],
                    [40,2571502],
                    [41,2569504],
                    [42,2568706],
                    [43,2565808],
                    [44,2563010],
                    [45,2562012],
                    [46,2560114],
                    [47,2558216],
                    [48,2556458],
                    [49,2554420]]

pnl_decreasing = [['Day','Sales','Trading Profit','Operating Expense','Net Profit'],
                    [40,14481055,6170905,3667884,2503021],
                    [41,14581932,6246685,3727854,2502020],
                    [42,14714710,6335491,3790422,2501012],
                    [43,14833531,6418158,3865832,2493018],
                    [44,14930686,6488829,3963814,2442010],
                    [45,15057632,6548661,4029052,2432016],
                    [46,15157737,6616222,4092941,2403009],
                    [47,16759515,6935340,4155458,2333001],
                    [48,16797892,6944441,4258004,2003013],
                    [49,16938318,6972213,4323322,2002055]]


coh_increasing = [['Day','Cash On Hand'],
                    [40,2571502],
                    [41,2573489],
                    [42,2575476],
                    [43,2577463],
                    [44,2579450],
                    [45,2581437],
                    [46,2583424],
                    [47,2585411],
                    [48,2587398],
                    [49,2589385]]

pnl_increasing =  [['Day','Sales','Trading Profit','Operating Expense','Net Profit'],
                    [40,14481055,6170905,3667884,2503021],
                    [41,14581932,6246685,3727854,2543025],
                    [42,14714710,6335491,3790422,2573023],
                    [43,14833531,6418158,3865832,2583024],
                    [44,14930686,6488829,3963814,2593010],
                    [45,15057632,6548661,4029052,2603026],
                    [46,15157737,6616222,4092941,2623000],
                    [47,16759515,6935340,4155458,2643028],
                    [48,16797892,6944441,4258004,2663129],
                    [49,16938318,6972213,4323322,2673050]]




coh_volatile = [['Day','Cash On Hand'],
                [40,2571502],
                [41,1115609],
                [42,1055099],
                [43,1003310],
                [44,364763],
                [45,244591],
                [46,300807],
                [47,316348],
                [48,564179],
                [49,179747]]

pnl_volatile =  [['Day','Sales','Trading Profit','Operating Expense','Net Profit'],
                [40,14481055,6170905,3667884,2503021],
                [41,14581932,6246685,3727854,2518831],
                [42,14714710,6335491,3790422,2545069],
                [43,14833531,6418158,3865832,2552326],
                [44,14930686,6488829,3963814,2525015],
                [45,15057632,6548661,4029052,2519609],
                [46,15157737,6616222,4092941,2523281],
                [47,16759515,6935340,4155458,2779882],
                [48,16797892,6944441,4258004,2686437],
                [49,16938318,6972213,4323322,2648891]]


overheads = [["Category","Overheads"],
            ["Salary Expense",25.66],
            ["Interest Expense ",2.14],
            ["Rental Expense",25.97],
            ["Overflow Expense - Retail",0.32],
            ["Overflow Expense - Warehouse",0.12],
            ["Penalty Expense",2.46],
            ["Depreciation Expense",17.3],
            ["Maintenance Expense",5.23],
            ["Shipping Expense",11.25],
            ["Human Resource Expense",15.55]]


all_data = [[coh_decreasing, pnl_decreasing, overheads],
        [coh_increasing, pnl_increasing, overheads],
        [coh_volatile, pnl_volatile, overheads]]


#for i in range(len(all_data)):
#    print(all_data[i][0]) # coh
#    print(all_data[i][1]) # pnl
#    print(all_data[i][2]) # overhead
    

all_data_dict = {'decreasing trend': [coh_decreasing, pnl_decreasing, overheads],
                 'increasing trend': [coh_increasing, pnl_increasing, overheads],
                 'volatile trend' : [coh_volatile, pnl_volatile, overheads]
                 }

#print(all_data_dict['decreasing_data'])

#for key in all_data_dict:
#    print(all_data_dict[key][0]) #coh
#    print(all_data_dict[key][1]) #pnl
#    print(all_data_dict[key][2]) #overheads
#    break