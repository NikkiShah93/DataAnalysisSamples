## When Excel messes up the CAS numbers
## As a data analyst that has to deal with CAS numbers frequently
## I need to know if a CAS number valid or not?
## So I developed the following function that would check for that!

## The CAS number could have 12 character tops (including the dashes)
## the first part could have between 2-7 digit, the second part must have 2 digits and last part is a single digit
## Read more about it here: https://www.cas.org/support/documentation/chemical-substances/checkdig

## This function would check for couple of things
## 1. the length can't be over 12 character
## 2. It has to contain 2 dashes
## 3. the middle part is 2 character
## 4. there's a single digit in the end
## 5. and finally, the single digit check
def CAS_validation_func(CAS):
    ## has to be string
    if type(CAS) == str:
        ## the fist 4 rules mentioned above
        if len(CAS) < 12 and CAS.count('-') == 2 and len(CAS.split('-')[1]) == 2 and len(CAS.split('-')[2]) == 1:
            modified_CAS = CAS.replace('-', '')
            check_digit = int(CAS[-1])
            sum_digit = 0
            for i in range(len(modified_CAS), 0, -1):
                sum_digit += (i-1)*int(modified_CAS[-i])
                print(i, sum_digit)
            if sum_digit/10 == (check_digit*10+check_digit)/10:
                return CAS
            else:
                return "Not valid!"            
        else:
            return "String, but not Valid!"
    
    else:
        return "Not string!"
cas = '107-07-3'
print(CAS_validation_func(cas))

## Another problem that I have encountered in the past is when Excel messes up your CAS number
## It treats them as date and rearrange them in a way that's not easy to retrive the correct CAS number
## I developed the function below to fix those cases
## couple of samples are 6/9/2102 when the correct number has to be 2102-06-9
## or 5/5/2151 when the correct one is 2151-05-5

def CAS_fixer_func(CAS):
    list_numbers = CAS.split('/')
    last_num = list_numbers[-2]
    list_numbers.pop(-2)
    list_numbers.reverse()
    list_numbers.append(last_num)
    if len(list_numbers[1])<2:
        list_numbers[1] = '0'+list_numbers[1]
    
    return '-'.join(list_numbers)

cas = '6/9/2102' ## it has to be 2102-06-9

print(cas_fixer(cas))