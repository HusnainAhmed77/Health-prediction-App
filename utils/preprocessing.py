def preprocess_input(data):
    # Map binary categories
    sex = 1 if data["Sex"] == "Male" else 0
    smoker = 1 if data["Smoker"] == "Yes" else 0
    activity = 1 if data["PhysicalActivity"] == "Active" else 0

    # One-hot encode stress level
    stress_levels = ['Low', 'Medium', 'High']
    stress_encoding = [1 if data["StressLevel"] == level else 0 for level in stress_levels]

    # One-hot encode diet type
    diet_types = ['High-carb', 'High-protein', 'Balanced']
    diet_encoding = [1 if data["DietType"] == diet else 0 for diet in diet_types]

    # Combine all features in the correct order
    features = [
        data["Age"],
        sex,
        data["BMI"],
        data["GlucoseLevel"],
        data["HbA1c"],
        data["BP_Systolic"],
        data["BP_Diastolic"],
        smoker,
        activity,
        *stress_encoding,      # ['Stress_Low', 'Stress_Medium', 'Stress_High']
        *diet_encoding         # ['DietType_High-carb', 'DietType_High-protein', 'DietType_Balanced']
    ]
    return features
