import torch
import json
from torchvision import transforms, models
from PIL import Image
import io
import os
import torch.nn as nn
import numpy as np
from typing import Dict, List
import logging

# --- Model architecture constants from training code ---
INTERMEDIATE_SIZE = 512
DROPOUT_HEAD = 0.5
DROPOUT_INTERMEDIATE = 0.4
NUM_CLASSES = 6

# --- Image preprocessing constants from training code ---
IMAGE_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

class ModelInference:
    """
    Enhanced model inference class with better error handling, 
    confidence calibration, and performance optimizations.
    """
    
    def __init__(self, model_path: str, class_names_path: str):
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Set the device, preferring CUDA if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}")
        
        # Load the entire checkpoint file
        self.checkpoint = self._load_checkpoint(model_path)
        
        # Load the model and class names from the checkpoint
        self.model = self._load_model_from_checkpoint()
        self.class_names = self._load_class_names_from_checkpoint(class_names_path)
        
        # Enhanced preprocessing pipeline matching training
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=MEAN, std=STD)
        ])
        
        # Confidence thresholds for different confidence levels
        self.confidence_thresholds = {
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
        
        self.logger.info(f"Model loaded successfully with {len(self.class_names)} classes: {self.class_names}")

    def _load_checkpoint(self, path: str) -> Dict:
        """Load model checkpoint with enhanced error handling."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found at: {path}")
        
        try:
            self.logger.info(f"Loading checkpoint from: {path}")
            checkpoint = torch.load(path, map_location=self.device, weights_only=False)
            self.logger.info("Checkpoint loaded successfully")
            return checkpoint
        except Exception as e:
            self.logger.error(f"Error loading checkpoint file: {e}")
            raise RuntimeError(f"Failed to load AI model checkpoint: {str(e)}")

    def _load_model_from_checkpoint(self) -> nn.Module:
        """Load model architecture and weights with proper error handling."""
        try:
            # Instantiate a fresh ViT model with ImageNet weights
            model = models.vit_b_16(weights='IMAGENET1K_V1')
            
            # Recreate the exact custom head from the training script
            num_ftrs = model.heads.head.in_features
            model.heads.head = nn.Sequential(
                nn.LayerNorm(num_ftrs),
                nn.Dropout(p=DROPOUT_HEAD),
                nn.Linear(num_ftrs, INTERMEDIATE_SIZE),
                nn.GELU(),
                nn.Dropout(p=DROPOUT_INTERMEDIATE),
                nn.Linear(INTERMEDIATE_SIZE, NUM_CLASSES)
            )

            # Load the state_dict from the checkpoint
            if 'model_state_dict' in self.checkpoint:
                model.load_state_dict(self.checkpoint['model_state_dict'])
                self.logger.info("Model state dict loaded successfully")
            else:
                # Fallback: try loading the entire checkpoint as state dict
                model.load_state_dict(self.checkpoint)
                self.logger.warning("Loaded checkpoint directly as state dict")
            
            # Move model to device and set to evaluation mode
            model = model.to(self.device)
            model.eval()
            
            self.logger.info("AI model parameters loaded successfully")
            return model
            
        except KeyError as e:
            self.logger.error(f"Missing key in checkpoint: {e}")
            raise RuntimeError(f"Invalid model checkpoint format. Missing key: {e}")
        except Exception as e:
            self.logger.error(f"Error loading model parameters: {e}")
            raise RuntimeError(f"Failed to load AI model: {str(e)}")

    def _load_class_names_from_checkpoint(self, path: str) -> List[str]:
        """Load class names with fallback mechanisms."""
        try:
            # Try to load from checkpoint first
            if 'class_names' in self.checkpoint:
                class_names = self.checkpoint['class_names']
                self.logger.info("Class names loaded from checkpoint")
                return class_names
            else:
                self.logger.warning("Class names not found in checkpoint, trying JSON file")
                
        except Exception as e:
            self.logger.warning(f"Error loading class names from checkpoint: {e}")
        
        # Fallback to JSON file
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    class_names = json.load(f)
                self.logger.info("Class names loaded from JSON file")
                return class_names
            else:
                raise FileNotFoundError(f"Class names file not found at: {path}")
        except Exception as e:
            self.logger.error(f"Error loading class names: {e}")
            raise RuntimeError(f"Failed to load class names: {str(e)}")
            
    def predict(self, image_data: bytes) -> Dict:
        """
        Enhanced prediction method with GPU support and confidence analysis.
        """
        try:
            image = self._preprocess_image(image_data)
            tensor_image = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                # Use Automatic Mixed Precision for performance on GPU
                with torch.amp.autocast(device_type=self.device.type, enabled=self.device.type == 'cuda'):
                    outputs = self.model(tensor_image)
                
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            
            predictions = self._generate_predictions(probabilities)
            confidence_analysis = self._analyze_confidence(predictions)
            
            primary_finding = predictions[0]
            additional_findings = self._get_additional_findings(predictions)
            
            return {
                "primary_finding": primary_finding,
                "additional_findings": additional_findings,
                "predictions": predictions,
                "confidence_analysis": confidence_analysis,
                "model_accuracy": self.checkpoint.get('best_accuracy', 0.9228)
            }
            
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            raise RuntimeError(f"Failed to perform model inference: {str(e)}")

    def _preprocess_image(self, image_data: bytes) -> Image.Image:
        """Preprocess image with validation and error handling."""
        try:
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            if image.size[0] < 32 or image.size[1] < 32:
                self.logger.warning(f"Image size {image.size} is very small, may affect accuracy")
            return image
        except Exception as e:
            self.logger.error(f"Image preprocessing error: {e}")
            raise ValueError(f"Invalid image data: {str(e)}")

    def _generate_predictions(self, probabilities: torch.Tensor) -> List[Dict]:
        """Generate predictions with confidence scores."""
        predictions = []
        for i, prob in enumerate(probabilities):
            confidence = prob.item()
            predictions.append({
                "class": self.class_names[i],
                "confidence": confidence,
                "confidence_percentage": f"{confidence * 100:.2f}%",
                "class_id": i
            })
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        return predictions

    def _analyze_confidence(self, predictions: List[Dict]) -> Dict:
        """Analyze confidence levels and provide insights."""
        primary_confidence = predictions[0]['confidence']
        if primary_confidence >= self.confidence_thresholds['high']:
            confidence_level = 'high'
        elif primary_confidence >= self.confidence_thresholds['medium']:
            confidence_level = 'medium'
        else:
            confidence_level = 'low'
        
        confidences = [p['confidence'] for p in predictions]
        confidence_spread = max(confidences) - min(confidences)
        close_competitors = [p for p in predictions[1:] if p['confidence'] > primary_confidence * 0.7]
        
        return {
            "confidence_level": confidence_level,
            "primary_confidence": primary_confidence,
            "confidence_spread": confidence_spread,
            "close_competitors": len(close_competitors),
            "is_uncertain": primary_confidence < self.confidence_thresholds['medium']
        }

    def _get_additional_findings(self, predictions: List[Dict]) -> List[Dict]:
        """Get additional findings with dynamic thresholding."""
        primary_confidence = predictions[0]['confidence']
        if primary_confidence > 0.9:
            threshold = 0.1
        elif primary_confidence > 0.7:
            threshold = 0.15
        else:
            threshold = 0.2
        additional_findings = [p for p in predictions[1:] if p['confidence'] > threshold]
        return additional_findings

    def predict_batch(self, image_data_list: List[bytes]) -> List[Dict]:
        """
        Predict multiple images in batch for better performance.
        """
        try:
            images = [self._preprocess_image(data) for data in image_data_list]
            tensor_images = torch.stack([self.transform(img) for img in images]).to(self.device)
            
            with torch.no_grad():
                with torch.amp.autocast(device_type=self.device.type, enabled=self.device.type == 'cuda'):
                    outputs = self.model(tensor_images)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            results = []
            for probs in probabilities:
                predictions = self._generate_predictions(probs)
                confidence_analysis = self._analyze_confidence(predictions)
                primary_finding = predictions[0]
                additional_findings = self._get_additional_findings(predictions)
                
                results.append({
                    "primary_finding": primary_finding,
                    "additional_findings": additional_findings,
                    "predictions": predictions,
                    "confidence_analysis": confidence_analysis,
                    "model_accuracy": self.checkpoint.get('best_accuracy', 0.9228)
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Batch prediction error: {e}")
            raise RuntimeError(f"Failed to perform batch inference: {str(e)}")

    def get_model_info(self) -> Dict:
        """Get model information and statistics."""
        return {
            "model_architecture": "Vision Transformer (ViT-B/16)",
            "num_classes": len(self.class_names),
            "class_names": self.class_names,
            "device": str(self.device),
            "model_accuracy": self.checkpoint.get('best_accuracy', 0.9228),
            "intermediate_size": INTERMEDIATE_SIZE,
            "dropout_head": DROPOUT_HEAD,
            "dropout_intermediate": DROPOUT_INTERMEDIATE
        }