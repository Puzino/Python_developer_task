async def clean_state(state) -> dict:
    async with state.proxy() as data:
        return data
