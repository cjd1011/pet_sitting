import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

#display title and description
st.header("Whiskers & Wagging Tails: Juliana's Expert Petsitting Services in *Melbourne*", divider='rainbow')
st.image("chester_juli.jpg", )

st.markdown("At Whiskers & Wagging Tails, we believe that every tail wag and gentle purr deserves the utmost care and attention. I'm Juliana, your dedicated pet sitter, and I've transformed my passion for animals into a commitment to providing top-notch care for your beloved cats and dogs.")

#Establishing a google sheet connection 
#conn = st.experimental_connection("gsheets",type=GSheetsConnection)
conn = st._connection("gsheets",type=GSheetsConnection)
#Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(9)),ttl=5)
#existing_data = conn.read(worksheet="Entry-form", sheet_name= "Vendors", usecols=list(range(6)),ttl=5)
existing_data = existing_data.dropna(how="all")

#List of business types and products

PET_TYPES = [
    "Dog",
    "Cat",
    "Other: Please, specify below in Additional info section",
    
]
SERVICES = [
    "Dog Walking ($25 AUD): For just 25 AUD, treat your furry friend to a 30-minute adventure with our personalized dog walking service. We'll fetch your dog right from your doorstep, ensuring they get the exercise and attention they need. Because every wag deserves a walk to remember!",
    "One home visit a day ($20 AUD): Schedule a personalized home visit with me. We'll drop by once a day to ensure your pet is well-fed, happy, and receives some extra playtime.",
    "Two home visits a day ($50 AUD): Double the joy for your pet! Your furry friend gets not one, but two personalized drop-in visits. We'll make sure your pet is well-fed, entertained, and feeling the love—twice a day! ",

]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    Pet_name = st.text_input(label="Pet Name*")
    Pet_type = st.selectbox("Pet Type*", options=PET_TYPES, index=None)
    services = st.multiselect("Services Offered", options=SERVICES)
    quantity_days = st.slider("Quantity of Days", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    address = st.text_input(label="Address*")
    suburb = st.text_input(label="Suburb*")
    phone_number = st.text_input(label="Phone Number*")
    additional_info = st.text_area(label="Additional Notes: Please, specify pet breed, weight or if is other kind of small animal (Bird, rabbit, ferret, etc)")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not Pet_name or not Pet_type:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        #elif existing_data["Pet Name"].str.contains(Pet_name).any():
        #    st.warning("A vendor with this company name already exists.")
        #    st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "Pet Name": Pet_name,
                        "Pet Type": Pet_type,
                        "Services": ", ".join(services),
                        "Quantity Days": quantity_days,
                        "Onboarding Date": onboarding_date.strftime("%Y-%m-%d"),
                        "Address": address,
                        "Suburb": suburb,
                        "Phone Number": phone_number,
                        "Additional Info": additional_info,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Vendors", data=updated_df)

            st.success("Vendor details successfully submitted!")  