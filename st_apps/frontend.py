import streamlit as st
import requests
import google.generativeai as genai


CHAT_KEY = st.secrets["CHAT_KEY"]
tab1, tab2 = st.tabs(["Prediagnose Diabetes Model", "AI Chatbot"])

with tab1:  # Added the missing colon here
    st.title("Diabetes Prediction")

    # Input fields
    option1 = st.selectbox("Do you have high blood pressure?", ("Yes", "No"))
    option2 = st.selectbox("Do you have high cholesterol?", ("Yes", "No"))
    option3 = st.selectbox("Do you have your cholesterol check in the last 5 years?", ("Yes", "No"))
    option4 = st.select_slider("What is your BMI", options=range(15, 61, 1))
    option5 = st.selectbox("Have you smoked at least 100 cigarettes (5 packs) in your entire life", ("Yes", "No"))
    option6 = st.selectbox("Have you ever had a stroke", ("Yes", "No"))
    option7 = st.selectbox("Do you have heart disease or attack?", ("Yes", "No"))
    option8 = st.selectbox("Have you done any physical activity in the last 30 days (excluding job)?", ("Yes", "No"))
    option9 = st.selectbox("Do you consume fruit 1 or more times per day?", ("Yes", "No"))
    option10 = st.selectbox("Do you consume vegetables 1 or more times per day?", ("Yes", "No"))
    option11 = st.selectbox("Do you consume 14 drinks for men and 7 drinks for women per week?", ("Yes", "No"))
    option12 = st.selectbox("Do you have any kind of health care coverage, including health insurance, prepaid plans, etc?", ("Yes", "No"))
    option13 = st.selectbox("Was there a time in the past 12 months when you needed to see a doctor but could not due to the cost?", ("Yes", "No"))
    option14 = st.selectbox("Would you say that in general your health is:\n\n(1-excellent, 2-very good, 3-good, 4-fair, 5-poor)", (1, 2, 3, 4, 5))
    option15 = st.select_slider("Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good?", options=range(0, 31, 1))
    option16 = st.select_slider("Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good?", options=range(0, 31, 1))
    option17 = st.selectbox("Do you have serious difficulty walking or climbing stairs?", ("Yes", "No"))
    option18 = st.selectbox("What is your gender?", ("Male", "Female"))
    option19 = st.selectbox("What age range are you in?\n\n1-(18-24),   2-(25-29)\n\n 3-(30-34),   4-(35-39)\n\n 5-(40-44),   6-(45-49)\n\n 7-(50-54),   8-(55-59)\n\n 9-(60-64),   10-(65-69)\n\n 11-(70-74),   12(75-79)\n\n 13-(80 or more)", range(1, 14, 1))
    option20 = st.selectbox("Your Education level?\n\n1 = Never attended school or only kindergarten\n \n 2 = Grades 1 through 8 (Elementary)\n \n 3 = Grades 9 through 11 (Some high school)\n \n 4 = Grade 12 or GED (High school graduate)\n \n 5 = College 1 year to 3 years (Some college or technical school)\n \n 6 = College 4 years or more", range(1, 7, 1))
    option21 = st.selectbox("Your Income level (in a year)?\n\n1 = <\$10000, 2 = <\$15000, 3 = <\$20000, 4 = <\$25000, 5 = <\$35000, 6 = <\$50000, 7 = <\$75000, 8 = >\$75000", range(1, 9, 1))

    if st.button("Submit"):
        HighBP = 1 if option1 == "Yes" else 0
        HighChol = 1 if option2 == "Yes" else 0
        CholCheck = 1 if option3 == "Yes" else 0
        BMI = option4
        Smoker = 1 if option5 == "Yes" else 0
        Stroke = 1 if option6 == "Yes" else 0
        HeartDiseaseorAttack = 1 if option7 == "Yes" else 0
        PhysActivity = 1 if option8 == "Yes" else 0
        Fruits = 1 if option9 == "Yes" else 0
        Veggies = 1 if option10 == "Yes" else 0
        HvyAlcoholConsump = 1 if option11 == "Yes" else 0
        AnyHealthcare = 1 if option12 == "Yes" else 0
        NoDocbcCost = 1 if option13 == "Yes" else 0
        GenHlth = option14
        MentHlth = option15
        PhysHlth = option16
        DiffWalk = 1 if option17 == "Yes" else 0
        Sex = 1 if option18 == "Male" else 0
        Age = option19
        Education = option20
        Income = option21

        if HighBP is None or HighChol is None or CholCheck is None or BMI is None or Smoker is None or Stroke is None or HeartDiseaseorAttack is None or PhysActivity is None or Fruits is None or Veggies is None or HvyAlcoholConsump is None or AnyHealthcare is None or NoDocbcCost is None or GenHlth is None or MentHlth is None or PhysHlth is None or DiffWalk is None or Sex is None or Age is None or Education is None or Income is None:
            st.error("Please fill in all fields")
        else:
            # Send data to FastAPI backend
            with st.spinner("Uploading and processing..."):
                try:
                    data = {
                        "HighBP": HighBP,
                        "HighChol": HighChol,
                        "CholCheck": CholCheck,
                        "BMI": BMI,
                        "Smoker": Smoker,
                        "Stroke": Stroke,
                        "HeartDiseaseorAttack": HeartDiseaseorAttack,
                        "PhysActivity": PhysActivity,
                        "Fruits": Fruits,
                        "Veggies": Veggies,
                        "HvyAlcoholConsump": HvyAlcoholConsump,
                        "AnyHealthcare": AnyHealthcare,
                        "NoDocbcCost": NoDocbcCost,
                        "GenHlth": GenHlth,
                        "MentHlth": MentHlth,
                        "PhysHlth": PhysHlth,
                        "DiffWalk": DiffWalk,
                        "Sex": Sex,
                        "Age": Age,
                        "Education": Education,
                        "Income": Income,
                    }

                    response = requests.post("https://fast-api-deploy-nyav.onrender.com/predict", json=data)

                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"{result['result']}")
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"Failed to connect to the backend: {e}")

with tab2:
    # Create configuration for Gemini
    genai.configure(api_key= CHAT_KEY)

    # Create model chatbot
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("AI Chatbot")

    # Display chat history
    for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
        st.markdown(f"*You:* {user_msg}")
        st.markdown(f"*AI chat box:* {ai_msg}")

    # User Input
    user_input = st.text_input("Enter your question:")

    # Handle user input
    if user_input:
        # Send request to Gemini API
        response = model.generate_content(user_input)
        ai_reply = response.text

        # Update chat history
        st.session_state.chat_history.append((user_input, ai_reply))

        # Display the new messages
        st.markdown(f"*You:* {user_input}")
        st.markdown(f"*AI chat box:* {ai_reply}")
