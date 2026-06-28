import mlflow
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def mock_train_and_log():
    """
    Demonstrates MLflow tracking for the Sentence-BERT model and scoring logic.
    In a real scenario, this would track fine-tuning metrics.
    """
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("SmartHire_Candidate_Matching")

    with mlflow.start_run():
        model_name = "all-MiniLM-L6-v2"
        # Log parameters
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("semantic_weight", 0.5)
        mlflow.log_param("skill_weight", 0.3)
        mlflow.log_param("exp_weight", 0.2)
        
        # Load model and 'test' on validation data
        model = SentenceTransformer(model_name)
        
        val_data = [
            ("Python developer with React", "Looking for fullstack python react"),
            ("Data Entry clerk", "Senior Data Scientist needed")
        ]
        
        avg_score = 0
        for cand, jd in val_data:
            e1 = model.encode(cand).reshape(1, -1)
            e2 = model.encode(jd).reshape(1, -1)
            score = float(cosine_similarity(e1, e2)[0][0])
            avg_score += score
            
        avg_score /= len(val_data)
        
        # Log metrics
        mlflow.log_metric("val_avg_semantic_similarity", avg_score)
        print(f"Logged mock training run to MLflow. Validation Similarity: {avg_score:.4f}")

if __name__ == "__main__":
    mock_train_and_log()
