"""ML layer: model artifacts loading and inference.

Framework-specific code (PyTorch, YOLO, OpenCV) lives ONLY in this package.
Routes and services depend on `CropDiseasePredictor`, never on torch.
"""