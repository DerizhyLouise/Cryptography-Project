m = int(input("Input Rows : "))
n = int(input("Input Columns : "))

inputMatrix = []
outputMatrix = []

print("Input number of elements in a row (1, 2, 3)")

for i in range(m):
    y = [int(z) for z in input().split()]
    inputMatrix.append(y)
    
for j in range(len(inputMatrix[0])):
    row = []
    for k in range(len(inputMatrix)):
        row.append(inputMatrix[k][j])
    outputMatrix.append(row)
        
print("Print Matrix:")
for row in outputMatrix:
    print(' '.join(str(num) for num in row))