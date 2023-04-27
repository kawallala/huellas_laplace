f = open("/home/laplace/Documents/Laplace_code/a.txt", "rt")
num = int(f.read())
f.close()
num += 1
f = open("/home/laplace/Documents/Laplace_code/a.txt", "wt")
f.write(str(num))
f.close()