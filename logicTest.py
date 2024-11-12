class Test:
    def __init__(self):
        pass
    def Test1(self,test_in=0):
        test_out=[]
        for num in test_in:
            buf =""
            for text in str(num):
                buf = text + buf
            test_out.append(buf)
        print(test_out)
    def Test2(self, text=""):

        char_count = {}
        for char in text.upper():
            if char != ' ':  # 跳過空格
                if char in char_count:
                    char_count[char] += 1
                else:
                    char_count[char] = 1

        for char, count in char_count.items():
            print(char, count)

    def Test3(self, input_num):
        if input_num <= 0:
            print("人數必須大於 0")
            return 0
        people = list(range(1, input_num + 1))
        index = 0

        while len(people) > 1:
            index = (index + 2 ) % len(people)
            people.pop(index)

        print(people[0])

    def Main(self):
        self.Test1([35, 46, 57, 91, 29])
        self.Test2("Hello welcome to Cathay 60th year anniversary")
        self.Test3(int(input("請輸入0~100")))

if __name__ == '__main__':
    obj = Test()
    obj.Main()