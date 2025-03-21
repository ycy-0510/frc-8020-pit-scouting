import streamlit as st
import pandas as pd  # type: ignore
import os

st.set_page_config(page_title="FRC#8020 Pit Scouting", layout="centered")

st.title("FRC#8020 Pit Scouting")

# Tabs for Form and Data
tab1, tab2, tab3 = st.tabs(["📝 Form", "📊 View Data", "📊 Edit data"])

# --- Tab 1: Form ---
with tab1:
    st.subheader("Submit Your Information")

    with st.form("user_form"):
        teamnumber = st.text_input("Team Number", placeholder="Enter Team Number")
        drivetrain = st.selectbox("Drivetrain", ["Swerve", "Mecanum", "Omni", "Tank"])
        # a select with other that can input text
        coralfrom = st.multiselect("Coral From", ["Floor", "CS", "Needs lining Up"])
        # row layout
        ccol1, ccol2, ccol3, ccol4 = st.columns(4)
        with ccol1:
            coralL1 = st.checkbox("Coral L1")
        with ccol2:
            coralL2 = st.checkbox("Coral L2")
        with ccol3:
            coralL3 = st.checkbox("Coral L3")
        with ccol4:
            coralL4 = st.checkbox("Coral L4")
        # algea
        preferred_coral = st.multiselect(
            "Preferred Coral",
            ["L1", "L2", "L3", "L4"],
            help="Select the preferred coral levels",
        )
        algae = st.multiselect("Algae", ["Remove", "Net", "Processor"])
        cage = st.selectbox("Cage", ["Deep", "Shallow", "Park", "None"])
        # multi select
        hp = st.selectbox("Human Player", ["CS", "Processor", "Must CS", "Both"])
        image1 = st.file_uploader("Upload Image 1", type=["jpg", "png", "jpeg"])
        image2 = st.file_uploader("Upload Image 2", type=["jpg", "png", "jpeg"])
        btn1, btn2 = st.columns(2)
        with btn1:
            submitted = st.form_submit_button("Submit")
        with btn2:
            reset = st.form_submit_button("Reset")
    if submitted:
        if teamnumber and drivetrain and cage and hp:
            # header: Team Number,Drive Train,Coral From,Coral L1,Coral L2,Coral L3,Coral L4,Algae,Cage,Hp
            # Save to CSV
            data = {
                "Teamnumber": teamnumber,
                "Drivetrain": drivetrain,
                "Coral From": coralfrom,
                "Coral L1": coralL1,
                "Coral L2": coralL2,
                "Coral L3": coralL3,
                "Coral L4": coralL4,
                "Preferred Coral": preferred_coral,
                "Algae": algae,
                "Cage": cage,
                "Human Player": hp,
            }
            df = pd.DataFrame([data])

            # Append or create CSV
            if os.path.exists("data.csv"):
                df.to_csv("data.csv", mode="a", header=False, index=False)
            else:
                df.to_csv("data.csv", index=False)
            # Save images
            # if folder does not exist, create it
            if not os.path.exists(f"images/{teamnumber}"):
                os.makedirs(f"images/{teamnumber}")
            if image1:
                with open(f"images/{teamnumber}/1.jpg", "wb") as f:
                    f.write(image1.read())
            if image2:
                with open(f"images/{teamnumber}/2.jpg", "wb") as f:
                    f.write(image2.read())
            # check teamnumber in data
            if os.path.exists("data.csv"):
                st.success("✅ Form submitted successfully!")
                # reset form after submission

        else:
            st.error("⚠️ Please fill out all fields.")

# --- Tab 2: View Data ---
with tab2:
    st.subheader("Submitted Data with Images")

    # Display stored data
    if os.path.exists("data.csv") and os.stat("data.csv").st_size > 0:
        all_data = pd.read_csv("data.csv")
        # Set index to teamnumber
        all_data.set_index("Team Number", inplace=True)
        refresh1 = st.button("Refresh Data",key="refresh1")
        if refresh1:
            st.rerun()
        st.dataframe(all_data)

        # Select team number to view images
        opt = all_data.index
        #sort the team numbers
        opt_sorted = sorted(opt)
        selected_team = st.selectbox(
            "Select Team Number to View Images", opt_sorted
        )

        if selected_team:
            #show data
            st.write(all_data.loc[selected_team])
            image1_path = f"images/{selected_team}/1.jpg"
            image2_path = f"images/{selected_team}/2.jpg"

            if os.path.exists(image1_path):
                st.image(image1_path, caption="Image 1", use_container_width=True)
            else:
                st.warning("Images1 not found for the selected team.")
            if os.path.exists(image2_path):
                st.image(image2_path, caption="Image 2", use_container_width=True)
            else:
                st.warning("Images2 not found for the selected team.")
    else:
        st.info("No data submitted yet.")

with tab3:
    st.subheader("Edit Data")
    if os.path.exists("data.csv") and os.stat("data.csv").st_size > 0:
        all_data = pd.read_csv("data.csv")
        refresh2 = st.button("Refresh Data", key="refresh2")
        if refresh2:
            st.rerun()
        edited_df = st.data_editor(all_data, num_rows="dynamic")
        if st.button("Save Changes"):
            edited_df.to_csv("data.csv", index=False)

            st.success("✅ Data saved successfully!")
    else:
        st.info("No data submitted yet.")
