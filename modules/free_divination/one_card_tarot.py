from aiogram import F
from aiogram.types import Message, KeyboardButton, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from modules.profile.texts import get_text
from modules.database.db import get_user_language
import random
import os

# Полный список карт Таро
TAROT_CARDS = {
    "en": {
        # Старшие Арканы
        "The Fool": "New beginnings, spontaneity, and infinite potential.",
        "The Magician": "Manifestation, resourcefulness, and power.",
        "The High Priestess": "Intuition, mystery, and inner wisdom.",
        "The Empress": "Fertility, abundance, and nurturing energy.",
        "The Emperor": "Authority, structure, and leadership.",
        "The Hierophant": "Tradition, conformity, and spiritual guidance.",
        "The Lovers": "Love, relationships, and choices.",
        "The Chariot": "Victory, willpower, and determination.",
        "Strength": "Courage, inner strength, and compassion.",
        "The Hermit": "Soul searching, introspection, and solitude.",
        "Wheel of Fortune": "Change, cycles, and destiny.",
        "Justice": "Fairness, truth, and accountability.",
        "The Hanged Man": "Surrender, letting go, and new perspectives.",
        "Death": "Transformation, endings, and rebirth.",
        "Temperance": "Balance, moderation, and harmony.",
        "The Devil": "Bondage, materialism, and temptation.",
        "The Tower": "Sudden upheaval, destruction, and revelation.",
        "The Star": "Hope, inspiration, and renewal.",
        "The Moon": "Illusion, fear, and the subconscious.",
        "The Sun": "Success, joy, and vitality.",
        "Judgement": "Rebirth, awakening, and transformation.",
        "The World": "Completion, fulfillment, and wholeness.",

        # Младшие Арканы
        "Ace of Cups": "Emotional beginnings, love, and creativity.",
        "Two of Cups": "Partnership, harmony, and connection.",
        "Three of Cups": "Celebration, friendship, and community.",
        "Four of Cups": "Apathy, contemplation, and missed opportunities.",
        "Five of Cups": "Loss, regret, and disappointment.",
        "Six of Cups": "Nostalgia, memories, and healing.",
        "Seven of Cups": "Choices, illusions, and wishful thinking.",
        "Eight of Cups": "Leaving behind, moving on, and seeking truth.",
        "Nine of Cups": "Satisfaction, contentment, and fulfillment.",
        "Ten of Cups": "Harmony, happiness, and emotional fulfillment.",
        "Page of Cups": "Emotional exploration, creativity, and sensitivity.",
        "Knight of Cups": "Romance, charm, and emotional expression.",
        "Queen of Cups": "Compassion, intuition, and emotional depth.",
        "King of Cups": "Emotional balance, control, and wisdom.",

        # Жезлы (Wands)
        "Ace of Wands": "Inspiration, potential, and new beginnings.",
        "Two of Wands": "Planning, future prospects, and decisions.",
        "Three of Wands": "Expansion, foresight, and exploration.",
        "Four of Wands": "Celebration, homecoming, and stability.",
        "Five of Wands": "Conflict, competition, and challenges.",
        "Six of Wands": "Victory, success, and recognition.",
        "Seven of Wands": "Defense, perseverance, and standing your ground.",
        "Eight of Wands": "Movement, progress, and swift action.",
        "Nine of Wands": "Resilience, persistence, and inner strength.",
        "Ten of Wands": "Burden, responsibility, and hard work.",
        "Page of Wands": "Exploration, freedom, and enthusiasm.",
        "Knight of Wands": "Adventure, passion, and boldness.",
        "Queen of Wands": "Confidence, charisma, and independence.",
        "King of Wands": "Visionary leadership, courage, and authority.",

        # Мечи (Swords)
        "Ace of Swords": "Clarity, breakthrough, and mental power.",
        "Two of Swords": "Stalemate, indecision, and compromise.",
        "Three of Swords": "Heartbreak, sorrow, and emotional pain.",
        "Four of Swords": "Rest, recovery, and contemplation.",
        "Five of Swords": "Conflict, defeat, and betrayal.",
        "Six of Swords": "Transition, moving on, and leaving the past.",
        "Seven of Swords": "Deception, trickery, and hidden motives.",
        "Eight of Swords": "Restriction, entrapment, and self-imposed limits.",
        "Nine of Swords": "Anxiety, fear, and nightmares.",
        "Ten of Swords": "Betrayal, crisis, and rock bottom.",
        "Page of Swords": "Curiosity, intellect, and sharp thinking.",
        "Knight of Swords": "Action, ambition, and haste.",
        "Queen of Swords": "Wisdom, clarity, and direct communication.",
        "King of Swords": "Authority, intellect, and fairness.",

        # Пентакли (Pentacles)
        "Ace of Pentacles": "Opportunity, prosperity, and new ventures.",
        "Two of Pentacles": "Balance, adaptability, and multitasking.",
        "Three of Pentacles": "Teamwork, collaboration, and skill.",
        "Four of Pentacles": "Stability, possession, and conservatism.",
        "Five of Pentacles": "Hardship, poverty, and isolation.",
        "Six of Pentacles": "Generosity, charity, and sharing.",
        "Seven of Pentacles": "Patience, investment, and long-term results.",
        "Eight of Pentacles": "Dedication, craftsmanship, and mastery.",
        "Nine of Pentacles": "Luxury, independence, and self-sufficiency.",
        "Ten of Pentacles": "Wealth, legacy, and family.",
        "Page of Pentacles": "Opportunity, ambition, and practicality.",
        "Knight of Pentacles": "Responsibility, diligence, and routine.",
        "Queen of Pentacles": "Nurturing, comfort, and abundance.",
        "King of Pentacles": "Wealth, security, and leadership.",
    },
    "ru": {
        # Старшие Арканы
        "Шут": "Новые начинания, спонтанность, безграничный потенциал.",
        "Маг": "Манифестация, находчивость, сила.",
        "Жрица": "Интуиция, тайна, внутренняя мудрость.",
        "Императрица": "Плодородие, изобилие, забота.",
        "Император": "Авторитет, структура, лидерство.",
        "Иерофант": "Традиции, конформизм, духовное руководство.",
        "Влюблённые": "Любовь, отношения, выбор.",
        "Колесница": "Победа, воля, решимость.",
        "Сила": "Храбрость, внутренняя сила, сострадание.",
        "Отшельник": "Поиск души, самоанализ, уединение.",
        "Колесо Фортуны": "Изменения, циклы, судьба.",
        "Правосудие": "Справедливость, правда, ответственность.",
        "Повешенный": "Отказ, отпускание, новые перспективы.",
        "Смерть": "Преобразование, окончания, возрождение.",
        "Умеренность": "Баланс, умеренность, гармония.",
        "Дьявол": "Рабство, материализм, искушение.",
        "Башня": "Внезапные потрясения, разрушение, откровение.",
        "Звезда": "Надежда, вдохновение, обновление.",
        "Луна": "Иллюзии, страх, подсознание.",
        "Солнце": "Успех, радость, жизненная сила.",
        "Суд": "Возрождение, пробуждение, преобразование.",
        "Мир": "Завершение, исполнение, целостность.",

        # Младшие Арканы
        "Туз Чаш": "Эмоциональные начала, любовь, творчество.",
        "Двойка Чаш": "Партнёрство, гармония, связь.",
        "Тройка Чаш": "Праздник, дружба, сообщество.",
        "Четвёрка Чаш": "Апатия, размышления, упущенные возможности.",
        "Пятерка Чаш": "Потери, сожаление, разочарование.",
        "Шестёрка Чаш": "Ностальгия, воспоминания, исцеление.",
        "Семёрка Чаш": "Выбор, иллюзии, фантазии.",
        "Восьмёрка Чаш": "Перемены, оставление позади, поиск ясности.",
        "Девятка Чаш": "Удовлетворение, довольство, исполнение желаний.",
        "Десятка Чаш": "Гармония, семья, эмоциональное удовлетворение.",
        "Паж Чаш": "Эмоциональное исследование, творчество, любопытство.",
        "Рыцарь Чаш": "Романтика, очарование, эмоциональное выражение.",
        "Королева Чаш": "Эмоциональная глубина, интуиция, сострадание.",
        "Король Чаш": "Эмоциональный баланс, дипломатия, контроль.",

        "Туз Пентаклей": "Материальные начала, процветание, возможность.",
        "Двойка Пентаклей": "Баланс, адаптивность, жонглирование приоритетами.",
        "Тройка Пентаклей": "Командная работа, сотрудничество, мастерство.",
        "Четвёрка Пентаклей": "Стабильность, безопасность, удержание.",
        "Пятерка Пентаклей": "Трудности, бедность, изоляция.",
        "Шестёрка Пентаклей": "Щедрость, благотворительность, разделение богатства.",
        "Семёрка Пентаклей": "Терпение, настойчивость, долгосрочные цели.",
        "Восьмёрка Пентаклей": "Преданность, мастерство, развитие навыков.",
        "Девятка Пентаклей": "Независимость, роскошь, самодостаточность.",
        "Десятка Пентаклей": "Богатство, наследие, семейное процветание.",
        "Паж Пентаклей": "Практичность, амбиции, обучение.",
        "Рыцарь Пентаклей": "Ответственность, трудолюбие, усердие.",
        "Королева Пентаклей": "Забота, практичность, изобилие.",
        "Король Пентаклей": "Богатство, стабильность, лидерство.",

        "Туз Мечей": "Ясность, прорыв, умственная сила.",
        "Двойка Мечей": "Тупик, нерешительность, компромисс.",
        "Тройка Мечей": "Разбитое сердце, печаль, эмоциональная боль.",
        "Четвёрка Мечей": "Отдых, восстановление, размышления.",
        "Пятерка Мечей": "Конфликт, поражение, предательство.",
        "Шестёрка Мечей": "Переход, движение вперёд, исцеление.",
        "Семёрка Мечей": "Обман, стратегия, скрытые мотивы.",
        "Восьмёрка Мечей": "Ограничение, чувство ловушки, самоограничение.",
        "Девятка Мечей": "Тревога, страх, кошмары.",
        "Десятка Мечей": "Предательство, окончания, дно.",
        "Паж Мечей": "Любопытство, исследование, умственная гибкость.",
        "Рыцарь Мечей": "Действие, амбиции, поспешность.",
        "Королева Мечей": "Ясность, независимость, острый ум.",
        "Король Мечей": "Авторитет, логика, интеллектуальная сила.",

        "Туз Жезлов": "Вдохновение, страсть, новые начинания.",
        "Двойка Жезлов": "Планирование, будущие начинания, решения.",
        "Тройка Жезлов": "Расширение, исследование, прогресс.",
        "Четвёрка Жезлов": "Праздник, гармония, возвращение домой.",
        "Пятерка Жезлов": "Конфликт, соперничество, вызовы.",
        "Шестёрка Жезлов": "Победа, признание, успех.",
        "Семёрка Жезлов": "Защита, настойчивость, стояние на своём.",
        "Восьмёрка Жезлов": "Скорость, движение, быстрые действия.",
        "Девятка Жезлов": "Устойчивость, выносливость, осторожность.",
        "Десятка Жезлов": "Бремя, ответственность, тяжёлая работа.",
        "Паж Жезлов": "Исследование, свобода, энтузиазм.",
        "Рыцарь Жезлов": "Приключения, страсть, импульсивность.",
        "Королева Жезлов": "Уверенность, харизма, независимость.",
        "Король Жезлов": "Лидерство, видение, харизма.",
    }
}


# Обработчик кнопки "Гадание на одной карте Таро"
async def one_card_tarot(message: Message):
    user_id = message.chat.id
    user_language = get_user_language(user_id) or "ru"  # По умолчанию язык 'ru'

    # Выбираем случайную карту
    card_name, card_description = random.choice(list(TAROT_CARDS[user_language].items()))

    # Путь к GIF-файлу
    gif_path = "static/images/cards.gif"

    # Проверяем существование файла
    if not os.path.exists(gif_path):
        error_text = "Извините, анимация временно недоступна."
        await message.answer(error_text)
        return

    # Отправляем анимацию с ответом
    await message.answer_animation(animation=FSInputFile(gif_path))

    # Формируем текст сообщения
    text = f"{card_name}:\n{card_description}"

    # Создаём клавиатуру с кнопкой "Назад в меню"
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=get_text(user_language, "back_to_menu"))
    )
    keyboard.adjust(2)

    # Отправляем сообщение с картой
    await message.answer(text, reply_markup=keyboard.as_markup(resize_keyboard=True))