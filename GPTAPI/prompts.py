from string import Template


analyze_before_str = '''
Вот структура ответа:
- settings: список наиболее популярных по данным таблицы сеттингов с указанием их преимуществ и числа человек, которые их выбрали. $setting_indication
- npc_number: наиболее популярный вариант количества NPC в игре.
- days_duration: число - оптимальная длительность игры в днях. $num_indication
- session_duration: число - оптимальная длительность сессии игры в часах. $num_indication
- enemy_npc: список наиболее популярных типов NPC и врагов и указанием их преимуществ. $npc_enemy_indication
- ambient: Самый популярный ответ.
- location_number: число - оптимальное количество локаций в игре. $num_indication
- purpose_game: список наиболее распространённых целей игры с указанием потенциальной причины их выбора.
'''
analyze_before = Template(analyze_before_str)


recommendations_before_str = '''
Вот структура ответа:
- settings: общий сеттинг игры. $setting_indication
- beginning: начало сюжета игры. $beginning_indication
- story_itself: развитие сюжета игры. $story_itself_indication
- endings: список концовок игры – позитивной, нейтральной, негативной. $endings_indication
- locations: список локаций с их названием и описанием. $location_indication
- npcs: список NPC, помогающих в прохождении игры, c описанием расы, имени или клички, особенностей и способностей NPC, списка локаций где он встречается. $npc_indication
- enemies: список врагов, усложняющих прохождении игры, c описанием расы, имени или клички, особенностей и способностей врага, списка локаций где он встречается. $enemy_indication
- bosses_heroes: список из нескольких уникальных NPC и врагов с указанием для каждого расы, имени или клички, особенностей и способностей, списка локаций, где он встречается. $uniq_indication
'''
recommendations_before = Template(recommendations_before_str)


recommendations_quick_quest_str = '''
Вот структура ответа:
- quest_name: название квеста. $quest_name_indication
- npcs: список NPC, состоящий из одного или более NPC, задействованных в квесте, c описанием расы, имени или клички, особенностей и способностей NPC, списка локаций где он встречается. $npc_indication
- enemies: список врагов, состоящий из одного или более врагов, задействованных в квесте, c описанием расы, имени или клички, особенностей и способностей врага, списка локаций где он встречается. $enemy_indication
- location: название локации, в которой происходит квест. $location_indication
- description: описание квеста и действий, необходимых для его прохождения. $description_indication
- rewards: список наград, получаемых за выполнение квеста, с описанием названия, особенностей и предыстории. $rewards_indication
'''
recommendations_quick_quest = Template(recommendations_quick_quest_str)


recommendations_about_character_str = '''
Вот структура ответа:
- type: раса персонажа. $type_indication
- gender: пол персонажа выбранный и следующего списка [Мужской, Женский, Бесполый]
- name: имя персонажа. $name_indication
- appearance: подробное описание внешнего вида персонажа. $appearance_indication
- kandinsky_appearance: описание изображения верхней части тела персонажа, с упоминанием значений параметров type, gender, но без упоминания парметра name, основанное на параметре appearance в одном предложении. Указание: Необходимо описать фон, на котором находится персонаж. Указание: kandinsky_appearance должен быть написан на английском языке.
- personality: список качеств персонажа с большой буквы. $personality_indication
- description: описание персонажа и его роли внутри игры. $description_indication
- phrases: список фраз с их тематикой (тематика с маленькой буквы) и самой фразой, стилизованной под персонажа. $phrases_indication
'''
recommendations_about_character = Template(recommendations_about_character_str)


recommendations_about_location_str = '''
Вот структура ответа:
- name: название локации. $name_indication
- appearance: подробное описание внешнего вида локации. $appearance_indication
- kandinsky_appearance: краткое сухое описание внешнего вида локации с основными характеристиками в 1 предложении, основанное на параметре appearance. Указание: kandinsky_appearance должен быть написан на английском языке.
- description: описание локации и её роли внутри игры. $description_indication
'''
recommendations_about_location = Template(recommendations_about_location_str)
