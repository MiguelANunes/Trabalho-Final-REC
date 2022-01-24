from contextlib import redirect_stdout

list1 = ["0.001", "0.01", "0.1", "1", "10"]
list2 = ["0", "12.5", "100", "200"]
list3 = ["1gbit", "10mbit"]
list4 = [0, 1, 2]
path = "/home/miguel/Documentos/Udesc/Matérias/REC/Trabalho Final/Algoritmos/Inputs/"
i = 0

for x in list1:
    for y in list2:
        for z in list3:
            for w in list4:
                with open(path+"teste"+str(i), 'w') as f:
                    with redirect_stdout(f):
                        print(x)
                        print(y)
                        print(z)
                        print(w)
                with open(path+"netem"+str(i), 'w') as f:
                    with redirect_stdout(f):
                        string = "tc qdisc add dev lo root netem loss "+x+" delay "+y+" rate "+z
                        print(string)
                        i+=1
with open((path+"clean"), 'w') as f:
    with redirect_stdout(f):
        string = "tc qdisc del dev lo root"
        print(string)