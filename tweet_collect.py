#!/usr/bin/env python
# encoding: utf-8
"""
__author__ = "Ahirton Lopes"
__copyright__ = "Copyright 2015/2016/2017, Mackenzie University"
__credits__ = ["Ahirton Lopes", "Rodrigo Pasti"]
__license__ = "None"
__version__ = "1.0"
__maintainer__ = "Ahirton Lopes"
__email__ = "ahirton.xd@gmail.com"
__status__ = "Beta"
"""
'''
-----------------------------------------------------------------------------------------------------------------------
COLETA AUTOMÁTICA DE TWEETS POR PERFIL (@) E CONSTRUCAO DE ARQUIVO CSV
-----------------------------------------------------------------------------------------------------------------------
"""
#Passos:
    #--------------------------------------------------------------------------------------------------------
    # Com este método temos acesso aos ultimos 3240 tweets de cada dado usuario 
    #--------------------------------------------------------------------------------------------------------
    #(1) Instalar Tweepy através do Pip (https://github.com/tweepy/tweepy)
    #(2) Obter 'api_key', 'api_secret', 'oauth_token' e 'oauth_token_secret'(vide documentação do Twitter)
    #(3) Modificar o presente codigo para cada necessidade especifica
    #--------------------------------------------------------------------------------------------------------
'''

import tweepy #https://github.com/tweepy/tweepy
import csv

'''
-----------------------------------------------------------------------------------------------------------------------
DEFINICAO DOS PARAMETROS DE CONTROLE, AUTENTICACAO E IMPORTACAO DO TWEEPY
-----------------------------------------------------------------------------------------------------------------------
'''   

#Credenciais da API do Twitter criada (vide documentação do Twitter)
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

'''
-----------------------------------------------------------------------------------------------------------------------
MECANISMO DE COLETA AUTOMATICA DE TWEETS POR PERFIL (@) E CONSTRUCAO DE ARQUIVO .CSV POR PERFIL
-----------------------------------------------------------------------------------------------------------------------
'''

def get_all_tweets(screen_name):
	
	#Autenticação 
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#Criação de lista para tweets importados via Tweepy
	alltweets = []	
	
	#Requisição para Importação dos 200 tweets mais recentes (limite)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#Salva-se os 200 tweets Importados
	alltweets.extend(new_tweets)
	
	#Salva-se o id dos últimos tweets importados -1
	oldest = alltweets[-1].id - 1
	
	#Continua-se a importação de tweets até que não hajam mais tweets ou se alcance o limite
	while len(new_tweets) > 0:
		print "Importando tweets antes de %s" % (oldest)
  
		#Tweets subsequentes utilizam-se de max_id para que não haja duplicatas
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#Salva-se os novos 200 tweets importados
		alltweets.extend(new_tweets)
		
		#Salva-se o id dos tweets importados anteriormente -1
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets importados ate o momento" % (len(alltweets))
 
	#Transforma-se os tweets em array afim de popular o arquivo .csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets if (not tweet.retweeted) and ('RT @' not in tweet.text)]

	#Cria-se o arquivo .csv
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	pass

'''
-----------------------------------------------------------------------------------------------------------------------
DEFINICAO DO PERFIL A SER MINERADO
-----------------------------------------------------------------------------------------------------------------------
'''

if __name__ == '__main__':
	#Username da conta a ser minerada
	get_all_tweets("@profile")
