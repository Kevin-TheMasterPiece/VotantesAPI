from rest_framework import serializers
from .models import Votante

class VotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = '__all__'
        read_only_fields = ['id', 'predicted_vote', 'confidence', 'created_at', 
                          'age_group', 'political_engagement', 'media_consumption']
