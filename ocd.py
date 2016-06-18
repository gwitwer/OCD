years = [
    '1966',
    '1971',
    '1976',
    '1981',
    '1986',
    '1991',
    '1996'
]

end = 2015
start = 1998
for x in range ((end + 1) - start):
    print(x + start)
    years.append(str(x + start))


print(years)
