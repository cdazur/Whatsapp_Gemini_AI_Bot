import google.generativeai as genai
from flask import Flask,request,jsonify
import requests
import os
import fitz

wa_token=os.environ.get("WA_TOKEN")
genai.configure(api_key=os.environ.get("GEN_API"))
phone_id=os.environ.get("PHONE_ID")
phone=os.environ.get("PHONE_NUMBER")
name="AZA" #The bot will consider this person as its owner or creator
bot_name="SVS WAG" #This will be the name of your bot, eg: "Hello I am Astro Bot"
model_name="gemini-2.0-flash" #Switch to "gemini-1.0-pro" or any free model, if "gemini-1.5-flash" becomes paid in future.

app=Flask(__name__)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_MEDIUM_AND_ABOVE"},  
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name=model_name,
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])

# convo.send_message(f'''I am using Gemini api as a customer service bot in whatsapp,
# 				   to support contacts in questions about my services: 
# 				   So from now you are "{bot_name}" created by {name} ( Yeah it's me, my name is {name}). 
# 				   And don't give any response to this prompt. 
# 				   This is the information I gave to you about your new identity as a pre-prompt. 
# 				   This message always gets executed when i run this bot script. 
# 				   So reply to only the prompts after this. Remeber your new identity is {bot_name}.''')

