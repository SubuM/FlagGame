import streamlit as st
import random
import requests
from PIL import Image
from io import BytesIO
import time

# Tiered country data for different difficulty levels
COMMON_COUNTRIES = {
    "United States": {"capital": "Washington, D.C.", "flag_url": "https://flagcdn.com/w320/us.png"},
    "Canada": {"capital": "Ottawa", "flag_url": "https://flagcdn.com/w320/ca.png"},
    "United Kingdom": {"capital": "London", "flag_url": "https://flagcdn.com/w320/gb.png"},
    "France": {"capital": "Paris", "flag_url": "https://flagcdn.com/w320/fr.png"},
    "Germany": {"capital": "Berlin", "flag_url": "https://flagcdn.com/w320/de.png"},
    "Italy": {"capital": "Rome", "flag_url": "https://flagcdn.com/w320/it.png"},
    "Spain": {"capital": "Madrid", "flag_url": "https://flagcdn.com/w320/es.png"},
    "China": {"capital": "Beijing", "flag_url": "https://flagcdn.com/w320/cn.png"},
    "India": {"capital": "New Delhi", "flag_url": "https://flagcdn.com/w320/in.png"},
    "Japan": {"capital": "Tokyo", "flag_url": "https://flagcdn.com/w320/jp.png"},
    "Australia": {"capital": "Canberra", "flag_url": "https://flagcdn.com/w320/au.png"},
    "Brazil": {"capital": "Brasília", "flag_url": "https://flagcdn.com/w320/br.png"},
    "Mexico": {"capital": "Mexico City", "flag_url": "https://flagcdn.com/w320/mx.png"},
    "Russia": {"capital": "Moscow", "flag_url": "https://flagcdn.com/w320/ru.png"},
    "Egypt": {"capital": "Cairo", "flag_url": "https://flagcdn.com/w320/eg.png"},
    "South Africa": {"capital": "Pretoria", "flag_url": "https://flagcdn.com/w320/za.png"},
    "Argentina": {"capital": "Buenos Aires", "flag_url": "https://flagcdn.com/w320/ar.png"},
    "Saudi Arabia": {"capital": "Riyadh", "flag_url": "https://flagcdn.com/w320/sa.png"},
    "South Korea": {"capital": "Seoul", "flag_url": "https://flagcdn.com/w320/kr.png"},
    "Indonesia": {"capital": "Jakarta", "flag_url": "https://flagcdn.com/w320/id.png"},
    "Greece": {"capital": "Athens", "flag_url": "https://flagcdn.com/w320/gr.png"},
    "Sweden": {"capital": "Stockholm", "flag_url": "https://flagcdn.com/w320/se.png"},
    "Norway": {"capital": "Oslo", "flag_url": "https://flagcdn.com/w320/no.png"},
    "Finland": {"capital": "Helsinki", "flag_url": "https://flagcdn.com/w320/fi.png"},
    "Ireland": {"capital": "Dublin", "flag_url": "https://flagcdn.com/w320/ie.png"},
    "New Zealand": {"capital": "Wellington", "flag_url": "https://flagcdn.com/w320/nz.png"},
    "Singapore": {"capital": "Singapore", "flag_url": "https://flagcdn.com/w320/sg.png"},
    "Thailand": {"capital": "Bangkok", "flag_url": "https://flagcdn.com/w320/th.png"},
    "Portugal": {"capital": "Lisbon", "flag_url": "https://flagcdn.com/w320/pt.png"},
    "Netherlands": {"capital": "Amsterdam", "flag_url": "https://flagcdn.com/w320/nl.png"},
    "Belgium": {"capital": "Brussels", "flag_url": "https://flagcdn.com/w320/be.png"},
    "Switzerland": {"capital": "Bern", "flag_url": "https://flagcdn.com/w320/ch.png"},
    "Austria": {"capital": "Vienna", "flag_url": "https://flagcdn.com/w320/at.png"},
    "Poland": {"capital": "Warsaw", "flag_url": "https://flagcdn.com/w320/pl.png"},
    "Hungary": {"capital": "Budapest", "flag_url": "https://flagcdn.com/w320/hu.png"},
    "Czechia": {"capital": "Prague", "flag_url": "https://flagcdn.com/w320/cz.png"},
    "Iceland": {"capital": "Reykjavik", "flag_url": "https://flagcdn.com/w320/is.png"},
    "Denmark": {"capital": "Copenhagen", "flag_url": "https://flagcdn.com/w320/dk.png"},
    "Israel": {"capital": "Jerusalem", "flag_url": "https://flagcdn.com/w320/il.png"}
}

