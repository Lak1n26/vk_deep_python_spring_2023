class SomeModel:
    def predict(self, message: str) -> float:
        return 1


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """
    "неуд", если предсказание модели меньше bad_threshold
    "отл", если предсказание модели больше good_threshold
    "норм" в остальных случаях
    """
    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"
    return "норм"
