from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

import requests
from bs4 import BeautifulSoup as BS

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from  kivy.uix.label import Label
from kivy.core.image import Image as CoreImage

class StandApp(App):
	def window_settings(self):
		Window.size = (1280, 720)
		Window.clearcolor = (.04, .24, .65, .4)
		Window.minimum_width = 1280
		Window.minimum_height = 720

	def covid(self):
		try:
			html = requests.get(r'https://www.worldometers.info/coronavirus').content
			soup = BS(html, 'html.parser')
			hum = soup.find('div', class_='maincounter-number')
			rus = str(soup.find_all('td', string='Russia')[0].find_next('td').string)
			labelCOVID = str(hum.span.text)
			self.lb_covid_world.text = labelCOVID
			self.lb_covid_russia.text = rus
		except:
			pass

	def rate(self):
		try:
			html = requests.get(r'https://quote.rbc.ru/ticker/59111').content
			soup = BS(html, 'html.parser')
			rub = str(soup.find('span', class_='chart__info__sum').text).replace('₽', '')
			self.lb_rubble_rate.text = rub
		except:
			pass

	def weather(self):
		try:
			html = requests.get(r'https://yandex.ru/pogoda/usman').content
			soup = BS(html, 'html.parser')
			weather = str(soup.find('div', class_='link__condition day-anchor i-bem').string)
			self.lb_weather.text = weather
		except:
			pass

	def temperature(self):
		try:
			html = requests.get(r'https://yandex.ru/pogoda/usman').content
			soup = BS(html, 'html.parser')
			temp = str(soup.find('div', class_='temp fact__temp fact__temp_size_s').span.find_next('span').string)
			self.lb_temperature.text = temp
		except:
			pass

	def time(self):
		try:
			html = requests.get(r'http://www.gmt.su/time-zones/time-zone/Arabia%20Standard%20Time/').content
			soup = BS(html, 'html.parser')
			findet_time_hrs = soup.find('span', id="time_hrs")
			findet_time_min = soup.find('span', id="time_min")
			time = str(findet_time_hrs.string)+':'+str(findet_time_min.string)
			self.lb_time.text = time
		except:
			pass

	def date(self):
		try:
			html = requests.get(r'https://voshod-solnca.ru/time/москва').content
			soup = BS(html, 'html.parser')
			date = str(soup.find('li', class_="footer_cur_date").string)
			week_day = str(soup.find('li', class_="first_letter_uppercase footer_weekday").string).title()	
			self.lb_date.text = date
			self.lb_week_day.text = week_day
		except:
			pass

	def build(self):
		gl = GridLayout(cols=3,rows=2, padding=[40, 25], spacing=[15])
		self.window_settings()

		covid_label_1 = Label(text='Заражённые CoVid-19', size_hint=(1, .25), text_size=(389, 81.875),
			valign='bottom', halign='center', font_size=30)
		self.lb_covid_world = Label(text='', size_hint=(1, .25), text_size=(389, 81.875),
			valign='top', halign='center', font_size=65, bold = True)
		covid_label_2 = Label(text='Заражённые в России', size_hint=(1, .25), text_size=(389, 81.875),
			valign='bottom', halign='center', font_size=25)
		self.lb_covid_russia = Label(text='', size_hint=(1, .25), text_size=(389, 81.875),
			valign='top', halign='center', font_size=55, bold = True)
		box1 = BoxLayout(orientation='vertical')
		self.covid()
		box1.add_widget(covid_label_1)
		box1.add_widget(self.lb_covid_world)
		box1.add_widget(covid_label_2)
		box1.add_widget(self.lb_covid_russia)
		gl.add_widget(box1) # Число заболевших CoVid-19

		rubble_label = Label(text='Курс рубля', size_hint=(1, .5), text_size=(389, 163.75),
			halign='center', valign='center', font_size=35)
		self.lb_rubble_rate = Label(text='', size_hint=(1, .5), text_size=(389, 163.75),
			halign='center', valign='top', font_size=60, bold = True)
		box2 = BoxLayout(orientation='vertical')
		self.rate()
		box2.add_widget(rubble_label)
		box2.add_widget(self.lb_rubble_rate)
		gl.add_widget(box2) # Курс доллара к рублю

		
		self.lb_date = Label(text='', valign='bottom', 
			size_hint=(1, .5), text_size=(389, 163.75), halign='center', font_size=35, bold=True)
		self.lb_week_day = Label(text='', valign='top', 
			size_hint=(1, .5), text_size=(389, 163.75), halign='center', font_size=35, bold=True)
		box3 = BoxLayout(orientation='vertical')
		self.date()
		box3.add_widget(self.lb_date)
		box3.add_widget(self.lb_week_day)
		gl.add_widget(box3) # Дата НЕМЕНЯЕТСЯ

		self.lb_weather = Label(text='', font_size=45, bold = True)
		self.weather()
		box4 = BoxLayout(orientation='vertical')
		box4.add_widget(self.lb_weather)
		gl.add_widget(box4) # Погода НЕМЕНЯЕТСЯ

		temp_label = Label(text='Температура', size_hint=(1, .4), text_size=(389, 131),
			halign='center', valign='center', font_size=35)
		self.lb_temperature = Label(text='', size_hint=(1, .6), text_size=(389, 196.5),
			halign='center', valign='top', font_size=65, bold = True)
		box5 = BoxLayout(orientation='vertical')
		self.temperature()
		box5.add_widget(temp_label)
		box5.add_widget(self.lb_temperature)
		gl.add_widget(box5) # Температура в городе

		
		self.lb_time = Label(text='', font_size=70, bold = True)
		box6 = BoxLayout(orientation='vertical')
		self.time()
		box6.add_widget(self.lb_time)
		gl.add_widget(box6) # Время по МСК (UTC +3)

		try:
			self.covid()
		except:
			pass

		try:
			self.rate()
		except:
			pass

		try:
			self.temperature()
		except:
			pass

		try:
			self.weather()
		except:
			pass

		try:
			self.date()
		except:
			pass

		try:
			self.time()
		except:
			pass

		Clock.schedule_interval(lambda dt: self.time(), 1)
		Clock.schedule_interval(lambda dt: self.covid(), 1200)
		Clock.schedule_interval(lambda dt: self.rate(), 2400)
		Clock.schedule_interval(lambda dt: self.temperature(), 600)
		Clock.schedule_interval(lambda dt: self.weather(), 300)
		Clock.schedule_interval(lambda dt: self.date(), 60)

		return gl

if __name__ == '__main__':
    StandApp().run()
