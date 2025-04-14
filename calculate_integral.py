from scipy.integrate import quad
import pandas as pd
import numpy as np
from scipy.linalg import solve
import time


def calculate_R(triangular_fuzzy1, triangular_fuzzy2):
    a1, b1, c1 = triangular_fuzzy1
    a2, b2, c2 = triangular_fuzzy2

    if b1 > b2:
        a1, b1, c1 = triangular_fuzzy2
        a2, b2, c2 = triangular_fuzzy1

    def left_membership1(x, a, b):
        if x <= a:
            return 0
        elif a < x <= b:
            return ((1 / (b - a)) ** 3 * (x - a) ** 2 * (b - x)) + ((x - a) / (b - a))
        else:
            return 0

    def right_membership1(x, b, c):
        if x >= c:
            return 0
        elif b <= x < c:
            return ((1 / (b - c)) ** 3 * (x - c) ** 2 * (b - x)) + ((x - c) / (b - c))
        else:
            return 0

    def left_membership2(x, a, b):
        if x <= a:
            return 0
        elif a < x <= b:
            return ((1 / (b - a)) ** 3 * (x - a) ** 2 * (b - x)) + ((x - a) / (b - a))
        else:
            return 0

    def right_membership2(x, b, c):
        if x >= c:
            return 0
        elif b <= x < c:
            return ((1 / (b - c)) ** 3 * (x - c) ** 2 * (b - x)) + ((x - c) / (b - c))
        else:
            return 0

    def diff_function1(x, a1, b1, a2, b2):
        return left_membership1(x, a1, b1) - left_membership2(x, a2, b2)

    I1, error1 = quad(diff_function1, min(a1, a2), b1, args=(a1, b1, a2, b2))

    def diff_function2(x, b1, c1, a2, b2):
        return abs(right_membership1(x, b1, c1) - left_membership2(x, a2, b2))

    I2, error2 = quad(diff_function2, b1, b2, args=(b1, c1, a2, b2))

    def diff_function3(x, b2, c2, b1, c1):
        return right_membership2(x, b2, c2) - right_membership1(x, b1, c1)

    I3, error3 = quad(diff_function3, b2, max(c1, c2), args=(b2, c2, b1, c1))

    R = I1 + I2 + I3


    return R


#triangular_fuzzy_number1 = (1,1.5,2)
#triangular_fuzzy_number2 = (-1,1.7,1.9)
#I1, error1, I2, error2,  I3, error3, R, error = calculate_R(triangular_fuzzy_number1, triangular_fuzzy_number2)
# خواندن داده‌های از فایل اکسل برای هر دسته
df1 = pd.read_excel('fuzzy_numbers5.xlsx', sheet_name='Sheet1')
df2 = pd.read_excel('fuzzy_numbers5.xlsx', sheet_name='Sheet2')
# محاسبه مقادیر R بین هر جفت متناظر از هر دسته
R_values = []
start_time = time.time()
for index, (row1, row2) in enumerate(zip(df1.iterrows(), df2.iterrows())):
    triangular_fuzzy1 = (row1[1]['a'], row1[1]['b'], row1[1]['c'])
    triangular_fuzzy2 = (row2[1]['a'], row2[1]['b'], row2[1]['c'])

    R = calculate_R(triangular_fuzzy1, triangular_fuzzy2)
    R_values.append(R)
end_time = time.time()
# ایجاد DataFrame برای نتایج
results_df = pd.DataFrame(R_values, columns=['calculate_R'])

# ذخیره نتایج در شیت جدید فایل اکسل
with pd.ExcelWriter('fuzzy_numbers5.xlsx', engine='openpyxl', mode='a') as writer:
    results_df.to_excel(writer, sheet_name='calculate_R', index=False)

print("Data processed and saved to fuzzy_numbers.xlsx")
# پایان زمان‌گیری


# محاسبه و چاپ زمان اجرا
execution_time = end_time - start_time
print(f"زمان اجرا: {execution_time:.2f} ثانیه")