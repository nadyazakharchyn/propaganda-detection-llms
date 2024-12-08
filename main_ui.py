import streamlit as st
from openai import OpenAI
import os
import re
from io import StringIO
from annotated_text import annotated_text
from prompts import prompt_base, prompt
from dotenv import load_dotenv

def wrap_detected_phrases(detected_str, text):
    # Parse detected techniques and phrases
    detected_pairs = []
    for line in detected_str.split(",\n"):
        if ":" in line:
            technique, phrase = line.split(":", 1)
            detected_pairs.append((phrase.strip(), technique.strip()))
    
    # Sort phrases by their position in the text for correct order wrapping
    detected_pairs = sorted(
        detected_pairs, 
        key=lambda x: text.find(x[0]) if text.find(x[0]) != -1 else float('inf')
    )

    # Wrap the detected phrases in the text
    result = []
    current_index = 0
    
    for phrase, technique in detected_pairs:
        start_index = text.find(phrase, current_index)
        if start_index != -1:
            # Add the text before the detected phrase
            result.append(text[current_index:start_index])
            # Add the detected phrase and its technique as a tuple
            result.append((phrase, technique))
            # Update the current index to after the detected phrase
            current_index = start_index + len(phrase)
    
    # Add any remaining text after the last detected phrase
    result.append(text[current_index:]+",")
    
    return result

# List of allowed phrases
allowed_phrases = [
    'Appeal_to_Authority', 'Appeal_to_fear-prejudice', 'Bandwagon', 'Reductio_ad_hitlerum',
    'Black-and-White_Fallacy', 'Causal_Oversimplification', 'Doubt', 'Exaggeration,Minimisation',
    'Flag-Waving', 'Loaded_Language', 'Name_Calling,Labeling', 'Repetition', 'Slogans',
    'Thought-terminating_Cliches', 'Whataboutism', 'Straw_Men', 'Red_Herring'
]

# Regular expression pattern for allowed phrases
pattern = r'^(?:' + '|'.join(map(re.escape, allowed_phrases)) + r')'


def respond(input_text):    

    response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
              ],
              temperature=0.6
        )
    response_message = response.choices[0].message.content

    return response_message

            # messages= [ {'role': 'assistant', 'content': f"""{prompt1}"""},],
            # temperature=0.0

def format_response(response):
    st_response = response.split(',\n')
    st_response = list(set(st_response))
    st_response = ",\n".join(l for l in st_response)
    st_response = st_response.replace('\n', '  \n')
    return st_response


load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()

# model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AAc7yCJG' # first model
# model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AUWrtC4j' # escaped
# model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AUfXOlYY' # russian
#model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AUt4YzLL' # without spans
#model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AUvfOA86' # phrases instead of start-end
model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AVIkMPT1' # normal phrases
# model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AW8HKdcw' # final with spans

st.set_page_config(page_title=' Detect Propaganda Easily!')
st.title('Асистент із виявлення пропаганди')
title = st.text_input("Вставте текст новини", "")

uploaded_file = st.file_uploader("Оберіть текстовий файл із новинною статтею чи постом", accept_multiple_files=False,
                                 type=['txt'])

text_data = ""
techniques = ""
formatted_techniques = ""

if uploaded_file is not None:
    file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}

    if uploaded_file.type == "text/plain":
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        text_data = stringio.read()
        techniques = respond(text_data)
        formatted_techniques = format_response(techniques)
        print(formatted_techniques)
        
    else:
        text_data = ""
        techniques = ""
        
if title!="":
    techniques = respond(text_data)
    formatted_techniques = format_response(techniques)

with st.sidebar:
    st.subheader("Техніки пропаганди: довідка", divider=True)
    add_selectbox = st.markdown(
   ''':red[**Loaded_Language (навантажена мова):**] Слова/фрази з сильним емоційним забарвленням, наприклад, «дитячий крик самотнього депутата».
  \n:red[**Name_Calling,Labeling:**] Наклеювання на когось або щось позитивних/негативних ярликів, наприклад, «Буш менший».
  \n:red[**Repetition:**] Повторення повідомлення з метою його посилення, наприклад: «Наш великий лідер є втіленням мудрості».
  \n:red[**Exaggeration,Minimisation:**] Перебільшення або применшення чогось, наприклад: «Я не бився з нею, ми просто гралися».
  \n:red[**Appeal_to_fear-prejudice:**] Використання страху або упереджень для впливу на думку, наприклад: «Зупиніть цих біженців, вони терористи».
  \n:red[**Flag-Waving:**] Апеляція до сильних національних/групових почуттів, наприклад: «Вступ у цю війну забезпечить наше майбутнє».
  \n:red[**Causal_Oversimplification:**] Спрощення складних причин, наприклад: «Якби Франція не оголосила війну Німеччині, Другої світової війни не сталося б».
  \n:red[**Appeal_to_Authority:**] Ствердження, що щось є правдою, тому що авторитет підтримує це, наприклад: «ВООЗ заявила, що це найкращий метод лікування».
  \n:red[**Slogans:**] Короткі, яскраві фрази, наприклад, «Зробимо Америку знову великою!»
  \n:red[**Thought-terminating_Cliches:**] Заперечення дискусії, наприклад, «Є те, що є».
  \n:red[**Whataboutism:**] Дискредитація аргументів шляхом звинувачення в лицемірстві, наприклад: «Ви хочете зберегти репутацію ФБР?»
  \n:red[**Black-and-White_Fallacy:**] Надання лише двох альтернатив, наприклад, «Ви повинні бути республіканцем або демократом».
  \n:red[**Reductio_ad_hitlerum:**] Асоціювання ідеї з ненависними групами, наприклад: «Тільки комуніст може так думати».
  \n:red[**Doubt:**] Ставить під сумнів достовірність, наприклад: «Чи готовий він бути мером?»
  \n:red[**Red herring:**] Відволікання уваги за допомогою нерелевантного матеріалу, наприклад: «А як щодо жертв злочинів?»
  \n:red[**Bandwagon:**] Переконання, тому що «всі так роблять», наприклад, «57 відсотків кажуть “так”.
  \n:red[**Obfuscation,Intentional_Vagueness,Confusion:**] Використання нечітких формулювань з метою введення в оману, наприклад: «Це гарна ідея - прислухатися до жертв».
  \n:red[**Straw man:**] Спотворення аргументу з метою його спростування.'''
    )

    

st.subheader("Тут з'являться виявлені техніки пропаганди та фрази:")
st.write(formatted_techniques)

st.markdown("**Виділені фрагменти, на які слід звернути увагу**")
text = text_data.replace("\n", " ")
output = wrap_detected_phrases(techniques, text)

annotated_text(output)

# Parse response and highlight text
# parsed_phrases = parse_response(process_phrases(techniques))
# highlighted_content = highlight_text(text_data, parsed_phrases)
