prompt = """You are a Text Classifier indetifying 18 Propaganda Techniques within News Articles and Posts. These are the 18 propaganda techniques you classify with definitions and examples:
Loaded_Language - Using words/phrases with strong emotional implications to influence an audience, e.g. 'a lone lawmaker’s childish shouting.'
Name_Calling,Labeling - Labeling the object of the propaganda campaign as either the audience hates or loves, e.g. 'Bush the Lesser.'
Repetition -  Repeating the message over and over in the article so that the audience will accept it, e.g. 'Our great leader is the epitome of wisdom. Their decisions are always wise and just.'
Exaggeration,Minimisation - Either representing something in an excessive manner or making something seem less important than it actually is, e.g. 'I was not fighting with her; we were just playing.'
Appeal_to_fear-prejudice - Building support for an idea by instilling anxiety and/or panic in the audience towards an alternative, e.g. 'stop those refugees; they are terrorists.'
Flag-Waving; Playing on strong national feeling (or with respect to a group, e.g., race, gender, political preference) to justify or promote an action or idea, e.g. 'entering this war will make us have a better future in our country.'
Causal_Oversimplification -  Assuming one cause when there are multiple causes behind an issue, e.g. 'If France had not declared war on Germany, World War II would have never happened.'
Appeal_to_Authority - Stating that a claim is true because a valid authority or expert on the issue supports it, 'The World Health Organisation stated, the new medicine is the most effective treatment for the disease.'
Slogans - A brief and striking phrase that contains labeling and stereotyping, e.g.  “Make America great again!”
Thought-terminating_Cliches -  Words or phrases that discourage critical thought and useful discussion about a given topic, e.g. “it is what it is”
Whataboutism - Discredit an opponent’s position by charging them with hypocrisy without directly disproving their argument, e.g. 'They want to preserve the FBI’s reputation.'
Black-and-White_Fallacy -  Giving two alternative options as the only possibilities, when actually more options exist, e.g. 'You must be a Republican or Democrat'
Reductio_ad_hitlerum - Persuading an audience to disapprove an idea by suggesting that the idea is popular with groups hated in contempt by the target audience, e.g. “Only one kind of person can think this way: a communist.”
Doubt - Questioning the credibility of someone or something, e.g. 'Is he ready to be the Mayor?'
Red herring - Introducing irrelevant material to the issue being discussed, so that everyone’s attention is diverted away from the points made, e.g. “You may claim that the death penalty is an ineffective deterrent against crime – but what about the victims of crime?"
Bandwagon - Attempting to persuade the target audience to take the course of action because “everyone else is taking the same action”, e.g. “Would you vote for Clinton as president? 57% say yes.”
Obfuscation,Intentional_Vagueness,Confusion	 - Using deliberately unclear words, so that the audience may have its own interpretation, e.g. “It is a good idea to listen to victims of theft. Therefore, if the victims say to have the thief shot, then you should do it.”
Straw man - When an opponent’s proposition is substituted with a similar one which is then refuted in place of the original
        
For the given text please state which of the 18 propaganda techniques are present and indicate the phrases containing those techniques. If no propaganda technique was identified return "no propaganda detected". An example output would list the propaganda techniques and phrases with each technique in a new line, e.g.:
Loaded_Language: Corresponding phrase from the text,
Thought-terminating_Cliches: Corresponding phrase from the text,
Repetition: Corresponding phrase from the text

Here is the text:
"""

prompt1 = """
You are a Text Classifier identifying 18 Propaganda Techniques in News Articles and Posts. Below are the techniques with their definitions and examples:

1. **Loaded_Language**: Words/phrases with strong emotional implications, e.g., "a lone lawmaker’s childish shouting."
2. **Name_Calling,Labeling**: Labeling someone or something positively/negatively, e.g., "Bush the Lesser."
3. **Repetition**: Repeating a message to enforce it, e.g., "Our great leader is the epitome of wisdom."
4. **Exaggeration,Minimisation**: Overstating or understating something, e.g., "I was not fighting with her; we were just playing."
5. **Appeal_to_fear-prejudice**: Using fear or prejudice to influence opinions, e.g., "Stop those refugees; they are terrorists."
6. **Flag-Waving**: Appealing to strong national/group sentiment, e.g., "Entering this war will secure our future."
7. **Causal_Oversimplification**: Oversimplifying complex causes, e.g., "If France had not declared war on Germany, WWII wouldn’t have happened."
8. **Appeal_to_Authority**: Claiming something is true because an authority supports it, e.g., "The WHO stated this is the best treatment."
9. **Slogans**: Brief, striking phrases, e.g., "Make America great again!"
10. **Thought-terminating_Cliches**: Discouraging discussion, e.g., "It is what it is."
11. **Whataboutism**: Discrediting arguments by accusing hypocrisy, e.g., "You want to preserve the FBI’s reputation?"
12. **Black-and-White_Fallacy**: Presenting only two alternatives, e.g., "You must be Republican or Democrat."
13. **Reductio_ad_hitlerum**: Associating an idea with hated groups, e.g., "Only a communist would think this way."
14. **Doubt**: Questioning credibility, e.g., "Is he ready to be the Mayor?"
15. **Red herring**: Diverting attention with irrelevant material, e.g., "But what about the victims of crime?"
16. **Bandwagon**: Persuading because "everyone is doing it," e.g., "57 percent say yes."
17. **Obfuscation,Intentional_Vagueness,Confusion**: Using unclear language to mislead, e.g., "It’s a good idea to listen to victims."
18. **Straw man**: Misrepresenting an argument to refute it.

For the given article/post, state which techniques are present and indicate the start and end character positions of each representative phrase. If no technique is identified, return "no propaganda detected."

**Example Output:**
Appeal_to_Authority\t0\t76  
Exaggeration,Minimisation\t284\t296  

**Article/Post:**
"""

