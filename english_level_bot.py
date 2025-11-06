import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import json
from datetime import datetime
import asyncio

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# بانک سوالات گسترده - 100+ سوال
QUESTIONS = {
    'grammar': [
        # A1 Level (10 سوال)
        {'q': 'She ___ to school every day.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 1, 'level': 'A1'},
        {'q': 'I ___ coffee in the morning.', 'options': ['drinks', 'drink', 'drinking', 'drank'], 'answer': 1, 'level': 'A1'},
        {'q': 'They ___ watching TV now.', 'options': ['is', 'am', 'are', 'be'], 'answer': 2, 'level': 'A1'},
        {'q': '___ you like pizza?', 'options': ['Do', 'Does', 'Are', 'Is'], 'answer': 0, 'level': 'A1'},
        {'q': 'He ___ a teacher.', 'options': ['am', 'is', 'are', 'be'], 'answer': 1, 'level': 'A1'},
        {'q': 'We ___ students.', 'options': ['am', 'is', 'are', 'be'], 'answer': 2, 'level': 'A1'},
        {'q': 'This is ___ book.', 'options': ['a', 'an', 'the', '-'], 'answer': 0, 'level': 'A1'},
        {'q': 'I have ___ apple.', 'options': ['a', 'an', 'the', '-'], 'answer': 1, 'level': 'A1'},
        {'q': 'She ___ not like cats.', 'options': ['do', 'does', 'is', 'are'], 'answer': 1, 'level': 'A1'},
        {'q': 'Where ___ you from?', 'options': ['is', 'am', 'are', 'be'], 'answer': 2, 'level': 'A1'},
        
        # A2 Level (15 سوال)
        {'q': 'I ___ him for 5 years.', 'options': ['know', 'knew', 'have known', 'knowing'], 'answer': 2, 'level': 'A2'},
        {'q': 'She ___ to London last year.', 'options': ['go', 'goes', 'went', 'gone'], 'answer': 2, 'level': 'A2'},
        {'q': 'They ___ football when it started raining.', 'options': ['play', 'played', 'were playing', 'are playing'], 'answer': 2, 'level': 'A2'},
        {'q': 'I ___ finish my homework yesterday.', 'options': ['don\'t', 'didn\'t', 'doesn\'t', 'wasn\'t'], 'answer': 1, 'level': 'A2'},
        {'q': 'She is ___ than her sister.', 'options': ['tall', 'taller', 'tallest', 'more tall'], 'answer': 1, 'level': 'A2'},
        {'q': 'This is ___ book I\'ve ever read.', 'options': ['good', 'better', 'best', 'the best'], 'answer': 3, 'level': 'A2'},
        {'q': 'I ___ to the gym twice a week.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 0, 'level': 'A2'},
        {'q': 'He ___ watching TV at 8 pm yesterday.', 'options': ['is', 'was', 'were', 'be'], 'answer': 1, 'level': 'A2'},
        {'q': 'We ___ lived here since 2010.', 'options': ['are', 'were', 'have', 'has'], 'answer': 2, 'level': 'A2'},
        {'q': 'There ___ many people at the party.', 'options': ['is', 'are', 'was', 'were'], 'answer': 3, 'level': 'A2'},
        {'q': 'She can ___ English very well.', 'options': ['speak', 'speaks', 'speaking', 'spoke'], 'answer': 0, 'level': 'A2'},
        {'q': 'I ___ going to visit my parents tomorrow.', 'options': ['am', 'is', 'are', 'be'], 'answer': 0, 'level': 'A2'},
        {'q': 'He has ___ finished his work.', 'options': ['yet', 'already', 'still', 'since'], 'answer': 1, 'level': 'A2'},
        {'q': 'How ___ money do you have?', 'options': ['many', 'much', 'some', 'any'], 'answer': 1, 'level': 'A2'},
        {'q': 'I don\'t have ___ time.', 'options': ['many', 'much', 'some', 'few'], 'answer': 1, 'level': 'A2'},
        
        # B1 Level (15 سوال)
        {'q': 'If I ___ rich, I would travel the world.', 'options': ['am', 'was', 'were', 'be'], 'answer': 2, 'level': 'B1'},
        {'q': 'By the time you arrive, I ___ dinner.', 'options': ['finish', 'will finish', 'will have finished', 'finished'], 'answer': 2, 'level': 'B1'},
        {'q': 'The car ___ last week.', 'options': ['is repaired', 'was repaired', 'has repaired', 'repairs'], 'answer': 1, 'level': 'B1'},
        {'q': 'She suggested ___ to the cinema.', 'options': ['go', 'to go', 'going', 'went'], 'answer': 2, 'level': 'B1'},
        {'q': 'I wish I ___ speak Chinese.', 'options': ['can', 'could', 'will', 'would'], 'answer': 1, 'level': 'B1'},
        {'q': 'He ___ have arrived by now.', 'options': ['must', 'can', 'may', 'might'], 'answer': 0, 'level': 'B1'},
        {'q': 'The book ___ by millions of people.', 'options': ['has read', 'has been read', 'was reading', 'reads'], 'answer': 1, 'level': 'B1'},
        {'q': 'I would rather ___ at home tonight.', 'options': ['stay', 'to stay', 'staying', 'stayed'], 'answer': 0, 'level': 'B1'},
        {'q': 'She made me ___ the dishes.', 'options': ['wash', 'to wash', 'washing', 'washed'], 'answer': 0, 'level': 'B1'},
        {'q': 'The film was ___ boring that I fell asleep.', 'options': ['so', 'such', 'too', 'very'], 'answer': 0, 'level': 'B1'},
        {'q': 'I look forward to ___ you soon.', 'options': ['see', 'seeing', 'saw', 'seen'], 'answer': 1, 'level': 'B1'},
        {'q': 'Unless you ___ now, you\'ll be late.', 'options': ['leave', 'left', 'will leave', 'leaving'], 'answer': 0, 'level': 'B1'},
        {'q': 'I\'m not used to ___ up early.', 'options': ['get', 'getting', 'got', 'gotten'], 'answer': 1, 'level': 'B1'},
        {'q': 'The house ___ built in 1990.', 'options': ['is', 'was', 'has', 'had'], 'answer': 1, 'level': 'B1'},
        {'q': 'She denied ___ the money.', 'options': ['steal', 'to steal', 'stealing', 'stole'], 'answer': 2, 'level': 'B1'},
        
        # B2 Level (15 سوال)
        {'q': 'He wishes he ___ harder last year.', 'options': ['studied', 'had studied', 'has studied', 'studies'], 'answer': 1, 'level': 'B2'},
        {'q': 'Rarely ___ seen such a beautiful sunset.', 'options': ['I have', 'have I', 'I had', 'had I'], 'answer': 1, 'level': 'B2'},
        {'q': 'The proposal ___ by the committee tomorrow.', 'options': ['will be reviewing', 'will have been reviewed', 'is being reviewed', 'will be reviewed'], 'answer': 3, 'level': 'B2'},
        {'q': 'No sooner ___ than it started to rain.', 'options': ['had we left', 'we had left', 'we left', 'did we leave'], 'answer': 0, 'level': 'B2'},
        {'q': '___ the difficulties, they completed the project.', 'options': ['Despite', 'Although', 'However', 'But'], 'answer': 0, 'level': 'B2'},
        {'q': 'She would rather you ___ there yesterday.', 'options': ['were', 'had been', 'are', 'have been'], 'answer': 1, 'level': 'B2'},
        {'q': 'Little ___ that his life was about to change.', 'options': ['he knew', 'did he know', 'he knows', 'does he know'], 'answer': 1, 'level': 'B2'},
        {'q': 'I\'d sooner you ___ mention it to anyone.', 'options': ['don\'t', 'didn\'t', 'haven\'t', 'won\'t'], 'answer': 1, 'level': 'B2'},
        {'q': 'It\'s high time we ___ something about it.', 'options': ['do', 'did', 'have done', 'will do'], 'answer': 1, 'level': 'B2'},
        {'q': 'Scarcely ___ when the phone rang.', 'options': ['had I arrived', 'I had arrived', 'I arrived', 'did I arrive'], 'answer': 0, 'level': 'B2'},
        {'q': 'Were I ___ do it again, I would do it differently.', 'options': ['for', 'to', 'at', 'in'], 'answer': 1, 'level': 'B2'},
        {'q': 'The manager insisted that the report ___ by Friday.', 'options': ['is completed', 'be completed', 'will be completed', 'completes'], 'answer': 1, 'level': 'B2'},
        {'q': 'Not until yesterday ___ the truth.', 'options': ['did I discover', 'I discovered', 'I did discover', 'discovered I'], 'answer': 0, 'level': 'B2'},
        {'q': 'Provided that you ___ on time, we can leave.', 'options': ['arrive', 'will arrive', 'arrived', 'arriving'], 'answer': 0, 'level': 'B2'},
        {'q': 'Such ___ the circumstances, we had no choice.', 'options': ['were', 'was', 'are', 'is'], 'answer': 0, 'level': 'B2'},
        
        # C1 Level (15 سوال)
        {'q': 'Had I known about the traffic, I ___ earlier.', 'options': ['left', 'would leave', 'would have left', 'will leave'], 'answer': 2, 'level': 'C1'},
        {'q': 'Not only ___ the exam, but she also got the highest score.', 'options': ['she passed', 'did she pass', 'she did pass', 'passed she'], 'answer': 1, 'level': 'C1'},
        {'q': 'Never before ___ such determination.', 'options': ['I have seen', 'have I seen', 'I had seen', 'had I seen'], 'answer': 1, 'level': 'C1'},
        {'q': 'It is imperative that he ___ the meeting.', 'options': ['attends', 'attend', 'attended', 'will attend'], 'answer': 1, 'level': 'C1'},
        {'q': 'Only after the exam ___ the results.', 'options': ['they announced', 'did they announce', 'they did announce', 'announced they'], 'answer': 1, 'level': 'C1'},
        {'q': 'Lest you ___ confused, let me explain.', 'options': ['are', 'be', 'were', 'will be'], 'answer': 1, 'level': 'C1'},
        {'q': 'So complex ___ that few understood it.', 'options': ['the theory was', 'was the theory', 'the theory is', 'is the theory'], 'answer': 1, 'level': 'C1'},
        {'q': 'Were it not for your help, I ___ failed.', 'options': ['will have', 'would have', 'had', 'have'], 'answer': 1, 'level': 'C1'},
        {'q': 'Much as I ___ to help, I simply cannot.', 'options': ['would like', 'like', 'will like', 'liked'], 'answer': 0, 'level': 'C1'},
        {'q': 'He demanded that the work ___ immediately.', 'options': ['is done', 'be done', 'will be done', 'was done'], 'answer': 1, 'level': 'C1'},
        {'q': 'Under no circumstances ___ tolerated.', 'options': ['such behavior is', 'is such behavior', 'such behavior will', 'will such behavior be'], 'answer': 3, 'level': 'C1'},
        {'q': 'The more you practice, ___ you will become.', 'options': ['the better', 'better', 'the best', 'best'], 'answer': 0, 'level': 'C1'},
        {'q': 'Barely ___ when the alarm went off.', 'options': ['had I fallen asleep', 'I had fallen asleep', 'I fell asleep', 'did I fall asleep'], 'answer': 0, 'level': 'C1'},
        {'q': 'It behooves us ___ with caution.', 'options': ['proceed', 'to proceed', 'proceeding', 'proceeded'], 'answer': 1, 'level': 'C1'},
        {'q': 'Should you ___ any problems, contact me.', 'options': ['encounter', 'encountered', 'encountering', 'encounters'], 'answer': 0, 'level': 'C1'},
        
        # C2 Level (10 سوال)
        {'q': 'The government is contemplating ___ new legislation.', 'options': ['to enact', 'enacting', 'enact', 'enacted'], 'answer': 1, 'level': 'C2'},
        {'q': 'Notwithstanding the objections, the motion ___.', 'options': ['passed', 'was passed', 'has passed', 'had passed'], 'answer': 1, 'level': 'C2'},
        {'q': 'The data, ___ by experts, proved conclusive.', 'options': ['analyzing', 'analyzed', 'having analyzed', 'having been analyzed'], 'answer': 3, 'level': 'C2'},
        {'q': 'It is incumbent upon us ___ responsibility.', 'options': ['take', 'to take', 'taking', 'taken'], 'answer': 1, 'level': 'C2'},
        {'q': 'The committee recommended that funding ___.', 'options': ['is increased', 'be increased', 'will be increased', 'increases'], 'answer': 1, 'level': 'C2'},
        {'q': 'Insofar as the evidence ___, he is innocent.', 'options': ['goes', 'go', 'going', 'gone'], 'answer': 0, 'level': 'C2'},
        {'q': 'The proposal, ___ ambitious, is feasible.', 'options': ['although', 'however', 'while', 'whereas'], 'answer': 2, 'level': 'C2'},
        {'q': '___ the document thoroughly before signing.', 'options': ['Peruse', 'Perusing', 'To peruse', 'Perused'], 'answer': 0, 'level': 'C2'},
        {'q': 'The findings ___ further investigation.', 'options': ['warrant', 'warrants', 'warranting', 'warranted'], 'answer': 0, 'level': 'C2'},
        {'q': 'His erudition, ___ remarkable, was widely acknowledged.', 'options': ['though', 'however', 'while', 'despite'], 'answer': 0, 'level': 'C2'},
    ],
    
    'vocabulary': [
        # A1 Level (8 سوال)
        {'q': 'What is the opposite of "hot"?', 'options': ['cold', 'warm', 'cool', 'freezing'], 'answer': 0, 'level': 'A1'},
        {'q': 'A person who teaches is a ___', 'options': ['doctor', 'teacher', 'student', 'worker'], 'answer': 1, 'level': 'A1'},
        {'q': 'I need to ___ my teeth.', 'options': ['wash', 'brush', 'clean', 'wipe'], 'answer': 1, 'level': 'A1'},
        {'q': 'The opposite of "big" is ___', 'options': ['small', 'tiny', 'little', 'short'], 'answer': 0, 'level': 'A1'},
        {'q': 'We use a ___ to write.', 'options': ['pen', 'book', 'paper', 'desk'], 'answer': 0, 'level': 'A1'},
        {'q': 'The opposite of "old" is ___', 'options': ['new', 'young', 'fresh', 'modern'], 'answer': 1, 'level': 'A1'},
        {'q': 'A place where you buy food is a ___', 'options': ['hospital', 'school', 'supermarket', 'bank'], 'answer': 2, 'level': 'A1'},
        {'q': 'The opposite of "happy" is ___', 'options': ['sad', 'angry', 'tired', 'bored'], 'answer': 0, 'level': 'A1'},
        
        # A2 Level (10 سوال)
        {'q': 'He is very ___ and always helps others.', 'options': ['selfish', 'generous', 'mean', 'rude'], 'answer': 1, 'level': 'A2'},
        {'q': 'The movie was so ___ that I fell asleep.', 'options': ['boring', 'excited', 'interesting', 'thrilling'], 'answer': 0, 'level': 'A2'},
        {'q': 'Please ___ the lights when you leave.', 'options': ['turn off', 'turn on', 'turn up', 'turn down'], 'answer': 0, 'level': 'A2'},
        {'q': 'She is very ___ about her appearance.', 'options': ['careless', 'careful', 'caring', 'cared'], 'answer': 1, 'level': 'A2'},
        {'q': 'The weather is ___ today.', 'options': ['awful', 'beauty', 'wonder', 'terrible good'], 'answer': 0, 'level': 'A2'},
        {'q': 'He made a ___ mistake.', 'options': ['terrible', 'terribly', 'terror', 'terrified'], 'answer': 0, 'level': 'A2'},
        {'q': 'I need to ___ my English skills.', 'options': ['improve', 'improvement', 'improving', 'improved'], 'answer': 0, 'level': 'A2'},
        {'q': 'She ___ forgot her keys.', 'options': ['accident', 'accidental', 'accidentally', 'accidents'], 'answer': 2, 'level': 'A2'},
        {'q': 'That\'s a very ___ idea!', 'options': ['brilliance', 'brilliant', 'brilliantly', 'brillianted'], 'answer': 1, 'level': 'A2'},
        {'q': 'He spoke very ___.', 'options': ['quiet', 'quietly', 'quietness', 'quieted'], 'answer': 1, 'level': 'A2'},
        
        # B1 Level (12 سوال)
        {'q': 'The company aims to ___ its market share.', 'options': ['expand', 'reduce', 'decrease', 'minimize'], 'answer': 0, 'level': 'B1'},
        {'q': 'We need to ___ the problem before it gets worse.', 'options': ['ignore', 'address', 'avoid', 'escape'], 'answer': 1, 'level': 'B1'},
        {'q': 'The new policy will be ___ next month.', 'options': ['implemented', 'implicated', 'implied', 'imported'], 'answer': 0, 'level': 'B1'},
        {'q': 'His behavior was completely ___.', 'options': ['acceptable', 'unacceptable', 'accepting', 'acceptance'], 'answer': 1, 'level': 'B1'},
        {'q': 'The project requires ___ planning.', 'options': ['careful', 'care', 'carefully', 'careless'], 'answer': 0, 'level': 'B1'},
        {'q': 'She made a ___ contribution to the team.', 'options': ['significance', 'significant', 'significantly', 'signify'], 'answer': 1, 'level': 'B1'},
        {'q': 'The results were quite ___.', 'options': ['impress', 'impressive', 'impression', 'impressed'], 'answer': 1, 'level': 'B1'},
        {'q': 'We need to find a ___ solution.', 'options': ['sustain', 'sustainable', 'sustainability', 'sustained'], 'answer': 1, 'level': 'B1'},
        {'q': 'The situation is becoming ___.', 'options': ['urgent', 'urgently', 'urgency', 'urge'], 'answer': 0, 'level': 'B1'},
        {'q': 'He is known for his ___.', 'options': ['reliable', 'reliability', 'reliably', 'reliance'], 'answer': 1, 'level': 'B1'},
        {'q': 'The ___ of the project was unexpected.', 'options': ['succeed', 'success', 'successful', 'successfully'], 'answer': 1, 'level': 'B1'},
        {'q': 'She handled the situation ___.', 'options': ['profession', 'professional', 'professionally', 'professionalism'], 'answer': 2, 'level': 'B1'},
        
        # B2 Level (12 سوال)
        {'q': 'Her argument was very ___ and convincing.', 'options': ['persuasive', 'aggressive', 'passive', 'defensive'], 'answer': 0, 'level': 'B2'},
        {'q': 'The evidence was ___ and could not be disputed.', 'options': ['ambiguous', 'vague', 'irrefutable', 'questionable'], 'answer': 2, 'level': 'B2'},
        {'q': 'The politician\'s speech was full of ___.', 'options': ['clarity', 'rhetoric', 'simplicity', 'honesty'], 'answer': 1, 'level': 'B2'},
        {'q': 'The study provided ___ results.', 'options': ['comprehensive', 'comprehend', 'comprehension', 'comprehensible'], 'answer': 0, 'level': 'B2'},
        {'q': 'His ___ attitude helped resolve the conflict.', 'options': ['diplomatic', 'diplomat', 'diplomacy', 'diplomatically'], 'answer': 0, 'level': 'B2'},
        {'q': 'The report contains ___ information.', 'options': ['substance', 'substantial', 'substantially', 'substantiate'], 'answer': 1, 'level': 'B2'},
        {'q': 'She showed remarkable ___ under pressure.', 'options': ['compose', 'composure', 'composed', 'composing'], 'answer': 1, 'level': 'B2'},
        {'q': 'The decision had ___ consequences.', 'options': ['far-reach', 'far-reaching', 'far-reached', 'far-reaches'], 'answer': 1, 'level': 'B2'},
        {'q': 'His ___ to detail is impressive.', 'options': ['attend', 'attention', 'attentive', 'attentively'], 'answer': 1, 'level': 'B2'},
        {'q': 'The plan requires ___ consideration.', 'options': ['meticulous', 'meticulously', 'meticulousness', 'meticulate'], 'answer': 0, 'level': 'B2'},
        {'q': 'The ___ of the argument was weak.', 'options': ['coherent', 'coherence', 'coherently', 'cohere'], 'answer': 1, 'level': 'B2'},
        {'q': 'She displayed ___ in her work.', 'options': ['diligent', 'diligence', 'diligently', 'diligenced'], 'answer': 1, 'level': 'B2'},
        
        # C1 Level (12 سوال)
        {'q': 'His ___ behavior made everyone uncomfortable.', 'options': ['erratic', 'stable', 'consistent', 'predictable'], 'answer': 0, 'level': 'C1'},
        {'q': 'The lawyer tried to ___ the witness\'s testimony.', 'options': ['support', 'discredit', 'praise', 'validate'], 'answer': 1, 'level': 'C1'},
        {'q': 'The proposal showed ___ thinking.', 'options': ['ingenious', 'ingenuous', 'indigenous', 'ingenuity'], 'answer': 0, 'level': 'C1'},
        {'q': 'His ___ remarks offended many.', 'options': ['polite', 'derogatory', 'kind', 'supportive'], 'answer': 1, 'level': 'C1'},
        {'q': 'The situation requires ___ action.', 'options': ['expedite', 'expeditious', 'expedition', 'expedited'], 'answer': 1, 'level': 'C1'},
        {'q': 'Her ___ nature made her popular.', 'options': ['affable', 'affability', 'affably', 'affableness'], 'answer': 0, 'level': 'C1'},
        {'q': 'The article was full of ___ language.', 'options': ['bombast', 'bombastic', 'bombastically', 'bombastness'], 'answer': 1, 'level': 'C1'},
        {'q': 'His ___ attitude hindered progress.', 'options': ['obstinate', 'obstinately', 'obstinacy', 'obstinated'], 'answer': 0, 'level': 'C1'},
        {'q': 'The speaker\'s ___ captivated the audience.', 'options': ['eloquent', 'eloquence', 'eloquently', 'eloquented'], 'answer': 1, 'level': 'C1'},
        {'q': 'The evidence was merely ___.', 'options': ['circumstance', 'circumstantial', 'circumstantially', 'circumstances'], 'answer': 1, 'level': 'C1'},
        {'q': 'His ___ for detail was legendary.', 'options': ['fastidious', 'fastidiousness', 'fastidiously', 'fastidiate'], 'answer': 1, 'level': 'C1'},
        {'q': 'The report was criticized for its ___.', 'options': ['verbose', 'verbosity', 'verbosely', 'verboseness'], 'answer': 1, 'level': 'C1'},
        
        # C2 Level (8 سوال)
        {'q': 'The novel explores the ___ nature of human existence.', 'options': ['simple', 'ephemeral', 'permanent', 'obvious'], 'answer': 1, 'level': 'C2'},
        {'q': 'The theory remains largely ___.', 'options': ['proven', 'disproven', 'unsubstantiated', 'validated'], 'answer': 2, 'level': 'C2'},
        {'q': 'His writing style is characterized by ___.', 'options': ['prolixity', 'brevity', 'simplicity', 'clarity'], 'answer': 0, 'level': 'C2'},
        {'q': 'The committee showed ___ in their decision.', 'options': ['precipitous', 'precipitousness', 'precipitously', 'precipitate'], 'answer': 3, 'level': 'C2'},
        {'q': 'The argument was based on ___ reasoning.', 'options': ['specious', 'genuine', 'valid', 'sound'], 'answer': 0, 'level': 'C2'},
        {'q': 'Her ___ manner impressed everyone.', 'options': ['imperious', 'humble', 'modest', 'shy'], 'answer': 0, 'level': 'C2'},
        {'q': 'The text was filled with ___ references.', 'options': ['simple', 'abstruse', 'clear', 'obvious'], 'answer': 1, 'level': 'C2'},
        {'q': 'His ___ opinions caused controversy.', 'options': ['conventional', 'iconoclastic', 'traditional', 'mainstream'], 'answer': 1, 'level': 'C2'},
    ],
    
    'spelling': [
        # A1-A2 Level (5 سوال)
        {'q': 'Which word is spelled correctly?', 'options': ['recieve', 'receive', 'recive', 'receeve'], 'answer': 1, 'level': 'A2'},
        {'q': 'Choose the correct spelling:', 'options': ['occured', 'ocurred', 'occurred', 'occurrd'], 'answer': 2, 'level': 'A2'},
        {'q': 'Which is correct?', 'options': ['seperate', 'separate', 'separete', 'seperete'], 'answer': 1, 'level': 'A2'},
        {'q': 'Select the right spelling:', 'options': ['definately', 'definetly', 'definitely', 'definitly'], 'answer': 2, 'level': 'A2'},
        {'q': 'Which is spelled correctly?', 'options': ['beleive', 'believe', 'beleave', 'belive'], 'answer': 1, 'level': 'A2'},
        
        # B1 Level (5 سوال)
        {'q': 'Choose the correct spelling:', 'options': ['accomodate', 'accommodate', 'acommodate', 'acomodate'], 'answer': 1, 'level': 'B1'},
        {'q': 'Which word is correct?', 'options': ['embarass', 'embarras', 'embarrass', 'embaress'], 'answer': 2, 'level': 'B1'},
        {'q': 'Select the right spelling:', 'options': ['necesary', 'neccessary', 'necessary', 'neccesary'], 'answer': 2, 'level': 'B1'},
        {'q': 'Which is spelled correctly?', 'options': ['occassion', 'occasion', 'ocasion', 'occaison'], 'answer': 1, 'level': 'B1'},
        {'q': 'Choose the correct spelling:', 'options': ['maintainance', 'maintenance', 'maintenence', 'maintanance'], 'answer': 1, 'level': 'B1'},
        
        # B2 Level (5 سوال)
        {'q': 'Which word is correct?', 'options': ['priviledge', 'privilege', 'privilage', 'privlege'], 'answer': 1, 'level': 'B2'},
        {'q': 'Select the right spelling:', 'options': ['conscientous', 'conscientious', 'consientious', 'consciencious'], 'answer': 1, 'level': 'B2'},
        {'q': 'Choose the correct spelling:', 'options': ['liason', 'liaison', 'liasion', 'liaision'], 'answer': 1, 'level': 'B2'},
        {'q': 'Which is spelled correctly?', 'options': ['perseverance', 'perserverance', 'perseverence', 'perserverence'], 'answer': 0, 'level': 'B2'},
        {'q': 'Select the right spelling:', 'options': ['exhilerate', 'exhilarate', 'exhilirate', 'exhillarate'], 'answer': 1, 'level': 'B2'},
        
        # C1 Level (5 سوال)
        {'q': 'Which word is correct?', 'options': ['acquaintence', 'acquaintance', 'acquaintence', 'aquaintance'], 'answer': 1, 'level': 'C1'},
        {'q': 'Choose the correct spelling:', 'options': ['bureacracy', 'bureaucracy', 'burocracy', 'bureaucrasy'], 'answer': 1, 'level': 'C1'},
        {'q': 'Select the right spelling:', 'options': ['idiosyncracy', 'idiosyncrasy', 'idiosynchrasy', 'ideosyncrasy'], 'answer': 1, 'level': 'C1'},
        {'q': 'Which is spelled correctly?', 'options': ['maneuver', 'manuever', 'manouver', 'manouvre'], 'answer': 0, 'level': 'C1'},
        {'q': 'Choose the correct spelling:', 'options': ['millennium', 'millenium', 'milennium', 'milenium'], 'answer': 0, 'level': 'C1'},
        
        # C2 Level (5 سوال)
        {'q': 'Which word is correct?', 'options': ['pharaoh', 'pharoah', 'pharoh', 'pharao'], 'answer': 0, 'level': 'C2'},
        {'q': 'Select the right spelling:', 'options': ['onomatopoeia', 'onomatopeia', 'onomatopoea', 'onomatapoeia'], 'answer': 0, 'level': 'C2'},
        {'q': 'Choose the correct spelling:', 'options': ['desiccate', 'desicate', 'dessicate', 'dessiccate'], 'answer': 0, 'level': 'C2'},
        {'q': 'Which is spelled correctly?', 'options': ['reconnaissance', 'reconaissance', 'reconassance', 'reconnaisance'], 'answer': 0, 'level': 'C2'},
        {'q': 'Select the right spelling:', 'options': ['supersede', 'supercede', 'superceed', 'superseed'], 'answer': 0, 'level': 'C2'},
    ],
    
    'usage': [
        # A2 Level (3 سوال)
        {'q': 'I am looking forward ___ meeting you.', 'options': ['for', 'to', 'at', 'in'], 'answer': 1, 'level': 'A2'},
        {'q': 'She is good ___ mathematics.', 'options': ['in', 'at', 'on', 'with'], 'answer': 1, 'level': 'A2'},
        {'q': 'He insisted ___ paying the bill.', 'options': ['on', 'in', 'at', 'to'], 'answer': 0, 'level': 'A2'},
        
        # B1 Level (4 سوال)
        {'q': 'The decision depends ___ several factors.', 'options': ['of', 'on', 'in', 'at'], 'answer': 1, 'level': 'B1'},
        {'q': 'She is allergic ___ cats.', 'options': ['with', 'of', 'to', 'for'], 'answer': 2, 'level': 'B1'},
        {'q': 'He succeeded ___ convincing them.', 'options': ['in', 'at', 'on', 'to'], 'answer': 0, 'level': 'B1'},
        {'q': 'The book consists ___ ten chapters.', 'options': ['in', 'on', 'of', 'with'], 'answer': 2, 'level': 'B1'},
        
        # B2 Level (4 سوال)
        {'q': 'She refrained ___ making comments.', 'options': ['to', 'from', 'of', 'in'], 'answer': 1, 'level': 'B2'},
        {'q': 'The plan is susceptible ___ change.', 'options': ['for', 'of', 'to', 'with'], 'answer': 2, 'level': 'B2'},
        {'q': 'He is proficient ___ several languages.', 'options': ['at', 'in', 'on', 'with'], 'answer': 1, 'level': 'B2'},
        {'q': 'The theory is conducive ___ learning.', 'options': ['for', 'to', 'of', 'in'], 'answer': 1, 'level': 'B2'},
        
        # C1 Level (4 سوال)
        {'q': 'His actions are tantamount ___ treason.', 'options': ['of', 'to', 'with', 'for'], 'answer': 1, 'level': 'C1'},
        {'q': 'She is impervious ___ criticism.', 'options': ['to', 'of', 'for', 'with'], 'answer': 0, 'level': 'C1'},
        {'q': 'The evidence is germane ___ the case.', 'options': ['of', 'to', 'with', 'for'], 'answer': 1, 'level': 'C1'},
        {'q': 'His behavior is antithetical ___ our values.', 'options': ['of', 'with', 'to', 'for'], 'answer': 2, 'level': 'C1'},
    ]
}

# تعداد سوالات برای هر دسته در آزمون 30 سوالی
TEST_DISTRIBUTION = {
    'grammar': 15,
    'vocabulary': 10,
    'spelling': 3,
    'usage': 2
}

CEFR_LEVELS = {
    'A1': {'min': 0, 'max': 30, 'name_en': 'Beginner', 'name_fa': 'مبتدی'},
    'A2': {'min': 31, 'max': 45, 'name_en': 'Elementary', 'name_fa': 'پایه'},
    'B1': {'min': 46, 'max': 60, 'name_en': 'Intermediate', 'name_fa': 'متوسط'},
    'B2': {'min': 61, 'max': 75, 'name_en': 'Upper-Intermediate', 'name_fa': 'متوسط به بالا'},
    'C1': {'min': 76, 'max': 88, 'name_en': 'Advanced', 'name_fa': 'پیشرفته'},
    'C2': {'min': 89, 'max': 100, 'name_en': 'Proficiency', 'name_fa': 'تسلط کامل'}
}

# زمان آزمون به ثانیه (30 دقیقه)
TEST_TIME_LIMIT = 1800

class UserData:
    def __init__(self):
        self.users = {}
    
    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                'current_question': 0,
                'answers': [],
                'test_started': False,
                'language': 'fa',
                'history': [],
                'test_questions': [],
                'start_time': None
            }
        return self.users[user_id]
    
    def reset_test(self, user_id):
        user = self.get_user(user_id)
        user['current_question'] = 0
        user['answers'] = []
        user['test_started'] = False
        user['test_questions'] = []
        user['start_time'] = None

user_data = UserData()

TEXTS = {
    'fa': {
        'welcome': '🎓 به ربات تعیین سطح زبان انگلیسی خوش آمدید!\n\n📋 مشخصات آزمون:\n• تعداد سوالات: 30 سوال\n• زمان: 30 دقیقه\n• انواع سوال: گرامر، واژگان، املا، کاربرد\n\n✨ این آزمون سطح دقیق شما را بر اساس استاندارد CEFR تعیین می‌کند.\n\n⚠️ توجه: پس از شروع آزمون، 30 دقیقه وقت دارید!\n\n🔹 از منوی زیر گزینه مورد نظر را انتخاب کنید:',
        'start_test': '🎯 شروع آزمون (30 دقیقه)',
        'view_history': '📜 تاریخچه آزمون‌ها',
        'change_language': '🌐 تغییر زبان',
        'help': '❓ راهنما',
        'test_started': '⏱ آزمون شروع شد!\n\n⏰ زمان باقی‌مانده: 30:00\n📝 تعداد سوالات: 30\n\n🎯 موفق باشید!',
        'question': 'سوال',
        'of': 'از',
        'time_left': '⏰ زمان باقی‌مانده',
        'submit': '✅ ثبت پاسخ',
        'next': '➡️ سوال بعدی',
        'finish': '🏁 پایان آزمون',
        'time_up': '⏰ زمان آزمون به پایان رسید!',
        'score': 'امتیاز شما',
        'level': 'سطح شما',
        'results': '📊 نتایج آزمون',
        'correct_answers': 'پاسخ‌های صحیح',
        'wrong_answers': 'پاسخ‌های غلط',
        'accuracy': 'دقت',
        'time_taken': 'زمان صرف شده',
        'strengths': '💪 نقاط قوت',
        'weaknesses': '⚠️ نقاط ضعف',
        'recommendations': '💡 توصیه‌ها',
        'back_to_menu': '🏠 بازگشت به منوی اصلی',
        'no_history': 'هنوز آزمونی نداده‌اید!',
        'help_text': '''📚 راهنمای آزمون تعیین سطح:

⏱ زمان آزمون:
• مدت: 30 دقیقه
• 30 سوال جامع
• تایمر خودکار

📝 انواع سوال:
• گرامر (15 سوال)
• واژگان (10 سوال)
• املا (3 سوال)
• کاربرد (2 سوال)

📊 سطوح CEFR:
• A1: مبتدی (0-30%)
• A2: پایه (31-45%)
• B1: متوسط (46-60%)
• B2: متوسط به بالا (61-75%)
• C1: پیشرفته (76-88%)
• C2: تسلط کامل (89-100%)

💯 نکات مهم:
• پس از شروع، باید تمام سوالات را پاسخ دهید
• نمی‌توانید به سوال قبلی برگردید
• در صورت اتمام زمان، آزمون خودکار پایان می‌یابد
• نتایج شما ذخیره می‌شود''',
    },
    'en': {
        'welcome': '🎓 Welcome to English Level Test Bot!\n\n📋 Test Details:\n• Questions: 30 questions\n• Time: 30 minutes\n• Types: Grammar, Vocabulary, Spelling, Usage\n\n✨ This test determines your exact level based on CEFR standard.\n\n⚠️ Note: After starting, you have 30 minutes!\n\n🔹 Choose an option from the menu below:',
        'start_test': '🎯 Start Test (30 minutes)',
        'view_history': '📜 Test History',
        'change_language': '🌐 Change Language',
        'help': '❓ Help',
        'test_started': '⏱ Test Started!\n\n⏰ Time remaining: 30:00\n📝 Total questions: 30\n\n🎯 Good luck!',
        'question': 'Question',
        'of': 'of',
        'time_left': '⏰ Time left',
        'submit': '✅ Submit Answer',
        'next': '➡️ Next Question',
        'finish': '🏁 Finish Test',
        'time_up': '⏰ Time is up!',
        'score': 'Your Score',
        'level': 'Your Level',
        'results': '📊 Test Results',
        'correct_answers': 'Correct Answers',
        'wrong_answers': 'Wrong Answers',
        'accuracy': 'Accuracy',
        'time_taken': 'Time Taken',
        'strengths': '💪 Strengths',
        'weaknesses': '⚠️ Weaknesses',
        'recommendations': '💡 Recommendations',
        'back_to_menu': '🏠 Back to Main Menu',
        'no_history': 'You haven\'t taken any tests yet!',
        'help_text': '''📚 Level Test Guide:

⏱ Test Duration:
• Duration: 30 minutes
• 30 comprehensive questions
• Automatic timer

📝 Question Types:
• Grammar (15 questions)
• Vocabulary (10 questions)
• Spelling (3 questions)
• Usage (2 questions)

📊 CEFR Levels:
• A1: Beginner (0-30%)
• A2: Elementary (31-45%)
• B1: Intermediate (46-60%)
• B2: Upper-Intermediate (61-75%)
• C1: Advanced (76-88%)
• C2: Proficiency (89-100%)

💯 Important Notes:
• Once started, you must complete all questions
• You cannot return to previous questions
• Test ends automatically when time is up
• Your results will be saved''',
    }
}

def get_text(user_id, key):
    user = user_data.get_user(user_id)
    lang = user.get('language', 'fa')
    return TEXTS[lang].get(key, key)

def get_main_keyboard(user_id):
    keyboard = [
        [KeyboardButton(get_text(user_id, 'start_test'))],
        [KeyboardButton(get_text(user_id, 'view_history')), KeyboardButton(get_text(user_id, 'help'))],
        [KeyboardButton(get_text(user_id, 'change_language'))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def select_test_questions():
    """انتخاب 30 سوال متنوع و سطح‌بندی شده"""
    import random
    
    selected = []
    
    # انتخاب سوالات گرامر (15 سوال)
    grammar_by_level = {level: [q for q in QUESTIONS['grammar'] if q['level'] == level] 
                        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']}
    for level, questions in grammar_by_level.items():
        count = min(3, len(questions)) if level != 'C2' else min(2, len(questions))
        selected.extend(random.sample(questions, count))
    
    # انتخاب سوالات واژگان (10 سوال)
    vocab_by_level = {level: [q for q in QUESTIONS['vocabulary'] if q['level'] == level] 
                      for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']}
    for level, questions in vocab_by_level.items():
        count = min(2, len(questions)) if level != 'C2' else min(1, len(questions))
        if questions:
            selected.extend(random.sample(questions, min(count, len(questions))))
    
    # انتخاب سوالات املا (3 سوال)
    spelling_questions = random.sample(QUESTIONS['spelling'], min(3, len(QUESTIONS['spelling'])))
    selected.extend(spelling_questions)
    
    # انتخاب سوالات کاربرد (2 سوال)
    usage_questions = random.sample(QUESTIONS['usage'], min(2, len(QUESTIONS['usage'])))
    selected.extend(usage_questions)
    
    # مخلوط کردن سوالات
    random.shuffle(selected)
    
    return selected[:30]

def format_time(seconds):
    """تبدیل ثانیه به فرمت mm:ss"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = user_data.get_user(user_id)
    
    await update.message.reply_text(
        get_text(user_id, 'welcome'),
        reply_markup=get_main_keyboard(user_id)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == get_text(user_id, 'start_test') or 'شروع آزمون' in text or 'Start Test' in text:
        await start_test(update, context)
    elif text == get_text(user_id, 'view_history') or 'تاریخچه' in text or 'History' in text:
        await show_history(update, context)
    elif text == get_text(user_id, 'help') or 'راهنما' in text or 'Help' in text:
        await show_help(update, context)
    elif text == get_text(user_id, 'change_language') or 'تغییر زبان' in text or 'Change Language' in text:
        await change_language(update, context)

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = user_data.get_user(user_id)
    
    # ریست و آماده‌سازی آزمون
    user_data.reset_test(user_id)
    user['test_started'] = True
    user['start_time'] = datetime.now()
    user['test_questions'] = select_test_questions()
    user['current_question'] = 0
    user['answers'] = []
    
    await update.message.reply_text(get_text(user_id, 'test_started'))
    
    # شروع تایمر
    context.job_queue.run_once(
        time_up_callback,
        TEST_TIME_LIMIT,
        data={'user_id': user_id, 'chat_id': update.effective_chat.id},
        name=f'timer_{user_id}'
    )
    
    await send_question(update.effective_chat.id, context, user_id)

async def time_up_callback(context: ContextTypes.DEFAULT_TYPE):
    """callback برای پایان زمان"""
    user_id = context.job.data['user_id']
    chat_id = context.job.data['chat_id']
    user = user_data.get_user(user_id)
    
    if user['test_started']:
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_text(user_id, 'time_up')
        )
        await show_results(chat_id, context, user_id)

async def send_question(chat_id, context: ContextTypes.DEFAULT_TYPE, user_id):
    user = user_data.get_user(user_id)
    
    if not user['test_started']:
        return
    
    current_q = user['current_question']
    questions = user['test_questions']
    
    if current_q >= len(questions):
        # حذف تایمر
        current_jobs = context.job_queue.get_jobs_by_name(f'timer_{user_id}')
        for job in current_jobs:
            job.schedule_removal()
        await show_results(chat_id, context, user_id)
        return
    
    question = questions[current_q]
    
    # محاسبه زمان باقی‌مانده
    elapsed = (datetime.now() - user['start_time']).total_seconds()
    time_left = max(0, TEST_TIME_LIMIT - int(elapsed))
    
    question_text = f"❓ {get_text(user_id, 'question')} {current_q + 1} {get_text(user_id, 'of')} 30\n"
    question_text += f"⏰ {get_text(user_id, 'time_left')}: {format_time(time_left)}\n\n"
    question_text += f"❔ {question['q']}"
    
    keyboard = []
    for idx, option in enumerate(question['options']):
        keyboard.append([InlineKeyboardButton(f"{chr(65+idx)}) {option}", callback_data=f'answer_{idx}')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=question_text,
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = user_data.get_user(user_id)
    
    if query.data.startswith('answer_'):
        if not user['test_started']:
            return
            
        answer_idx = int(query.data.replace('answer_', ''))
        user['answers'].append(answer_idx)
        user['current_question'] += 1
        
        await query.message.delete()
        await send_question(query.message.chat_id, context, user_id)
    
    elif query.data == 'lang_fa':
        user['language'] = 'fa'
        await query.message.edit_text("✅ زبان به فارسی تغییر یافت!")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=get_text(user_id, 'welcome'),
            reply_markup=get_main_keyboard(user_id)
        )
    
    elif query.data == 'lang_en':
        user['language'] = 'en'
        await query.message.edit_text("✅ Language changed to English!")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=get_text(user_id, 'welcome'),
            reply_markup=get_main_keyboard(user_id)
        )
    
    elif query.data == 'back_menu':
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=get_text(user_id, 'welcome'),
            reply_markup=get_main_keyboard(user_id)
        )

async def show_results(chat_id, context: ContextTypes.DEFAULT_TYPE, user_id):
    user = user_data.get_user(user_id)
    
    questions = user['test_questions']
    answers = user['answers']
    
    # محاسبه امتیاز
    correct = 0
    category_scores = {'grammar': [0, 0], 'vocabulary': [0, 0], 'spelling': [0, 0], 'usage': [0, 0]}
    level_scores = {'A1': 0, 'A2': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0}
    
    for i, question in enumerate(questions):
        # تشخیص دسته سوال
        category = 'grammar'
        for cat, qs in QUESTIONS.items():
            if question in qs:
                category = cat
                break
        
        category_scores[category][1] += 1
        
        if i < len(answers) and answers[i] == question['answer']:
            correct += 1
            category_scores[category][0] += 1
            level_scores[question['level']] += 1
    
    total_score = round((correct / 30) * 100)
    accuracy = round((correct / 30) * 100, 1)
    
    # محاسبه زمان صرف شده
    time_taken = (datetime.now() - user['start_time']).total_seconds()
    time_str = format_time(int(time_taken))
    
    # تعیین سطح
    user_level = 'A1'
    for level, data in CEFR_LEVELS.items():
        if data['min'] <= total_score <= data['max']:
            user_level = level
            break
    
    # ذخیره در تاریخچه
    test_result = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'score': total_score,
        'level': user_level,
        'correct': correct,
        'total': 30,
        'time': time_str,
        'category_scores': category_scores
    }
    user['history'].append(test_result)
    
    # تحلیل نقاط قوت و ضعف
    strengths = []
    weaknesses = []
    
    for cat, (correct_count, total_count) in category_scores.items():
        percentage = (correct_count / total_count * 100) if total_count > 0 else 0
        cat_name_fa = {'grammar': 'گرامر', 'vocabulary': 'واژگان', 'spelling': 'املا', 'usage': 'کاربرد'}
        cat_name_en = {'grammar': 'Grammar', 'vocabulary': 'Vocabulary', 'spelling': 'Spelling', 'usage': 'Usage'}
        
        lang = user.get('language', 'fa')
        cat_name = cat_name_fa[cat] if lang == 'fa' else cat_name_en[cat]
        
        if percentage >= 70:
            strengths.append(f"{cat_name} ({correct_count}/{total_count})")
        elif percentage < 50:
            weaknesses.append(f"{cat_name} ({correct_count}/{total_count})")
    
    lang = user.get('language', 'fa')
    level_info = CEFR_LEVELS[user_level]
    
    # ساخت پیام نتیجه
    result_text = f"""
🎉 {get_text(user_id, 'results')}

📊 {get_text(user_id, 'score')}: {total_score}/100
🏆 {get_text(user_id, 'level')}: {user_level} - {level_info['name_fa' if lang == 'fa' else 'name_en']}

✅ {get_text(user_id, 'correct_answers')}: {correct}/{30}
❌ {get_text(user_id, 'wrong_answers')}: {30 - correct}
📈 {get_text(user_id, 'accuracy')}: {accuracy}%
⏱ {get_text(user_id, 'time_taken')}: {time_str}

{get_text(user_id, 'strengths')}: {', '.join(strengths) if strengths else '-'}
{get_text(user_id, 'weaknesses')}: {', '.join(weaknesses) if weaknesses else '-'}

{get_text(user_id, 'recommendations')}:
"""
    
    # توصیه‌ها بر اساس سطح
    recommendations = {
        'fa': {
            'A1': '📚 برای پیشرفت:\n• تمرکز بر گرامر پایه و فعل‌های ساده\n• یادگیری 500 کلمه پرکاربرد\n• تمرین جملات روزمره\n• استفاده از Duolingo یا Memrise\n• 15 دقیقه تمرین روزانه',
            'A2': '📚 برای پیشرفت:\n• تقویت زمان‌های گذشته و آینده\n• یادگیری 1000 کلمه مفید\n• تمرین مکالمات ساده\n• تماشای ویدیوهای آموزشی ساده\n• خواندن داستان‌های کوتاه',
            'B1': '📚 برای پیشرفت:\n• تسلط بر جملات شرطی\n• مطالعه مقالات ساده\n• گوش دادن به پادکست متوسط\n• نوشتن پاراگراف‌های کوتاه\n• مکالمه 20 دقیقه روزانه',
            'B2': '📚 برای پیشرفت:\n• تقویت ساختارهای پیچیده\n• مطالعه روزنامه و مجلات\n• تماشای سریال‌ها بدون زیرنویس\n• نوشتن مقالات کوتاه\n• شرکت در کلاس‌های مکالمه',
            'C1': '📚 برای تثبیت:\n• مطالعه ادبیات و متون آکادمیک\n• نوشتن مقالات تخصصی\n• شرکت در بحث‌های علمی\n• تدریس یا کمک به دیگران\n• استفاده روزانه در محیط کار',
            'C2': '📚 برای حفظ سطح:\n• مطالعه مداوم منابع پیشرفته\n• نوشتن و ارائه مطالب حرفه‌ای\n• تعامل با native speakers\n• تدریس در سطح پیشرفته\n• شرکت در کنفرانس‌های بین‌المللی'
        },
        'en': {
            'A1': '📚 To Improve:\n• Focus on basic grammar and simple verbs\n• Learn 500 common words\n• Practice daily phrases\n• Use Duolingo or Memrise\n• 15 minutes daily practice',
            'A2': '📚 To Improve:\n• Strengthen past and future tenses\n• Learn 1000 useful words\n• Practice simple conversations\n• Watch simple educational videos\n• Read short stories',
            'B1': '📚 To Improve:\n• Master conditional sentences\n• Read simple articles\n• Listen to intermediate podcasts\n• Write short paragraphs\n• 20 minutes daily conversation',
            'B2': '📚 To Improve:\n• Strengthen complex structures\n• Read newspapers and magazines\n• Watch series without subtitles\n• Write short essays\n• Join conversation classes',
            'C1': '📚 To Maintain:\n• Read literature and academic texts\n• Write professional articles\n• Participate in academic discussions\n• Teach or help others\n• Daily use in work environment',
            'C2': '📚 To Maintain:\n• Continuous reading of advanced sources\n• Write and present professional content\n• Interact with native speakers\n• Teach at advanced level\n• Participate in international conferences'
        }
    }
    
    result_text += recommendations[lang][user_level]
    
    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back_to_menu'), callback_data='back_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=result_text,
        reply_markup=reply_markup
    )
    
    user_data.reset_test(user_id)

async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = user_data.get_user(user_id)
    
    if not user['history']:
        await update.message.reply_text(get_text(user_id, 'no_history'))
        return
    
    lang = user.get('language', 'fa')
    history_text = "📜 " + ("تاریخچه آزمون‌های شما:" if lang == 'fa' else "Your Test History:") + "\n\n"
    
    for idx, test in enumerate(reversed(user['history'][-10:]), 1):
        level_info = CEFR_LEVELS[test['level']]
        history_text += f"{idx}. {test['date']}\n"
        history_text += f"   📊 " + (f"امتیاز: {test['score']}/100" if lang == 'fa' else f"Score: {test['score']}/100") + "\n"
        history_text += f"   🏆 " + (f"سطح: {test['level']} - {level_info['name_fa']}" if lang == 'fa' else f"Level: {test['level']} - {level_info['name_en']}") + "\n"
        history_text += f"   ✅ {test['correct']}/{test['total']}\n"
        history_text += f"   ⏱ " + (f"زمان: {test['time']}" if lang == 'fa' else f"Time: {test['time']}") + "\n\n"
    
    await update.message.reply_text(history_text)

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(get_text(user_id, 'help_text'))

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌐 Choose your language / زبان خود را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ خطایی رخ داد. لطفاً دوباره تلاش کنید.\n"
                "An error occurred. Please try again."
            )
    except:
        pass

def main():
    """راه‌اندازی ربات"""
    TOKEN = "8011292710:AAHS4cXdhGRM35itA6hfWhY4xJpg019cXiU"
    
    application = Application.builder().token(TOKEN).build()
    
    # دستورات
    application.add_handler(CommandHandler("start", start))
    
    # دکمه‌های callback
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # مدیریت خطا
    application.add_error_handler(error_handler)
    
    # شروع ربات
    print("🤖 ربات تعیین سطح زبان انگلیسی راه‌اندازی شد...")
    print("📋 آزمون 30 سوالی با زمان 30 دقیقه")
    print("✅ آماده دریافت درخواست...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()