CHALLENGING_COUNTRIES = {
    "Kazakhstan": {"capital": "Nur-Sultan", "flag_url": "https://flagcdn.com/w320/kz.png"},
    "Myanmar": {"capital": "Naypyidaw", "flag_url": "https://flagcdn.com/w320/mm.png"},
    "Côte d'Ivoire": {"capital": "Yamoussoukro", "flag_url": "https://flagcdn.com/w320/ci.png"},
    "Nigeria": {"capital": "Abuja", "flag_url": "https://flagcdn.com/w320/ng.png"},
    "Tanzania": {"capital": "Dodoma", "flag_url": "https://flagcdn.com/w320/tz.png"},
    "Morocco": {"capital": "Rabat", "flag_url": "https://flagcdn.com/w320/ma.png"},
    "Turkey": {"capital": "Ankara", "flag_url": "https://flagcdn.com/w320/tr.png"},
    "Pakistan": {"capital": "Islamabad", "flag_url": "https://flagcdn.com/w320/pk.png"},
    "Sri Lanka": {"capital": "Sri Jayawardenepura Kotte", "flag_url": "https://flagcdn.com/w320/lk.png"},
    "Vietnam": {"capital": "Hanoi", "flag_url": "https://flagcdn.com/w320/vn.png"},
    "Ecuador": {"capital": "Quito", "flag_url": "https://flagcdn.com/w320/ec.png"},
    "Bolivia": {"capital": "Sucre", "flag_url": "https://flagcdn.com/w320/bo.png"},
    "Libya": {"capital": "Tripoli", "flag_url": "https://flagcdn.com/w320/ly.png"},
    "Sudan": {"capital": "Khartoum", "flag_url": "https://flagcdn.com/w320/sd.png"},
    "Madagascar": {"capital": "Antananarivo", "flag_url": "https://flagcdn.com/w320/mg.png"},
    "Belarus": {"capital": "Minsk", "flag_url": "https://flagcdn.com/w320/by.png"},
    "Slovenia": {"capital": "Ljubljana", "flag_url": "https://flagcdn.com/w320/si.png"},
    "Slovakia": {"capital": "Bratislava", "flag_url": "https://flagcdn.com/w320/sk.png"},
    "Estonia": {"capital": "Tallinn", "flag_url": "https://flagcdn.com/w320/ee.png"},
    "Latvia": {"capital": "Riga", "flag_url": "https://flagcdn.com/w320/lv.png"},
    "Lithuania": {"capital": "Vilnius", "flag_url": "https://flagcdn.com/w320/lt.png"},
    "Moldova": {"capital": "Chișinău", "flag_url": "https://flagcdn.com/w320/md.png"},
    "Georgia": {"capital": "Tbilisi", "flag_url": "https://flagcdn.com/w320/ge.png"},
    "Armenia": {"capital": "Yerevan", "flag_url": "https://flagcdn.com/w320/am.png"},
    "Azerbaijan": {"capital": "Baku", "flag_url": "https://flagcdn.com/w320/az.png"},
    "Uzbekistan": {"capital": "Tashkent", "flag_url": "https://flagcdn.com/w320/uz.png"},
    "Kyrgyzstan": {"capital": "Bishkek", "flag_url": "https://flagcdn.com/w320/kg.png"},
    "Tajikistan": {"capital": "Dushanbe", "flag_url": "https://flagcdn.com/w320/tj.png"},
    "Turkmenistan": {"capital": "Ashgabat", "flag_url": "https://flagcdn.com/w320/tm.png"},
    "Mongolia": {"capital": "Ulaanbaatar", "flag_url": "https://flagcdn.com/w320/mn.png"},
    "Laos": {"capital": "Vientiane", "flag_url": "https://flagcdn.com/w320/la.png"},
    "Cambodia": {"capital": "Phnom Penh", "flag_url": "https://flagcdn.com/w320/kh.png"},
    "Brunei": {"capital": "Bandar Seri Begawan", "flag_url": "https://flagcdn.com/w320/bn.png"},
    "Bhutan": {"capital": "Thimphu", "flag_url": "https://flagcdn.com/w320/bt.png"},
    "Nepal": {"capital": "Kathmandu", "flag_url": "https://flagcdn.com/w320/np.png"},
    "Bangladesh": {"capital": "Dhaka", "flag_url": "https://flagcdn.com/w320/bd.png"},
    "Afghanistan": {"capital": "Kabul", "flag_url": "https://flagcdn.com/w320/af.png"},
    "Jordan": {"capital": "Amman", "flag_url": "https://flagcdn.com/w320/jo.png"},
    "Lebanon": {"capital": "Beirut", "flag_url": "https://flagcdn.com/w320/lb.png"},
    "Syria": {"capital": "Damascus", "flag_url": "https://flagcdn.com/w320/sy.png"},
    "Yemen": {"capital": "Sana'a", "flag_url": "https://flagcdn.com/w320/ye.png"},
    "Oman": {"capital": "Muscat", "flag_url": "https://flagcdn.com/w320/om.png"},
    "Qatar": {"capital": "Doha", "flag_url": "https://flagcdn.com/w320/qa.png"},
    "Kuwait": {"capital": "Kuwait City", "flag_url": "https://flagcdn.com/w320/kw.png"},
    "Bahrain": {"capital": "Manama", "flag_url": "https://flagcdn.com/w320/bh.png"},
    "United Arab Emirates": {"capital": "Abu Dhabi", "flag_url": "https://flagcdn.com/w320/ae.png"},
    "Ethiopia": {"capital": "Addis Ababa", "flag_url": "https://flagcdn.com/w320/et.png"},
    "Kenya": {"capital": "Nairobi", "flag_url": "https://flagcdn.com/w320/ke.png"},
    "Uganda": {"capital": "Kampala", "flag_url": "https://flagcdn.com/w320/ug.png"},
    "Rwanda": {"capital": "Kigali", "flag_url": "https://flagcdn.com/w320/rw.png"},
    "Burundi": {"capital": "Gitega", "flag_url": "https://flagcdn.com/w320/bi.png"},
    "Ghana": {"capital": "Accra", "flag_url": "https://flagcdn.com/w320/gh.png"},
    "Senegal": {"capital": "Dakar", "flag_url": "https://flagcdn.com/w320/sn.png"},
    "Mali": {"capital": "Bamako", "flag_url": "https://flagcdn.com/w320/ml.png"},
    "Burkina Faso": {"capital": "Ouagadougou", "flag_url": "https://flagcdn.com/w320/bf.png"},
    "Niger": {"capital": "Niamey", "flag_url": "https://flagcdn.com/w320/ne.png"},
    "Chad": {"capital": "N'Djamena", "flag_url": "https://flagcdn.com/w320/td.png"}
}

