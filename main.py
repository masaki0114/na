import numpy
input_path = "input_text"
with open(input_path) as f:
	input_text = f.read().split('\n')
nmat = int(input_text.pop(0))#　材料の種類の数
matdat = float(input_text.pop(0))#　熱伝導率
ne = int(input_text.pop(0))#　要素数
ne_data = []
for i in range(ne):
	line = input_text.pop(0).split(" ")
	ne_data.append([int(j) for j in line])
ne_data = numpy.array(ne_data)
ne_num = ne_data[:,0]#　ne_dataの先頭の数字
mat = ne_data[:,1]#　材料番号
nop = ne_data[:,2:]#　要素の接続情報


np_data = []
np = int(input_text.pop(0))#　接点数
for i in range(np):
	line = input_text.pop(0).split(" ")
	np_data.append([float(j) for j in line])
	np_data[i][0] = int(np_data[i][0])
np_data = numpy.array(np_data)
np_num = np_data[:,0]#　np_dataの先頭の数字
crd = np_data[:,1]#　接点座標



nb = int(input_text.pop(0))#　境界条件
nb_data = []
for i in range(nb):
	line = input_text.pop(0).split(" ")
	nb_data.append([float(j) for j in line])
	nb_data[i][0] = int(nb_data[i][0])
nb_data = numpy.array(nb_data)
nbc = nb_data[:,0]#　境界条件を与える接点番号
temp = nb_data[:,1]#　境界条件の設定温度
qbar = float(input_text.pop(0))#　発熱量
print(nb_data)
print(nbc)
lamda = matdat#λとmatdatって一緒じゃないの？
# print(nop[-1][-1])
# 要素行列Aの生成
NPMAX = nop[-1][-1]
a = numpy.zeros([NPMAX,NPMAX])
q = numpy.zeros([NPMAX,1])

for i in range(ne):
	# 要素行列とベクトルの計算プログラム
	lenght = crd[nop[i][1]-1] - crd[nop[i][0]-1]
	ai = numpy.array([[1.0,-1.0],[-1.0,1.0]])*(lamda/lenght)
	qi = numpy.array([[1],[1]])*(qbar*lenght)/2
	j = nop[i][0]-1
	k = nop[i][1]-1

	a[j][j] = a[j][j] + ai[0][0]
	a[j][k] = a[j][k] + ai[0][1]
	a[k][j] = a[k][j] + ai[1][0]
	a[k][k] = a[k][k] + ai[1][1]
# 要素行列Aの全体化が完成
	q[j][0] = q[j][0] + qi[0][0]
	q[k][0] = q[k][0] + qi[1][0]
print("nb = ",nb)
print("np = ",np)


# 境界条件の処理
for i in range(nb):
	for j in range(np):
		a[nbc[i]-1][j] = 0.0
	a[nbc[i]-1][nbc[i]-1] = 1.0
	q[nbc[i]-1][0] = temp[i]
print(a)
print(q)