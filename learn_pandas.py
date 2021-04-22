import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from datetime import date, timedelta

'''
1.创建文件
'''
df = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['james', 'cuixin', 'nick']})
df = df.set_index('ID')
df.to_excel('/Users/cuixin/Desktop/output.xlsx')
print('ok！')

'''
2.读取文件
'''
area_info = pd.read_excel('./idcard2021.xls', header=0)  # header默认是0
area_info = pd.read_excel('./idcard2021.xls', header=1)  # header取第一行
area_info = pd.read_excel('./idcard2021.xls', header=None)  # 没有header，自行定义header
area_info.columns = ['编码', '省', '市', '区县', '省市', '省市县']
area_info.set_index('编码', inplace=True)  # 去除下标 0，1，2,...
area_info.to_excel('./idcard1.xlsx')
print(area_info.shape)  # 总行数和列数
print(area_info.columns)  # 列名
print(area_info.head(3))  # 看前几行

'''
3.行,列,单元格
'''
# 字典
d = {'x': 100, 'y': 200, 'z': 300}
pd = pd.Series(d)
print(pd.index)
print(pd)
# 列表
L1 = [100, 200, 300]
L2 = ['x', 'y', 'z']
pd = pd.Series(L1, index=L2)
print(pd)
# 操作行列
s1 = pd.Series([1, 2, 3], index=[1, 2, 3], name='A')
s2 = pd.Series([10, 20, 30], index=[1, 2, 3], name='B')
s3 = pd.Series([100, 200, 300], index=[1, 2, 3], name='C')
# s3 = pd.Series([100, 200, 300], index=[2, 3, 4], name='C')
df = pd.DataFrame({s1.name: s1, s2.name: s2, s3.name: s3})
print(df)

'''
4.数字区域读取,填充数字,日期序列
'''


def add_month(d, md):
    yd = md // 12
    m = d.month + md % 12
    if m != 12:
        yd += m // 12
        m = m % 12
    return date(d.year + yd, m, d.day)


books = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Books.xlsx', skiprows=3, usecols='C:F',
                      dtype={'ID': str, 'InStore': str, 'Date': str})
start = date(2021, 1, 1)
for i in books.index:
    # 写法一
    books['ID'].at[i] = i + 1
    books['InStore'].at[i] = 'Yes' if i % 2 == 0 else 'No'
    books['Date'].at[i] = start + timedelta(days=i)  # 天增长
    books['Date'].at[i] = date(start.year + i, start.month, start.day)  # 年增长
    books['Date'].at[i] = add_month(start, i)  # 月增长
    # 写法二
    books.at[i, 'ID'] = i + 1
    books.at[i, 'InStore'] = 'Yes' if i % 2 == 0 else 'No'
    books.at[i, 'Date'] = start + timedelta(days=i)  # 天增长
    books.at[i, 'Date'] = date(start.year + i, start.month, start.day)  # 年增长
    books.at[i, 'Date'] = add_month(start, i)  # 月增长

books.set_index('ID', inplace=True)
print(books)
books.to_excel('/Users/cuixin/Desktop/card/output22.xlsx')

'''
5.函数填充，计算列
'''
books = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Books.xlsx', index_col='ID')
books['Price'] = books['ListPrice'] * books['Discount']
books['ListPrice'] = books['ListPrice'].apply(lambda x: x + 2)
print(books)

'''
6.排序，多重排序
'''
# 单排
products = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/List.xlsx', index_col='ID')
products.sort_values(by='Price', inplace=True, ascending=False)
print(products)
# 多重排序
products = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/List.xlsx', index_col='ID')
products.sort_values(by=['Worthy', 'Price'], inplace=True, ascending=[True, False])
print(products)

'''
7.数据筛选，过滤
'''


def age_18_to_30(age):
    return 18 <= age < 30

def level_a(score):
    return 85 <= score < 100

students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx', index_col='ID')
students = students.loc[students['Age'].apply(lambda age: 18 <= age < 30)].loc[students['Score'].apply(lambda score: 85 <= score < 100)]
# students=students.loc[students.Age.apply(age_18_to_30)].loc[students.Score.apply(level_a)]
print(students)

'''
8.柱状图
'''
# pandas绘图
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx')
students.sort_values(by='Number', inplace=True, ascending=False)
students.plot.bar(x='Field', y='Number', color='green', title='internation student by field')
plt.tight_layout()
plt.show()

# matplotlib绘图
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx')
students.sort_values(by='Number', inplace=True, ascending=False)
plt.bar(students.Field, students.Number, color='green')
plt.xticks(students.Field, rotation='90')
plt.xlabel('Field')
plt.ylabel('Number')
plt.title('internation student by field')
plt.tight_layout()
plt.show()

