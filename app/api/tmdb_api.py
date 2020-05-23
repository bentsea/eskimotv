import requests
import random
import sys, getopt
import json
import re
import time
import os
import datetime
from dateutil.parser import *
from PIL import Image
from io import BytesIO
from resizeimage import resizeimage
from jinja2 import FileSystemLoader, Environment
from pathlib import Path
from flask import current_app




def set_globals(date=datetime.datetime.now()):
   #Base Variables
   globals()['pathPrefix']="/home/eskimotv"
   globals()['appPrefix'] ="/app/app"
   globals()['dateSuffix']  = date.strftime("/%Y/%m/")
   globals()['max_width']  = 1920

   #Compound variables
   globals()['postSuffix']  = "/_posts" + dateSuffix
   globals()['imgSuffix']  = "/static/img" + dateSuffix
   globals()['thumbsSuffix']  = "/thumbs/img" + dateSuffix
   globals()['postPath'] =pathPrefix + appPrefix + postSuffix
   globals()['imgPath'] =pathPrefix + appPrefix + imgSuffix
   globals()['thumbsPath'] =pathPrefix + appPrefix + thumbsSuffix


   #need a better way to deal with these variables.
   globals()['apiKey'] ="6cd4598528ca8c2817528493556b2d49"
   globals()['url'] ="https://api.themoviedb.org/3/"
   globals()['multiSearch']  = "search/multi"
   globals()['site_url']  = "https://www.themoviedb.org"

   # if os.path.isdir(postPath) == False:
   #    os.makedirs(postPath)
   # if os.path.isdir(imgPath) == False:
   #    os.makedirs(imgPath)
   # if os.path.isdir(thumbsPath) == False:
   #    os.makedirs(thumbsPath)

def generateSession():
   readAccessToken="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Y2Q0NTk4NTI4Y2E4YzI4MTc1Mjg0OTM1NTZiMmQ0OSIsInN1YiI6IjU5MjEwMzhmYzNhMzY4N2E2NDA1MDEwZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.A2sLjkzHDwJz5luDyRp9To_0beIxkPtIJJs_sUQCRSA"
   validate1="bentsea"
   validate2="k1Doq8NCz7HEaw3"
   payload={'api_key':apiKey}
   payload['request_token']=json.loads(requests.get(url+'authentication/token/new',params=payload).text)['request_token']
   payload['username']=validate1
   payload['password']=validate2
   requests.get(url+'authentication/token/validate_with_login',params=payload)
   return json.loads(requests.get(url+'authentication/session/new',params=payload).text)

def saveImage(imgURL,imgName):
   response = requests.get(imgURL)
   img = Image.open(BytesIO(response.content))
   new_height = int(img.height * (max_width / img.width))
   img = img.resize((max_width,new_height))
   img = resizeimage.resize_crop(img,[1920,900])
   img.save(imgPath + imgName,optimize=True,quality=60)
   img = img.resize((480,225))
   img.save(thumbsPath + imgName,optimize=True,quality=60)
   return imgSuffix + imgName

def slugify(s):
    s = s.lower()
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')
    return s

#Return a list of TMDB categories.

#Return item release date depending on item type.
def item_release_date(movie_object):
    return movie_object.get('release_date') or movie_object.get('first_air_date') or ""

#Get a list of backdrops to choose from based on a specific item.
def get_backdrops(media_type,id):
    auth={'api_key':apiKey}
    return [{'file_path':backdrop['file_path'],'height':backdrop['height'],'width':backdrop['width']} for backdrop in json.loads(requests.get("{}{}/{}/images".format(url,media_type,id), params=auth).text)['backdrops']]
media={'movie':[{'id':20,'name':'test'},{'id':22,'name':'test'}],'tv':[{'id':24,'name':'test'},{'id':26,'name':'test'}]}

