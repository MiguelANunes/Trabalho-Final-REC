import os
import re
from contextlib import redirect_stdout

# Lê os resultados dos testes feitos pelo network_test.py e salva eles em um unico arquivo
# em formato human readable (e, se possível, Latex-ready tbm)

partial_path = "/home/miguel/Documentos/Udesc/Matérias/REC/Trabalho Final/Algoritmos/Outputs/"

def get_perda(file):
    if(file.split("%")[0] == "0.001"):
        return "0.001%"
    elif(file.split("%")[0] == "0.01"):
        return "0.01%"
    elif(file.split("%")[0] == "0.1"):
        return "0.1%"
    elif(file.split("%")[0] == "1"):
        return "1%"
    elif(file.split("%")[0] == "10"):
        return "10%"

def get_atraso(file):
    if("200ms" in file):
        return "200 ms"
    elif("100ms" in file):
        return "100 ms"
    elif("12.5ms" in file):
        return "12.5 ms"
    elif("0ms" in file):
        return "0 ms"

def get_rate(file):
    if("gbit" in file):
        return "1gbits"
    else:
        return "10mbits"

def parse(algoritmo1, algoritmo2, path, end_path, lista_arquivos):

    resultados = dict()

    for file in lista_arquivos:
        with open(path+"/"+file) as f:
            file_contents = f.readlines()

            temp_list = []
            for f in file_contents:

                string = re.search("     (.+?)  ", f)
                if string:
                    substring = string.group(1)
                    f = f.replace("     "+substring+"  "," ")

                string = re.search("0    (.+?)  ", f)
                if string:
                    substring = string.group(1)
                    f = f.replace("0    "+substring+"  ","0 ")
                
                string = re.search("    (.+?)   ", f)
                if string:
                    substring = string.group(1)
                    f = f.replace("    "+substring+"   "," "+substring+"x ")

                string = re.search("x (.+?)\n", f)
                if string:
                    substring = string.group(1)
                    f = f.replace("x "+substring+"\n","")

                temp_list.append(f)
            
            file_contents = temp_list

            temp_string = "Instante | Bitrate | Pacotes Perdidos"
            file_contents.insert(0, temp_string)
            temp_string = "****************************"
            file_contents.insert(len(file_contents)-1, temp_string)
            temp_string = "Bitrate Médio e Perda Total:"
            file_contents.insert(len(file_contents)-1, temp_string)

            temp_list = []
            for f in file_contents:
                f = "\t\t\t"+f
                temp_list.append(f)

            file_contents = temp_list
            temp_string = "\t\tAtraso: "+get_atraso(file)
            file_contents.insert(0, temp_string)
            temp_string = "\tPerda: " + get_perda(file)
            file_contents.insert(0, temp_string)
            temp_string = "Bitrate: " + get_rate(file)
            file_contents.insert(0, temp_string)
            resultados[(get_rate(file), get_perda(file), get_atraso(file))] = file_contents

    result_path = "/home/miguel/Documentos/Udesc/Matérias/REC/Trabalho Final/Algoritmos/Results/"+end_path
    filename = algoritmo1+" - 1Gbits.txt"

    list1 = ["0.001%", "0.01%", "0.1%", "1%", "10%"]
    list2 = ["0 ms", "12.5 ms", "100 ms", "200 ms"]

    open(result_path+"/"+filename, 'w') # limpando o arquivo antes de escrever o resultado

    for x in list1:
        for y in list2:
            for out_string in resultados[("1gbits", x, y)]:
                with open(result_path+"/"+filename, 'a') as f:
                    with redirect_stdout(f):
                        print(out_string)
    
    result_path = "/home/miguel/Documentos/Udesc/Matérias/REC/Trabalho Final/Algoritmos/Results/"+end_path
    filename = algoritmo1+" - 10Mbits.txt"
    for x in list1:
        for y in list2:
            for out_string in resultados[("10mbits", x, y)]:
                with open(result_path+"/"+filename, 'a') as f:
                    with redirect_stdout(f):
                        print(out_string)


def main():

    subdirs = os.listdir(partial_path)
    results = []

    for subdir in subdirs:
        x = subdir.split('x')
        results.append(tuple((x)))

    for pair in results:
        
        alg1, alg2 = pair
        path = partial_path + alg1+"x"+alg2
        path += "/"+alg1
        file_list = []

        with os.scandir(path) as folder:
            for item in folder:
                if item.is_file():
                    file_list.append(item.name)

        end_path = alg1+"x"+alg2
        parse(alg1, alg2, path, end_path, file_list)

        path = "".join(path.rsplit("/"+alg1,1))
        path += "/"+alg2

        file_list = []
        with os.scandir(path) as folder:
            for item in folder:
                if item.is_file():
                    file_list.append(item.name)

        parse(alg2, alg1, path, end_path, file_list)

if __name__ == "__main__":
    main()