convo.send_message(f"""
Я использую API Gemini в качестве бота службы поддержки в WhatsApp, чтобы помогать контактам с вопросами о моих услугах.
Ты "{bot_name}", созданный {name}.  Твоя задача - отвечать на вопросы о клинике изучения Эпилепсии, используя *только* предоставленную ниже информацию.  Если вопрос выходит за рамки этой информации, пожалуйста, сообщи, что это информация из интернета.
И не отвечай на этот запрос.
Это информация, которую я предоставил тебе о твоей новой личности в качестве пре-подсказки.
Это сообщение всегда выполняется при запуске скрипта этого бота.
Поэтому отвечай только на запросы после этого. Помни, твоя новая личность - {bot_name}.
***
Клиника изучения Эпилепсии
г. Алматы
(бывшая SVS клиника имени С.В. Савинова, лаборатория изучения эпилепсии и судорожных состояний имени С.В. Савинова)
Клиника изучения эпилепсии - это медицинский центр, занимающийся исследованиями, диагностикой и лечением эпилепсии.
Нужен грамотный эпилептолог в Алматы, дающий результат? Ищете невролога, нейрохирурга, психиатра? У нас работают сильнейшие специалисты.
Нужен видео ЭЭГ мониторинг экспертного уровня?
Добро пожаловать к нам на сайт, ознакомьтесь с отзывами о нас, прочтите наши статьи и убедитесь во всем сами!

Предлагаем следующие виды услуг:
Видео ЭЭГ мониторинг
•	3х часовой
•	дневной
•	ночной
•	суточный
•	выездной
Консультации специалистов
•	Невролог-эпилептолог
•	Нейрохирург
•	Психиатр
•	Логопед-дефектолог
Широкий спектр анализов
Наши ВРАЧИ:
Плотников Василий Сергеевич - Врач невролог-эпилептолог
Гизатуллин Марат Римович - Врач нейрохирург
Шеин Павел Владиславович - Психиатр, Психотерапевт

Заметки и статьи врачей, мед персонала клиники:

Препараты, запрещенные при эпилепсии
Какие лекарства (препараты) нельзя принимать при эпилепсии?
Понятие абсолютного запрета здесь неприменимо и данные препараты при определенных условиях могут быть использованы при эпилепсии.
Однако стоит проявлять предосторожность, следуя предостережениям в инструкции к препарату и обсудив возможность их замены с врачом, который их назначил.

Читать статью на казахском языке Эпилепсия кезінде тыйым салынған препараттар
Данный перечень, конечно, не может заменить актуализированных инструкций к препаратам.

Всегда проверяйте в инструкции наличие противопоказаний, особых указаний и взаимодействий с другими лекарствами, чтобы убедиться, что оно Вам подходит.

При этом, пользуясь как инструкцией, так и этим перечнем искать нужно не по торговому названию препарата, например "Депакин", а по действующему веществу - вальпроевая кислота.

Итак, вот собственно сам перечень.

Противоинфекционные препараты
Антибиотики (пенициллиновые - например, пенициллин, амоксициллин, цефалоспориновые - цефазолин, цефтриаксон, карбапенемы - меропенем, имипенем) – редко и при высоких дозах
Метронидазол, хлорамфеникол
Противотуберкулезные антибиотики – изониазид (риск снижается при добавлении пиридоксина)
Противомалярийные (хлорохин, мефлохин)
Анальгетические препараты
Опиоидные (морфин, трамадол, петидин, фентанил, кодеин)
Кокаин провоцирует особую разновидность приступов за счет активации норадренергической и дофаминергической систем в амигдале – купируются пиридоксином, хлорпромазином, резерпином.
Новокаин, лидокаин, бупивакаин.
Неопиоидные анальгетики – индометацин, мефенамовая кислота
Неврологические и психиатрические препараты
Симпатомиметики - адреналин, эфедрин.
Антиэпилептические препараты – все в токсичных дозах и при неправильной резкой отмене, а в рабочих дозах - карбамазепин, окскарбазепин – в отношении миоклоний, абсансов и при некоторых формах эпилепсии могут способствовать озлокачествлению эпилепсии в целом.
Антипсихотики – клозапин, в меньшей степени – оланзапин, рисперидон, затем арипиразол, галоперидол. Однако иногда возникает неизбежная необходимость их использования, поскольку прямой замены им нет среди других препаратов, и при купировании психотических состояний в таком случае предпочтение можно отдавать рисперидону, арипиразолу, галоперидолу.
Антидепрессанты – бупропион, в высоких дозах – трициклики (амитриптилин, нортриптилин).
Дисульфирам (используется для кодирования от алкогольной зависимости)
Кофеин
Психостимуляторы
Пирацетам при внутривенном введении
Остальные препараты с отмеченным эффектом провокации судорог
Метилксантины – теофиллин, аминофиллин
Алкоголь – при отмене
С острожностью антигистаминные
С осторожностью метоклопамид (противорвотное)
Интратекальное введение (в оболочку спинного мозга) антибиотиков, баклофена, цитостатиков, констраста.
Злоупотребление наркотиками (особенно - кокаин, героин, ЛСД)
Сердечные гликозиды, циклоспорин, простагландины
Инфузии (избыток жидкости)
Инсулин, аспирин - при передозировке
Препараты для наркоза - смотрите подробнее в отдельной статье на сайте.
Так же не забудьте ознакомиться со статьей о лекарственных взаимодействиях наиболее часто применяемых препаратов.

Автор: врач Клиники эпилептологии имени Савинова
невролог-эпилептолог Плотников Василий Сергеевич.

Подготовка к операции при эпилепсии
Поставлен диагноз эпилепсия и предстоит операция?
Врачи боятся брать на операционный стол или сами переживаете на этот счет?
Пациенты с эпилепсией часто подвергаются риску неоправданного отказа в оперативном вмешательстве. Эта статья призвана развенчать опасения хирургов, врачей-анестезиологов и ее можно показать Вашим врачам, для того, чтобы они могли соблюсти все необходимые предостережения и знали, какой наркоз необходимо выбирать в первую очередь, чего необходимо избегать и какие предостережения имеют под собой реальную основу, а какие представляют собой миф. Имея данную статью на руках, Вы и сами получаете инструмент для оценки и предотвращения возможных рисков.

Потенциальные проблемы, связанные с операцией

Умение персонала оказать помощь в случае приступа
Провокация приступов стрессом, самой операцией, наркозом
Межлекарственные взаимодействия
Пропуск приема АЭП
Необходимость диффференцировки приступов с неэпилептическими судорожными состояниями (обмороки, брадикардия)

Что предпринимаем?

Избегаем уже известные нам провоцирующие факторы
За 4 дня до операции категорически запрещен алкоголь!
Не пропускаем препараты! В крайнем случае возможно внутривенное или ректальное введение препарата, используем структурные аналоги (например, фенобарбитал и тиопентал)
Попросить проверить количество тромбоцитов перед операцией в случае приема фенитоина, вальпроата, карбамазепина.
Попросить снотворное накануне операции – для избежания бессонницы (лишение сна - провоцирующий приступ фактор)

Премедикация и обезболивание перед операцией

Тучным пациентам или с ГЭРБ – требуются ингибиторы протонной помпы, метоклопрамид – с осторожностью при эпилепсии
Пациентам на кетогенной диете – предупредить, чтоб мониторировали глюкозу крови и не вводили глюкозу внутривенно. Также - мониторировать рН крови
Если в анамнезе уже были приступы после выхода из наркоза – рекомендовано увеличение дозы противоэпилептических препаратов перед операцией, также назначение бензодиазепинов составе наркоза.

Теперь поговорим отдельно о различных группах препаратов...

Ингаляционные анестетики
Энфлуран – самый опасный (избегать высоких концентраций – не более 1-1,5 %!) Не сочетать с индуцированной гипервентиляцией! Потенциально плохо сочетается с тиопенталом и диазепамом (на удивление), но допустимо сочетание с закисью азота.
Потенциально опасен также севофлуран, особенно у детей до 5 лет (при взаимодействии с закисью азота, тиопенталом, мидазоламом становится меньше эпиактивности)
Более безопасны – изофлуран и десфлуран
Наименее опасный – галотан (описана провокация приступов при комбинации с закисью азота)
Закись азота сама по себе не провоцирует приступы, а при неудачных сочетаниях (см. выше)
Внутривенные анестетики

Барбитураты – в низких дозах могут провоцировать, в высоких – обладают противосудорожным эффектом
Тиопентал – используется безопасно для индукции в наркоз
Метогекситал – в низких дозах может провоцировать приступы и эпиактивность при фокальной эпилепсии, используется в тесте подавления при ВБС в электрокортикографии
Этомидат – чаще провоцирует миоклонии неэпилептического характера.
Бензодиазепины – противосудорожный эффект
Опиаты – чаще провоцируют неэпилептические двигательные реакции, в высоких дозах могут провоцировать эпиприступы
Кетамин – провоцирует приступы и эпиактивность
Пропофол – очень мощный антиконвульсант, иногда помогает при резистентном эпилептическом статусе, когда другие препараты не помогают. Но !! в низких дозах может провоцировать приступы и в течение 7-23 дней после операции могут возникать приступы после его использования.

Местная анестезия

Лидокаин – низкие дозы – антиконвульсивный эффект. В больших – провоцирует приступы, которые лечатся барбитуратами.
Бупивакаин в высоких дозах (более 4 мг\мл) потенциально провоцирует приступы.
Новокаин (прокаин) – в низких дозах – антиконсульсивные свойства, в высоких (18-29 мг\кг) – провоцирует судороги, которые лечатся тиопенталом.

Адъювантная терапия к наркозу

АХЭ, холиноблокаторы, миорелаксанты, аспирин, парацетамол, ибупрофен – ни один из препаратов не провоцирует эпиактивность.



Автор статьи Плотников Василий Сергеевич, врач Клиники имени С.В.Савинова.

Оперативное реагирование через +7-700-912-52-49
Детская и взрослая эпилептология, кетогенная диета, нейрохирургическая и психиатрическая помощь.
По акции есть услуга - бесплатная консультация эпилептолога.
ПИШИТЕ НАМ НА WhatsApp для более оперативной записи на прием напрямую через администратора клиники!

ЦЕНЫ НА АНАЛИЗЫ
Вальпроевая кислота (1 забор) 7000 тенге
Карбамазепин (финлепсин) 1 забор 12000 тенге
Ламотриджин (ламиктал) (1 забор) 18000 тенге
Левитирацетам(кеппра, эпикс) (1 забор) 18000 тенге
Топиромат (топамакс) (1 забор)18000 тенге

О клинике!
Привлекая мировое внимание к борьбе с эпилепсией...
Клиника изучения эпилепсии - это одна из ведущих медицинских организаций, посвященных исследованию и лечению эпилепсии в Казахстане. Названная в честь выдающегося эпилептолога Савинова Сергея Викторовича, клиника проделывает важную работу по повышению осведомленности о данном неврологическом заболевании и разработке современных методов медикаментозного и физиотерапевтического.
История и предназначение
Клиника была основана в 2005 году и с тех пор активно работает над исследованиями, диагностикой и лечением эпилепсии. В клинике собран сильный исследовательский коллектив, состоящий из врачей - невролога, нейрохирурга, психиатра, которые постоянно стремятся к развитию новых технологий и подходов к лечению эпилепсии и сопутствующей неврологической патологии.
Основными целями клиники являются:
Предоставление комплексного диагностического обследования пациентов с эпилепсией.
Эффективное лечение пациентов на всех этапах болезни.
Строгое следование международным научным подходам, избегание назначения разрекламированных в странах СНГ неэффективных препаратов, избегание полипрагмазии
Разработка и внедрение новых подходов к лечению эпилепсии.
Поддержка пациентов и создание условий для улучшения их качества жизни.
Анализ и, при необходимости, исправление неточностей на предыдущих этапах лечения
Уровень экспертности
Клиника изучения эпилепсии имени Савинова С.В. известна своим высоким уровнем экспертности в исследованиях и лечении эпилепсии. Ее команда специалистов использует современные диагностические и лечебные методы, включая консультации невролога, эпилептолога, нейрохирурга, психиатра, исследование неврологического, психического статуса, электроэнцефалографию (ЭЭГ), лабораторный мониторинг эффективности и безопасности принимаемой терапии, генетические исследования крови, и другие распространённые технологии.
Занимается лечением пациентов любых возрастов, начиная с самых маленьких детей и включая также людей пожилого возраста.
Осуществляется ведение беременности при эпилепсии.
Ведение пациентов на кетогенной диете.
Большое внимание уделяется индивидуальному подходу к каждому пациенту. Клиника работает над разработкой оптимальных программ лечения, исходя из особенностей заболевания и потребностей пациента. Команда специалистов стремится к достижению максимальных результатов и улучшению качества жизни пациентов, минимизируя частоту эпилептических приступов и их последствия.
Развитие научных исследований
Клиника активно участвует в научных исследованиях, связанных с эпилепсией. Их целью является разработка новых стратегий лечения данного заболевания. Кроме того, клиника тесно сотрудничает с другими медицинскими учреждениями и университетами, как в Казахстане, так в России и Германии, для обмена знаниями и опытом.
Благодаря этой активности исследователи и клиницисты из клиники имени Савинова С.В. привлекают внимание как национального, так и международного сообщества. Это способствует развитию и социальной значимости их работы, а также укрепляет клинику в качестве лидера в области эпилептологии.

Казахстан, город Алматы
WhatsApp: +7-700-912-52-49
Телефон: +727-317-83-73
E-mail: svs.klinikasavinova@mail.ru


ЭЭГ мониторинг в клинике савинова.
доверяя здоровье экспертам!
Живете в Алматы или в другом городе Казахстана и ищете, где лучше сделать длительный видео-ЭЭГ мониторинг (ночная ЭЭГ сна)? Ответ на этот вопрос уже выведен временем. В статье постараемся разобраться, почему многие специалисты неврологи рекомендуют делать ЭЭГ именно в клинике Савинова и чем отличается ЭЭГ в других клиниках.
Видео-ЭЭГ мониторинг
Заботливый невролог и эпилептолог
Прогрессивный психиатр-психотерапевт
Оперирующий нейрохирург эксперт-класса
Преданный делу логопед-дефектолог
Несколько слов в качестве вступления...
Доверить свое здоровье можно не каждому специалисту и не каждой клинике, даже в Алматы. Еще начиная со времен, когда был жив один из основателей клиники Савинов С.В. мы всегда являлись тем местом, где задерживались только реально экспертные сотрудники. Репутация была и есть для нас важнее числа.

В конце концов, можно пожертвовать перспективой расширения клиники, продвижению всего многообразия возможных коммерческих услуг ради удержания максимального уровня качества оказания помощи и реализации ожиданий и надежд наших пациентов.

Поэтому мы до сих пор являемся уютной клиникой без шумных толп людей, суеты, не работаем на поток, а работаем на результат. Каждый пациент - для нас как Гость. Говорим без преувеличения. Именно поэтому мы не открывали и никогда не планировали открывать филиалы. Все филиалы, именующие себя клиникой Савинова в других городах - ненастоящие. Клиника Савинова только одна и располагается по адресу улица Мамытова 77 (до переезда мы располагались неподалеку, в здании по улице Мамытова 99).

Преимущества выполнения ЭЭГ-мониторинга в клинике-эксперт класса:

1. В нашем Центре ЭЭГ расшифровывают опытные и ответственные доктора, всегда следящие за своей репутацией и репутацией Клиники и не ставящие себе целью прочесть максимальное число ЭЭГ на скорую руку и побыстрей уехать домой. Опять же, со времен жизни Савинова, тот врач, который смотрит ЭЭГ, смотрит и пациента, что повышает чувство вовлеченности и ответственности. Это принцип остался неизменным все это время и это самый эффективный способ лечения больных с эпилепсией. Так, глядя, на положительную динамику своего пациента на ЭЭГ на фоне лечения врач вдохновляется дальше работать на максимуме своих возможностей, постоянно совершенствуясь.

2. Вам или Вашему родному человеку будут качественно (по международно утвержденным стандартам) будут наложены электроды, поскольку у нас работают только профессионалы, то исключена возможность ошибки, путаницы при наложении электродов.

3. Накладываем одиночные электроды вручную! Еще со времен жизни Савинова С.В. мы не признаем накладываемые в других местах шапочки, поскольку:
- Во-первых, не будет возникать необходимости будить пациента каждые полчаса-час и доливать ему гель под электрод. Используемые к нашей клинике электроды позволяют оставлять пациента на целую ночь в покое, не заставляя его просыпаться несколько раз, чтобы долить гель из шприца.
- Во вторых, плохое прилегание электродов (снова спасибо попыткам универсализации пациентов - якобы все должны соответствовать одному мерилу) - из-за этого от некоторых отведений чаще пропадает сигнал, из-за чего можно пропустить эпилептический разряд или неправильно определить место, из которого он возникает, а это может, на-секундочку, привести к операции на голове в неправильно выбранной области.
- В третьих, голова у каждого человека индивидуальна, шапочка идеально соответствует форме головы у небольшого процента пациентов и дает заметное искажение топографических результатов.
- Наконец, синтетический материал электродной шапочки нарушает теплообмен и неестественен для кожи - в нем неприятно долго находится, а детям бывает трудно в нем заснуть. Также в нем чаще возникает головная боль за счет сдавления подкожных мышц скальпа черепа, что приводит к их спазму и голова начинает болеть так сильно, что продолжать исследование становится невозможно. Практикуемые нами бинты/эластичные бинты, наложенные на одиночные электроды, не оказывают такого сильного сдавливающего эффекта и их степень натяжения можно регулировать.

4. В клинике уютно - нет большого количества народа, относятся дружелюбно, никогда не грубят и не решают свои личные проблемы, унижая других людей. Всегда учитываются интересы наших Гостей, за чем всегда лично следит директор Клиники.

5. Предоставлены основные удобства - ночлег для ночных ЭЭГ-исследований от 6 часов, в том числе одна отдельная кровать для родственника. В клинике имеется просторная полноценная кухня с посудой, холодильником, микроволновой печью, туалет для взрослых и детей, а также придомовая территория в зеленом окружении, уличный столик по типу летнего кафе. При необходимости детям предоставляются игрушки.

6. При прохождении консультации у нашего специалиста в нашей клинике результат практически всегда отдается сразу же на руки. Поскольку мы не работаем на поток, то даже тем, кто не идет далее на консультацию к нашему врачу так же удается ЭЭГ описывать вовремя, без задержек, чаще в течение 1 часа - 1 суток, если не выпадает на выходные дни.

7. Выполняем и описываем ЭЭГ всех видов и любой сложности: ЭЭГ с функциональными пробами; ночной, суточный, многосуточный видео-ЭЭГ мониторинг сна; ЭЭГ с ЭКГ отведением; ЭЭГ новорожденным детям; реанимационный видео-ЭЭГ мониторинг, в том числе выездное длительное видео-ЭЭГ исследование (выезд по адресу или в больницу, реанимационное отделение).

8. Результаты нашего ЭЭГ признают все ведомства и страны.
Все доктора владеют английским, могут написать report для зарубежных учреждений.
Поэтому при необходимости предоставления результатов ЭЭГ за границу или в официальное ведомство, даже в военкомат, результаты будут приняты.


А что в других клиниках?
ЭЭГ в других клиниках описывают с разной степени качественности: мы встречали разное, вплоть до написания роботом (искусственным "интеллектом")!
Нередко видим как описывают снимки по старым советским методичкам, а не в соответствии с современными международными требованиями (и ладно если б разница была только в терминах, но не передается суть и перефразируются до неузнаваемости понятия и вообще представления о целях исследования). При этом мы сами, если к нам приходят люди только на ЭЭГ и наблюдаются в другом месте, стараемся отражать в заключении всю необходимую информацию, указывая также и степень представленности эпилептиформной активности по международным критериям, чтоб можно было отследить динамику результатов во времени, чего к нашему глубочайшему удивлению не делают в других центрах.
К тому же в других клиниках специалист, описывая ЭЭГ, не сопоставляет ее данные с клинической картиной пациента, из-за чего одно когнитивное искажение накладывается на другое, нет взаимной сверки данных (при исследовании разными людьми это сложно устранить, вот поэтому у нас ЭЭГ и пациента смотрит один и тот же специалист, имеющий сертификат невролога с нейрофизиологией по своей специализации).
Одно в отрыве от другого невозможно. Всегда помните, что ЭЭГ, как и УЗИ - это оператор-зависимая методика, 99% достоверности результатов зависит от специалиста и мы к сожалению наблюдали случаи, когда неправильно интерпретированная ЭЭГ приводила к неправильному диагнозу - и как следствие к неправильному лечению.
Специалист-эпилептолог, даже если Вы принесете ему диск с ЭЭГ из другого учреждения, не успеет в пределах консультации так же подробно его отсмотреть, как если бы описывал все исследование изначально самостоятельно, так как только сама консультация длится минимум час.
Поэтому наш эпилептолог признает более полезным проведение исследования именно в стенах нашего учреждения.
S.V.Savïnov atındağı emhana.

Клиника имени С.В. Савинова.

Эпилепсияны емдеу.
Успешно лечим эпилепсию с 2005 года
Клиника - Лидер эпилептологии в Казахстане
  """)

