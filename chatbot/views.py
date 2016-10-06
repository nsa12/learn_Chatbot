#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import re

import random
import pprint
# Create your views here.

VERIFY_TOKEN = 'ChuckyJokes'
PAGE_ACCESS_TOKEN = 'EAAZAI1H5VMtkBAMrgf8r0QCUR7t5ZBy4f3wuZATZCF5S80nZBS4s7UJECnfZBks9STzjooX1WM8Syq0TgYbXRjhTFoqRV2xWUy3HWgtQszSVttLSQMle3Ck8oSVTlIbCBituCh4QDWqj6UHF1EpvrZCKAbUrJlsOLdCV9zBMrpZC9wZDZD'

pokemon_data = {"Bulbasaur":"http://img.pokemondb.net/artwork/bulbasaur.jpg","Ivysaur":"http://img.pokemondb.net/artwork/ivysaur.jpg","Venusaur":"http://img.pokemondb.net/artwork/venusaur.jpg","Charmander":"http://img.pokemondb.net/artwork/charmander.jpg","Charmeleon":"http://img.pokemondb.net/artwork/charmeleon.jpg","Charizard":"http://img.pokemondb.net/artwork/charizard.jpg","Squirtle":"http://img.pokemondb.net/artwork/squirtle.jpg","Wartortle":"http://img.pokemondb.net/artwork/wartortle.jpg","Blastoise":"http://img.pokemondb.net/artwork/blastoise.jpg","Caterpie":"http://img.pokemondb.net/artwork/caterpie.jpg","Metapod":"http://img.pokemondb.net/artwork/metapod.jpg","Butterfree":"http://img.pokemondb.net/artwork/butterfree.jpg","Weedle":"http://img.pokemondb.net/artwork/weedle.jpg","Kakuna":"http://img.pokemondb.net/artwork/kakuna.jpg","Beedrill":"http://img.pokemondb.net/artwork/beedrill.jpg","Pidgey":"http://img.pokemondb.net/artwork/pidgey.jpg","Pidgeotto":"http://img.pokemondb.net/artwork/pidgeotto.jpg","Pidgeot":"http://img.pokemondb.net/artwork/pidgeot.jpg","Rattata":"http://img.pokemondb.net/artwork/rattata.jpg","Raticate":"http://img.pokemondb.net/artwork/raticate.jpg","Spearow":"http://img.pokemondb.net/artwork/spearow.jpg","Fearow":"http://img.pokemondb.net/artwork/fearow.jpg","Ekans":"http://img.pokemondb.net/artwork/ekans.jpg","Arbok":"http://img.pokemondb.net/artwork/arbok.jpg","Pikachu":"http://img.pokemondb.net/artwork/pikachu.jpg","Raichu":"http://img.pokemondb.net/artwork/raichu.jpg","Sandshrew":"http://img.pokemondb.net/artwork/sandshrew.jpg","Sandslash":"http://img.pokemondb.net/artwork/sandslash.jpg","Nidoran?":"http://img.pokemondb.net/artwork/nidoran?.jpg","Nidorina":"http://img.pokemondb.net/artwork/nidorina.jpg","Nidoqueen":"http://img.pokemondb.net/artwork/nidoqueen.jpg","Nidorino":"http://img.pokemondb.net/artwork/nidorino.jpg","Nidoking":"http://img.pokemondb.net/artwork/nidoking.jpg","Clefairy":"http://img.pokemondb.net/artwork/clefairy.jpg","Clefable":"http://img.pokemondb.net/artwork/clefable.jpg","Vulpix":"http://img.pokemondb.net/artwork/vulpix.jpg","Ninetales":"http://img.pokemondb.net/artwork/ninetales.jpg","Jigglypuff":"http://img.pokemondb.net/artwork/jigglypuff.jpg","Wigglytuff":"http://img.pokemondb.net/artwork/wigglytuff.jpg","Zubat":"http://img.pokemondb.net/artwork/zubat.jpg","Golbat":"http://img.pokemondb.net/artwork/golbat.jpg","Oddish":"http://img.pokemondb.net/artwork/oddish.jpg","Gloom":"http://img.pokemondb.net/artwork/gloom.jpg","Vileplume":"http://img.pokemondb.net/artwork/vileplume.jpg","Paras":"http://img.pokemondb.net/artwork/paras.jpg","Parasect":"http://img.pokemondb.net/artwork/parasect.jpg","Venonat":"http://img.pokemondb.net/artwork/venonat.jpg","Venomoth":"http://img.pokemondb.net/artwork/venomoth.jpg","Diglett":"http://img.pokemondb.net/artwork/diglett.jpg","Dugtrio":"http://img.pokemondb.net/artwork/dugtrio.jpg","Meowth":"http://img.pokemondb.net/artwork/meowth.jpg","Persian":"http://img.pokemondb.net/artwork/persian.jpg","Psyduck":"http://img.pokemondb.net/artwork/psyduck.jpg","Golduck":"http://img.pokemondb.net/artwork/golduck.jpg","Mankey":"http://img.pokemondb.net/artwork/mankey.jpg","Primeape":"http://img.pokemondb.net/artwork/primeape.jpg","Growlithe":"http://img.pokemondb.net/artwork/growlithe.jpg","Arcanine":"http://img.pokemondb.net/artwork/arcanine.jpg","Poliwag":"http://img.pokemondb.net/artwork/poliwag.jpg","Poliwhirl":"http://img.pokemondb.net/artwork/poliwhirl.jpg","Poliwrath":"http://img.pokemondb.net/artwork/poliwrath.jpg","Abra":"http://img.pokemondb.net/artwork/abra.jpg","Kadabra":"http://img.pokemondb.net/artwork/kadabra.jpg","Alakazam":"http://img.pokemondb.net/artwork/alakazam.jpg","Machop":"http://img.pokemondb.net/artwork/machop.jpg","Machoke":"http://img.pokemondb.net/artwork/machoke.jpg","Machamp":"http://img.pokemondb.net/artwork/machamp.jpg","Bellsprout":"http://img.pokemondb.net/artwork/bellsprout.jpg","Weepinbell":"http://img.pokemondb.net/artwork/weepinbell.jpg","Victreebel":"http://img.pokemondb.net/artwork/victreebel.jpg","Tentacool":"http://img.pokemondb.net/artwork/tentacool.jpg","Tentacruel":"http://img.pokemondb.net/artwork/tentacruel.jpg","Geodude":"http://img.pokemondb.net/artwork/geodude.jpg","Graveler":"http://img.pokemondb.net/artwork/graveler.jpg","Golem":"http://img.pokemondb.net/artwork/golem.jpg","Ponyta":"http://img.pokemondb.net/artwork/ponyta.jpg","Rapidash":"http://img.pokemondb.net/artwork/rapidash.jpg","Slowpoke":"http://img.pokemondb.net/artwork/slowpoke.jpg","Slowbro":"http://img.pokemondb.net/artwork/slowbro.jpg","Magnemite":"http://img.pokemondb.net/artwork/magnemite.jpg","Magneton":"http://img.pokemondb.net/artwork/magneton.jpg","Farfetch'd":"http://img.pokemondb.net/artwork/farfetch'd.jpg","Doduo":"http://img.pokemondb.net/artwork/doduo.jpg","Dodrio":"http://img.pokemondb.net/artwork/dodrio.jpg","Seel":"http://img.pokemondb.net/artwork/seel.jpg","Dewgong":"http://img.pokemondb.net/artwork/dewgong.jpg","Grimer":"http://img.pokemondb.net/artwork/grimer.jpg","Muk":"http://img.pokemondb.net/artwork/muk.jpg","Shellder":"http://img.pokemondb.net/artwork/shellder.jpg","Cloyster":"http://img.pokemondb.net/artwork/cloyster.jpg","Gastly":"http://img.pokemondb.net/artwork/gastly.jpg","Haunter":"http://img.pokemondb.net/artwork/haunter.jpg","Gengar":"http://img.pokemondb.net/artwork/gengar.jpg","Onix":"http://img.pokemondb.net/artwork/onix.jpg","Drowzee":"http://img.pokemondb.net/artwork/drowzee.jpg","Hypno":"http://img.pokemondb.net/artwork/hypno.jpg","Krabby":"http://img.pokemondb.net/artwork/krabby.jpg","Kingler":"http://img.pokemondb.net/artwork/kingler.jpg","Voltorb":"http://img.pokemondb.net/artwork/voltorb.jpg","Electrode":"http://img.pokemondb.net/artwork/electrode.jpg","Exeggcute":"http://img.pokemondb.net/artwork/exeggcute.jpg","Exeggutor":"http://img.pokemondb.net/artwork/exeggutor.jpg","Cubone":"http://img.pokemondb.net/artwork/cubone.jpg","Marowak":"http://img.pokemondb.net/artwork/marowak.jpg","Hitmonlee":"http://img.pokemondb.net/artwork/hitmonlee.jpg","Hitmonchan":"http://img.pokemondb.net/artwork/hitmonchan.jpg","Lickitung":"http://img.pokemondb.net/artwork/lickitung.jpg","Koffing":"http://img.pokemondb.net/artwork/koffing.jpg","Weezing":"http://img.pokemondb.net/artwork/weezing.jpg","Rhyhorn":"http://img.pokemondb.net/artwork/rhyhorn.jpg","Rhydon":"http://img.pokemondb.net/artwork/rhydon.jpg","Chansey":"http://img.pokemondb.net/artwork/chansey.jpg","Tangela":"http://img.pokemondb.net/artwork/tangela.jpg","Kangaskhan":"http://img.pokemondb.net/artwork/kangaskhan.jpg","Horsea":"http://img.pokemondb.net/artwork/horsea.jpg","Seadra":"http://img.pokemondb.net/artwork/seadra.jpg","Goldeen":"http://img.pokemondb.net/artwork/goldeen.jpg","Seaking":"http://img.pokemondb.net/artwork/seaking.jpg","Staryu":"http://img.pokemondb.net/artwork/staryu.jpg","Starmie":"http://img.pokemondb.net/artwork/starmie.jpg","Mr. Mime":"http://img.pokemondb.net/artwork/mr. mime.jpg","Scyther":"http://img.pokemondb.net/artwork/scyther.jpg","Jynx":"http://img.pokemondb.net/artwork/jynx.jpg","Electabuzz":"http://img.pokemondb.net/artwork/electabuzz.jpg","Magmar":"http://img.pokemondb.net/artwork/magmar.jpg","Pinsir":"http://img.pokemondb.net/artwork/pinsir.jpg","Tauros":"http://img.pokemondb.net/artwork/tauros.jpg","Magikarp":"http://img.pokemondb.net/artwork/magikarp.jpg","Gyarados":"http://img.pokemondb.net/artwork/gyarados.jpg","Lapras":"http://img.pokemondb.net/artwork/lapras.jpg","Ditto":"http://img.pokemondb.net/artwork/ditto.jpg","Eevee":"http://img.pokemondb.net/artwork/eevee.jpg","Vaporeon":"http://img.pokemondb.net/artwork/vaporeon.jpg","Jolteon":"http://img.pokemondb.net/artwork/jolteon.jpg","Flareon":"http://img.pokemondb.net/artwork/flareon.jpg","Porygon":"http://img.pokemondb.net/artwork/porygon.jpg","Omanyte":"http://img.pokemondb.net/artwork/omanyte.jpg","Omastar":"http://img.pokemondb.net/artwork/omastar.jpg","Kabuto":"http://img.pokemondb.net/artwork/kabuto.jpg","Kabutops":"http://img.pokemondb.net/artwork/kabutops.jpg","Aerodactyl":"http://img.pokemondb.net/artwork/aerodactyl.jpg","Snorlax":"http://img.pokemondb.net/artwork/snorlax.jpg","Articuno":"http://img.pokemondb.net/artwork/articuno.jpg","Zapdos":"http://img.pokemondb.net/artwork/zapdos.jpg","Moltres":"http://img.pokemondb.net/artwork/moltres.jpg","Dratini":"http://img.pokemondb.net/artwork/dratini.jpg","Dragonair":"http://img.pokemondb.net/artwork/dragonair.jpg","Dragonite":"http://img.pokemondb.net/artwork/dragonite.jpg","Mewtwo":"http://img.pokemondb.net/artwork/mewtwo.jpg","Mew":"http://img.pokemondb.net/artwork/mew.jpg"}

