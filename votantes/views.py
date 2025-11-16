import os
import numpy as np
import joblib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Votante
from .serializers import VotanteSerializer
from django.db.models import Count, Avg
from rest_framework.generics import ListAPIView
from ml_model.model_handler import voter_model

class PredictVoteView(APIView):
    def post(self, request):
        serializer = VotanteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Realizar predicción
                prediction_result = voter_model.predict(request.data)
                
                # Calcular características adicionales para guardar en BD
                age_group = voter_model._calculate_age_group(float(request.data.get('age', 0)))
                political_engagement = float(request.data.get('party_id_strength', 0)) * float(request.data.get('civic_participation', 0))
                media_consumption = float(request.data.get('tv_news_hours', 0)) + float(request.data.get('social_media_hours', 0))
                
                # Guardar el resultado en la base de datos
                votante = Votante(
                    # Campos originales
                    age=float(request.data.get('age', 0)),
                    gender=float(request.data.get('gender', 0)),
                    education=float(request.data.get('education', 0)),
                    employment_status=float(request.data.get('employment_status', 0)),
                    employment_sector=float(request.data.get('employment_sector', 0)),
                    income_bracket=float(request.data.get('income_bracket', 0)),
                    marital_status=float(request.data.get('marital_status', 0)),
                    household_size=float(request.data.get('household_size', 0)),
                    has_children=float(request.data.get('has_children', 0)),
                    urbanicity=float(request.data.get('urbanicity', 0)),
                    region=float(request.data.get('region', 0)),
                    voted_last=float(request.data.get('voted_last', 0)),
                    party_id_strength=float(request.data.get('party_id_strength', 0)),
                    union_member=float(request.data.get('union_member', 0)),
                    public_sector=float(request.data.get('public_sector', 0)),
                    home_owner=float(request.data.get('home_owner', 0)),
                    small_biz_owner=float(request.data.get('small_biz_owner', 0)),
                    owns_car=float(request.data.get('owns_car', 0)),
                    will_turnout=float(request.data.get('will_turnout', 0)),
                    undecided=float(request.data.get('undecided', 0)),
                    preference_strength=float(request.data.get('preference_strength', 0)),
                    tv_news_hours=float(request.data.get('tv_news_hours', 0)),
                    social_media_hours=float(request.data.get('social_media_hours', 0)),
                    trust_media=float(request.data.get('trust_media', 0)),
                    civic_participation=float(request.data.get('civic_participation', 0)),
                    job_tenure_years=float(request.data.get('job_tenure_years', 0)),
                    
                    # Nuevos campos calculados
                    age_group=age_group,
                    political_engagement=political_engagement,
                    media_consumption=media_consumption,
                    
                    # Resultado de la predicción
                    predicted_vote=prediction_result['candidate'],
                    confidence=prediction_result['confidence']
                )
                votante.save()

                return Response({
                    "id": votante.id,
                    "predicted_vote": prediction_result['candidate'],
                    "confidence": round(prediction_result['confidence'], 4),
                    "top_candidates": [
                        {"candidate": cand, "probability": round(prob, 4)} 
                        for cand, prob in prediction_result['top_candidates']
                    ]
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    {"error": f"Error en la predicción: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatsView(APIView):

    permission_classes = [permissions.IsAuthenticated] # Asegura que solo usuarios autenticados puedan acceder

    def get(self, request):
        total_votantes = Votante.objects.count()
        votos_por_candidato = Votante.objects.values('predicted_vote').annotate(total=Count('id')).order_by('-total')
        promedio_edad = Votante.objects.aggregate(promedio_edad=Avg('age'))['promedio_edad']

        # Ejemplo: distribución por género
        distribucion_genero = Votante.objects.values('gender').annotate(total=Count('id'))

        return Response({
            "total_votantes": total_votantes,
            "votos_por_candidato": list(votos_por_candidato),
            "promedio_edad": round(promedio_edad, 2) if promedio_edad else 0,
            "distribucion_genero": list(distribucion_genero),
        })

class VotanteListView(ListAPIView):

    permission_classes = [permissions.IsAuthenticated]  # Asegura que solo usuarios autenticados puedan acceder
    
    queryset = Votante.objects.all().order_by('-created_at')
    serializer_class = VotanteSerializer