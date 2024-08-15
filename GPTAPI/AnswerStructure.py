from pydantic import BaseModel


class BeforeGameAnalysis(BaseModel):
    class Setting(BaseModel):
        type: str
        justification: str
        those_num: int

    class EnemyNPC(BaseModel):
        type: str
        justification: str

    class PurposeGame(BaseModel):
        type: str
        justification: str

    settings: list[Setting]
    gameplay_style: str
    npc_number: str
    days_duration: int
    session_duration: int
    enemy_npc: list[EnemyNPC]
    ambient: str
    location_number: int
    purpose_game: list[PurposeGame]


class BeforeGameRecommendations(BaseModel):
    class Ending(BaseModel):
        type: str
        description: str

    class Location(BaseModel):
        name: str
        description: str

    class Character(BaseModel):
        type: str
        name: str
        description: str
        locations: list[str]

    setting: str
    beginning: str
    story_itself: str
    endings: list[Ending]
    locations: list[Location]
    npcs: list[Character]
    enemies: list[Character]
    bosses_heroes: list[Character]


class QuickQuestRecommendations(BaseModel):
    class Character(BaseModel):
        type: str
        name: str
        description: str

    class Reward(BaseModel):
        name: str
        description: str

    quest_name: str
    npcs: list[Character]
    enemies: list[Character]
    location: str
    description: str
    rewards: list[Reward]


class AboutCharacter(BaseModel):
    class Phrase(BaseModel):
        theme: str
        phrase: str

    type: str
    gender: str
    name: str
    appearance: str
    kandinsky_appearance: str
    personality: list[str]
    description: str
    phrases: list[Phrase]


class AboutLocation(BaseModel):
    name: str
    appearance: str
    kandinsky_appearance: str
    description: str