#Return a tmdb genre name from an id.
def get_genre_info(id=None,name=None,language='en-US'):
    data={'api_key':apiKey,'language':language}
    media=[]
    media.append(json.loads(requests.get(url+'genre/movie/list',params=data).text).get('genres'))
    media.append(json.loads(requests.get(url+'genre/tv/list',params=data).text).get('genres'))
    data = {genre['id']:genre['name'] for genres in media for genre in genres}
    if id:
        return data[int(id)]
    else:
        return data

def find_subjects(title='', release_year=None, language='en-US', data=None, media_type=None):
    set_globals(datetime.datetime.now())
    if not data:
        data={'api_key':apiKey,'query':title,'language':language}
    results = json.loads(requests.get(url+multiSearch,params=data).text).get('results')
    no_results = [{"error":"No Results Found","backdrop_path":"https://www.eskimotv.net/img/site-resource/logo-page.jpg","overview":"No results were returned for your search. Please try again or select 'Do Not Use a Subject'."}]
    if not release_year:
        return results or no_results
    else:
        return [result for result in results if item_release_date(result).find(release_year) != -1] or no_results

def get_creative_work(tmdb_id,media_type):
    subject_info = {}
    item = {}
    #print(movie_database_search_object)

    auth={'api_key':apiKey}
    raw_info = json.loads(requests.get(url+media_type + '/' + str(tmdb_id), params=auth).text)
    credits = credits=json.loads(requests.get(url+media_type + '/' + str(tmdb_id) + '/credits',params=auth).text)
    current_app.logger.info(raw_info)

    #Use a dictionary of media types to translate between The Movie Database media type and Schema.org media type.
    media_types = {'tv':'TVSeries','movie':'Movie'}
    subject_info['media_type'] = media_type
    subject_info['type'] = media_types[media_type]
    subject_info['categories'] = [d['name'] for d in raw_info['genres']]
    subject_info['images'] = json.loads(requests.get("{}{}/{}/images".format(url,media_type,tmdb_id), params=auth).text)


    #Create the title for articles based on the type of object and whether or not there is a published year.
    title = raw_info.get('title') or raw_info.get('name')

    item['name'] = title

    item['sameAs'] = "{}/{}/{}".format(site_url,media_type,raw_info['id'])
    item['image'] = "https://image.tmdb.org/t/p/original{}".format(raw_info['poster_path'])

    director = get_crew(credits,"Director")
    if director:
        item['director'] = director

    #Use either the release date or the first air date as the datePublished
    item['datePublished'] = (raw_info.get('release_date') or raw_info.get('first_air_date'))

    #Create a title and slug based on whether or not there is a date
    subject_info['title'] = "{} ({})".format(title,item.get('datePublished').split('-')[0])
    subject_info['slug'] = slugify(subject_info['title'])
    current_app.logger.info(subject_info)
    if len(subject_info['images']['backdrops']) != 0:
        imageIndex = random.randint(0,len(subject_info['images']['backdrops'])-1)
        #subject_info['cover_image'] = ""
        #subject_info['cover_image'] = saveImage('https://image.tmdb.org/t/p/original{}'.format(subject_info['images']['backdrops'][imageIndex]['file_path']),"{}-{}-cover.jpg".format(subject_info['slug'],imageIndex))
    else:
        print("No backdrop available from The Movie Datbase, leaving cover blank.")
        subject_info['cover_image'] = ""

    subject_info['item'] = item
    return subject_info

#Iterate through crew and return the name of the crew matching the role title specified.
def get_crew(credits,role):
  return next((item for item in credits['crew'] if item["job"] == role),{}).get('name')