# Additional tricky capital cities for wrong answers
TRICKY_CAPITALS = [
    "Sydney", "Melbourne", "Rio de Janeiro", "São Paulo", "Mumbai", "Kolkata", 
    "Istanbul", "Casablanca", "Lagos", "Johannesburg", "Montreal", "Toronto",
    "New York", "Los Angeles", "Shanghai", "Hong Kong", "Zurich", "Geneva",
    "Milan", "Naples", "Barcelona", "Seville", "Hamburg", "Munich",
    "Karachi", "Lahore", "Ho Chi Minh City", "Almaty", "Yangon"
]

def load_flag_image(url):
    """Load flag image from URL"""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"Error loading flag image: {e}")
        return None

def initialize_session_state():
    """Initialize session state variables"""
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
    if 'question_number' not in st.session_state:
        st.session_state.question_number = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'question_answered' not in st.session_state:
        st.session_state.question_answered = False
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'timer_start_time' not in st.session_state:
        st.session_state.timer_start_time = None
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = "Medium"

def generate_quiz_questions(level):
    """Generate 20 random questions for the quiz based on difficulty level"""
    common_countries = list(COMMON_COUNTRIES.keys())
    challenging_countries = list(CHALLENGING_COUNTRIES.keys())
    
    selected_countries = []
    
    if level == "Super Easy":
        selected_countries = random.sample(common_countries, 20)
    elif level == "Easy":
        selected_countries = random.sample(common_countries, 18) + random.sample(challenging_countries, 2)
        random.shuffle(selected_countries)
    elif level == "Medium":
        selected_countries = random.sample(common_countries, 17) + random.sample(challenging_countries, 3)
        random.shuffle(selected_countries)
    elif level == "Hard":
        selected_countries = random.sample(common_countries, 15) + random.sample(challenging_countries, 5)
        random.shuffle(selected_countries)
        
    questions = []
    
    for country in selected_countries:
        country_data = COMMON_COUNTRIES.get(country) or CHALLENGING_COUNTRIES.get(country)
        correct_capital = country_data["capital"]
        
        all_countries_data = {**COMMON_COUNTRIES, **CHALLENGING_COUNTRIES}
        
        # Generate wrong options based on a mix of all capitals and tricky cities
        other_capitals = [all_countries_data[c]["capital"] for c in all_countries_data.keys() if c != country]
        wrong_options = random.sample(other_capitals + TRICKY_CAPITALS, 5)

        # Ensure correct capital is not in wrong options and take only 3
        wrong_options = [opt for opt in wrong_options if opt != correct_capital][:3]

        # Generate country options (more challenging - similar flags/regions)
        wrong_countries = random.sample([c for c in all_countries_data.keys() if c != country], 3)
        country_options = [country] + wrong_countries
        random.shuffle(country_options)

        capital_options = [correct_capital] + wrong_options
        random.shuffle(capital_options)
        
        questions.append({
            'country': country,
            'capital': correct_capital,
            'flag_url': country_data['flag_url'],
            'country_options': country_options,
            'capital_options': capital_options
        })
    
    return questions


