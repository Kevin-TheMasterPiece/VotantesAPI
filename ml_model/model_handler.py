# ml_model/model_handler.py
import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings

class VoterModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.load_model()
    
    def load_model(self):
        """Cargar el modelo entrenado"""
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_model', 'voter_knn_model.joblib')
            model_data = joblib.load(model_path)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.label_encoder = model_data['label_encoder']
            self.feature_names = model_data['feature_names']
            self.candidate_names = model_data['candidate_names']
            
            print("✅ Modelo KNN cargado exitosamente")
            print(f"🔧 Características: {len(self.feature_names)}")
            print(f"🎯 Candidatos: {list(self.candidate_names)}")
            
        except Exception as e:
            print(f"❌ Error cargando el modelo: {e}")
            raise
    
    def prepare_features(self, data):
        """Preparar características para la predicción"""
        # Crear diccionario con todas las características
        features = {}
        
        # Mapear campos básicos
        basic_fields = [
            "age", "gender", "education", "employment_status", "employment_sector",
            "income_bracket", "marital_status", "household_size", "has_children",
            "urbanicity", "region", "voted_last", "party_id_strength", "union_member",
            "public_sector", "home_owner", "small_biz_owner", "owns_car", "will_turnout",
            "undecided", "preference_strength", "tv_news_hours", "social_media_hours",
            "trust_media", "civic_participation", "job_tenure_years"
        ]
        
        for field in basic_fields:
            features[field] = float(data.get(field, 0))
        
        # Calcular características adicionales
        features['age_group'] = self._calculate_age_group(features['age'])
        features['political_engagement'] = features['party_id_strength'] * features['civic_participation']
        features['media_consumption'] = features['tv_news_hours'] + features['social_media_hours']
        
        return features
    
    def _calculate_age_group(self, age):
        """Calcular grupo de edad"""
        if age <= 25:
            return 0
        elif age <= 40:
            return 1
        elif age <= 60:
            return 2
        else:
            return 3
    
    def predict(self, data):
        """Realizar predicción"""
        if self.model is None:
            raise ValueError("Modelo no cargado")
        
        # Preparar características
        features_dict = self.prepare_features(data)
        
        # Crear array en el orden correcto
        feature_array = []
        for feature_name in self.feature_names:
            feature_array.append(features_dict.get(feature_name, 0))
        
        # Convertir a numpy array y escalar
        features = np.array([feature_array])
        features_scaled = self.scaler.transform(features)
        
        # Predecir
        prediction_encoded = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Decodificar resultado
        candidate = self.label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = probabilities[prediction_encoded]
        
        # Obtener top 3 candidatos
        candidate_probs = {}
        for i, candidate_name in enumerate(self.candidate_names):
            candidate_probs[candidate_name] = float(probabilities[i])
        
        top_candidates = sorted(candidate_probs.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'candidate': candidate,
            'confidence': float(confidence),
            'all_probabilities': candidate_probs,
            'top_candidates': top_candidates,
            'features_used': features_dict
        }

# Instancia global del modelo
voter_model = VoterModel()