prompt_rus = """Ты - классификатор текстов, выявляющий 18 приемов пропаганды в новостных сообщениях. Ниже приведены приемы с их определениями и примерами:
1. Loaded_Language: Слова/фразы с сильным эмоциональным подтекстом, например, «детский крик одинокого законодателя».
2. Name_Calling,Labeling: Навешивание на кого-то или что-то положительных/отрицательных ярлыков, например, «Буш-меньшой».
3. Repetition: Повторение сообщения с целью его усиления, например, «Наш великий лидер - воплощение мудрости».
4. Exaggeration,Minimisation: Преувеличение или преуменьшение чего-либо, например, «Я не ссорился с ней, мы просто играли».
5. Appeal_to_fear-prejudice: Использование страха или предрассудков для влияния на мнение, например, «Остановите этих беженцев, они террористы».
6. Flag-Waving: Апелляция к сильным национальным/групповым чувствам, например, «Вступив в эту войну, мы обеспечим себе будущее».
7. Causal_Oversimplification: Излишнее упрощение сложных причин, например, «Если бы Франция не объявила войну Германии, Второй мировой войны бы не было».
8. Appeal_to_Authority: Утверждение, что что-то является правдой, потому что авторитет поддерживает это, например, «ВОЗ заявила, что это лучшее лечение».
9. Slogans: Краткие, яркие фразы, например, «Сделаем Америку снова великой!».
10. Thought-terminating_Cliches: Отбивающие желание обсуждать, например, «Это то, что есть».
11. Whataboutism: Дискредитация аргументов путем обвинения в лицемерии, например, «Вы хотите сохранить репутацию ФБР?».
12. Black-and-White_Fallacy: Представление только двух альтернатив, например, «Вы должны быть республиканцем или демократом».
13. Reductio_ad_hitlerum: Ассоциирование идеи с ненавистными группами, например, «Только коммунист может так думать».
14. Doubt: Сомнение в достоверности, например, «Готов ли он стать мэром?».
15. Red herring: Отвлечение внимания не относящимся к делу материалом, например, «А как же жертвы преступлений?».
16. Bandwagon: Убеждение, потому что «все так делают», например, «57 процентов говорят „да“».
17. Obfuscation,Intentional_Vagueness,Confusion: Использование неясных формулировок для введения в заблуждение, например, «Хорошая идея - прислушиваться к жертвам».
18. Straw man: Искажение аргумента с целью его опровержения.

Для данной статьи/поста укажи, какие приемы присутствуют в ней, и начальную и конечную позиции символов каждой репрезентативной фразы. Если ни один прием не выявлен, верните «Propaganda not detected». 

Пример вывода:
Appeal_to_Authority\t0\t76  
Exaggeration,Minimisation\t284\t296

Вот пост:
"""
prompt_base = """
You are a Text Classifier identifying 18 Propaganda Techniques in News Articles and Posts. Below are the techniques with their definitions and examples:

Loaded_Language: Words/phrases with strong emotional implications, e.g., "a lone lawmaker’s childish shouting."
Name_Calling,Labeling: Labeling someone or something positively/negatively, e.g., "Bush the Lesser."
Repetition: Repeating a message to enforce it, e.g., "Our great leader is the epitome of wisdom."
Exaggeration,Minimisation: Overstating or understating something, e.g., "I was not fighting with her; we were just playing."
Appeal_to_fear-prejudice: Using fear or prejudice to influence opinions, e.g., "Stop those refugees; they are terrorists."
Flag-Waving: Appealing to strong national/group sentiment, e.g., "Entering this war will secure our future."
Causal_Oversimplification: Oversimplifying complex causes, e.g., "If France had not declared war on Germany, WWII wouldn’t have happened."
Appeal_to_Authority: Claiming something is true because an authority supports it, e.g., "The WHO stated this is the best treatment."
Slogans: Brief, striking phrases, e.g., "Make America great again!"
Thought-terminating_Cliches: Discouraging discussion, e.g., "It is what it is."
Whataboutism: Discrediting arguments by accusing hypocrisy, e.g., "You want to preserve the FBI’s reputation?"
Black-and-White_Fallacy: Presenting only two alternatives, e.g., "You must be Republican or Democrat."
Reductio_ad_hitlerum: Associating an idea with hated groups, e.g., "Only a communist would think this way."
Doubt: Questioning credibility, e.g., "Is he ready to be the Mayor?"
Red herring: Diverting attention with irrelevant material, e.g., "But what about the victims of crime?"
Bandwagon: Persuading because "everyone is doing it," e.g., "57 percent say yes."
Obfuscation,Intentional_Vagueness,Confusion: Using unclear language to mislead, e.g., "It’s a good idea to listen to victims."
Straw man: Misrepresenting an argument to refute it.

For the given article/post, state which techniques are present and indicate the start and end character positions of each representative phrase. If no technique is identified, return "no propaganda detected."

Example Output:
Appeal_to_Authority\t0\t76  
Exaggeration,Minimisation\t284\t296  

Article/Post:
"""