#Takes a movie title and release year and returns a subject_info dictionary and saves an image with a cover image from the movie.
def get_info(title='', search_release_year=None, language='en-US', data=None, media_type=None):

   if not data:
      data={'api_key':apiKey,'query':title,'language':language}

   search_data=json.loads(requests.get(url+multiSearch,params=data).text)['results']

   def return_none():
      print('No results found for subject query.')
      return None

   def get_data(movie_database_search_object):
      subject_info = {}
      item = {}
      #print(movie_database_search_object)

      auth={'api_key':apiKey}
      raw_info = json.loads(requests.get(url+movie_database_search_object['media_type'] + '/' + str(movie_database_search_object['id']), params=auth).text)
      credits = credits=json.loads(requests.get(url+movie_database_search_object['media_type'] + '/' + str(movie_database_search_object['id']) + '/credits',params=auth).text)

      #Use a dictionary of media types to translate between The Movie Database media type and Schema.org media type.
      media_types = {'tv':'TVSeries','movie':'Movie'}
      subject_info['media_type'] = movie_database_search_object['media_type']
      subject_info['type'] = media_types[movie_database_search_object['media_type']]
      subject_info['categories'] = [d['name'] for d in raw_info['genres']]
      subject_info['images'] = json.loads(requests.get("{}{}/{}/images".format(url,movie_database_search_object['media_type'],movie_database_search_object['id']), params=auth).text)


      #Create the title for articles based on the type of object and whether or not there is a published year.
      title = raw_info.get('title') or raw_info.get('name')

      item['name'] = title

      item['sameAs'] = "{}/{}/{}".format(site_url,movie_database_search_object['media_type'],raw_info['id'])
      item['image'] = "https://image.tmdb.org/t/p/original{}".format(raw_info['poster_path'])

      director = get_crew(credits,"Director")
      if director:
         item['director'] = director

      #Use either the release date or the first air date as the datePublished
      item['datePublished'] = (movie_database_search_object.get('release_date') or movie_database_search_object.get('first_air_date'))

      #Create a title and slug based on whether or not there is a date
      subject_info['title'] = "{} ({})".format(title,item.get('datePublished').split('-')[0])
      subject_info['slug'] = slugify(subject_info['title'])
      if len(subject_info['images']['backdrops']) != 0:
         imageIndex = random.randint(0,len(subject_info['images']['backdrops'])-1)
         #subject_info['cover_image'] = ""
         subject_info['cover_image'] = saveImage('https://image.tmdb.org/t/p/original{}'.format(subject_info['images']['backdrops'][imageIndex]['file_path']),"{}-{}-cover.jpg".format(subject_info['slug'],imageIndex))
      else:
         print("No backdrop available from The Movie Datbase, leaving cover blank.")
         subject_info['cover_image'] = ""

      subject_info['item'] = item
      return subject_info

   if not search_data:
      return return_none()



   if not media_type:
      if not search_release_year:
         return get_data(search_data[0])
      else:
         for i in search_data:
            if item_release_date(i).find(search_release_year) != -1:
               return get_data(i)
   else:
      for i in search_data:
         if i['media_type'].find(media_type) != -1:
            if not search_release_year:
               return get_data(i)
            elif item_release_date(i).find(search_release_year) != -1:
               return get_data(i)

   if not subject_info:
      return return_none()

#Returna the name of a file based on the path and also checks for a pre-existing file.
def filename(name):
   file = Path(postPath+name)
   if file.is_file():
      option = ""
      while(option not in ['o','g','c']):
         option = input("{} already exists. [o]verwrite,[g]enerate as parralel article, or [c]ancel? ".format(name))
      if option == 'o':
         return name
      elif option == 'g':
         file_chunks = name.split('.')
         if len(file_chunks) == 2:
            return filename("{}.{}.{}".format(file_chunks[0],"alternate",file_chunks[1]))
         elif len(file_chunks) > 2:
            extension = file_chunks.pop(-1)
            return filename("{}.{}.{}".format(".".join(file_chunks),"alternate",extension))
      else:
         print("Exiting without saving.")
         exit()
   else:
      return name

def error(err = None):
   if not err:
      print('Type "new --help" for assistance with using the new post command.')
      sys.exit(1)
   else:
      print(str(err))
      print('Type "new --help" for assistance with using the new post command.')
      sys.exit(2)

def help():
   templateLoader = FileSystemLoader("{}/scripts/templates".format(pathPrefix))
   env = Environment(loader=templateLoader)
   template = env.get_template('help')
   print(template.render())
   sys.exit(1)

