 # Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_session = get_active_session()
from snowflake.snowpark.functions import col
import requests

st.title(f":cup_with_straw: Customize your Smooothie :cup_with_straw: ")
st.write("""Choose the fruits you want in your smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    ,my_dataframe
    ,max_selections=5
)

name_on_order = st.text_input("Name on the Smoothie:", "")
st.write("The name on your Smoothie will be:", name_on_order)

if ingredients_list: # if ingredients_list is not null: then do everything below this line that is indented. 
    st.write("You selected:", ingredients_list) # Numbered, vertical
    ingredients_string =''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(smoothiefroot_response.json(),use_container_width=True)

    my_insert_stmt = """use warehouse COMPUTE_WH;  insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()        
        st.success((name_on_order, ' your Smoothie is ordered!'), icon="✅")




