class Calculator:
    def __init__(self):
        self.arr = None

    def minimum(self,arr):
        self.arr = arr

        min_x = 1000
        min_y = 1000
        for x in range(0, 5):
            temp_x = self.arr[x][0]
            temp_y = self.arr[x][1]
            if (temp_x < min_x):
                min_x = temp_x
            elif (temp_y < min_y):
                min_y = temp_y
        return (min_x, min_y)

    def maximum(self,arr):
        self.arr = arr
        max_x = 0
        max_y = 0
        for x in range(0, 5):
            temp_x = self.arr[x][0]
            temp_y = self.arr[x][1]
            if (temp_x > max_x):
                max_x = temp_x
            elif (temp_y > max_y):
                max_y = temp_y
        return (max_x, max_y)

    def avg(self,arr):
        self.arr = arr
        sum = 0
        for i in self.arr:
            sum += i
        avg = sum / len(self.arr)
        return avg