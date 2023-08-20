from aiogram.fsm.context import FSMContext


async def reset_state_wo_locale(state: FSMContext, data: dict | None = None):
    if not data:
        data = await state.get_data()
    lc = data.get('locale')
    await state.set_state(None)
    await state.set_data({'locale': lc})