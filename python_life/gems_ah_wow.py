#-*- encoding: utf-8 -*-
from urllib2 import urlopen
import json
import time
import sys

DEBUG = 0
GOD_GEMS = [
    76692,
    76693,
    76694,
    76695,
    76696,
    76636,
    76637,
    76638,
    76639,
    76697,
    76698,
    76699,
    76700,
    76701,
    76680,
    76681,
    76682,
    76683,
    76684,
    76685,
    76686,
    76687,
    76688,
    76689,
    76690,
    76691,
    89674,
    89680,
    76640,
    76641,
    76642,
    76643,
    76644,
    76645,
    76646,
    76647,
    76648,
    76649,
    76650,
    76651,
    76652,
    76653,
    76654,
    76655,
    76656,
    76657,
    93705,
    76658,
    76659,
    76660,
    76661,
    76662,
    76663,
    76664,
    76665,
    76666,
    76667,
    76668,
    76669,
    76670,
    76671,
    76672,
    76673,
    76674,
    76675,
    76676,
    76677,
    76678,
    76679,
    76879,
    76884,
    76885,
    76886,
    76887,
    76888,
    76890,
    76891,
    76892,
    76893,
    76894,
    76895,
    76896,
    76897,
    76629,
    76614,
    76570,
    76571,
    76572,
    76573,
    76631,
    76632,
    76633,
    76634,
    76635,
    76628,
    76615,
    76616,
    76617,
    76618,
    76619,
    76620,
    76621,
    76622,
    76623,
    76624,
    76625,
    89676,
    76574,
    76575,
    76576,
    76577,
    76578,
    76579,
    76580,
    76581,
    76582,
    76583,
    76584,
    76585,
    76586,
    76587,
    76588,
    76589,
    76590,
    76591,
    93707,
    76592,
    76593,
    76594,
    76595,
    76596,
    76597,
    76598,
    76599,
    76600,
    76601,
    76602,
    76603,
    76604,
    76605,
    76606,
    76607,
    76608,
    76609,
    76610,
    76611,
    76612,
    76613,
    76626,
    76627,
    76630,
    89679 
]


def get_jsonfile(server='nemesis'):
    try:
        url = 'http://us.battle.net/api/wow/auction/data/' + server
        url = urlopen(url).read()
        url = json.loads(url.decode('utf-8'))

        url_arquivo = str(url['files'][0]['url'])
        modificado = str(url['files'][0]['lastModified'])

        modificado = float(modificado[:-3] + "." + modificado[-3:])

        if DEBUG:
            print("Arquivo de dados da AH: %s" % url_arquivo)
            print("Ultima modificacao: %s" % modificado)
            print(time.localtime(modificado))

        return url_arquivo
    except Exception as e:
        print("Erro %s" % e)
        sys.exit(1)


def get_ah_data(url=""):
    try:
        url = urlopen(url).read()

        f = open("ah.txt", "w")
        f.write(url)
        f.close()

        url = json.loads(url.decode('utf-8'))
        auctions = url["auctions"]

        return auctions
    except Exception as e:
        print("Erro %s" % e)
        sys.exit(1)


def get_item(item):
    try:
        # http://us.battle.net/wow/pt/item/76666
        url = 'http://us.battle.net/api/wow/item/' + str(item)
        url = urlopen(url).read()
        url = json.loads(url.decode('utf-8'))

        name = str(url[u'name'])
        itemLevel = str(url[u'itemLevel'])
        itemClass = int(url[u'itemClass'])
        sellPrice = int(url[u'sellPrice'])

        msg = {
            "name": name,
            "url": "http://us.battle.net/wow/pt/item/" + str(item),
            "ilvl": itemLevel,
            "itemClass": str(itemClass),
            "sellPrice": sellPrice
        }

        return msg
    except Exception as e:
        print("Erro %s" % e)
        sys.exit(1)

azralon = get_jsonfile(server='azralon')
auctions = get_ah_data(url=str(azralon))
gems_found = []

for auction in auctions[u'auctions']:
    timeLeft = unicode(auction[u'timeLeft'])
    bid = int(auction[u'bid'])
    item = int(auction[u'item'])
    seed = int(auction[u'seed'])
    owner = unicode(auction[u'owner'])
    buyout = int(auction[u'buyout'])
    quantity = int(auction[u'quantity'])

    if item in GOD_GEMS:
        gems_found.append(item)

list_subtraction = list(set(GOD_GEMS) - set(gems_found))

print("Gemas faltantes na AH: ")
print("~-"*50)
for item in list_subtraction:
    dict_item = get_item(item)
    print("Nome do item: " + dict_item['name'])
    print("URL: " + dict_item['url'])
    print("Preco de venda em cobre: " + str(dict_item['sellPrice']))
    print("~-"*50)
