# Treinamento_IS

Projeto final para conclusão do treinamento do espaço inteligente.
O projeto consiste em três containers chamados: client, gateway e robot. Estes simulam o controle de um robô no espaço inteligente.

Para rodar a aplicação basta utilizar os seguintes comandos:

1- Subir o container do broker:
  
  docker run -d --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.7.6-management

2- Subir o container do robô:

  sudo docker run --rm --network=host vinihernech/is_training:robot_image
  
3 - Subir o container do gateway:

  sudo docker run --rm --network=host vinihernech/is_training:gateway_image

4 - Subir o container do client:

  sudo docker run --rm --network=host vinihernech/is_training:client_image

Dessa forma as imagens serão baixadas automaticamente no DockerHub e os containers serão levantados. 

Primeiramente o sistema tentará ligar, após inicializado, solicitará a posição atual do robô ou mudará sua posição de forma aleatória e autônoma. O ID do robô foi fixado para facilitar a visualização do "get position" e "set position", os valores das novas posições são aleatórios, o valor da coordenada Z tem a possibilidade de ser negativo para demonstrar o tratamento da mensagem e a utilização de Logs e Status. 