def calculate_difficulty_score(correct_answers, total_questions):
    """Calculate performance rating based on score"""
    percentage = (correct_answers / total_questions) * 100
    if percentage >= 90:
        return "🏆 Geography Master", "gold"
    elif percentage >= 80:
        return "🥇 Excellent", "success"
    elif percentage >= 70:
        return "🥈 Very Good", "success"
    elif percentage >= 60:
        return "🥉 Good", "info"
    elif percentage >= 50:
        return "📚 Keep Learning", "warning"
    else:
        return "🗺️ Geography Explorer", "error"

def main():
    st.set_page_config(
        page_title="World Flag Quiz Challenge",
        page_icon="🧐🌍",
        layout="wide"
    )

    initialize_session_state()

    # Header and Sidebar
    st.title("🌍 World Flag Quiz Challenge")
    
    # Display selected difficulty level or the intro text
    if st.session_state.quiz_active:
        st.markdown(f"**Difficulty Level:** :green[{st.session_state.difficulty_level}]")
    else:
        st.markdown("**Test your knowledge with 20 challenging countries and their capitals!**")
    
    st.markdown("---")
    
    with st.sidebar:
        st.header("🎯 Quiz Progress")
        if st.session_state.quiz_active:
            progress = st.session_state.question_number / 20
            st.progress(progress)
            st.metric("Question", f"{st.session_state.question_number}/20")
            st.metric("Current Score", f"{st.session_state.score}/{st.session_state.question_number}")
            if st.session_state.question_number > 0:
                current_percentage = (st.session_state.score / st.session_state.question_number) * 100
                st.metric("Current %", f"{current_percentage:.1f}%")
        st.markdown("---")
        st.subheader("🎮 Quiz Controls")
        if not st.session_state.quiz_active:
            st.markdown("**Test your knowledge with 20 challenging countries and their capitals!**")
            st.session_state.difficulty_level = st.selectbox(
                "Choose Difficulty Level:",
                ["Super Easy", "Easy", "Medium", "Hard"],
                index=2 # Set Medium as the default
            )
            if st.button("🚀 Start New Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_questions = generate_quiz_questions(st.session_state.difficulty_level)
                st.session_state.quiz_active = True
                st.session_state.question_number = 1
                st.session_state.score = 0
                st.session_state.current_question = st.session_state.quiz_questions[0]
                st.session_state.question_answered = False
                st.session_state.quiz_completed = False
                st.session_state.user_answers = []
                st.session_state.timer_start_time = None
                st.rerun()
        if st.session_state.quiz_active and not st.session_state.quiz_completed:
            if st.button("🔄 Restart Quiz", type="secondary", use_container_width=True):
                st.session_state.quiz_active = False
                st.rerun()
        st.markdown("---")
        st.subheader("🔥 Challenge Level")
        st.write("**Super Easy:** all common countries")
        st.write("**Easy:** 90% common, 10% challenging")
        st.write("**Medium:** 85% common, 15% challenging")
        st.write("**Hard:** 75% common, 25% challenging")


    # Main content area
    if not st.session_state.quiz_active:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ## 🎯 Ready for the Challenge?
            - **20 carefully selected questions**
            - **Challenging countries** from around the world
            - **Tricky capital cities** that might surprise you
            - **Multiple choice format** with 4 options each
            - **Detailed scoring** and performance analysis
            ### 🏆 Scoring System:
            - 90%+ = Geography Master 🏆
            - 80-89% = Excellent 🥇
            - 70-79% = Very Good 🥈
            - 60-69% = Good 🥉
            - 50-59% = Keep Learning 📚
            - <50% = Geography Explorer 🗺️
            Click "Start New Quiz" in the sidebar when you're ready!
            """)
    elif st.session_state.quiz_completed:
        st.subheader("🎊 Quiz Complete!")
        final_percentage = (st.session_state.score / 20) * 100
        rating, color = calculate_difficulty_score(st.session_state.score, 20)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if color == "gold":
                st.balloons()
            st.markdown(f"""
            ## Final Results
            **Score:** {st.session_state.score}/20 ({final_percentage:.1f}%)
            **Rating:** {rating}
            """)
            if final_percentage >= 80:
                st.success("Outstanding performance! You're a geography expert! 🌟")
            elif final_percentage >= 60:
                st.info("Great job! You have solid geography knowledge! 👍")
            else:
                st.warning("Good effort! Keep exploring the world to improve! 🗺️")
            st.subheader("📊 Detailed Review")
            for i, (question, answer) in enumerate(zip(st.session_state.quiz_questions, st.session_state.user_answers)):
                with st.expander(f"Question {i+1}: {question['country']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Your Country Answer:** {answer['selected_country']}")
                        if answer['country_correct']:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Correct: {question['country']}")
                    with col_b:
                        st.write(f"**Your Capital Answer:** {answer['selected_capital']}")
                        if answer['capital_correct']:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Correct: {question['capital']}")
            if st.button("🔄 Take Another Quiz", type="primary"):
                st.session_state.quiz_active = False
                st.rerun()
    else:
        # Active quiz with centered flag and side-by-side questions
        question = st.session_state.current_question

        # Centered Flag Display
        col_flag_left, col_flag_center, col_flag_right = st.columns([1, 2, 1])
        with col_flag_center:
            st.subheader(f"🏳️ Question {st.session_state.question_number}/20")
            flag_img = load_flag_image(question['flag_url'])
            if flag_img:
                st.image(flag_img, width=350, caption="Identify this flag and its capital!")
                
        # Side-by-side Radio Buttons
        col_country, col_capital = st.columns(2)
        
        with col_country:
            st.subheader("🌍 Which country is this?")
            selected_country = st.radio(
                "Select the country:",
                question['country_options'],
                key=f"country_{st.session_state.question_number}",
                disabled=st.session_state.question_answered
            )

        with col_capital:
            st.subheader("🏛️ What's the capital city?")
            selected_capital = st.radio(
                "Select the capital city:",
                question['capital_options'],
                key=f"capital_{st.session_state.question_number}",
                disabled=st.session_state.question_answered
            )

        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if not st.session_state.question_answered:
                if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                    country_correct = selected_country == question['country']
                    capital_correct = selected_capital == question['capital']
                    st.session_state.user_answers.append({
                        'selected_country': selected_country,
                        'selected_capital': selected_capital,
                        'country_correct': country_correct,
                        'capital_correct': capital_correct
                    })
                    if country_correct and capital_correct:
                        st.session_state.score += 1
                    st.session_state.question_answered = True
                    st.session_state.timer_start_time = time.time()
                    st.rerun()
            else:
                st.markdown("---")
                col_res1, col_res2 = st.columns([1, 1])
                with col_res1:
                    if st.session_state.user_answers[-1]['country_correct']:
                        st.success(f"✅ Country: **{question['country']}** - Correct!")
                    else:
                        st.error(f"❌ Country: You selected **{selected_country}**")
                        st.info(f"💡 Correct: **{question['country']}**")
                with col_res2:
                    if st.session_state.user_answers[-1]['capital_correct']:
                        st.success(f"✅ Capital: **{question['capital']}** - Correct!")
                    else:
                        st.error(f"❌ Capital: You selected **{selected_capital}**")
                        st.info(f"💡 Correct: **{question['capital']}**")
                
                st.markdown("---")
                col_next_btn, col_finish_btn = st.columns(2)

                is_last_question = st.session_state.question_number == 20

                with col_next_btn:
                    if not is_last_question:
                        if st.button("⏭️ Next Question", use_container_width=True):
                            st.session_state.question_number += 1
                            st.session_state.current_question = st.session_state.quiz_questions[st.session_state.question_number - 1]
                            st.session_state.question_answered = False
                            st.session_state.timer_start_time = None
                            st.rerun()
                
                with col_finish_btn:
                    if st.button("🏁 Finish Quiz", type="primary", use_container_width=True):
                        st.session_state.quiz_completed = True
                        st.session_state.timer_start_time = None
                        st.rerun()

                elapsed_time = time.time() - st.session_state.timer_start_time
                remaining_time = max(0, 10 - int(elapsed_time))
                
                if remaining_time > 0 and not st.session_state.quiz_completed:
                    st.info(f"Moving to next question in {remaining_time} seconds...")
                    time.sleep(1)
                    st.rerun()
                elif remaining_time <= 0 and not st.session_state.quiz_completed:
                    if not is_last_question:
                        st.session_state.question_number += 1
                        st.session_state.current_question = st.session_state.quiz_questions[st.session_state.question_number - 1]
                        st.session_state.question_answered = False
                        st.session_state.timer_start_time = None
                        st.rerun()
                    else:
                        st.session_state.quiz_completed = True
                        st.session_state.timer_start_time = None
                        st.rerun()

if __name__ == "__main__":
    main()