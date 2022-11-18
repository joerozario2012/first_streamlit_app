import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list.set_index(['Fruit'], inplace=True)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

# New section to display fruity advice response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
if not fruit_choice:
  stramlit.error("Please select a fruit to get information")
else:
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)  
  # Normalizes the jason response
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  # Output as a table
  streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
  
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
fruit_add = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ' + fruit_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