def send(answer):
    url=f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers={
        'Authorization': f'Bearer {wa_token}',
        'Content-Type': 'application/json'
    }
    data={
          "messaging_product": "whatsapp", 
          "to": f"{phone}", 
          "type": "text",
          "text":{"body": f"{answer}"},
          }
    
    response=requests.post(url, headers=headers,json=data)
    return response

def remove(*file_paths):
    for file in file_paths:
        if os.path.exists(file):
            os.remove(file)
        else:pass

@app.route("/",methods=["GET","POST"])
def index():
    return "Bot"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == "BOT":
            return challenge, 200
        else:
            return "Failed", 403
    elif request.method == "POST":
        try:
            data = request.get_json()["entry"][0]["changes"][0]["value"]["messages"][0]
            if data["type"] == "text":
                prompt = data["text"]["body"]
                convo.send_message(prompt)
                send(convo.last.text)
            else:
                media_url_endpoint = f'https://graph.facebook.com/v18.0/{data[data["type"]]["id"]}/'
                headers = {'Authorization': f'Bearer {wa_token}'}
                media_response = requests.get(media_url_endpoint, headers=headers)
                media_url = media_response.json()["url"]
                media_download_response = requests.get(media_url, headers=headers)
                if data["type"] == "audio":
                    filename = "/tmp/temp_audio.mp3"
                elif data["type"] == "image":
                    filename = "/tmp/temp_image.jpg"
                elif data["type"] == "document":
                    doc=fitz.open(stream=media_download_response.content,filetype="pdf")
                    for _,page in enumerate(doc):
                        destination="/tmp/temp_image.jpg"
                        pix = page.get_pixmap()
                        pix.save(destination)
                        file = genai.upload_file(path=destination,display_name="tempfile")
                        response = model.generate_content(["What is this",file])
                        answer=response._result.candidates[0].content.parts[0].text
                        convo.send_message(f"This message is created by an llm model based on the image prompt of user, reply to the user based on this: {answer}")
                        send(convo.last.text)
                        remove(destination)
                else:send("This format is not Supported by the bot ☹")
                with open(filename, "wb") as temp_media:
                    temp_media.write(media_download_response.content)
                file = genai.upload_file(path=filename,display_name="tempfile")
                response = model.generate_content(["What is this",file])
                answer=response._result.candidates[0].content.parts[0].text
                remove("/tmp/temp_image.jpg","/tmp/temp_audio.mp3")
                convo.send_message(f"This is an voice/image message from user transcribed by an llm model, reply to the user based on the transcription: {answer}")
                send(convo.last.text)
                files=genai.list_files()
                for file in files:
                    file.delete()
        except :pass
        return jsonify({"status": "ok"}), 200
if __name__ == "__main__":
    app.run(debug=True, port=8000)
