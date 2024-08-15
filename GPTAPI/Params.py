from .prompts import (
    analyze_before, recommendations_before,
    recommendations_quick_quest, recommendations_about_character,
    recommendations_about_location
)

from .AnswerStructure import *


class AnalyzeBF:
    type = 'analyzeBF'

    structure = BeforeGameAnalysis

    def __init__(self,
                 indication: str =
                 '''
                 Ты помощник по игре в настольную игру D&D. 
                 На вход тебе даётся таблица, которую ты должен проанализировать.
                 После чего выдать краткие сводки по её анализу.
                 ''',

                 setting_indication: str = '',
                 num_indication: str = '',
                 npc_enemy_indication: str = ''
                 ):
        self.indication = indication
        self.setting_indication = setting_indication
        self.num_indication = num_indication
        self.npc_enemy_indication = npc_enemy_indication

    async def comb(self):
        return {
            "role": "system",
            "content":
                f'''
                {self.indication}\n
                {analyze_before.substitute(
                    setting_indication=f'Указание: {self.setting_indication}',
                    num_indication=f'Указание: {self.num_indication}',
                    npc_enemy_indication=f'Указание: {self.npc_enemy_indication}'
                )}
                '''

        }


class RecommendationsBF:
    type = 'recommendationsBF'

    structure = BeforeGameRecommendations

    def __init__(self,
                 indication: str =
                 '''
                 Ты помощник по игре в настольную игру D&D. 
                 На основе этих данных собери общий сеттинг игры
                 продумай сюжет, локации и героев.
                 ''',

                 setting_indication: str = '',
                 beginning_indication: str = '',
                 story_itself_indication: str = '',
                 endings_indication: str = '',
                 location_indication: str = '',
                 npc_indication: str = '',
                 enemy_indication: str = '',
                 uniq_indication: str = '',
                 ):
        self.indication = indication
        self.setting_indication = setting_indication
        self.beginning_indication = beginning_indication
        self.story_itself_indication = story_itself_indication
        self.endings_indication = endings_indication
        self.location_indication = location_indication
        self.npc_indication = npc_indication
        self.enemy_indication = enemy_indication
        self.uniq_indication = uniq_indication

    async def comb(self):
        return {
            "role": "system",
            "content":
                f'''
                {self.indication}\n
                {recommendations_before.substitute(
                    setting_indication=f'Указание: {self.setting_indication}',
                    beginning_indication=f'Указание: {self.beginning_indication}',
                    story_itself_indication=f'Указание: {self.story_itself_indication}',
                    endings_indication=f'Указание: {self.endings_indication}',
                    location_indication=f'Указание: {self.location_indication}',
                    npc_indication=f'Указание: {self.npc_indication}',
                    enemy_indication=f'Указание: {self.enemy_indication}',
                    uniq_indication=f'Указание: {self.uniq_indication}'
                )}
                '''
        }


class RecommendationsQQ:
    type = 'recommendationsQQ'

    structure = QuickQuestRecommendations

    def __init__(self,
                 indication: str =
                 '''
                 Ты помощник по игре в настольную игру D&D. 
                 На основе введённых данных, а именно,
                 сеттинга, сюжета, локаций, NPC, врагов, уникальных NPC и врагов
                 придумай несколько интересных и подробно описанных квестов.
                 ''',

                 quest_name_indication: str = '',
                 npc_indication: str = '',
                 enemy_indication: str = '',
                 location_indication: str = '',
                 description_indication: str = '',
                 rewards_indication: str = ''
                 ):
        self.indication = indication
        self.quest_name_indication = quest_name_indication
        self.npc_indication = npc_indication
        self.enemy_indication = enemy_indication
        self.location_indication = location_indication
        self.description_indication = description_indication
        self.rewards_indication = rewards_indication

    async def comb(self):
        return {
            "role": "system",
            "content":
                f'''
                {self.indication}\n
                {recommendations_quick_quest.substitute(
                    quest_name_indication=f'Указание: {self.quest_name_indication}',
                    npc_indication=f'Указание: {self.npc_indication}',
                    enemy_indication=f'Указание: {self.enemy_indication}',
                    location_indication=f'Указание: {self.location_indication}',
                    description_indication=f'Указание: {self.description_indication}',
                    rewards_indication=f'Указание: {self.rewards_indication}'
                )}
                '''
        }


class RecommendationsAC:
    type = 'recommendationsAC'

    structure = AboutCharacter

    def __init__(self,
                 indication: str =
                 '''
                 Ты помощник по игре в настольную игру D&D. 
                 На основе введённых данных, а именно,
                 сеттинга, типа персонажа, рассы, имени, описания, списка локаций,
                 где встречается персонаж, придумай его подробное описание
                 с примерами диалогов с ним.
                 ''',

                 type_indication: str = '',
                 name_indication: str = '',
                 appearance_indication: str = '',
                 personality_indication: str = '',
                 description_indication: str = '',
                 phrases_indication: str = ''
                 ):
        self.indication = indication
        self.type_indication = type_indication
        self.name_indication = name_indication
        self.appearance_indication = appearance_indication
        self.personality_indication = personality_indication
        self.description_indication = description_indication
        self.phrases_indication = phrases_indication

    async def comb(self):
        return {
            "role": "system",
            "content":
                f'''
                {self.indication}\n
                {recommendations_about_character.substitute(
                    type_indication=f'Указание: {self.type_indication}',
                    name_indication=f'Указание: {self.name_indication}',
                    appearance_indication=f'Указание: {self.appearance_indication}',
                    personality_indication=f'Указание: {self.personality_indication}',
                    description_indication=f'Указание: {self.description_indication}',
                    phrases_indication=f'Указание: {self.phrases_indication}'
                )}
                '''
        }


class RecommendationsLOC:
    type = 'recommendationsLOC'

    structure = AboutLocation

    def __init__(self,
                 indication: str =
                 '''
                 Ты помощник по игре в настольную игру D&D. 
                 На основе введённых данных, а именно,
                 общего сеттинга игры, названия и описания, локации,
                 придумай подробное описание этой локации.
                 ''',

                 name_indication: str = '',
                 appearance_indication: str = '',
                 description_indication: str = '',
                 ):
        self.indication = indication
        self.name_indication = name_indication
        self.appearance_indication = appearance_indication
        self.description_indication = description_indication

    async def comb(self):
        return {
            "role": "system",
            "content":
                f'''
                {self.indication}\n
                {recommendations_about_location.substitute(
                    name_indication=f'Указание: {self.name_indication}',
                    appearance_indication=f'Указание: {self.appearance_indication}',
                    description_indication=f'Указание: {self.description_indication}',
                )}
                '''
        }
