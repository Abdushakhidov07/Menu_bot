from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *
from keyboards import *
from aiogram.types import CallbackQuery


router = Router()


class AddDishes(StatesGroup):
    get_catgory_id= State()
    get_name = State()
    get_caption = State()
    get_price = State()
    get_photo_id = State()
    
    
class AddCategory(StatesGroup):
    get_title = State()
    
    
    
    



@router.message(F.text == "Добавить категорию")
@router.message(Command("add_category"))
async def add_category(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя категории:")
        await state.set_state(AddCategory.get_title)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()


@router.message(AddCategory.get_title)
async def add_category_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    data = await state.get_data()
    status = await create_category_db(data['title'])
    if status:
        await message.answer("Ваша категория создана")
        
    else:
        await message.answer("Ошибка при создании категория!")
    await state.clear()





@router.message(F.text == "Добавить блюдо")
@router.message(Command("add_dishes"))
async def add_category(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        button = await get_category_button()
        await message.answer("Выбирите категорию", reply_markup= button)
        await state.set_state(AddDishes.get_catgory_id)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()



@router.callback_query(AddDishes.get_catgory_id, F.data.startswith("category_"))
async def get_catgory_id_dishes(callback : CallbackQuery, state : FSMContext):
    cat_id = callback.data.split("_")[1]
    await state.update_data(category_id = cat_id)
    await callback.answer("Категория выбрана")
    await callback.message.answer("Введите имя блюдо: ")
    await state.set_state(AddDishes.get_name)




@router.message(AddDishes.get_name)
async def get_name_dishes(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введите описание блюдо: ")
    await state.set_state(AddDishes.get_caption)
    
@router.message(AddDishes.get_caption)
async def get_caption_dishes(message: Message, state: FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Введите ценю блюдо: ")
    await state.set_state(AddDishes.get_price)
    
    
@router.message(AddDishes.get_price)
async def get_price_dishes(message: Message, state: FSMContext):
    await state.update_data(price = message.text)
    await message.answer("Отправте фото: ")
    await state.set_state(AddDishes.get_photo_id)
    
@router.message(AddDishes.get_photo_id)
async def get_photo_id_dishes(message: Message, state: FSMContext):
    if not message.photo:
            await message.answer("Вы отправили не фото пожайлусто отправте фото блюда")
            return None
    photo = message.photo[-1]
    
    await state.update_data(file_id = photo.file_id)
    data = await state.get_data()
    if await create_dishes_db(data['category_id'], data['name'], data['caption'], data['price'], data['file_id']):
        await message.answer("Блюдо добавлено удачно")
    else:
        await message.answer("При добовлении блюда произошла ошибка")
    await state.clear()

    
    