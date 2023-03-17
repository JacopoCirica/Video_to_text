from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup
import requests
from youtube_transcript_api import YouTubeTranscriptApi





app = Flask(__name__)

class NameForm(FlaskForm):
    name = StringField('Insert youtube link to get transcript:', validators=[DataRequired()])
    submit = SubmitField('Submit')


app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/', methods=['GET', 'POST'])
def index():
    id_url = None
    name = None
    title= None
    keywords= None
    transcript=None
    description= None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        id_url=name.split('=')
        id_url=id_url[1]
        #scrape youtube video
        r = requests.get(name)
        s = BeautifulSoup(r.text, "html.parser")
        title_scrape = [] 
        title_scrape.extend(
            (i.prettify() for i in s.find_all('meta', {"name" : "title"}))
            )
        title=[]
        
        
        for x in title_scrape: 
            z=x.replace('<meta content=\"', "")
            z=z.replace('\" name=\"title"/>\n',"")
            title.append(z)
        
        title=title[0]
        print(title)
        #extract description
        description_scrape = [] 

        description_scrape.extend(
            (i.prettify() for i in s.find_all('meta', {"name" : "description"}))
            )
        description=[]
        for x in description_scrape: 
            z=x.replace('<meta content=\"', "")
            z=z.replace('\" name=\"description"/>\n',"")
            description.append(z)
        description=description[0]
        print(description)
        #extract keywords
        keywords_scrape = [] 

        keywords_scrape.extend(
            (i.prettify() for i in s.find_all('meta', {"name" : "keywords"}))
        )
        keywords=[]
        for x in keywords_scrape: 
            z=x.replace('<meta content=\"', "")
            z=z.replace('\" name=\"keywords"/>\n',"")
            keywords.append(z)
        print(keywords)
        #extract transcript
        transcript=[]
        x=YouTubeTranscriptApi.get_transcript(id_url)
        i=0
        transcript1=''
        while i <len(x):
            transcript1=transcript1+ ' ' + x[i]['text']
            i=i+1
            transcript.append(transcript1)
        print(transcript)
    return render_template('index.html', form=form, name=name, id_url=id_url,title=title, description=description,keywords=keywords,transcript=transcript)
    
    