'''
There are 4, 5 and 6 band resistors.

4 band resistor = 1st digit, 2nd digit, multiplier & tolerance
5 band resitor = 1st digit, 2nd digit, 3rd digit, multiplier & tolerance
6 band resitor = 1st digit, 2nd digit, 3rd digit, multiplier, tolerance & Temperature coefficient

check if the user inputs either 4, 5 or 6 band resistor, then calculate the resistance, tolerance & Temp Co if applicable.

Single black band resistor = 0 ohm resistor

example resistors:

4 band = green,blue,red & gold == 5600 omhs
5 band = brown','yellow','violet','black','green' == 147 omhs +-0.5%
6 band = 'orange','red','brown','brown','green','red' == 3210 omhs +/-0.5% 50 ppm/k
'''

digits_dict={
"black":        0,
"brown":        1,
"red":          2,
"orange":       3,
"yellow":       4,
"green":        5,
"blue":         6,
"violet":       7,
"gray":         8,
"white":        9
}
magnitude_dict={
"black":        0,
"brown":        1,
"red":          2,
"orange":       3,
"yellow":       4,
"green":        5,
"blue":         6,
"violet":       7,
"gray":         8,
"white":        9,
"gold":         -1,
"silver":       -2
}
tolerance_dict={
"brown":   "+/-1%",
"red":     "+/-2%",
"green":   "+/-0.5%",
"blue":    "+/-0.25%",
"violet":  "+/-0.1%",
"gray":    "+/-0.05%",
"gold":    "+/-5%",
"silver":  "+/-10%"
}
tcr_dict={
"brown":    "100ppm/k",
"red":      "50ppm/k",
"orange":   "15ppm/k",
"yellow":   "25ppm/k",
"blue":     "10ppm/k",
"violet":   "5ppm/k"
}
def returnMagnitude(stri, band):
    if band <= 4:
        stri = str(stri)[2:]
        x = len(stri)
    elif band >= 5:
        stri = str(stri)[3:]
        x = len(stri)
    return x

def CountStr(stri,check):
    check = str(check)
    stri = str(stri)
    print(stri +' Running')
    add = 0
    
    for i in stri:
        for v in check:
            if i == v:
                add += 1
    new = len(stri) - add
    if new == 1:
        add -= 1
        return add
    
    if len(stri) == 3 and add == 2:
        print("test")
        add = 0
    if len(stri) == 4 and add == 1:
        add =+ 2
    return add

def resistorColourGen(resistance, bands=4, tol='+/-5%', tcr='50ppm/k'):
    if int(str(resistance)[2]) != 0:
        if bands < 5:
            bands = 5
    print(f"You have chosen to generate a {resistance:,}ohm. {bands} band resistor")
    digits_dict_r = dict(((value, key) for key, value in digits_dict.items()))
    magnitude_dictt = dict(((value, key) for key, value in magnitude_dict.items()))
    tolerance_dictt = dict(((value, key) for key, value in tolerance_dict.items()))
    tcr_dictt = dict(((value, key) for key, value in tcr_dict.items()))
    colours = ['','','','','','']
    res = str(resistance)
    check = returnMagnitude(resistance, bands)
    lengthRes = len(res)
         
    colours[0] = digits_dict_r[int(res[0])]
    colours[1] = digits_dict_r[int(res[1])]
    if lengthRes <= 2:
        colours[3] = magnitude_dictt[1]
        for x in range(3):
            colours.remove('')            
    colours[2] = digits_dict_r[int(res[2])]            
    if bands == 4:        
        colours[2] = magnitude_dictt[check]
        colours[3] = tolerance_dictt[tol]
    elif bands == 6 :        
        colours[3] = magnitude_dictt[check]
        colours[4] = tolerance_dictt[tol]
        colours[5] = tcr_dictt[tcr]
    elif bands == 5:
        colours[4] = tolerance_dictt[tol]
        colours[3] = magnitude_dictt[check]
        if len(res) == 3:
            if int(str(res)[2]) != 0:
                print(len(res) == 3)
                print(res[2] == 0)
                colours[3] = magnitude_dictt[check]
            if int(str(res)[2]) == 0:
                colours[3] = magnitude_dictt[0]
                print(colours)                
    elif bands == 3:           
        colours[2] = magnitude_dictt[check]
        colours[3] = ''
        colours[4] = ''
    try:
        for x in range(len(colours)):            
            colours.remove('')
    except ValueError:
        print('')
    
    return colours
                
    
def KiloTeraMega(value):
    x = len(str(value))
    if x < 4:
        value = str(value)
    elif x < 7:
        value = value / 1000
        value = str(value)
        if x < 5:
            value += 'K'
        else:            
            value = value[:-2] + 'K'
    elif x < 10:
        value = value / 1000000        
        value = str(value)
        if x < 8:
            value += 'M'
        else:            
            value = value[:-2] + 'M'
    elif x < 13:        
        value = value / 1000000000
        value = str(value)
        if x < 11:
            value += 'G'
        else:            
            value = value[:-2] + 'G'
    elif x < 16:
        value = value / 1000000000000
        value = str(value)
        if x < 14:
            value += 'T'
        else:            
            value = value[:-2] + 'T'
    else:
        value = value / 1000000000000000
        value = str(value)
        value = value[:-2] + 'P'
    return value

def checkResistorColours(*args):
    lenArgs = len(args)
    if lenArgs >= 7: return print("There are too many colours! (More than 6 arguments passed through.)")
    try:        
        if lenArgs == 3:
            first = digits_dict[args[0]]
            second = digits_dict[args[1]]
            multi = pow(10 ,magnitude_dict[args[2]])
            ans = int(str(first) + str(second))
            ans = ans * multi
            ans = KiloTeraMega(ans)
            print(str(ans) + ' Omhs')
        elif lenArgs == 4:
            first = digits_dict[args[0]]
            second = digits_dict[args[1]]
            multi = pow(10 ,magnitude_dict[args[2]])
            tol = tolerance_dict[args[3]]
            ans = int(str(first) + str(second))
            ans = ans * multi
            ans = KiloTeraMega(ans)
            print(str(ans) + ' Omhs ' + tol)
        elif lenArgs == 5:
            first = digits_dict[args[0]]
            second = digits_dict[args[1]]
            third = digits_dict[args[2]]
            multi = pow(10 ,magnitude_dict[args[3]])
            tol = tolerance_dict[args[4]]
            ans = int(str(first) + str(second) + str(third))
            ans = ans * multi
            ans = KiloTeraMega(ans)
            print(str(ans) + ' Omhs ' + tol )
        elif lenArgs == 6:
            first = digits_dict[args[0]]
            second = digits_dict[args[1]]
            third = digits_dict[args[2]]
            multi = pow(10 ,magnitude_dict[args[3]])
            tol = tolerance_dict[args[4]]
            tempco = tcr_dict[args[5]]
            ans = int(str(first) + str(second) + str(third))
            ans = ans * multi
            ans = KiloTeraMega(ans)
            print(str(ans) + ' Omhs ' + tol + ' ' + tempco)
        elif args[0] == 'black':
            print('0 Omhs')
            ans = 0
        else:
            x = 'Double check the colours are correct, not enough or too many arguments passed.'
            return x
        return ans
    except KeyError:
        print("Please double check your spellings.")



print(resistorColourGen(150,5))
checkResistorColours('brown', 'green', 'black', 'black', 'gold')
print(resistorColourGen(150,4))
checkResistorColours('brown', 'green', 'brown', 'gold')
print(resistorColourGen(100,3))
checkResistorColours('brown','black','brown')