def quizGen():
	pokemon_arr = []
	for key,value in pokemon_data.iteritems():
		pokemon_arr.append([key,value])

	random.shuffle(pokemon_arr)
	answer = pokemon_arr[0]
	options = [i[0] for i in pokemon_arr[:4]]
	random.shuffle(options)
	return dict(answer=answer, options=options)

def index(request):
	output_text = quizGen()
	output_text = pprint.pformat(output_text)
#	print output_text
	return HttpResponse(output_text, content_type='application/json')

def chuck():
	url = 'https://api.chucknorris.io/jokes/random'
	resp = requests.get(url=url).text
	data = json.loads(resp)
	return data['value'], data['url'], data['icon_url']

def wikisearch(title='tomato'):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=%s'%(title)
    resp = requests.get(url=url).text
    data = json.loads(resp)
    scoped_data = data['query']['pages']
    print scoped_data
    page_id = data['query']['pages'].keys()[0]
    wiki_url = 'https://en.m.wikipedia.org/?curid=%s'%(page_id)
    try:
        wiki_content = scoped_data[page_id]['extract']
        wiki_content = re.sub(r'[^\x00-\x7F]+',' ', wiki_content)
        wiki_content = re.sub(r'\([^)]*\)', '', wiki_content)
        
        if len(wiki_content) > 315:
            wiki_content = wiki_content[:315] + ' ...'
    except KeyError:
        wiki_content = ''

    return wiki_content

