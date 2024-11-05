from collections import OrderedDict
from django.db import models
from torch import nn

# Create your models here.
class ChessCNN(nn.Module):
    def __init__(self, learning_rate=1e-4, batch_size=5000, layer_count=10):
        super().__init__()

        layers = []
        for i in range(layer_count - 1):
            layers.append((f"linear-{i}", nn.Linear(395, 395)))
            layers.append((f"relu-{i}", nn.ReLU()))
        layers.append((f"linear-{layer_count-1}", nn.Linear(395, 1)))
        self.seq = nn.Sequential(OrderedDict(layers))

    def forward(self, x):
        return self.seq(x)