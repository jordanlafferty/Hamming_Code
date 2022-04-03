import math


class HammingCode_Encode:
    def __init__(self, n):
        self.data = n
        self.m = len(n)
        self.r = self.redundantBits()
        self.arr = self.adjust()
        self.arr = self.parityBits()

    def redundantBits(self):
        for i in range(self.m):
            if 2 ** i >= self.m + i + 1:
                return i

    def parityBits(self):
        x = len(self.arr)
        for i in range(self.r):
            val = 0
            for j in range(0, x + 1):
                if j & (2 ** i) == (2 ** i):
                    val = val ^ int(self.arr[-1 * j])
            self.arr = self.arr[:x - (2 ** i)] + str(val) + self.arr[x - (2 ** i) + 1:]
        return self.arr

    def adjust(self):
        x = 0
        y = 1
        res = ''

        for i in range(1, self.m + self.r + 1):
            if i == 2 ** x:
                res = res + '0'
                x += 1
            else:
                res = res + self.data[-1 * y]
                y += 1
        return res[::-1]

    def detectError(self, errorMessage):
        n = len(errorMessage)
        res = 0

        # Calculate parity bits again
        for i in range(self.r):
            val = 0
            for j in range(1, n + 1):
                if j & (2 ** i) == (2 ** i):
                    val = val ^ int(errorMessage[-1 * j])

            res = res + val * (10 ** i)

        if int(str(res), 2) == 0:
            return str(-1)

        # Convert binary to decimal
        return j - int(str(res), 2)

    def reverse(self):
        reverseArr = ""
        for i in range(len(self.arr)):
            reverseArr = self.arr[i] + reverseArr
        return reverseArr

    def decodeHamming(self):
        decoded = ""
        power = 0
        orderedBits = self.reverse()
        for i in range(1, len(self.arr) + 1):
            if i == pow(2, power):
                power += 1
            else:
                decoded = orderedBits[i - 1] + decoded

        return decoded


def textToBinary(text):
    res = ''.join(format(i, '08b') for i in bytearray(text, encoding='utf-8'))

    return res


def binaryToDecimal(binary):
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def binaryToText(binary):
    l = []
    m = ""
    for i in binary:
        b = 0
        c = 0
        k = int(math.log10(i)) + 1
        for j in range(k):
            b = ((i % 10) * (2 ** j))
            i = i // 10
            c = c + b
        l.append(c)
    for x in l:
        m = m + chr(x)
    return m


def checkAndCorrectError(hamming, code):
    errorPoint = hamming.detectError(code)
    if errorPoint == str(-1):
        print("There is no error in the code")
        return code
    else:
        print("There is an error at position: " + str(errorPoint))
        correct = correctError(errorPoint, code)
        print("The corrected data is: " + correct)
        return correct


def correctError(pointOfError, errorData):
    correctedData = ''
    for i in range(len(errorData)):
        if i == pointOfError:
            if errorData[i] == '0':
                correctedData = correctedData + '1'
            else:
                correctedData = correctedData + '0'
        else:
            correctedData = correctedData + errorData[i]

    return str(correctedData)


def HammingCodeExample(read):
    print("This is the original text: " + read)
    print("\n")
    letters = []
    for i in range(len(read)):
        x = textToBinary(read[i])
        letters.append(x)
    print("this is the text in binary form: ")
    print(letters)
    print("\n")

    dataStruct = []
    encodedArr = []
    decodedArr = []
    for i in range(len(letters)):
        h_Encode = HammingCode_Encode(str(letters[i]))
        encodedArr.append(h_Encode.arr)
        dataStruct.append(h_Encode)
    print("this is the text in encoded: ")
    print(encodedArr)
    print("\n")

    for i in range(len(encodedArr)):
        s = dataStruct[i].decodeHamming()
        decodedArr.append(s)
    print("this is the text after being decoded: ")
    print(decodedArr)
    print("\n")

    for i in range(len(decodedArr)):
        decodedArr[i] = int(decodedArr[i])
    print("this is the text after being encoded and decoded: ")
    print(binaryToText(decodedArr))
    print("\n")


# text for the Hamming Code
txt = "Praise the Lord, all you nations; extol him, all you peoples. For great is his love toward us, " \
      "and the faithfulness of the Lord endures forever. Praise the Lord. "

# gives all the information and does the hamming code with the text
HammingCodeExample(txt)


# example with error correcting on a smaller scale so it is easier to read

txt2 = "a"
print("example text: 'a'")
txt2Binary = textToBinary(txt2)
letters = []
x = textToBinary(txt2)
letters.append(x)
print("this is the correct data: ")

encodedArr = []
h_Encode = HammingCode_Encode(str(letters[0]))
encodedArr.append(h_Encode.arr)
print(encodedArr)
print("we are going to pretend we received this: ")
incorrectArr = ['01100010110']
print(incorrectArr)
print("After Detecting: ")
error = checkAndCorrectError(h_Encode, incorrectArr[0])

print("\nThe Hamming Code can only correct one mistake so if I do multiple errors it will not work!")
print("It will change a correct bit-- here is an example using 'a' again\n")
incorrectArr = ['01100110110']
print("correct code: " + encodedArr[0])
print("Code with 2 mistakes:" + incorrectArr[0])
print("After Detecting: ")
error2 = checkAndCorrectError(h_Encode, incorrectArr[0])