'''
9.分组柱图，深度优化
'''
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx')
students.sort_values(by='2017', inplace=True, ascending=False)
print(students)
students.plot.bar(x='Field', y=['2016', '2017'], color=['green', 'red'], title='internation student by field')
plt.title('zheshi gfenxi tu', fontsize=16, fontweight='bold')
plt.xlabel('Field', fontweight='bold')
plt.ylabel('Number', fontweight='bold')
ax = plt.gca()
ax.set_xticklabels(students['Field'], rotation=45, ha='right')
f = plt.gcf()
f.subplots_adjust(left=0.2, bottom=0.42)
# plt.tight_layout()
plt.show()

'''
10.叠加柱状图，水平柱状图
'''
users = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Users.xlsx', index_col='ID')
users['Total'] = users['Oct'] + users['Nov'] + users['Dec']
users.sort_values(by='Total', inplace=True, ascending=True)
print(users)
users.plot.barh(x='Name', y=['Oct', 'Nov', 'Dec'], stacked=True, title='User Behavior')
plt.tight_layout()
plt.show()


'''
11.饼图
'''
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx', index_col='From')
print(students)
# students['2017'].sort_values(ascending=True).plot.pie(fontsize=8, startangle=-270)
students['2017'].plot.pie(fontsize=8, counterclock=False, startangle=-270)
plt.title('zhu zhuang tu student', fontsize=16, fontweight='bold')
plt.ylabel('2017', fontsize=12, fontweight='bold')
plt.show()


'''
12.折线图
'''
weeks = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Orders.xlsx', index_col='Week')
print(weeks)
print(weeks.columns)
weeks.plot.area(y=['Accessories', 'Bikes', 'Clothing', 'Components', 'Grand Total'])
plt.title('zhe xian tu weeks', fontsize=16, fontweight='bold')
plt.ylabel('Total', fontsize=12, fontweight='bold')
plt.xticks(weeks.index, fontsize=8)
plt.show()


'''
13.散点图，直方图，密度图，数据相关性
'''
# 散点图
pd.options.display.max_columns = 777
homes = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/home_data.xlsx')
print(homes.head())
homes.plot.scatter(x='sqft_living', y='price')
plt.show()

# 直方图
pd.options.display.max_columns = 777
homes = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/home_data.xlsx')
print(homes.head())
homes.sqft_living.plot.hist(bins=100)
plt.xticks(range(0, max(homes.sqft_living), 500), fontsize=8, rotation=90)
plt.show()

# 密度图
pd.options.display.max_columns = 777
homes = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/home_data.xlsx')
print(homes.head())
homes.sqft_living.plot.kde()
plt.xticks(range(0, max(homes.sqft_living), 500), fontsize=8, rotation=90)
plt.show()

'''
14.多表联合，（从VLOOKUP到JOIN）
'''
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Student_score.xlsx', sheet_name='Students', index_col='ID')
scores = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Student_score.xlsx', sheet_name='Scores', index_col='ID')
# table = students.merge(scores, how='left', on='ID').fillna(0)
table = students.join(scores, how='left').fillna(0)
table.Score = table.Score.astype(int)
print(table)


'''
15.数据校验，轴的概念
'''


def score_validation(row):
    try:
        assert 0 <= row.Score <= 100
    except:
        print('#%s\t student %s has an invalid score %s' % (row.ID, row.Name, row.Score))
def score_validation(row):
    if not 0 <= row.Score <= 100:
        print('#%s\t student %s has an invalid score %s' % (row.ID, row.Name, row.Score))

students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx')
students.apply(score_validation, axis=1)
print(students)


'''
16.把一列数据分成两列 Employees
'''
employees = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Employees.xlsx', index_col='ID')
df = employees['Full Name'].str.split(expand=True)
employees['First Name'] = df[0]
employees['Last Name'] = df[1]
# print(df)
print(employees)


'''
17.求和，求平均，统计导引
'''
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students.xlsx', index_col='ID')
temp = students[['Test_1', 'Test_2', 'Test_3']]
students['Total'] = temp.sum(axis=1)
students['Average'] = temp.mean(axis=1)

col_mean = students[['Test_1', 'Test_2', 'Test_3', 'Total', 'Average']].mean()
col_mean['Name'] = 'Sunmary'
students = students.append(col_mean, ignore_index=True)
print(students)


'''
18.定位，消除重复数据
'''
# 定位
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students_Duplicates.xlsx')
dupe = students.duplicated(subset='Name')
dupe = dupe[dupe == True]
print(students.iloc[dupe.index])

# 消除重复数据
students = pd.read_excel('/Users/cuixin/Desktop/card/Pandas vs Excel/Students_Duplicates.xlsx', index_col='ID')
students.drop_duplicates(subset='Name', inplace=True, keep='first')
print(students)
