# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie!  """
)

#import streamlit as st

name_of_order = st.text_input('Name On New Smoothie:')
st.write('The Name Of Your Smoothie Will Be:', name_of_order)


#option = st.selectbox(
#    "what is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    ) 
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for friut_chosen in ingredients_list:
        ingredients_string += friut_chosen + ' '

    st.write(ingredients_string)    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                    values ('""" + ingredients_string + """','""" + name_of_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_of_order +'!',  icon="✅")
        
