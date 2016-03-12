import requests
import os
import requestsEngine
import staticRequests
import sqlite3
import time
import datetime

conn = sqlite3.connect('rito.db')
c = conn.cursor()

def createUser(user):
    name = (str)(raw_input('\nType your Summoner Name herer and DO NOT INCLUDE SPACES: '))
    nameMin = str.lower(name)
    userPassword = 4321 ###Generar Pass
    ##Generar dia de creacion de usuario##
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    ##Obtener region##
    print "\nEnter your region to get started"
    print "Type in one of the following regions or else the program wont work correctly:\n"
    print "NA EUW EUNE LAN BR KR LAS OCE TR RU PBE\n"
    region = str.lower((str)(raw_input('Type in one of the regions above: ')))
    ##Obtener los datods haciendo el request##
    summonerData = requestsEngine.requestSummonerData(region, nameMin)
    ##Meter los datos obtenidos##
    c.execute("INSERT INTO Users (userName, userPassword, summonerName, summonerID, userRegion, dateCreated, revisionDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (user, userPassword, nameMin, summonerData[nameMin]['id'], region, date, summonerData[nameMin]['revisionDate']))
    conn.commit()

def createMatchTable(userData):
    staticChampion = staticRequests.requestStaticChampion(userData)
    staticSpells = staticRequests.requestStaticSpells(userData)
    matchData = requestsEngine.requestMatchData(userData)
    tableName = "match" + str(matchData['matchId']) ##Lo tuve que hace asi...##
    c.execute('CREATE TABLE IF NOT EXISTS ' + tableName + ' (participantId INTEGER, summonerId INTEGER, summonerName TEXT, champPlayed TEXT, summonerSpells TEXT, role TEXT, kills INTEGER, deaths INTEGER, assists INTEGER, killParticipation TEXT, kda text, csTotal Text, csPerMin TEXT, totalGold TEXT, comments TEXT)')
    matchID = matchData['matchId']
    ##Datos de la partida que no vienen en la data solos##
    matchDuration = matchData['matchDuration'] / 60.0
    team100Deaths = 0
    team200Deaths = 0
    for i in matchData['participants']:
        if i['teamId'] == 100:
            team100Deaths = i['stats']['deaths'] + team100Deaths
        else:
            team200Deaths = i['stats']['deaths'] + team200Deaths
    ## Para meter los nombres de sumoner y el ID de summoner (tambien se puedes sacar Icono, Url de match History
    for i in matchData['participantIdentities']:
        c.execute("INSERT INTO " + tableName + " (participantId, summonerId, summonerName) VALUES (?, ?, ?)",
                  (i['participantId'], i['player']['summonerId'], i['player']['summonerName']))
    ##Para meter los datos de la partida de cada summoner
    for i in matchData['participants']:
        champion = staticChampion['data'][(str)(i['championId'])]['name'] #Campeon usado
        spell1 = staticSpells['data'][(str)(i['spell1Id'])]['name']
        spell2 = staticSpells['data'][(str)(i['spell2Id'])]['name']
        spellsUsed = spell1 + " / " + spell2 #Hechizos usados con formato
        ## Para calcular Kill Participation
        killsAssists = (int)(i['stats']['kills']) + (int)(i['stats']['assists'])
        kda = format((float(killsAssists) / (int)(i['stats']['deaths'])), '.2f')
        killPart = 0
        if i['teamId'] == 100:
            killPart = format((float(killsAssists) / team200Deaths), '.2f')
        else:
            killPart = format((float(killsAssists) / team100Deaths), '.2f')
        # Paca calcular CS (sumar los CS obtenidos
        minionsCS = i['stats']['minionsKilled']
        jungleCS = i['stats']['neutralMinionsKilled']
        totalCS = minionsCS + jungleCS
        csPerMin = format((totalCS / matchDuration), '.2f')
        ## Meter los datos obtenidos
        update = "UPDATE " + tableName + " SET champPlayed = " + champion + ", summonerSpells = " + spellsUsed + ", role = " + i['timeline']['lane'] + ", kills = " + str(i['stats']['kills']) + ", deaths = " + str(i['stats']['deaths']) + ", assists = " + str(i['stats']['assists']) + ", killParticipation = " + str(killPart) + ", kda = " + str(kda) + ", csTotal = " + str(totalCS) + ", csPerMin = " + str(csPerMin) + ", totalGold = " + str(i['stats']['goldEarned']) + " WHERE participantId = '" + str(i['participantId']) + "'"
        print update
        # puede ser que aca haya solucion http://stackoverflow.com/questions/28617847/sqlite-exception-no-such-column-in-android
        #c.execute(update)

        conn.commit()
