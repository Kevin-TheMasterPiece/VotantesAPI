from django.db import models

class Votante(models.Model):
    age = models.FloatField()
    gender = models.FloatField()
    education = models.FloatField()
    employment_status = models.FloatField()
    employment_sector = models.FloatField()
    income_bracket = models.FloatField()
    marital_status = models.FloatField()
    household_size = models.FloatField()
    has_children = models.FloatField()
    urbanicity = models.FloatField()
    region = models.FloatField()
    voted_last = models.FloatField()
    party_id_strength = models.FloatField()
    union_member = models.FloatField()
    public_sector = models.FloatField()
    home_owner = models.FloatField()
    small_biz_owner = models.FloatField()
    owns_car = models.FloatField()
    will_turnout = models.FloatField()
    undecided = models.FloatField()
    preference_strength = models.FloatField()
    tv_news_hours = models.FloatField()
    social_media_hours = models.FloatField()
    trust_media = models.FloatField()
    civic_participation = models.FloatField()
    job_tenure_years = models.FloatField()

    # Nuevas características calculadas
    age_group = models.FloatField(default=0)
    political_engagement = models.FloatField(default=0)
    media_consumption = models.FloatField(default=0)
    confidence = models.FloatField(default=0.0)


    # Resultado del modelo
    predicted_vote = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Votante {self.id} - Predicción: {self.predicted_vote}"
