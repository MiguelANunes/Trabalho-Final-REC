import subprocess
from contextlib import redirect_stdout

# Automaticamente testa dois algoritmos de controle de fluxo do tcp em paralelo
# e salva os resultados do teste

# TODO: Repetir testes
#       comando bash que faça todos os teste de uma vez só (rodar esse bash dentro do sudo su, bash deve executar esse arquivo tbm)
#       Makefile ^ ?
#       Fazer um outro arquivo para dar parse no output

alg1, alg2 = 0, 0
string1 = "iperf3 -c 127.0.0.1 -p"
string2 = "iperf3 -c 127.0.0.1 -p"

loss    = input("Perda de dados para esse teste: ")
delay   = input("Atraso de comunicação para esse teste: ")
bitrate = input("Bitrate simulado para esse teste (com unidade): ")

while(True):

    print("Escolha o teste a ser  feito:")
    print("\t0: Cubic vs Reno")
    print("\t1: Cubic vs Westwood")
    print("\t2: Reno  vs Westwood")

    option = int(input())

    if(option == 0):
        alg1 = "Cubic"
        alg2 = "Reno"
        string1 += " 30000 -C cubic"
        string2 += " 40000 -C reno"
        break
        
    elif(option == 1):
        alg1 = "Cubic"
        alg2 = "Westwood"
        string1 += " 30000 -C cubic"
        string2 += " 50000 -C westwood"
        break

    elif(option == 2):
        alg1 = "Reno"
        alg2 = "Westwood"
        string1 += " 40000 -C reno"
        string2 += " 50000 -C westwood"
        break

    else:
        print("Valor inválido")
        continue

#                                  Definindo Perda de Pacotes
#                                     || Quantos % são perdidos
#                                     ||   || Limitando Bitrate (importante p/ teste)
#                                     ||   ||   || Limite do Bitrate     
#                                     ||   ||   ||   || Simulando atraso
#                                     ||   ||   ||   ||   || Total de atraso
#                                     ||   ||   ||   ||   ||    ||
#                                     \/   \/   \/   \/   \/    \/
#sudo tc qdisc add dev lo root netem loss 0.1 rate 1gbit delay 12.5
#sudo tc qdisc del dev lo root
print_string = "### Rodando "+alg1+" e "+alg2+" com "+loss+"% de perda de pacotes, "+delay+" ms de atraso e "
print_string += "bitrate limitado a "+bitrate
print(print_string)

proc1 = subprocess.Popen(string1.split(), stdout=subprocess.PIPE)
proc2 = subprocess.Popen(string2.split(), stdout=subprocess.PIPE)

out1 = (proc1.communicate()[0]).decode('utf8')
out2 = (proc2.communicate()[0]).decode('utf8')

# *** Salvando output do iperf3 num arquivo para extrair os dados ***

# Salvando output raw só por garantia
tested_algs     = alg1+"x"+alg2
additional_info = loss+"% "+delay+"ms "+bitrate
partial_path    = "/home/miguel/Documentos/Udesc/Matérias/REC/Trabalho Final/Algoritmos/Outputs/"

filename = additional_info+".txt"
filepath = partial_path+tested_algs+"/"+alg1+"/RAW/"+filename
with open(filepath, 'w') as f:
    with redirect_stdout(f):
        print(out1)

filename = additional_info+".txt"
filepath = partial_path+tested_algs+"/"+alg2+"/RAW/"+filename
with open(filepath, 'w') as f:
    with redirect_stdout(f):
        print(out2)

out1 = out1.split('\n')
temp = []
for o in out1:
    o = o.replace("[  5]   ", "")
    o = o.replace("/sec","/seC")
    o = o.replace("sec","")
    o = o.replace("/seC","/sec")
    temp.append(o)

out1 = temp

del out1[13:15] # removendo a cauda
del out1[14:]   # removendo a cauda
del out1[0:3]   # removendo o cabeçalho

filename = additional_info+".txt"
filepath = partial_path+tested_algs+"/"+alg1+"/"+filename
with open(filepath, 'w') as f:
    with redirect_stdout(f):
        for x in out1:
            print(x)

out2 = out2.split('\n')
temp = []
for o in out2:
    o = o.replace("[  5]   ", "")
    o = o.replace("/sec","/seC")
    o = o.replace("sec","")
    o = o.replace("/seC","/sec")
    temp.append(o)

out2 = temp

del out2[13:15] # removendo a cauda
del out2[14:]   # removendo a cauda
del out2[0:3]   # removendo o cabeçalho

filename = additional_info+".txt"
filepath = partial_path+tested_algs+"/"+alg2+"/"+filename
with open(filepath, 'w') as f:
    with redirect_stdout(f):
        for x in out2:
            print(x)

print("Done !")

# https://iperf.fr/iperf-doc.php
# https://wiki.linuxfoundation.org/networking/netem
# https://c3lab.poliba.it/index.php?title=Westwood:Linux