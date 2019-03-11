letters_numbers = []
letters = []
numbers = []

for i in input().split():
    letters_numbers.append(str(i))

letters = letters_numbers[0:3] 

try:
    numbers = [int(x) for x in letters_numbers[3:]]
except ValueError:
    print("숫자를 입력해주세요")

i = ""

def AquickSort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [number for number in array[1:] if number<=pivot]
        greater = [number for number in array[1:] if number>pivot]   
        return AquickSort(less) + [pivot] + AquickSort(greater) #오름차순

def DquickSort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        greater = [number for number in array[1:] if number<=pivot]
        less = [number for number in array[1:] if number>pivot]   
        return DquickSort(less) + [pivot] + DquickSort(greater) #내림차순

result_dquick = DquickSort(numbers)
result_aquick = AquickSort(numbers)

if 'A' in letters[1]:
    print(result_aquick)
elif 'D' in letters[1]:
    print(result_dquick)
else:
     print('정렬 순서(A 또는 D)를 입력해주세요')

if '-o' not in letters[0]:
    print('정렬 순서 시작(-o)을 표시 해 주세요')
elif '-i' not in letters[2]:
    print('정렬할 숫자 시작(-i)을 표시 해 주세요')