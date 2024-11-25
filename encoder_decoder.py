import torch
import torch.nn as nn
import torch.nn.functional as F

class EncoderDecoder(nn.Module):
    def __init__(self, input_channels=4, latent_channels=3):
        super(EncoderDecoder, self).__init__()
        
        # Encoder: Reduce de 4 canales a 3 a través de varias capas convolucionales
        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 64, kernel_size=3, padding=1),  # Conv1
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # Conv2
            nn.ReLU(),
            nn.Conv2d(128, latent_channels, kernel_size=3, padding=1),  # Conv3
            nn.ReLU()
        )
        
        # Decoder: Reconstruye los 4 canales desde 3
        self.decoder = nn.Sequential(
            nn.Conv2d(latent_channels, 128, kernel_size=3, padding=1),  # Conv1
            nn.ReLU(),
            nn.Conv2d(128, 64, kernel_size=3, padding=1),  # Conv2
            nn.ReLU(),
            nn.Conv2d(64, input_channels, kernel_size=3, padding=1),  # Conv3
            nn.Sigmoid()  # Normalizar salida a [0, 1]
        )
    
    def forward(self, x):
        # Pasar por el encoder
        latent = self.encoder(x)
        # Pasar por el decoder
        reconstructed = self.decoder(latent)
        return reconstructed

# Instanciar el modelo
input_channels = 4
latent_channels = 3
model = EncoderDecoder(input_channels=input_channels, latent_channels=latent_channels)

# Verificar estructura

