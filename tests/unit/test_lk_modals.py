from utils.lk_modals import is_blocking_lk_modal_text


def test_curator_modal_is_blocking():
    text = (
        "Витрина\nПрофиль компании\nПодтвердите роль куратора\n"
        "Вам необходимо добавить документ"
    )
    assert is_blocking_lk_modal_text(text) is True


def test_chat_topics_are_not_blocking():
    assert is_blocking_lk_modal_text("Ассистент\nКак получить ID\nСервисы") is False
    assert is_blocking_lk_modal_text("") is False
