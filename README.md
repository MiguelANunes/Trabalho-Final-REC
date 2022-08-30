# Instruções de Compilação/Reprodução dos Testes

0.  Alterar as pastas que são acessadas nos arquivos .py e opcionalmente no arquivo auto_tester.sh
  
1. Executar o comando:
 
    ``python3 input_generator.py``
    
    Isso vai gerar os arquivos de input para o executar os testes
  
2. Na pasta onde estão os resultados do algoritmo acima, executar o comando
  
    ``chmod +x clean netem*``
        
    Isso dá permissão de execução para os arquivos gerados pelo algoritmo acima, necessário para o próximo passo
       
3. Executar o comando:

    ``chmod +x auto_tester.sh; ./auto_tester.sh``
    
    Isso irá iniciar a execução dos testes. Os testes levam aproximadamente 20 minutos para serem concluidos
   
4. (Opicional) Executar o comando:
 
    ``python3 parser.py``
      
    Isso vai processar os arquivos gerados pelo passo acima em um formato mais simples e condensado.
