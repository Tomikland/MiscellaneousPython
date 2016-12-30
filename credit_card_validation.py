import math

def sum_digits(number):
    total = 0
    while number > 0:
        total += number % 10
        number //= 10
    return total

def check_credit_card(card_number, checkdigit):
    number_of_digits = int(math.log10(card_number))+1
    if number_of_digits != 16:
        return false

    check_sum = 0
    for i in range(10):
        num = card_number % 10
        card_number //= 10
        
        if i % 2 == 0: #Even, double digit
            num *= 2

        check_sum += num    
        
    return check_sum % 10 == 0

if __name__ == '__main__':
    print(check_credit_card(4847352989263094, 5))