def post_facebook_message(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	
	output_text, output_url, output_image = chuck()
	output_text = output_text.replace('Chuck Norris', 'Rajnikant')

	quiz = quizGen()

	response_msg_with_button = {
	  	"recipient":{
	    	"id":fbid
	  	},
	  	"message":{
	    	"attachment":{
	    	  	"type":"template",
	    	  	"payload":{
		        	"template_type":"button",
	        		"text":output_text,
	        		"buttons":[
		          		{
		            		"type":"web_url",
		            		"url":output_url
		            		,
		            		"title":"Show Website"
		          		},
		          		{
		            		"type":"postback",
		            		"title":"Start Chatting",
		            		"payload":"USER_DEFINED_PAYLOAD"
		          		}
	       			]
	    		}
	    	}
	  	}
	}

	response_msg_generic = {
		"recipient":{
		    "id":fbid
		  },
		 "message":{
		 	"attachment":{
		    	"type":"template",
		      	"payload":{
		        	"template_type":"generic",
		        	"elements":[
		          	{
			            "title":output_text,
		            	"item_url":"https://api.chucknorris.io/jokes/random",
		            	"image_url": 'https://thecatapi.com/api/images/get?format=src&type=png',
		            	"subtitle":"Lolsters =D",
		            	"buttons":[
		              	{
			                "type":"web_url",
		                	"url": output_url,
		                	"title":"View Website"
		              	},
		              	{
		                	"type":"postback",
		                	"title":"Another Joke",
		                	"payload":"RANDOM_JOKE"
		              	}              
		            	]
		          	}
		        	]
		      	}
		    }
		  }
	}

	response_msg_quickreply = {
		"recipient":{
		    "id":fbid
		  },
		"message":{
			"text":"Which pokemon is this?",
		    "quick_replies":[
		    {
		    	"content_type":"text",
		        "title":quiz['options'][0],
		        "payload":"%s:%s"%(quiz['answer'][0], quiz['options'][0])
		    },
		    {
			    "content_type":"text",
		    	"title":quiz['options'][1],
		    	"payload":"%s:%s"%(quiz['answer'][0], quiz['options'][1])
		    }
		    {
			    "content_type":"text",
		    	"title":quiz['options'][2]
		    	"payload":"%s:%s"%(quiz['answer'][0], quiz['options'][2])
		    }
		    {
			    "content_type":"text",
		    	"title":quiz['options'][3]
		    	"payload":"%s:%s"%(quiz['answer'][0], quiz['options'][3])
		    }
		    ]
		}
	}

	response_msg_image = {
		"recipient":{
			"id":fbid
		},
		"message":{
			"attachment":{
		    	"type":"image",
		    	"payload":{
		        	"url":quizGen['answer'][1]
		      	}
		    }
		}
	}

	response_msg_with_button = json.dumps(response_msg_with_button)
	response_msg_generic = json.dumps(response_msg_generic)
	response_msg_quickreply = json.dumps(response_msg_quickreply)
	response_msg_image = json.dumps(response_msg_image)

	#response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	#status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

	#status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg_with_button)

	status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg_image)
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg_quickreply)
	print status.json()

def handle_postback(fbid, payload):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	output_text = 'Payload Received: ' + payload
	logg(payload, symbol='*')

	if payload == 'RANDOM_JOKE':
		post_facebook_message(fbid, 'foo')

def handle_quickreply(fbid, payload):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	logg(payload, symbol='--QR--')
	return

def logg(message, symbol='-'):
	print "%s\n%s\n%s"%(symbol*10, message, symbol*10)

class MyChatBotView(generic.View):
	def get (self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		logg(incoming_message)

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				
				try:
					if 'postback' in message:
						handle_postback(message['sender']['id'], message['postback']['payload'])
					else:
						pass
				except Exception as e:
					logg(e,symbol('--140--'))
				
				try:
					if 'quick_reply' in message['message']:
						handle_quickreply(message['sender']['id'], message['message']['quick_reply']['payload'])
					else:
						pass
				except Exception as e:
					logg(e,symbol('--143--'))
				
				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_facebook_message(sender_id,message_text)
				except Exception as e:
					logg(e, symbol='--147--')
					pass

		return HttpResponse()