# 打开文件
with open('m1111.txt', 'r') as f:
    data = f.read()

# 将每行2048个字符拆分为多行
lines = [data[i:i+30696] for i in range(0, len(data), 30696)]

# 将拆分后的文本写回文件
with open('m1111.txt', 'w') as f:
    f.write('\n'.join(lines))