def genArticle(title,userName,article_type="review",media_type="movie",subject_info=None):

   templateLoader = FileSystemLoader("{}/scripts/templates".format(pathPrefix))
   env = Environment(loader=templateLoader)
   template = env.get_template('article.markdown')
   output = template.render(title=title,author_username=userName,media_type=media_type,subjectItem=subject_info,article_type=article_type)

   fileName = filename("{}{}.markdown".format(time.strftime("%Y-%m-%d-"),slugify(title)))
   makeFile(fileName,output)

   exit()


def genReview(title,userName, release_year=""):

   movie_info = movie_info(title,release_year)

   templateLoader = FileSystemLoader("{}/scripts/templates".format(pathPrefix))
   env = Environment(loader=templateLoader)
   template = env.get_template('article.markdown')
   output = template.render(author_username=userName,subjectItem=movie_info,review=True)

   makeFile(movie_info['filename'],output)


def genEditorial(articleTitle, userName):

   templateLoader = FileSystemLoader("{}/scripts/templates".format(pathPrefix))
   env = Environment(loader=templateLoader)
   template = env.get_template('article.markdown')
   output = template.render(title=articleTitle,author_username=userName)


   fileName = filename("{}{}.markdown".format(time.strftime("%Y-%m-%d-"),slugify(articleTitle)))
   makeFile(fileName,output)

def makeFile(fileName,output):
   #Create a file using the filename and postpath arguments and populate it with the output.
   with open(postPath + fileName,"w",encoding='utf-8') as file:
      file.write(output)
   print("Success, new file created: " + fileName)

set_globals(datetime.datetime.now())

# def main(argv):
# #Get options from command line.
#    article_type="review"
#    userName="dscott"
#    release_year=None
#    subject=None
#    title=None
#    media_type=None
#    date=datetime.datetime.now()
#    try:
#       opts, args = getopt.getopt(argv,"enhm:y:t:u:s:d:",["news","help","test","subject=","title=","year=","user=","editorial=","media=","date="])
#    except getopt.GetoptError as err:
#       error(err)
#    #exit if no options are passed.
#    if len(opts) == 0:
#       error()
#    for opt, arg in opts:
#       if opt in ('-u','--user'):
#          userName = arg
#       elif opt in ("-d","--date"):
#          backdate = parse(arg)
#          answer = "awaiting input"
#          while(answer not in ['y','yes','','n','no']):
#             answer = input("Do you wish to backdate this post to {}? ([y]es|[n]o, or just hit Enter for yes.): ".format(backdate.strftime("%B %d, %Y"))).lower()
#             if answer in ['y','yes','']:
#                date = backdate
#             else:
#                print("Exiting without attempting to create post.")
#                exit()
#       elif opt in ("-t", "--title"):
#          title = arg
#       elif opt in ("-y", "--year"):
#          release_year = arg
#       elif opt in ("-e","--editorial"):
#          article_type = "editorial"
#       elif opt in ("-n","--news"):
#          article_type = "news"
#       elif opt in ("-h","--help"):
#          help()
#       elif opt in ("-m","--media"):
#          media_type = arg.lower()
#       elif opt in ("-s","--subject"):
#          subject = arg
#       else:
#          print('Boo Usage: new -t "Movie Title or article title" -u "Author Username" [ --editorial | --news | -s "Movie Title" | -y "Release year"]')
#          sys.exit(2)
#
#    set_globals(date)
#
#    if not subject:
#       if article_type == "review":
#          subject_info = get_info(title,release_year,media_type=media_type)
#          if not subject_info:
#             print('failed')
#             exit()
#          genArticle(subject_info['title'],userName,article_type=article_type,media_type=(media_type or subject_info['media_type']),subject_info=subject_info)
#       else:
#          genArticle(title,userName,article_type=article_type,media_type=media_type)
#    else:
#       subject_info = get_info(subject,release_year,media_type=media_type)
#       genArticle(title,userName,article_type=article_type,media_type=media_type,subject_info=subject_info)
