"""Module for converting arabic numbers to roman."""

def arabic_roman(nums):
    """Converts arabic number to roman."""
    def addition(num, length):
        def filling(length):
            zero = ['', '']
            i = 1
            while i + 1 < length:
                zero.append(zero[len(zero) - 1] + '0')
                i += 1
            return zero

        return num[:2] + filling(length)[length - 1 - len(num[2:])] + num[2:]

    nums = addition('0d' + str(nums), 6)[2:]
    results = ''
    liters = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 100: 'C',
              400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'}
    results += liters[1000] * int(nums[0])
    if int(nums[1]) == 0:
        results += ''
    elif 1 <= int(nums[1]) <= 3:
        results += liters[100] * int(nums[1])
    elif int(nums[1]) == 4:
        results += liters[400]
    elif int(nums[1]) == 5:
        results += liters[500]
    elif 6 <= int(nums[1]) <= 8:
        results += liters[500] + liters[100] * (int(nums[1]) - 5)
    else:
        results += liters[900]
    if int(nums[2]) == 0:
        results += ''
    elif 1 <= int(nums[2]) <= 3:
        results += liters[10] * int(nums[2])
    elif int(nums[2]) == 4:
        results += liters[40]
    elif int(nums[2]) == 5:
        results += liters[50]
    elif 6 <= int(nums[2]) <= 8:
        results += liters[50] + liters[10] * (int(nums[2]) - 5)
    else:
        results += liters[90]
    if int(nums[3]) == 0:
        results += ''
    elif 1 <= int(nums[3]) <= 3:
        results += liters[1] * int(nums[3])
    elif int(nums[3]) == 4:
        results += liters[4]
    elif int(nums[3]) == 5:
        results += liters[5]
    elif 6 <= int(nums[3]) <= 8:
        results += liters[5] + liters[1] * (int(nums[3]) - 5)
    else:
        results += liters[9]
    return results
